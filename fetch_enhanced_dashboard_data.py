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
    """Get all views/sheets for a workbook with their URLs and view counts"""
    try:
        # Include usage statistics in the request
        url = f"{SERVER}/api/{API_VERSION}/sites/{site_id}/workbooks/{workbook_id}/views"
        params = {"includeUsageStatistics": "true"}
        response = requests.get(url, headers={"X-Tableau-Auth": auth_token, "Accept": "application/json"}, params=params)
        response.raise_for_status()
        views = response.json().get('views', {}).get('view', [])
        
        view_data = []
        for view in views:
            content_url = view.get('contentUrl', '')
            if content_url:
                clean_url = content_url.replace('/sheets/', '/')
                # Get view count from usage statistics
                usage = view.get('usage', {})
                view_count = usage.get('totalViewCount', 0) if isinstance(usage, dict) else 0
                
                view_data.append({
                    'name': view.get('name', 'Unnamed'),
                    'id': view.get('id', ''),
                    'url': f"{SERVER}/#/views/{clean_url}",
                    'viewCount': view_count
                })
        
        # Sort views by view count (most viewed first)
        view_data.sort(key=lambda x: int(x.get('viewCount', 0) or 0), reverse=True)
        
        return view_data
    except Exception as e:
        print(f"    ⚠️ Error getting views: {e}")
        return []

def generate_description(name, project, data_sources):
    """Generate a one-sentence description based on workbook name and context"""
    name_lower = name.lower()
    
    # Keywords for different types of dashboards
    if 'hourly' in name_lower:
        return f"Monitors hourly trends and real-time performance metrics."
    elif 'daily' in name_lower:
        return f"Tracks daily metrics and day-over-day performance changes."
    elif 'alert' in name_lower:
        return f"Automated alerting dashboard for proactive issue detection."
    elif 'investigation' in name_lower or 'analysis' in name_lower:
        return f"Deep-dive analysis tool for investigating performance patterns."
    elif 'historical' in name_lower or 'seasonality' in name_lower:
        return f"Historical trend analysis for understanding seasonal patterns and YoY changes."
    elif 'revenue' in name_lower:
        return f"Revenue tracking and financial performance monitoring."
    elif 'triage' in name_lower:
        return f"Triage dashboard for prioritizing and managing operational issues."
    elif 'margin' in name_lower:
        return f"Margin analysis for profitability and cost optimization insights."
    elif 'health' in name_lower or 'status' in name_lower:
        return f"Health status overview for quick operational assessment."
    elif 'jira' in name_lower or 'roadmap' in name_lower:
        return f"Project tracking dashboard for Jira tickets and roadmap progress."
    elif 'constraint' in name_lower:
        return f"Market constraints monitoring and capacity management."
    elif 'user data' in name_lower:
        return f"User data metrics and audience insights dashboard."
    elif 'spend' in name_lower:
        return f"Spend tracking and budget utilization analysis."
    elif 'full data' in name_lower:
        return f"Comprehensive data exploration with flexible filtering options."
    elif 'trend' in name_lower:
        return f"Trend analysis dashboard for tracking performance over time."
    elif 'test' in name_lower or 'playground' in name_lower:
        return f"Development/test version for feature experimentation."
    elif 'publisher' in name_lower:
        return f"Publisher-focused performance metrics and analytics."
    elif 'advertiser' in name_lower:
        return f"Advertiser performance tracking and campaign analytics."
    elif 'roi' in name_lower:
        return f"ROI tracking and return on investment analysis."
    elif 'loss' in name_lower:
        return f"Revenue loss tracking and recovery opportunity identification."
    elif 'cpa' in name_lower or 'cvr' in name_lower:
        return f"CPA/CVR analysis for conversion optimization insights."
    elif 'proactive' in name_lower:
        return f"Proactive monitoring dashboard for early issue detection."
    elif 'supply' in name_lower:
        return f"Supply-side metrics and inventory management dashboard."
    elif 'readiness' in name_lower:
        return f"Readiness assessment and migration tracking dashboard."
    else:
        # Generic description based on project
        if project == 'ROC Protocol':
            return f"ROC Protocol operational dashboard for real-time monitoring."
        elif project == 'Triage':
            return f"Triage tool for operational analysis and decision support."
        elif project == 'ROC':
            return f"ROC team dashboard for business intelligence and reporting."
        else:
            return f"Analytics dashboard for {project} insights and monitoring."

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
    
    project_name = wb.get('project', {}).get('name', 'Unknown')
    
    # Use existing description or generate one
    existing_desc = wb.get('description', '').strip()
    if existing_desc:
        description = existing_desc
    else:
        description = generate_description(name, project_name, data_sources)
    
    # Calculate total views across all sheets
    total_views = sum(int(v.get('viewCount', 0) or 0) for v in views)
    
    enhanced = {
        'name': name,
        'description': description,
        'project': project_name,
        'owner': wb.get('owner', {}).get('name', 'Unknown'),
        'created': wb.get('createdAt', ''),
        'updated': wb.get('updatedAt', ''),
        'tags': tags,
        'views': views,
        'data_sources': data_sources,
        'sheet_count': len(views),
        'total_views': total_views,
        'size': wb.get('size', 0),
        'category': category,
        # First view URL for backward compatibility
        'url': views[0]['url'] if views else None
    }
    
    return enhanced

print("🔐 Authenticating...")
auth_token, site_id = sign_in()
print("✅ Authenticated!\n")

# Production Projects - ROC Protocol, Triage, and ROC
production_projects = ['ROC Protocol', 'Triage', 'ROC']

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

