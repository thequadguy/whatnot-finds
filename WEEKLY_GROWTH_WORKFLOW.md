# 🔄 Weekly Pinterest → Whatnot Growth Workflow

Follow this simple 10-minute weekly routine to operate the semi-automated growth engine.

---

## ⏱️ The 10-Minute Weekly Checklist

### 1. Export Data from Pinterest Analytics (2 mins)
- Log into your Pinterest Business account.
- Go to **Analytics** &rarr; **Overview**.
- Export impressions, saves, and outbound clicks for the past 7–14 days.
- Paste values into [`growth-engine/input/manual-data/pinterest-performance.csv`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/input/manual-data/pinterest-performance-template.csv).

### 2. Run the Growth Engine (1 min)
In your terminal, execute:
```bash
./growth-engine/run.sh
```
*The engine will automatically analyze winners, generate the next batch of pin concepts, run compliance checks, render high-res 1000 × 1500 px graphics, update the CSV manifest, and refresh the dashboard.*

### 3. Open the Local Dashboard (2 mins)
Open [`growth-engine/dashboard/index.html`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/dashboard/index.html) in your browser:
- Review top-performing categories, hooks, and visual templates.
- Check the weekly strategic audit in [`growth-engine/analysis/weekly-report.md`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/analysis/weekly-report.md).

### 4. Review the Ready-to-Post Queue (2 mins)
- View the contact sheet in [`growth-engine/ready-to-post/images/contact_sheet.jpg`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/ready-to-post/images/contact_sheet.jpg).
- Open the upload manifest: [`growth-engine/ready-to-post/csv/pinterest-upload-manifest.csv`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/ready-to-post/csv/pinterest-upload-manifest.csv).

### 5. Schedule / Publish on Pinterest (3 mins)
- Use Pinterest's native Pin Scheduler (free) or manual Pin Creator to upload the approved graphics to their designated boards.
- Copy/paste the Title, Description, and Destination URL from the manifest CSV.

---

## 🎯 Continuous Growth Cycle

```
[ POST PINS ] ──> [ GATHER DATA ] ──> [ RUN ./run.sh ] ──> [ REVIEW DASHBOARD ] ──> [ APPROVE NEXT BATCH ]
```
