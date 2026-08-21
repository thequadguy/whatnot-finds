#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/.."

echo "=================================================="
echo "☀️ WHATNOT FINDS — DAILY OPERATIONAL CHECK"
echo "=================================================="

# 1. Run Status
"$DIR/status.sh"

# 2. Check for newly dropped analytics CSV in manual-data
CSV_INPUT="$DIR/input/manual-data/pinterest-performance.csv"
if [ -f "$CSV_INPUT" ]; then
  echo ""
  echo "📥 New Pinterest Analytics CSV detected! Running engine update..."
  "$DIR/run.sh"
else
  echo ""
  echo "ℹ️  No new analytics CSV in input/manual-data/ — system on schedule."
fi

echo ""
echo "✨ Daily check complete. Have a great publishing day!"
