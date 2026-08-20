# 🚀 Pinterest → Whatnot Growth Engine

A semi-automated, data-driven organic growth and content optimization engine for driving high-intent Whatnot referral signups from Pinterest.

**Referral URL:** `https://whatnot.com/invite/gittles`  
**Operating Cost:** **$0 / month** (Zero paid APIs, zero paid hosting, zero paid tools)  
**Architecture:** 100% local Python pipeline + static client-side dashboard  

---

## 🏗️ System Architecture

```
Pinterest Organic Discovery (Visual Feed / Search)
               │
               ▼
   1000 × 1500 Curated Pin Graphic (Rotating Templates A–F)
               │
               ▼
  Dedicated Hub (e.g. /pokemon/, /sneakers/, /fashion/)
               │
               ▼
   Whatnot Referral CTA (whatnot.com/invite/gittles)
               │
               ▼
      Eligible New-User Signup ($10–$15 Credit)
```

---

## 📁 Directory Structure

```
growth-engine/
├── README.md                      # Complete system guide
├── run.sh                         # Single-command full pipeline execution script
├── config.json                    # Centralized settings (weights, dimensions, paths)
├── content-strategy.json          # 70/20/10 allocation logic and hook archetypes
├── performance-data.json          # Pin-level performance and conversion database
├── keyword-bank.json              # SEO keyword clusters and search intent
├── pin-history.json               # Master ledger of all generated pins (anti-duplicate)
├── winning-patterns.json          # Learned high-performing categories, hooks, templates
├── content-calendar.json          # Weekly publishing status schedule
│
├── dashboard/                     # Local visual intelligence UI
│   ├── index.html                 # Visual analytics & action checklist
│   ├── styles.css                 # Dark editorial dashboard design
│   └── data.js                    # Dynamic JSON sync bridge
│
├── input/
│   ├── manual-data/               # CSV template for Pinterest Analytics imports
│   └── imports/                   # Archived historical CSV exports
│
├── analysis/                      # Automatically generated intelligence reports
│   ├── category-analysis.md       # Category rankings and status
│   ├── hook-analysis.md           # Copy hook pattern breakdown
│   ├── visual-analysis.md         # Template performance breakdown
│   ├── funnel-analysis.md         # Landing page CRO & CTR tracking
│   └── weekly-report.md           # Consolidated weekly intelligence report
│
├── ready-to-post/                 # Finished, approved content queue
│   ├── images/                    # 1000 × 1500 px PNG graphics + contact sheet
│   ├── metadata/                  # Individual pin JSON metadata
│   └── csv/                       # Official upload manifest CSV
│
└── generated/
    ├── concepts/                  # Stage 1 conceptual blueprints
    ├── copy/                      # Evergreen headline & body copy
    ├── metadata/                  # SEO titles, descriptions, hashtags
    └── reports/                   # Timestamped weekly audit reports
```

---

## ⚡ How It Works

1. **Importing Performance Data:** Drop your weekly Pinterest Analytics CSV into `growth-engine/input/manual-data/pinterest-performance.csv`.
2. **Analysis & Learning:** The engine recalculates Outbound CTR, Save Rate, and Referral Click-throughs, scoring each Pin with sample size confidence thresholds.
3. **Dynamic Content Allocation:**
   - **70%** Proven winners (high CTR & referral intent)
   - **20%** Adjacent category/hook experiments
   - **10%** New format explorations
4. **Duplicate Protection & Compliance QA:** Checks against `pin-history.json` to prevent duplicate headlines or UTM IDs, and scans text for unsupported guarantees.
5. **Autonomous Graphic Generation:** Compiles and renders pixel-perfect **1000 × 1500 px PNGs** using the built-in WebKit rendering system.
6. **Human Approval Gate:** Output is placed in `ready-to-post/` for your review. No automated spam or policy violations.

---

## 💻 Running the Engine

To run the complete automated cycle in one step:

```bash
./growth-engine/run.sh
```

To view the live visual dashboard, open:
[`growth-engine/dashboard/index.html`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/dashboard/index.html) in your browser.
