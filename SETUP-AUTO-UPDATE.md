# 🤖 Setup Automatic Weekly Updates

Your dashboard will automatically update **every Monday at 10 AM Israel time** (8 AM UTC).

## Step 1: Add Tableau Credentials to GitHub Secrets

1. Go to your GitHub repository: **https://github.com/morhaliva/roc-dashboards**

2. Click **Settings** tab

3. In the left sidebar, click **Secrets and variables** → **Actions**

4. Click **New repository secret** (green button)

5. Add these 4 secrets one by one:

### Secret 1: TABLEAU_SERVER
- Name: `TABLEAU_SERVER`
- Value: `https://tableau.office.taboola.com`
- Click **Add secret**

### Secret 2: TABLEAU_SITE_NAME
- Name: `TABLEAU_SITE_NAME`
- Value: (leave empty or put the site name if not default)
- Click **Add secret**

### Secret 3: TABLEAU_PAT_NAME
- Name: `TABLEAU_PAT_NAME`
- Value: `mor.h2` (your Tableau Personal Access Token name)
- Click **Add secret**

### Secret 4: TABLEAU_PAT_VALUE
- Name: `TABLEAU_PAT_VALUE`
- Value: (your Tableau Personal Access Token secret - the long encrypted string)
- Click **Add secret**

---

## Step 2: Push the Workflow File to GitHub

Run these commands:

```bash
cd /Users/mor.h/.cursor/deployment
git add .github/workflows/update-dashboards.yml
git add generate_dashboard_html.py
git commit -m "Add automatic weekly update workflow"
git push
```

---

## Step 3: Test It! (Optional)

You can manually trigger the update to test it works:

1. Go to your repo: **https://github.com/morhaliva/roc-dashboards**
2. Click the **Actions** tab
3. Click **Update ROC Dashboards Weekly** on the left
4. Click **Run workflow** button (right side)
5. Click the green **Run workflow** button in the popup
6. Watch it run! Should complete in 1-2 minutes

---

## 🎉 That's It!

Your dashboard will now automatically update:
- ⏰ **Every Monday at 10 AM Israel time**
- 🔄 Fetches fresh data from Tableau
- 📊 Regenerates the dashboard HTML
- 🚀 Pushes changes to GitHub Pages
- 🌐 Live URL updates automatically

You can also manually trigger updates anytime from the Actions tab!

---

## Change the Schedule

To update more or less frequently, edit `.github/workflows/update-dashboards.yml`:

```yaml
schedule:
  # Daily at 10 AM Israel time
  - cron: '0 8 * * *'
  
  # OR Twice a week (Monday & Thursday)
  - cron: '0 8 * * 1,4'
  
  # OR Monthly (first Monday)
  - cron: '0 8 1-7 * 1'
```

---

## 🔒 Security Note

Your Tableau credentials are stored securely as GitHub Secrets. They:
- ✅ Are encrypted
- ✅ Never appear in logs
- ✅ Only accessible to your repository
- ✅ Can be rotated anytime in Settings → Secrets

