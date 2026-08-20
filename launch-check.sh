#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "🔍 WHATNOT PINTEREST FUNNEL — PRE-LAUNCH AUDIT"
echo "=================================================="
echo ""

FAILURES=0
WARNINGS=0

pass() {
  echo "  ✅ PASS: $1"
}

fail() {
  echo "  ❌ FAIL: $1"
  FAILURES=$((FAILURES + 1))
}

warn() {
  echo "  ⚠️ WARN: $1"
  WARNINGS=$((WARNINGS + 1))
}

echo "1. Checking Core Web Landing Pages..."
PAGES=("index.html" "pokemon/index.html" "sneakers/index.html" "fashion/index.html" "collectibles/index.html" "beauty/index.html" "vintage/index.html" "deals/index.html")
for p in "${PAGES[@]}"; do
  if [ -f "$p" ]; then
    pass "$p exists"
  else
    fail "$p missing"
  fi
done

echo ""
echo "2. Verifying Whatnot Referral Target Link..."
REF_TARGET="https://whatnot.com/invite/gittles"
for p in "${PAGES[@]}"; do
  if grep -q "$REF_TARGET" "$p"; then
    pass "$p contains exact referral URL"
  else
    fail "$p missing referral URL $REF_TARGET"
  fi
done

echo ""
echo "3. Checking SEO & Crawl Directives..."
if [ -f "robots.txt" ]; then pass "robots.txt exists"; else fail "robots.txt missing"; fi
if [ -f "sitemap.xml" ]; then pass "sitemap.xml exists"; else fail "sitemap.xml missing"; fi

echo ""
echo "4. Verifying All 40 Pin Graphics (1000 × 1500 px)..."
PIN_COUNT_01_30=$(find pins/exports -name "pin-*.png" | wc -l | tr -d ' ')
PIN_COUNT_31_40=$(find growth-engine/ready-to-post/images -name "pin-*.png" | wc -l | tr -d ' ')

if [ "$PIN_COUNT_01_30" -eq 30 ]; then
  pass "Batch #01 has 30 PNGs in pins/exports/"
else
  fail "Batch #01 expected 30 PNGs, found $PIN_COUNT_01_30"
fi

if [ "$PIN_COUNT_31_40" -eq 10 ]; then
  pass "Batch #02 has 10 PNGs in growth-engine/ready-to-post/images/"
else
  fail "Batch #02 expected 10 PNGs, found $PIN_COUNT_31_40"
fi

# Check dimensions on all 40 files
python3 - << 'PY_EOF'
import glob, sys
from PIL import Image

errors = 0
all_pins = glob.glob("pins/exports/pin-*.png") + glob.glob("growth-engine/ready-to-post/images/pin-*.png")
for p in all_pins:
    with Image.open(p) as img:
        if img.size != (1000, 1500):
            print(f"  ❌ Invalid dimension on {p}: {img.size}")
            errors += 1

if errors == 0:
    print("  ✅ PASS: All 40 PNG graphics verified at exact 1000 × 1500 pixels!")
else:
    print(f"  ❌ FAIL: {errors} files have incorrect dimensions.")
    sys.exit(1)
PY_EOF

echo ""
echo "5. Verifying Growth Engine & Local Dashboard..."
if [ -f "growth-engine/engine.py" ]; then pass "growth-engine/engine.py exists"; else fail "engine.py missing"; fi
if [ -f "growth-engine/run.sh" ]; then pass "growth-engine/run.sh exists"; else fail "run.sh missing"; fi
if [ -f "growth-engine/dashboard/index.html" ]; then pass "dashboard UI exists"; else fail "dashboard UI missing"; fi
if [ -f "growth-engine/ready-to-post/csv/pinterest-upload-manifest.csv" ]; then pass "upload manifest CSV exists"; else fail "upload manifest CSV missing"; fi
if [ -f "pins/whatnot-pinterest-30-pins.zip" ]; then pass "Batch #01 ZIP archive exists"; else fail "Batch #01 ZIP missing"; fi

echo ""
echo "=================================================="
if [ $FAILURES -eq 0 ]; then
  echo "🎉 ALL SYSTEMS PASS — FUNNEL IS 100% READY FOR LAUNCH!"
else
  echo "❌ $FAILURES FAILURES DETECTED. PLEASE REVIEW."
  exit 1
fi
echo "=================================================="
