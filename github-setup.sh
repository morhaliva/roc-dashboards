#!/bin/bash

echo "🚀 Quick GitHub Pages Setup for ROC Dashboards"
echo "==============================================="
echo ""

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed"
    exit 1
fi

# Create a new directory for the repo
REPO_DIR="roc-dashboards-site"

echo "📁 Creating repository directory..."
mkdir -p $REPO_DIR
cd $REPO_DIR

# Initialize git
git init

# Copy files
echo "📋 Copying dashboard files..."
cp ../roc_dashboards.html index.html
cp ../all_dashboards_data.json .

# Create README
cat > README.md << 'EOF'
# ROC Tableau Dashboards

Internal dashboard hub for ROC team.

## Access

Visit: https://YOUR-USERNAME.github.io/roc-dashboards-site/

## Update

To update the dashboard:
1. Replace `index.html` and `all_dashboards_data.json`
2. Commit and push changes
EOF

# Add all files
git add .
git commit -m "Initial commit - ROC Dashboards"

echo ""
echo "✅ Repository initialized!"
echo ""
echo "📝 Next steps:"
echo "1. Go to GitHub.com and create a new PRIVATE repository named 'roc-dashboards-site'"
echo "2. Run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR-USERNAME/roc-dashboards-site.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. In GitHub repo settings:"
echo "   - Go to Settings > Pages"
echo "   - Source: Deploy from branch 'main'"
echo "   - Folder: / (root)"
echo "   - Save"
echo ""
echo "4. Your dashboard will be at:"
echo "   https://YOUR-USERNAME.github.io/roc-dashboards-site/"
echo ""
echo "5. Share this URL with your team!"
echo ""

