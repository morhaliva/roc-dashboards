#!/usr/bin/env python3
"""
Generate HTML with correct Tableau dashboard URLs
Reads credentials from environment variables or mcp.json
"""
import requests
import json
import os

# Read credentials from environment variables (for GitHub Actions)
# or from mcp.json (for local use)
def get_credentials():
    # Try environment variables first (GitHub Actions)
    if os.environ.get('TABLEAU_SERVER'):
        return {
            'SERVER': os.environ.get('TABLEAU_SERVER'),
            'SITE_NAME': os.environ.get('TABLEAU_SITE_NAME', ''),
            'PAT_NAME': os.environ.get('TABLEAU_PAT_NAME'),
            'PAT_VALUE': os.environ.get('TABLEAU_PAT_VALUE')
        }
    
    # Fall back to mcp.json (local use)
    try:
        with open('mcp.json', 'r') as f:
            config = json.load(f)
            tableau = config.get('tableau', {})
            return {
                'SERVER': tableau.get('SERVER'),
                'SITE_NAME': tableau.get('SITE_NAME', ''),
                'PAT_NAME': tableau.get('PAT_NAME'),
                'PAT_VALUE': tableau.get('PAT_VALUE')
            }
    except FileNotFoundError:
        raise Exception("No credentials found. Set environment variables or create mcp.json")

creds = get_credentials()
SERVER = creds['SERVER']
SITE_NAME = creds['SITE_NAME']
PAT_NAME = creds['PAT_NAME']
PAT_VALUE = creds['PAT_VALUE']
API_VERSION = "3.19"

def sign_in():
    url = f"{SERVER}/api/{API_VERSION}/auth/signin"
    payload = {
        "credentials": {
            "personalAccessTokenName": PAT_NAME,
            "personalAccessTokenSecret": PAT_VALUE,
            "site": {"contentUrl": SITE_NAME}
        }
    }
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json", "Accept": "application/json"})
    response.raise_for_status()
    data = response.json()
    return data['credentials']['token'], data['credentials']['site']['id']

def get_all_workbooks(auth_token, site_id):
    all_workbooks = []
    page_number = 1
    page_size = 100
    
    while True:
        url = f"{SERVER}/api/{API_VERSION}/sites/{site_id}/workbooks?pageSize={page_size}&pageNumber={page_number}"
        response = requests.get(url, headers={"X-Tableau-Auth": auth_token, "Accept": "application/json"})
        response.raise_for_status()
        data = response.json()
        workbooks = data.get('workbooks', {}).get('workbook', [])
        
        if not workbooks:
            break
        
        # Filter for mor.h
        for wb in workbooks:
            if wb.get('owner', {}).get('name') == 'mor.h':
                all_workbooks.append(wb)
        
        pagination = data.get('pagination', {})
        total_available = int(pagination.get('totalAvailable', 0))
        if page_number * page_size >= total_available:
            break
        page_number += 1
    
    return all_workbooks

def get_first_view_url(auth_token, site_id, workbook_id):
    """Get the first view URL for a workbook"""
    try:
        url = f"{SERVER}/api/{API_VERSION}/sites/{site_id}/workbooks/{workbook_id}/views"
        response = requests.get(url, headers={"X-Tableau-Auth": auth_token, "Accept": "application/json"})
        response.raise_for_status()
        views = response.json().get('views', {}).get('view', [])
        
        if views:
            # Try to use the view ID format which works better
            view_id = views[0].get('id', '')
            content_url = views[0].get('contentUrl', '')
            
            # Format: /#/views/contentUrl
            if content_url:
                # Remove 'sheets/' prefix if present for cleaner URLs
                clean_url = content_url.replace('/sheets/', '/')
                return f"{SERVER}/#/views/{clean_url}"
    except Exception as e:
        pass
    
    return None

print("🔐 Authenticating...")
auth_token, site_id = sign_in()
print("✅ Authenticated!\n")

print("📊 Fetching your workbooks...")
workbooks = get_all_workbooks(auth_token, site_id)
print(f"✅ Found {len(workbooks)} workbooks\n")

print("🔗 Getting correct view URLs...")
dashboard_data = []

for i, wb in enumerate(workbooks, 1):
    print(f"  Processing {i}/{len(workbooks)}: {wb.get('name')}")
    url = get_first_view_url(auth_token, site_id, wb.get('id'))
    
    if url:
        dashboard_data.append({
            'name': wb.get('name', 'Unnamed'),
            'project': wb.get('project', {}).get('name', 'Unknown'),
            'updated': wb.get('updatedAt', ''),
            'url': url
        })

print(f"\n✅ Successfully got URLs for {len(dashboard_data)} workbooks")
print(f"❌ {len(workbooks) - len(dashboard_data)} workbooks have no views")

# Save to JSON for the HTML to use
with open('dashboards_data.json', 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print("\n✅ Data saved to dashboards_data.json")
