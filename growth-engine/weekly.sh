#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/.."

echo "=================================================="
echo "📊 WHATNOT FINDS — WEEKLY ENGINE CYCLE"
echo "=================================================="

# 1. Execute run.sh master pipeline
"$DIR/run.sh"

# 2. Archive the processed CSV if present
CSV_INPUT="$DIR/input/manual-data/pinterest-performance.csv"
ARCHIVE_DIR="$DIR/input/archive"
if [ -f "$CSV_INPUT" ]; then
  mkdir -p "$ARCHIVE_DIR"
  TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
  mv "$CSV_INPUT" "$ARCHIVE_DIR/pinterest_performance_$TIMESTAMP.csv"
  echo "📦 Archived imported data to input/archive/pinterest_performance_$TIMESTAMP.csv"
fi

echo ""
echo "=================================================="
echo "✅ WEEKLY CYCLE COMPLETE"
echo "=================================================="
echo "📊 Dashboard updated: growth-engine/dashboard/index.html"
echo "📈 Weekly report:    growth-engine/analysis/weekly-report.md"
