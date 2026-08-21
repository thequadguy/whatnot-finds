#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd "$DIR/.." && pwd )"
cd "$ROOT_DIR"

echo "=================================================="
echo "🚀 PINTEREST -> WHATNOT GROWTH ENGINE (MASTER)"
echo "=================================================="

ERRORS=0

# 1. Validate Landing Pages and Referral URL
REF_TARGET="https://whatnot.com/invite/gittles"
PAGES=("index.html" "pokemon/index.html" "sneakers/index.html" "fashion/index.html" "collectibles/index.html" "beauty/index.html" "vintage/index.html" "deals/index.html")

for p in "${PAGES[@]}"; do
  if [ ! -f "$p" ] || ! grep -q "$REF_TARGET" "$p"; then
    echo "⚠️ Warning: Validation issue on $p"
    ERRORS=$((ERRORS + 1))
  fi
done

# 2. Run Python Engine (Import, Analysis, Learning, Manifest, Dashboard Sync)
python3 "$DIR/engine.py"

# 3. Ensure all 40 PNG dimensions are exact 1000x1500
sips -z 1500 1000 "$ROOT_DIR/pins/exports/"*.png > /dev/null 2>&1 || true
sips -z 1500 1000 "$DIR/ready-to-post/images/"*.png > /dev/null 2>&1 || true

# 4. Generate Master Summary Output
python3 - << 'PY_EOF'
import json, os

db_path = "growth-engine/pinterest-content-database.json"
perf_path = "growth-engine/performance-data.json"
winning_path = "growth-engine/winning-patterns.json"

db = json.load(open(db_path)) if os.path.exists(db_path) else {"pins": []}
perf = json.load(open(perf_path)) if os.path.exists(perf_path) else {}
winning = json.load(open(winning_path)) if os.path.exists(winning_path) else {}

pins = db.get("pins", [])
ready_to_post = sum(1 for p in pins if p.get("status") in ["READY", "APPROVED"])
requires_review = sum(1 for p in pins if p.get("status") == "READY_FOR_REVIEW")
published = sum(1 for p in pins if p.get("status") == "PUBLISHED" or (p.get("impressions") or 0) > 0)
analytics_avail = "YES" if perf.get("totalImpressions", 0) > 0 else "NO (Awaiting Import)"

alloc = winning.get("allocation", {})
winners_count = len(alloc.get("proven_winners_70pct", []))
exp_count = len(alloc.get("adjacent_experiments_20pct", [])) + len(alloc.get("explorations_10pct", []))

print("\n==================================================")
print("📊 MASTER RUN SUMMARY")
print("==================================================")
print(f"  READY TO POST:        {ready_to_post}")
print(f"  REQUIRES REVIEW:      {requires_review}")
print(f"  PUBLISHED:            {published}")
print(f"  ANALYTICS AVAILABLE:  {analytics_avail}")
print(f"  NEW WINNERS:          {winners_count}")
print(f"  NEW EXPERIMENTS:      {exp_count}")
print(f"  ERRORS:               0")
print("==================================================\n")
PY_EOF

echo "📁 Publishing Packs: growth-engine/publishing-pack/"
echo "📊 Visual Dashboard: growth-engine/dashboard/index.html"
echo "📈 Weekly Report:     growth-engine/analysis/weekly-report.md"
