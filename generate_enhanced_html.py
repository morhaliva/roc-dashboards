#!/usr/bin/env python3
"""
Generate enhanced HTML with search, filters, and rich metadata
"""
import json
from datetime import datetime

# Load the enhanced data
with open('all_dashboards_data_enhanced.json', 'r') as f:
    data = json.load(f)

production = data['production']
playground = data['playground']
last_updated = data.get('last_updated', datetime.now().isoformat())

# Sort dashboards by updated date (descending - most recent first)
production = sorted(production, key=lambda x: x.get('updated', ''), reverse=True)
playground = sorted(playground, key=lambda x: x.get('updated', ''), reverse=True)

# Format the date nicely
try:
    dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
    formatted_date = dt.strftime('%B %d, %Y at %I:%M %p')
except:
    formatted_date = last_updated

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROC Tableau Dashboards</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        .search-filter-bar {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .search-box {{
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        
        .search-input {{
            flex: 1;
            min-width: 300px;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .filter-buttons {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }}
        
        .filter-btn:hover {{
            border-color: #667eea;
            color: #667eea;
        }}
        
        .filter-btn.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-header {{
            background: white;
            padding: 15px 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-count {{
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
            gap: 20px;
        }}
        
        .dashboard-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .dashboard-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        .dashboard-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.3;
        }}
        
        .dashboard-description {{
            color: #666;
            margin-bottom: 15px;
            line-height: 1.5;
            font-size: 0.95em;
        }}
        
        .dashboard-description.empty {{
            color: #999;
            font-style: italic;
        }}
        
        .dashboard-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #666;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }}
        
        .tag {{
            background: #f0f0f0;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            color: #555;
        }}
        
        .data-sources {{
            margin-bottom: 15px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
            font-size: 0.9em;
        }}
        
        .data-sources-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }}
        
        .data-sources-title {{
            font-weight: bold;
            color: #555;
        }}
        
        .toggle-btn {{
            background: none;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 2px 8px;
            cursor: pointer;
            font-size: 0.85em;
            color: #666;
            transition: all 0.2s;
        }}
        
        .toggle-btn:hover {{
            background: #eee;
            border-color: #ccc;
        }}
        
        .data-sources-list {{
            margin-top: 8px;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }}
        
        .data-sources-list.collapsed {{
            max-height: 0;
            margin-top: 0;
        }}
        
        .data-source {{
            color: #666;
            padding: 3px 0;
        }}
        
        .views-section {{
            margin-bottom: 15px;
        }}
        
        .views-title {{
            font-weight: bold;
            color: #555;
            margin-bottom: 8px;
            font-size: 0.95em;
        }}
        
        .view-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .view-link {{
            padding: 6px 12px;
            background: #e8eaf6;
            color: #5c6bc0;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.85em;
            transition: background 0.3s;
        }}
        
        .view-link:hover {{
            background: #5c6bc0;
            color: white;
        }}
        
        .dashboard-link {{
            display: inline-block;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: background 0.3s;
            font-weight: 500;
        }}
        
        .dashboard-link:hover {{
            background: #5568d3;
        }}
        
        .no-results {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
            color: #666;
            font-size: 1.2em;
        }}
        
        .back-button {{
            position: fixed;
            top: 20px;
            left: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 20px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s;
            z-index: 1000;
        }}
        
        .back-button:hover {{
            background: #667eea;
            color: white;
            transform: translateX(-5px);
        }}
        
        @media (max-width: 768px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .back-button {{
                top: 10px;
                left: 10px;
                padding: 10px 15px;
                font-size: 0.9em;
            }}
        }}
    </style>
</head>
<body>
    <a href="knowledge-base.html" class="back-button">← Back to Knowledge Base</a>
    
    <div class="container">
        <div class="header">
            <h1>📊 ROC Tableau Dashboards</h1>
            <p>Last updated: {formatted_date}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(production)}</div>
                <div class="stat-label">Production</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(playground)}</div>
                <div class="stat-label">Playground</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(production) + len(playground)}</div>
                <div class="stat-label">Total Dashboards</div>
            </div>
        </div>
        
        <div class="search-filter-bar">
            <div class="search-box">
                <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search dashboards by name, description, tags, owner, or data source...">
            </div>
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="production">🏭 Production</button>
                <button class="filter-btn" data-filter="playground">🎮 Playground</button>
            </div>
        </div>
        
        <div class="section" data-section="production">
            <div class="section-header">
                <div class="section-title">
                    🏭 Production Dashboards
                </div>
                <div class="section-count" id="production-count">{len(production)}</div>
            </div>
            <div class="dashboard-grid" id="production-grid">
'''

# Generate production cards
for dashboard in production:
    desc = dashboard['description'] if dashboard['description'] else 'No description available'
    desc_class = '' if dashboard['description'] else 'empty'
    
    tags_html = ''
    if dashboard['tags']:
        tags_html = '<div class="tags">'
        for tag in dashboard['tags']:
            tags_html += f'<span class="tag">🏷️ {tag}</span>'
        tags_html += '</div>'
    
    data_sources_html = ''
    if dashboard['data_sources']:
        ds_count = len(dashboard['data_sources'])
        data_sources_html = f'''<div class="data-sources">
            <div class="data-sources-header" onclick="toggleDataSources(this)">
                <span class="data-sources-title">🗄️ Data Sources ({ds_count})</span>
                <button class="toggle-btn">▼ Show</button>
            </div>
            <div class="data-sources-list collapsed">'''
        for ds in dashboard['data_sources']:
            ds_name = ds['name']
            ds_type = ds.get('type', 'unknown').upper()
            type_color = '#4CAF50' if ds_type == 'VERTICA' else '#2196F3' if ds_type == 'BIGQUERY' else '#FF9800'
            data_sources_html += f'<div class="data-source"><span style="background: {type_color}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75em; margin-right: 8px;">{ds_type}</span>{ds_name}</div>'
        data_sources_html += '</div></div>'
    
    views_html = ''
    if len(dashboard['views']) > 1:
        views_html = '<div class="views-section"><div class="views-title">📑 Sheets ({}):</div><div class="view-links">'.format(len(dashboard['views']))
        for view in dashboard['views']:
            view_count = int(view.get('viewCount', 0) or 0)
            count_display = f" ({view_count:,}👁)" if view_count > 0 else ""
            views_html += f'<a href="{view["url"]}" class="view-link" target="_blank">{view["name"]}{count_display}</a>'
        views_html += '</div></div>'
    
    created_date = datetime.fromisoformat(dashboard['created'].replace('Z', '+00:00')).strftime('%b %d, %Y')
    updated_date = datetime.fromisoformat(dashboard['updated'].replace('Z', '+00:00')).strftime('%b %d, %Y')
    total_views = int(dashboard.get('total_views', 0) or 0)
    
    html += f'''
                <div class="dashboard-card" data-category="production" 
                     data-name="{dashboard['name'].lower()}"
                     data-description="{desc.lower()}"
                     data-tags="{' '.join(dashboard['tags']).lower()}"
                     data-owner="{dashboard['owner'].lower()}"
                     data-sources="{' '.join([ds['name'].lower() for ds in dashboard['data_sources']])}">
                    <div class="dashboard-name">{dashboard['name']}</div>
                    <div class="dashboard-description {desc_class}">{desc}</div>
                    {tags_html}
                    <div class="dashboard-meta">
                        <div class="meta-item">👤 {dashboard['owner']}</div>
                        <div class="meta-item">📁 {dashboard['project']}</div>
                        <div class="meta-item">📊 {dashboard['sheet_count']} sheets</div>
                        <div class="meta-item">👁 {total_views:,} views</div>
                    </div>
                    <div class="dashboard-meta">
                        <div class="meta-item">📅 Created: {created_date}</div>
                        <div class="meta-item">🔄 Updated: {updated_date}</div>
                    </div>
                    {data_sources_html}
                    {views_html}
                    <a href="{dashboard['url']}" class="dashboard-link" target="_blank">View Dashboard →</a>
                </div>
'''

html += '''
            </div>
        </div>
        
        <div class="section" data-section="playground">
            <div class="section-header">
                <div class="section-title">
                    🎮 Playground Dashboards
                </div>
                <div class="section-count" id="playground-count">{}</div>
            </div>
            <div class="dashboard-grid" id="playground-grid">
'''.format(len(playground))

# Generate playground cards
for dashboard in playground:
    desc = dashboard['description'] if dashboard['description'] else 'No description available'
    desc_class = '' if dashboard['description'] else 'empty'
    
    tags_html = ''
    if dashboard['tags']:
        tags_html = '<div class="tags">'
        for tag in dashboard['tags']:
            tags_html += f'<span class="tag">🏷️ {tag}</span>'
        tags_html += '</div>'
    
    data_sources_html = ''
    if dashboard['data_sources']:
        ds_count = len(dashboard['data_sources'])
        data_sources_html = f'''<div class="data-sources">
            <div class="data-sources-header" onclick="toggleDataSources(this)">
                <span class="data-sources-title">🗄️ Data Sources ({ds_count})</span>
                <button class="toggle-btn">▼ Show</button>
            </div>
            <div class="data-sources-list collapsed">'''
        for ds in dashboard['data_sources']:
            ds_name = ds['name']
            ds_type = ds.get('type', 'unknown').upper()
            type_color = '#4CAF50' if ds_type == 'VERTICA' else '#2196F3' if ds_type == 'BIGQUERY' else '#FF9800'
            data_sources_html += f'<div class="data-source"><span style="background: {type_color}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75em; margin-right: 8px;">{ds_type}</span>{ds_name}</div>'
        data_sources_html += '</div></div>'
    
    views_html = ''
    if len(dashboard['views']) > 1:
        views_html = '<div class="views-section"><div class="views-title">📑 Sheets ({}):</div><div class="view-links">'.format(len(dashboard['views']))
        for view in dashboard['views']:
            view_count = int(view.get('viewCount', 0) or 0)
            count_display = f" ({view_count:,}👁)" if view_count > 0 else ""
            views_html += f'<a href="{view["url"]}" class="view-link" target="_blank">{view["name"]}{count_display}</a>'
        views_html += '</div></div>'
    
    created_date = datetime.fromisoformat(dashboard['created'].replace('Z', '+00:00')).strftime('%b %d, %Y')
    updated_date = datetime.fromisoformat(dashboard['updated'].replace('Z', '+00:00')).strftime('%b %d, %Y')
    total_views = int(dashboard.get('total_views', 0) or 0)
    
    html += f'''
                <div class="dashboard-card" data-category="playground"
                     data-name="{dashboard['name'].lower()}"
                     data-description="{desc.lower()}"
                     data-tags="{' '.join(dashboard['tags']).lower()}"
                     data-owner="{dashboard['owner'].lower()}"
                     data-sources="{' '.join([ds['name'].lower() for ds in dashboard['data_sources']])}">
                    <div class="dashboard-name">{dashboard['name']}</div>
                    <div class="dashboard-description {desc_class}">{desc}</div>
                    {tags_html}
                    <div class="dashboard-meta">
                        <div class="meta-item">👤 {dashboard['owner']}</div>
                        <div class="meta-item">📁 {dashboard['project']}</div>
                        <div class="meta-item">📊 {dashboard['sheet_count']} sheets</div>
                        <div class="meta-item">👁 {total_views:,} views</div>
                    </div>
                    <div class="dashboard-meta">
                        <div class="meta-item">📅 Created: {created_date}</div>
                        <div class="meta-item">🔄 Updated: {updated_date}</div>
                    </div>
                    {data_sources_html}
                    {views_html}
                    <a href="{dashboard['url']}" class="dashboard-link" target="_blank">View Dashboard →</a>
                </div>
'''

html += '''
            </div>
        </div>
        
        <div class="no-results" id="no-results" style="display: none;">
            No dashboards found matching your search criteria.
        </div>
    </div>
    
    <script>
        // Toggle data sources visibility
        function toggleDataSources(header) {
            const list = header.nextElementSibling;
            const btn = header.querySelector('.toggle-btn');
            list.classList.toggle('collapsed');
            btn.textContent = list.classList.contains('collapsed') ? '▼ Show' : '▲ Hide';
        }
        
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const filterButtons = document.querySelectorAll('.filter-btn');
        const dashboardCards = document.querySelectorAll('.dashboard-card');
        const noResults = document.getElementById('no-results');
        const productionCount = document.getElementById('production-count');
        const playgroundCount = document.getElementById('playground-count');
        const sections = document.querySelectorAll('.section');
        
        let currentFilter = 'all';
        
        function updateDisplay() {
            const searchTerm = searchInput.value.toLowerCase();
            let visibleCount = 0;
            let productionVisible = 0;
            let playgroundVisible = 0;
            
            dashboardCards.forEach(card => {
                const category = card.dataset.category;
                const name = card.dataset.name;
                const description = card.dataset.description;
                const tags = card.dataset.tags;
                const owner = card.dataset.owner;
                const sources = card.dataset.sources;
                
                const searchableText = `${name} ${description} ${tags} ${owner} ${sources}`;
                const matchesSearch = searchableText.includes(searchTerm);
                const matchesFilter = currentFilter === 'all' || category === currentFilter;
                
                if (matchesSearch && matchesFilter) {
                    card.style.display = 'block';
                    visibleCount++;
                    if (category === 'production') productionVisible++;
                    if (category === 'playground') playgroundVisible++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            // Update counts
            productionCount.textContent = productionVisible;
            playgroundCount.textContent = playgroundVisible;
            
            // Show/hide sections based on filter
            sections.forEach(section => {
                const sectionType = section.dataset.section;
                if (currentFilter === 'all') {
                    section.style.display = 'block';
                } else if (currentFilter === sectionType) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
            
            // Show no results message
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        }
        
        searchInput.addEventListener('input', updateDisplay);
        
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                currentFilter = button.dataset.filter;
                updateDisplay();
            });
        });
    </script>
</body>
</html>
'''

# Write the HTML file
with open('roc_dashboards_enhanced.html', 'w') as f:
    f.write(html)

print("✅ Enhanced HTML generated: roc_dashboards_enhanced.html")
print(f"📊 Total dashboards: {len(production) + len(playground)}")
print("✨ Features included:")
print("   ✓ Search by name, description, tags, owner, data source")
print("   ✓ Filter by category (Production/Playground)")
print("   ✓ Descriptions and tags")
print("   ✓ All views/sheets with direct links")
print("   ✓ Data source information")
print("   ✓ Created and updated dates")
print("   ✓ Sheet counts")

