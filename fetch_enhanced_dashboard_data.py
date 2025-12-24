#!/usr/bin/env python3
"""
Fetch enhanced Tableau dashboard data with descriptions, tags, views, and data sources
"""
import requests
import json
from datetime import datetime

# Load credentials
with open('mcp.json', 'r') as f:
    config = json.load(f)
    tableau = config['mcpServers']['tableau']['env']

SERVER = tableau['SERVER']
SITE_NAME = tableau['SITE_NAME']
PAT_NAME = tableau['PAT_NAME']
PAT_VALUE = tableau['PAT_VALUE']
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

def get_workbooks_by_project_name(auth_token, site_id, project_name):
    """Get all workbooks in a specific project by name"""
    all_workbooks = []
    page_number = 1
    page_size = 100
    
    while True:
        url = f"{SERVER}/api/{API_VERSION}/sites/{site_id}/workbooks"
        params = {
            "filter": f"projectName:eq:{project_name}",
            "pageSize": page_size,
            "pageNumber": page_number
        }
        response = requests.get(url, headers={"X-Tableau-Auth": auth_token, "Accept": "application/json"}, params=params)
        response.raise_for_status()
        data = response.json()
        
        workbooks = data.get('workbooks', {}).get('workbook', [])
        if not workbooks:
            break
        
        all_workbooks.extend(workbooks)
        
        pagination = data.get('pagination', {})
        total_available = int(pagination.get('totalAvailable', 0))
        if page_number * page_size >= total_available:
            break
        page_number += 1
    
    return all_workbooks

def get_all_views_for_workbook(auth_token, site_id, workbook_id):
    """Get all views/sheets for a workbook with their URLs"""
    try:
        url = f"{SERVER}/api/{API_VERSION}/sites/{site_id}/workbooks/{workbook_id}/views"
        response = requests.get(url, headers={"X-Tableau-Auth": auth_token, "Accept": "application/json"})
        response.raise_for_status()
        views = response.json().get('views', {}).get('view', [])
        
        view_data = []
        for view in views:
            content_url = view.get('contentUrl', '')
            if content_url:
                clean_url = content_url.replace('/sheets/', '/')
                view_data.append({
                    'name': view.get('name', 'Unnamed'),
                    'id': view.get('id', ''),
                    'url': f"{SERVER}/#/views/{clean_url}"
                })
        
        return view_data
    except Exception as e:
        print(f"    ⚠️ Error getting views: {e}")
        return []

def get_data_sources_for_workbook(auth_token, site_id, workbook_id):
    """Get data source information for a workbook"""
    try:
        url = f"{SERVER}/api/{API_VERSION}/sites/{site_id}/workbooks/{workbook_id}/connections"
        response = requests.get(url, headers={"X-Tableau-Auth": auth_token, "Accept": "application/json"})
        response.raise_for_status()
        connections = response.json().get('connections', {}).get('connection', [])
        
        data_sources = []
        seen = set()
        
        for conn in connections:
            # Build a unique identifier for the data source
            ds_type = conn.get('type', 'Unknown')
            server_address = conn.get('serverAddress', '')
            db_name = conn.get('datasourceName', '') or conn.get('dbname', '')
            
            # Create a readable name
            if db_name and db_name not in seen:
                data_sources.append({
                    'name': db_name,
                    'type': ds_type,
                    'server': server_address
                })
                seen.add(db_name)
            elif server_address and server_address not in seen:
                data_sources.append({
                    'name': server_address,
                    'type': ds_type,
                    'server': server_address
                })
                seen.add(server_address)
        
        return data_sources
    except Exception as e:
        print(f"    ⚠️ Error getting data sources: {e}")
        return []

def enhance_workbook_data(auth_token, site_id, wb, category):
    """Enhance workbook with views, data sources, tags, etc."""
    workbook_id = wb.get('id')
    name = wb.get('name', 'Unnamed')
    
    print(f"  📊 {name}")
    
    # Get all views
    print(f"    Getting views...")
    views = get_all_views_for_workbook(auth_token, site_id, workbook_id)
    print(f"    ✓ Found {len(views)} views")
    
    # Get data sources
    print(f"    Getting data sources...")
    data_sources = get_data_sources_for_workbook(auth_token, site_id, workbook_id)
    print(f"    ✓ Found {len(data_sources)} data sources")
    
    # Extract tags
    tags_obj = wb.get('tags', {})
    tags = []
    if isinstance(tags_obj, dict):
        tag_list = tags_obj.get('tag', [])
        if isinstance(tag_list, list):
            tags = [t.get('label', '') for t in tag_list if isinstance(t, dict)]
        elif isinstance(tag_list, dict):
            tags = [tag_list.get('label', '')]
    
    enhanced = {
        'name': name,
        'description': wb.get('description', ''),
        'project': wb.get('project', {}).get('name', 'Unknown'),
        'owner': wb.get('owner', {}).get('name', 'Unknown'),
        'created': wb.get('createdAt', ''),
        'updated': wb.get('updatedAt', ''),
        'tags': tags,
        'views': views,
        'data_sources': data_sources,
        'sheet_count': len(views),
        'size': wb.get('size', 0),
        'category': category,
        # First view URL for backward compatibility
        'url': views[0]['url'] if views else None
    }
    
    return enhanced

print("🔐 Authenticating...")
auth_token, site_id = sign_in()
print("✅ Authenticated!\n")

# Production Projects - ROC Protocol and Triage
production_projects = ['ROC Protocol', 'Triage']

print("=" * 80)
print("🏭 FETCHING PRODUCTION DASHBOARDS")
print("=" * 80)

production_workbooks = []
for proj_name in production_projects:
    print(f"\n📁 Fetching from '{proj_name}' project...")
    workbooks = get_workbooks_by_project_name(auth_token, site_id, proj_name)
    production_workbooks.extend(workbooks)
    print(f"✓ Found {len(workbooks)} workbooks")

print(f"\n✅ Total: {len(production_workbooks)} production workbooks\n")

production_data = []
for wb in production_workbooks:
    enhanced = enhance_workbook_data(auth_token, site_id, wb, 'production')
    if enhanced['url']:  # Only add if it has at least one view
        production_data.append(enhanced)
    print()

print(f"✅ Successfully processed {len(production_data)} production workbooks\n")

# Playground Projects - Guy, Mor, Yahel, Playground
playground_projects = ['Playground', 'Mor', 'Guy', 'Yahel']

print("=" * 80)
print("🎮 FETCHING PLAYGROUND DASHBOARDS")
print("=" * 80)

playground_workbooks = []
for proj_name in playground_projects:
    print(f"\n📁 Fetching from '{proj_name}' project...")
    workbooks = get_workbooks_by_project_name(auth_token, site_id, proj_name)
    playground_workbooks.extend(workbooks)
    print(f"✓ Found {len(workbooks)} workbooks")

print(f"\n✅ Total: {len(playground_workbooks)} playground workbooks\n")

playground_data = []
for wb in playground_workbooks:
    owner = wb.get('owner', {}).get('name', '')
    
    # Filter Guy's dashboards - only keep if "ROC" in title
    if owner == 'guy.d':
        if 'roc' not in wb.get('name', '').lower():
            print(f"  ⏭️  Skipping: {wb.get('name')} (Guy's non-ROC)")
            continue
    
    enhanced = enhance_workbook_data(auth_token, site_id, wb, 'playground')
    if enhanced['url']:  # Only add if it has at least one view
        playground_data.append(enhanced)
    print()

print(f"✅ Successfully processed {len(playground_data)} playground workbooks\n")

# Sort by updated date (most recent first)
production_data.sort(key=lambda x: x['updated'], reverse=True)
playground_data.sort(key=lambda x: x['updated'], reverse=True)

# Save enhanced data
all_dashboards = {
    'production': production_data,
    'playground': playground_data,
    'last_updated': datetime.now().isoformat()
}

with open('all_dashboards_data_enhanced.json', 'w') as f:
    json.dump(all_dashboards, f, indent=2)

print("=" * 80)
print("✅ SUMMARY")
print("=" * 80)
print(f"🏭 Production Dashboards: {len(production_data)}")
print(f"🎮 Playground Dashboards: {len(playground_data)}")
print(f"📊 Total: {len(production_data) + len(playground_data)}")
print(f"\n💾 Data saved to: all_dashboards_data_enhanced.json")
print(f"📅 Last updated: {all_dashboards['last_updated']}")
print("\n✨ Enhanced data includes:")
print("   ✓ Descriptions")
print("   ✓ Tags")
print("   ✓ All views/sheets")
print("   ✓ Data sources")
print("   ✓ Created dates")
print("   ✓ Sheet counts")

