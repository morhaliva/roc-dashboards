#!/usr/bin/env python3
"""
Generate enhanced HTML with search, filters, and rich metadata
Beautiful dark theme matching the Knowledge Base design
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a24;
            --bg-card-hover: #22222e;
            --border: rgba(255, 255, 255, 0.08);
            --border-hover: rgba(255, 255, 255, 0.15);
            --text-primary: #f8f8f8;
            --text-secondary: #a0a0b0;
            --text-muted: #6b6b7b;
            --accent-cyan: #00d4ff;
            --accent-purple: #a855f7;
            --accent-green: #10b981;
            --accent-orange: #f59e0b;
            --accent-pink: #ec4899;
            --accent-blue: #3b82f6;
            --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #00d4ff 0%, #a855f7 100%);
            --shadow-glow: 0 0 40px rgba(0, 212, 255, 0.15);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            min-height: 100vh;
            color: var(--text-primary);
            overflow-x: hidden;
        }}

        /* Animated Background */
        .bg-pattern {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(168, 85, 247, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(0, 212, 255, 0.05) 0%, transparent 70%);
            animation: bgPulse 15s ease-in-out infinite;
        }}

        @keyframes bgPulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}

        .container {{
            max-width: 1500px;
            margin: 0 auto;
            padding: 30px 40px 60px;
        }}

        /* Back Button */
        .back-button {{
            position: fixed;
            top: 25px;
            left: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 14px 22px;
            background: var(--bg-card);
            color: var(--accent-cyan);
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95em;
            border: 1px solid var(--border);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            z-index: 1000;
            backdrop-filter: blur(10px);
        }}

        .back-button:hover {{
            background: var(--accent-cyan);
            color: var(--bg-primary);
            transform: translateX(-5px);
            box-shadow: 0 0 25px rgba(0, 212, 255, 0.4);
        }}

        /* Header */
        .header {{
            text-align: center;
            padding: 60px 0 50px;
        }}

        .header-icon {{
            font-size: 4em;
            margin-bottom: 15px;
            display: inline-block;
            animation: float 3s ease-in-out infinite;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}

        .header h1 {{
            font-size: 3.2em;
            font-weight: 700;
            margin-bottom: 12px;
            background: var(--gradient-2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .header-subtitle {{
            font-size: 1.15em;
            color: var(--text-secondary);
            margin-bottom: 5px;
        }}

        .header-date {{
            font-size: 0.9em;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Stats */
        .stats {{
            display: flex;
            gap: 25px;
            justify-content: center;
            margin-bottom: 45px;
            flex-wrap: wrap;
        }}

        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 25px 40px;
            border-radius: 16px;
            text-align: center;
            transition: all 0.3s ease;
            min-width: 160px;
        }}

        .stat-card:hover {{
            border-color: var(--accent-cyan);
            box-shadow: var(--shadow-glow);
            transform: translateY(-3px);
        }}

        .stat-card.production {{ border-left: 4px solid var(--accent-green); }}
        .stat-card.playground {{ border-left: 4px solid var(--accent-purple); }}
        .stat-card.total {{ border-left: 4px solid var(--accent-cyan); }}

        .stat-number {{
            font-size: 2.8em;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 8px;
        }}

        .stat-card.production .stat-number {{ color: var(--accent-green); }}
        .stat-card.playground .stat-number {{ color: var(--accent-purple); }}
        .stat-card.total .stat-number {{ color: var(--accent-cyan); }}

        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.95em;
            font-weight: 500;
        }}

        /* Search & Filter */
        .search-filter-bar {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 25px 30px;
            border-radius: 16px;
            margin-bottom: 40px;
        }}

        .search-box {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }}

        .search-input {{
            flex: 1;
            padding: 16px 24px;
            background: var(--bg-secondary);
            border: 2px solid var(--border);
            border-radius: 12px;
            font-size: 1em;
            color: var(--text-primary);
            font-family: 'DM Sans', sans-serif;
            transition: all 0.3s ease;
        }}

        .search-input::placeholder {{
            color: var(--text-muted);
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.1);
        }}

        .filter-buttons {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            padding: 12px 24px;
            background: var(--bg-secondary);
            border: 2px solid var(--border);
            border-radius: 10px;
            color: var(--text-secondary);
            font-family: 'DM Sans', sans-serif;
            font-size: 0.95em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .filter-btn:hover {{
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }}

        .filter-btn.active {{
            background: var(--gradient-2);
            border-color: transparent;
            color: var(--bg-primary);
        }}

        /* Section Headers */
        .section {{
            margin-bottom: 50px;
        }}

        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding: 20px 25px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
        }}

        .section-title {{
            font-size: 1.6em;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .section-title.production {{ color: var(--accent-green); }}
        .section-title.playground {{ color: var(--accent-purple); }}

        .section-count {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1em;
            font-weight: 600;
            padding: 8px 18px;
            border-radius: 20px;
            color: white;
        }}

        .section-count.production {{ background: var(--accent-green); }}
        .section-count.playground {{ background: var(--accent-purple); }}

        /* Dashboard Grid */
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 25px;
        }}

        /* Dashboard Cards */
        .dashboard-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 28px;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
        }}

        .dashboard-card:hover {{
            border-color: var(--border-hover);
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}

        .dashboard-card[data-category="production"]:hover {{
            border-color: rgba(16, 185, 129, 0.4);
            box-shadow: 0 20px 40px rgba(16, 185, 129, 0.1);
        }}

        .dashboard-card[data-category="playground"]:hover {{
            border-color: rgba(168, 85, 247, 0.4);
            box-shadow: 0 20px 40px rgba(168, 85, 247, 0.1);
        }}

        .dashboard-name {{
            font-size: 1.3em;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 10px;
            line-height: 1.35;
        }}

        .dashboard-description {{
            color: var(--text-secondary);
            margin-bottom: 18px;
            line-height: 1.6;
            font-size: 0.95em;
        }}

        .dashboard-description.empty {{
            color: var(--text-muted);
            font-style: italic;
        }}

        /* Meta Info */
        .dashboard-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px 20px;
            margin-bottom: 16px;
            font-size: 0.88em;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-muted);
        }}

        .meta-item .icon {{
            font-size: 1em;
        }}

        .meta-highlight {{
            color: var(--accent-cyan);
            font-weight: 600;
        }}

        /* Tags */
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 16px;
        }}

        .tag {{
            background: rgba(168, 85, 247, 0.15);
            color: var(--accent-purple);
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 0.82em;
            font-weight: 500;
        }}

        /* Collapsible Sections */
        .collapsible-section {{
            margin-bottom: 16px;
            background: var(--bg-secondary);
            border-radius: 10px;
            overflow: hidden;
        }}

        .collapsible-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            cursor: pointer;
            transition: background 0.2s;
        }}

        .collapsible-header:hover {{
            background: rgba(255, 255, 255, 0.03);
        }}

        .collapsible-title {{
            font-weight: 600;
            font-size: 0.9em;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .toggle-icon {{
            font-size: 0.75em;
            color: var(--text-muted);
            transition: transform 0.3s;
        }}

        .toggle-icon.open {{
            transform: rotate(180deg);
        }}

        .collapsible-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }}

        .collapsible-content.open {{
            max-height: 500px;
        }}

        .collapsible-inner {{
            padding: 0 16px 14px;
        }}

        /* Data Sources */
        .data-source {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 6px 0;
            font-size: 0.88em;
            color: var(--text-secondary);
        }}

        .ds-badge {{
            display: inline-flex;
            align-items: center;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.7em;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.5px;
        }}

        .ds-badge.vertica {{ background: rgba(0, 150, 136, 0.2); color: #00bfa5; }}
        .ds-badge.bigquery {{ background: rgba(66, 133, 244, 0.2); color: #4285f4; }}
        .ds-badge.other {{ background: rgba(255, 152, 0, 0.2); color: #ff9800; }}

        /* Views/Sheets */
        .view-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .view-link {{
            padding: 7px 14px;
            background: rgba(59, 130, 246, 0.1);
            color: var(--accent-blue);
            text-decoration: none;
            border-radius: 8px;
            font-size: 0.82em;
            font-weight: 500;
            transition: all 0.2s;
            border: 1px solid transparent;
        }}

        .view-link:hover {{
            background: var(--accent-blue);
            color: white;
            transform: translateY(-2px);
        }}

        .view-count {{
            opacity: 0.7;
            font-size: 0.9em;
        }}

        /* Dashboard Link Button */
        .dashboard-link {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 14px 28px;
            background: var(--gradient-2);
            color: var(--bg-primary);
            text-decoration: none;
            border-radius: 10px;
            font-weight: 700;
            font-size: 0.95em;
            transition: all 0.3s ease;
            margin-top: auto;
        }}

        .dashboard-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
        }}

        /* No Results */
        .no-results {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 60px 40px;
            border-radius: 16px;
            text-align: center;
        }}

        .no-results-icon {{
            font-size: 4em;
            margin-bottom: 20px;
            opacity: 0.5;
        }}

        .no-results-text {{
            color: var(--text-muted);
            font-size: 1.2em;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px 20px;
            margin-top: 40px;
            border-top: 1px solid var(--border);
            color: var(--text-muted);
        }}

        .footer-credit {{
            margin-top: 10px;
            font-size: 0.95em;
        }}

        .footer-credit strong {{
            color: var(--accent-cyan);
        }}

        /* Responsive */
        @media (max-width: 900px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}

            .container {{
                padding: 20px;
            }}

            .header h1 {{
                font-size: 2.2em;
            }}

            .back-button {{
                top: 15px;
                left: 15px;
                padding: 10px 16px;
                font-size: 0.85em;
            }}

            .stats {{
                gap: 15px;
            }}

            .stat-card {{
                padding: 20px 30px;
                min-width: 120px;
            }}

            .stat-number {{
                font-size: 2.2em;
            }}
        }}

        /* Animation for cards on load */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .dashboard-card {{
            animation: fadeInUp 0.5s ease forwards;
        }}
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    
    <a href="knowledge-base.html" class="back-button">
        <span>←</span> Back to Knowledge Base
    </a>

    <div class="container">
        <div class="header">
            <div class="header-icon">📊</div>
            <h1>ROC Tableau Dashboards</h1>
            <p class="header-subtitle">Revenue Operations Center Dashboard Portal</p>
            <p class="header-date">Last updated: {formatted_date}</p>
        </div>

        <div class="stats">
            <div class="stat-card production">
                <div class="stat-number">{len(production)}</div>
                <div class="stat-label">🏭 Production</div>
            </div>
            <div class="stat-card playground">
                <div class="stat-number">{len(playground)}</div>
                <div class="stat-label">🎮 Playground</div>
            </div>
            <div class="stat-card total">
                <div class="stat-number">{len(production) + len(playground)}</div>
                <div class="stat-label">📈 Total</div>
            </div>
        </div>

        <div class="search-filter-bar">
            <div class="search-box">
                <input type="text" id="searchInput" class="search-input" 
                       placeholder="🔍  Search by name, description, owner, or data source...">
            </div>
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">✨ All Dashboards</button>
                <button class="filter-btn" data-filter="production">🏭 Production</button>
                <button class="filter-btn" data-filter="playground">🎮 Playground</button>
            </div>
        </div>

        <div class="section" data-section="production">
            <div class="section-header">
                <div class="section-title production">
                    <span>🏭</span> Production Dashboards
                </div>
                <div class="section-count production" id="production-count">{len(production)}</div>
            </div>
            <div class="dashboard-grid" id="production-grid">
'''

def generate_card(dashboard, category):
    """Generate HTML for a single dashboard card"""
    desc = dashboard['description'] if dashboard['description'] else 'No description available'
    desc_class = '' if dashboard['description'] else 'empty'
    
    tags_html = ''
    if dashboard['tags']:
        tags_html = '<div class="tags">'
        for tag in dashboard['tags']:
            tags_html += f'<span class="tag">🏷️ {tag}</span>'
        tags_html += '</div>'
    
    # Data Sources Section
    data_sources_html = ''
    if dashboard['data_sources']:
        ds_count = len(dashboard['data_sources'])
        ds_items = ''
        for ds in dashboard['data_sources']:
            ds_name = ds['name']
            ds_type = ds.get('type', 'unknown').upper()
            badge_class = 'vertica' if 'vertica' in ds_type.lower() else 'bigquery' if 'bigquery' in ds_type.lower() else 'other'
            ds_items += f'<div class="data-source"><span class="ds-badge {badge_class}">{ds_type}</span>{ds_name}</div>'
        
        data_sources_html = f'''
            <div class="collapsible-section">
                <div class="collapsible-header" onclick="toggleSection(this)">
                    <span class="collapsible-title">🗄️ Data Sources ({ds_count})</span>
                    <span class="toggle-icon">▼</span>
                </div>
                <div class="collapsible-content">
                    <div class="collapsible-inner">{ds_items}</div>
                </div>
            </div>'''
    
    # Views/Sheets Section
    views_html = ''
    if len(dashboard['views']) > 0:
        view_count_total = len(dashboard['views'])
        view_items = ''
        for view in dashboard['views']:
            view_count = int(view.get('viewCount', 0) or 0)
            count_display = f' <span class="view-count">({view_count:,}👁)</span>' if view_count > 0 else ""
            view_items += f'<a href="{view["url"]}" class="view-link" target="_blank">{view["name"]}{count_display}</a>'
        
        views_html = f'''
            <div class="collapsible-section">
                <div class="collapsible-header" onclick="toggleSection(this)">
                    <span class="collapsible-title">📑 Sheets ({view_count_total})</span>
                    <span class="toggle-icon">▼</span>
                </div>
                <div class="collapsible-content">
                    <div class="collapsible-inner"><div class="view-links">{view_items}</div></div>
                </div>
            </div>'''
    
    created_date = datetime.fromisoformat(dashboard['created'].replace('Z', '+00:00')).strftime('%b %d, %Y')
    updated_date = datetime.fromisoformat(dashboard['updated'].replace('Z', '+00:00')).strftime('%b %d, %Y')
    total_views = int(dashboard.get('total_views', 0) or 0)
    
    return f'''
            <div class="dashboard-card" data-category="{category}" 
                 data-name="{dashboard['name'].lower()}"
                 data-description="{desc.lower()}"
                 data-tags="{' '.join(dashboard['tags']).lower()}"
                 data-owner="{dashboard['owner'].lower()}"
                 data-sources="{' '.join([ds['name'].lower() for ds in dashboard['data_sources']])}">
                <div class="dashboard-name">{dashboard['name']}</div>
                <div class="dashboard-description {desc_class}">{desc}</div>
                {tags_html}
                <div class="dashboard-meta">
                    <div class="meta-item"><span class="icon">👤</span> {dashboard['owner']}</div>
                    <div class="meta-item"><span class="icon">📁</span> {dashboard['project']}</div>
                    <div class="meta-item"><span class="icon">📊</span> {dashboard['sheet_count']} sheets</div>
                    <div class="meta-item"><span class="icon">👁</span> <span class="meta-highlight">{total_views:,}</span> views</div>
                </div>
                <div class="dashboard-meta">
                    <div class="meta-item"><span class="icon">📅</span> Created: {created_date}</div>
                    <div class="meta-item"><span class="icon">🔄</span> Updated: {updated_date}</div>
                </div>
                {data_sources_html}
                {views_html}
                <a href="{dashboard['url']}" class="dashboard-link" target="_blank">
                    View Dashboard <span>→</span>
                </a>
            </div>
'''

# Generate production cards
for dashboard in production:
    html += generate_card(dashboard, 'production')

html += f'''
            </div>
        </div>

        <div class="section" data-section="playground">
            <div class="section-header">
                <div class="section-title playground">
                    <span>🎮</span> Playground Dashboards
                </div>
                <div class="section-count playground" id="playground-count">{len(playground)}</div>
            </div>
            <div class="dashboard-grid" id="playground-grid">
'''

# Generate playground cards
for dashboard in playground:
    html += generate_card(dashboard, 'playground')

html += '''
            </div>
        </div>

        <div class="no-results" id="no-results" style="display: none;">
            <div class="no-results-icon">🔍</div>
            <div class="no-results-text">No dashboards found matching your search criteria.</div>
        </div>

        <footer class="footer">
            <p class="footer-credit">
                Created by <strong>Mor Haliva</strong> | ROC Team © 2025
            </p>
        </footer>
    </div>

    <script>
        // Toggle collapsible sections
        function toggleSection(header) {
            const content = header.nextElementSibling;
            const icon = header.querySelector('.toggle-icon');
            content.classList.toggle('open');
            icon.classList.toggle('open');
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

            dashboardCards.forEach((card, index) => {
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
                    card.style.display = 'flex';
                    card.style.animationDelay = `${index * 0.05}s`;
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

        // Keyboard shortcut for search
        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
            }
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
print("   ✓ Beautiful dark theme matching Knowledge Base")
print("   ✓ Animated background and card effects")
print("   ✓ Search by name, description, tags, owner, data source")
print("   ✓ Filter by category (Production/Playground)")
print("   ✓ Collapsible data sources and sheets sections")
print("   ✓ View counts for each sheet")
print("   ✓ Keyboard shortcut (Cmd+K) for search")
print("   ✓ Responsive design")
