# ⏱️ Local Scheduling & Automation Guide (macOS / Linux)

This guide documents how you can optionally schedule `./growth-engine/daily.sh` and `./growth-engine/weekly.sh` to run automatically on your local machine.

---

## 🔒 Safety & Control Notice
We do **not** silently install background daemons. You have complete control over whether and how automated scheduling is enabled.

---

## 🛠️ Option A: Standard `cron` Schedule (Recommended)

To run a daily health check at 9:00 AM and a weekly analysis on Sundays at 10:00 AM:

1. Open your terminal and edit your user crontab:
   ```bash
   crontab -e
   ```

2. Add the following two lines (adjust paths to your project):
   ```cron
   # Daily Pinterest Funnel Health Check at 9:00 AM
   0 9 * * * cd /Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing && ./growth-engine/daily.sh >> growth-engine/analysis/daily.log 2>&1

   # Weekly Performance Analysis & Report on Sundays at 10:00 AM
   0 10 * * 0 cd /Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing && ./growth-engine/weekly.sh >> growth-engine/analysis/weekly.log 2>&1
   ```

3. Save and exit (`:wq` in vim or `Ctrl+O`, `Ctrl+X` in nano).

---

## 🖥️ Option B: Manual Execution (Simplest)
Whenever you want to check status or run the weekly report, just run directly:
- Check status: `./growth-engine/status.sh`
- Daily check: `./growth-engine/daily.sh`
- Weekly cycle: `./growth-engine/weekly.sh`
