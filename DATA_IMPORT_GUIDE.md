# 📥 Pinterest Analytics Data Import Guide

This guide explains how to import performance metrics from Pinterest Analytics into the Growth Engine without manual data cleaning.

---

## 📍 Where to Put Your Analytics File

Save your CSV export to:
[`growth-engine/input/manual-data/pinterest-performance.csv`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/input/manual-data/pinterest-performance-template.csv)

---

## 📋 Supported CSV Formats

The importer is flexible and automatically accepts standard Pinterest Analytics columns or custom sheets:

### Minimal Required Format:
```csv
pin_id,impressions,saves,outbound_clicks
PIN-01,1240,48,22
PIN-02,3420,112,68
PIN-03,890,24,14
```

### Full Multi-Touch Funnel Format (Optional):
```csv
pin_id,date,impressions,saves,outbound_clicks,landing_sessions,referral_clicks,signups
PIN-01,2026-08-25,1240,48,22,19,4,Unavailable
PIN-02,2026-08-25,3420,112,68,61,15,Unavailable
```

---

## 🛠️ Automated Tolerances & Protections

- **Column Header Aliases:** Automatically accepts `Pin ID`, `pin_id`, `ID`, `Impressions`, `Views`, `Saves`, `Repins`, `Pin clicks`, `Outbound clicks`, `Link clicks`, etc.
- **Number Sanitization:** Automatically removes commas (e.g. `1,240` &rarr; `1240`) and percentage signs (e.g. `2.5%` &rarr; `2.5`).
- **Duplicate Protection:** Automatically ignores accidental repeated rows for the same Pin ID.
- **Zero Fabrication Guarantee:** Missing fields remain `0` or `Unavailable`. The system will never guess or invent data.

---

## ⚡ Run Import Command

To import and trigger the intelligence analysis:
```bash
# Option A: Run full pipeline with import
./growth-engine/run.sh

# Option B: Run import only
python3 growth-engine/engine.py --import growth-engine/input/manual-data/pinterest-performance.csv
```
