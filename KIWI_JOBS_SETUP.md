# ROC Kiwi Jobs Setup

## Overview
The ROC Kiwi Jobs page displays all ROC-related jobs from the Kiwi platform in a user-friendly directory format, similar to the ROC Alerts page.

## Files
- `roc-kiwi-jobs.html` - The generated HTML page
- `roc_kiwi_jobs.json` - JSON data file containing all ROC jobs
- `generate_kiwi_jobs_html.py` - Script to generate HTML from JSON

## How to Add/Update Jobs

### Option 1: Manual JSON Editing
1. Edit `roc_kiwi_jobs.json` in the `deployment` folder
2. Add job entries in this format:
```json
{
  "name": "Job Name",
  "creator": "mor.h",
  "description": "Job description",
  "schedule": "Hourly/Daily/etc",
  "last_run": "2025-12-31 10:00",
  "status": "Active",
  "url": "https://kiwi.taboolasyndication.com/reports/view_query/XXX",
  "category": "Revenue/Spend/Regional/etc"
}
```

3. Run the generator:
```bash
cd ~/.cursor && python3 generate_kiwi_jobs_html.py
```

4. Commit and push:
```bash
cd ~/.cursor/deployment && git add -A && git commit -m "Update Kiwi jobs" && git push
```

### Option 2: Automated Fetching (Future)
The `fetch_kiwi_jobs.py` script can be enhanced to automatically fetch jobs from Kiwi. It requires:
- Kiwi platform credentials
- Playwright installed (`pip3 install playwright && python3 -m playwright install chromium`)

## ROC Team Members
Jobs are filtered by these creators:
- mor.h
- guy.d
- yahel.o
- igor.g

Or jobs with "ROC" in their name.

## Updating the Page
After updating `roc_kiwi_jobs.json`, run:
```bash
python3 generate_kiwi_jobs_html.py
```

Then commit and push the changes.

