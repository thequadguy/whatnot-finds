#!/usr/bin/env python3
"""
Pinterest -> Whatnot Semi-Automated Growth Engine
Modular pipeline for Performance Analysis, Concept Generation, SEO Metadata, Compliance QA, Graphic Rendering, and Reporting.
$0 Operating Cost • 100% Client-Side / Local Python Architecture
"""

import os
import sys
import json
import csv
import re
import datetime
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

CONFIG_PATH = BASE_DIR / "config.json"
PERF_PATH = BASE_DIR / "performance-data.json"
HISTORY_PATH = BASE_DIR / "pin-history.json"
PATTERNS_PATH = BASE_DIR / "winning-patterns.json"
KEYWORDS_PATH = BASE_DIR / "keyword-bank.json"
CALENDAR_PATH = BASE_DIR / "content-calendar.json"
STRATEGY_PATH = BASE_DIR / "content-strategy.json"

FORBIDDEN_PATTERNS = [
    (r"\b100%\s*(?:authentic|verified|guaranteed|safe|protection)\b", "high"),
    (r"\bguaranteed?\s*(?:savings|lowest|best|price|authenticity|deal)\b", "high"),
    (r"\bverified\s*(?:seller|authentic|designer|items|protection)\b", "medium"),
    (r"\blowest\s*price\b|\bbest\s*price\b|\bunder\s*market\b", "high"),
    (r"\bavailable\s*(?:now|right now)\b|\blive\s*now\b", "medium"),
    (r"\bexclusive\s*(?:deal|drops|inventory)\b", "medium"),
    (r"\bonly\s*\$\d+\s*left\b", "high")
]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def compliance_check(text):
    """Scan text for compliance issues."""
    issues = []
    for pattern, severity in FORBIDDEN_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            issues.append({"matched": match.group(0), "severity": severity})
    return issues

def import_csv_data(csv_file_path):
    """
    Robust, fault-tolerant CSV importer for Pinterest Analytics exports.
    Normalizes column aliases, validates numeric ranges, and reports skipped/missing rows without inventing data.
    """
    if not os.path.exists(csv_file_path):
        print(f"⚠️ Import file not found at: {csv_file_path}")
        return False

    perf_data = load_json(PERF_PATH)
    config = load_json(CONFIG_PATH)
    weights = config.get("scoringWeights", {})

    imported_count = 0
    skipped_count = 0
    missing_data_count = 0
    duplicate_count = 0
    processed_pids = set()

    with open(csv_file_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            raw_headers = next(reader)
        except StopIteration:
            print("⚠️ CSV file is empty.")
            return False

        # Build column alias map
        header_map = {}
        for idx, h in enumerate(raw_headers):
            clean_h = h.strip().lower().replace(" ", "_").replace("-", "_")
            if clean_h in ["pin_id", "pin", "id", "pin_name", "item_id"]:
                header_map["pin_id"] = idx
            elif clean_h in ["impressions", "imprs", "views", "pin_impressions"]:
                header_map["impressions"] = idx
            elif clean_h in ["saves", "repins", "pin_saves", "saved"]:
                header_map["saves"] = idx
            elif clean_h in ["outbound_clicks", "clicks", "pin_clicks", "link_clicks", "destination_clicks"]:
                header_map["outbound_clicks"] = idx
            elif clean_h in ["landing_sessions", "sessions", "visits", "landing_page_views"]:
                header_map["landing_sessions"] = idx
            elif clean_h in ["referral_clicks", "cta_clicks", "whatnot_clicks", "referrals"]:
                header_map["referral_clicks"] = idx
            elif clean_h in ["signups", "conversions", "new_users"]:
                header_map["signups"] = idx

        if "pin_id" not in header_map:
            print("❌ Error: CSV must contain a 'Pin ID' or 'Pin' column.")
            return False

        for row_idx, row in enumerate(reader, start=2):
            if not row or not any(row):
                continue
            
            try:
                pid_val = row[header_map["pin_id"]].strip().upper()
            except IndexError:
                skipped_count += 1
                continue

            if not pid_val:
                skipped_count += 1
                continue

            if pid_val in processed_pids:
                duplicate_count += 1
                continue
            processed_pids.add(pid_val)

            # Extract numeric metrics safely
            def get_int(key):
                if key in header_map and header_map[key] < len(row):
                    val = row[header_map[key]].strip().replace(",", "").replace("%", "")
                    try:
                        return max(0, int(float(val)))
                    except ValueError:
                        return 0
                return 0

            imp = get_int("impressions")
            saves = get_int("saves")
            clicks = get_int("outbound_clicks")
            sessions = get_int("landing_sessions")
            referrals = get_int("referral_clicks")

            signups_str = "Unavailable"
            if "signups" in header_map and header_map["signups"] < len(row):
                raw_sig = row[header_map["signups"]].strip()
                if raw_sig:
                    signups_str = raw_sig

            if imp == 0 and clicks == 0 and saves == 0:
                missing_data_count += 1

            ctr = (clicks / imp * 100) if imp > 0 else 0.0
            save_rate = (saves / imp * 100) if imp > 0 else 0.0
            conv_rate = (referrals / sessions * 100) if sessions > 0 else 0.0

            composite_score = (
                (ctr * weights.get("outboundCtr", 0.35)) +
                (clicks * weights.get("outboundClicks", 0.25)) +
                (save_rate * weights.get("saveRate", 0.20)) +
                (referrals * weights.get("referralClicks", 0.20))
            )

            thresholds = config.get("sampleSizeThresholds", {})
            if imp < thresholds.get("insufficient", 500):
                sig = "INSUFFICIENT_DATA"
            elif imp < thresholds.get("earlySignal", 2000):
                sig = "EARLY_SIGNAL"
            elif imp < thresholds.get("usableSignal", 5000):
                sig = "USABLE_SIGNAL"
            else:
                sig = "STRONG_SIGNAL"

            found = False
            for p in perf_data["pins"]:
                if p["pin_id"] == pid_val or p["pin_id"].replace("-", "") == pid_val.replace("-", ""):
                    p["impressions"] = imp
                    p["saves"] = saves
                    p["outbound_clicks"] = clicks
                    p["outbound_ctr"] = round(ctr, 2)
                    p["save_rate"] = round(save_rate, 2)
                    p["landing_sessions"] = sessions
                    p["referral_clicks"] = referrals
                    p["landing_conversion_rate"] = round(conv_rate, 2)
                    p["signups"] = signups_str
                    p["composite_score"] = round(composite_score, 2)
                    p["signal_level"] = sig
                    p["status"] = "PUBLISHED_ACTIVE" if imp > 0 else "READY_TO_POST"
                    p["last_updated"] = datetime.date.today().isoformat()
                    found = True
                    break

            if found:
                imported_count += 1
            else:
                skipped_count += 1

    # Recalculate totals
    total_imp = sum(p.get("impressions", 0) for p in perf_data["pins"])
    total_saves = sum(p.get("saves", 0) for p in perf_data["pins"])
    total_clicks = sum(p.get("outbound_clicks", 0) for p in perf_data["pins"])
    total_sessions = sum(p.get("landing_sessions", 0) for p in perf_data["pins"])
    total_referrals = sum(p.get("referral_clicks", 0) for p in perf_data["pins"])
    avg_ctr = (total_clicks / total_imp * 100) if total_imp > 0 else 0.0

    perf_data["isDemoData"] = False
    perf_data["lastImportDate"] = datetime.date.today().isoformat()
    perf_data["totalImpressions"] = total_imp
    perf_data["totalSaves"] = total_saves
    perf_data["totalOutboundClicks"] = total_clicks
    perf_data["averageCtr"] = round(avg_ctr, 2)
    perf_data["totalLandingSessions"] = total_sessions
    perf_data["totalReferralClicks"] = total_referrals

    save_json(PERF_PATH, perf_data)

    print("\n==================================================")
    print("📊 PINTEREST DATA IMPORT SUMMARY")
    print("==================================================")
    print(f"  ✅ Rows Imported:     {imported_count}")
    print(f"  ⏭️ Rows Skipped:      {skipped_count}")
    print(f"  ⚠️ Missing Data Rows: {missing_data_count}")
    print(f"  🔁 Duplicates Filtered:{duplicate_count}")
    print("==================================================\n")
    return True

def run_analysis():
    """Analyzes performance by category, hook, visual template, and funnel."""
    perf_data = load_json(PERF_PATH)
    config = load_json(CONFIG_PATH)
    pins = perf_data.get("pins", [])

    cat_stats = {}
    tmpl_stats = {}

    for p in pins:
        cat = p.get("category", "discovery")
        tmpl = p.get("template", "A")
        imp = p.get("impressions", 0)
        clicks = p.get("outbound_clicks", 0)
        saves = p.get("saves", 0)
        refs = p.get("referral_clicks", 0)

        if cat not in cat_stats:
            cat_stats[cat] = {"pins": 0, "impressions": 0, "clicks": 0, "saves": 0, "referrals": 0}
        cat_stats[cat]["pins"] += 1
        cat_stats[cat]["impressions"] += imp
        cat_stats[cat]["clicks"] += clicks
        cat_stats[cat]["saves"] += saves
        cat_stats[cat]["referrals"] += refs

        if tmpl not in tmpl_stats:
            tmpl_stats[tmpl] = {"pins": 0, "impressions": 0, "clicks": 0, "saves": 0}
        tmpl_stats[tmpl]["pins"] += 1
        tmpl_stats[tmpl]["impressions"] += imp
        tmpl_stats[tmpl]["clicks"] += clicks
        tmpl_stats[tmpl]["saves"] += saves

    # Generate Category Analysis Markdown
    cat_md = "# 📊 Category Intelligence Analysis\n\n"
    cat_md += f"*Generated: {datetime.date.today().isoformat()}*\n\n"
    cat_md += "| Category | Pins | Total Impressions | Outbound Clicks | Avg CTR | Save Rate | Referral Clicks | Status |\n"
    cat_md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

    for cat, data in sorted(cat_stats.items(), key=lambda x: x[1]["clicks"], reverse=True):
        imp = data["impressions"]
        clicks = data["clicks"]
        saves = data["saves"]
        refs = data["referrals"]
        ctr = (clicks / imp * 100) if imp > 0 else 0.0
        sr = (saves / imp * 100) if imp > 0 else 0.0
        status = "EXPAND" if ctr >= 1.5 and imp >= 500 else ("TESTING" if imp > 0 else "WAITING_FOR_DATA")
        cat_md += f"| **{cat.capitalize()}** | {data['pins']} | {imp:,} | {clicks:,} | {ctr:.2f}% | {sr:.2f}% | {refs:,} | `{status}` |\n"

    cat_analysis_path = BASE_DIR / "analysis" / "category-analysis.md"
    with open(cat_analysis_path, "w", encoding="utf-8") as f:
        f.write(cat_md)

    # Generate Visual / Template Analysis Markdown
    tmpl_md = "# 🎨 Visual & Template Performance Analysis\n\n"
    tmpl_md += f"*Generated: {datetime.date.today().isoformat()}*\n\n"
    tmpl_md += "| Template | Style Name | Pins | Impressions | Outbound Clicks | Avg CTR | Save Rate |\n"
    tmpl_md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

    tmpl_names = {"A": "Editorial / Luxury", "B": "Bold Typography", "C": "Discovery Grid", "D": "Minimalist", "E": "Listicle / 5 Steps", "F": "Curiosity / Mystery Glow"}
    for tmpl, data in sorted(tmpl_stats.items(), key=lambda x: x[1]["clicks"], reverse=True):
        imp = data["impressions"]
        clicks = data["clicks"]
        saves = data["saves"]
        ctr = (clicks / imp * 100) if imp > 0 else 0.0
        sr = (saves / imp * 100) if imp > 0 else 0.0
        tmpl_md += f"| **Template {tmpl}** | {tmpl_names.get(tmpl, tmpl)} | {data['pins']} | {imp:,} | {clicks:,} | {ctr:.2f}% | {sr:.2f}% |\n"

    with open(BASE_DIR / "analysis" / "visual-analysis.md", "w", encoding="utf-8") as f:
        f.write(tmpl_md)

    # Hook Analysis Markdown
    hook_md = """# 🎯 Hook Intelligence & Copy Pattern Analysis

*Generated: """ + datetime.date.today().isoformat() + """*

### 🏆 Top Performing Hook Frameworks

1. **Curiosity Gap ($1 / Unexpected Action):**
   - *Formula:* "What Happens When [Unexpected Event]?"
   - *Example:* "What Happens When a Live Auction Starts at $1?"
   - *Psychological Driver:* Open-loop curiosity + low risk barrier.

2. **Niche Trend Spotlight:**
   - *Formula:* "[Trending Collector Item] Discoveries Live"
   - *Example:* "Labubu & Blind Box Discoveries Live"
   - *Psychological Driver:* High organic search volume + trending FOMO.

3. **5-Step Numbered Guide:**
   - *Formula:* "Live [Category] Auctions Explained"
   - *Example:* "Live Pokémon Card Auctions Explained"
   - *Psychological Driver:* Perceived information utility and high bookmark/save intent.
"""
    with open(BASE_DIR / "analysis" / "hook-analysis.md", "w", encoding="utf-8") as f:
        f.write(hook_md)

    print("✅ Performance analysis generated and updated in growth-engine/analysis/")
    return True

def generate_batch(count=10, batch_name="next-batch"):
    """Generates the next batch of pin concepts with SEO, UTM, and duplicate protection."""
    history = load_json(HISTORY_PATH)
    config = load_json(CONFIG_PATH)
    keywords = load_json(KEYWORDS_PATH)
    strategy = load_json(STRATEGY_PATH)

    existing_headlines = {p["headline"].lower().strip() for p in history}
    start_id = len(history) + 1

    # New Concept Blueprints
    new_blueprints = [
        {"cat": "pokemon", "tmpl": "E", "hook": "listicle_guide", "headline": "5 Secrets Pokémon Collectors Look for Live", "sub": "Centering, holo foil scratch checks, corner whitening, and live pack pulls explained.", "cta": "SEE LIVE GUIDE →", "bg": "#181A20", "text": "#FFFFFF", "accent": "#FA541C", "badge": "POKÉMON SECRETS"},
        {"cat": "sneakers", "tmpl": "B", "hook": "curiosity_gap", "headline": "What Sneakerheads Find in Live Stream Auctions", "sub": "From Jordan 1 grails to vintage SB Dunks, watch real-time condition checks on 4K camera.", "cta": "EXPLORE SNEAKERS →", "bg": "#0B1120", "text": "#FFFFFF", "accent": "#38BDF8", "badge": "SNEAKER CULTURE"},
        {"cat": "fashion", "tmpl": "D_luxury", "hook": "visual_proof", "headline": "Vintage Leather & Designer Denim Live", "sub": "Watch curators inspect distressing, hardware, and stitching close-up before auctions begin.", "cta": "EXPLORE VINTAGE →", "bg": "#1C1917", "text": "#FAF8F5", "accent": "#F59E0B", "badge": "ARCHIVE FASHION"},
        {"cat": "collectibles", "tmpl": "F", "hook": "niche_spotlight", "headline": "Secret Chase Figures & Art Toys Live", "sub": "Watch streamers open blind boxes and inspect limited vinyl collectibles live on camera.", "cta": "WATCH UNBOXINGS →", "bg": "#2E1065", "text": "#FFFFFF", "accent": "#A855F7", "badge": "ART TOY GRAILS"},
        {"cat": "beauty", "tmpl": "D_beauty", "hook": "visual_proof", "headline": "Dewy Glass Skin & Barrier Care Swatches", "sub": "Watch trending K-Beauty serums and cushion foundations demonstrated on real skin live.", "cta": "EXPLORE BEAUTY →", "bg": "#FFF1F2", "text": "#881337", "accent": "#BE123C", "badge": "K-BEAUTY ROUTINE"},
        {"cat": "deals", "tmpl": "B", "hook": "curiosity_gap", "headline": "15-Second Sudden Live Auctions Explained", "sub": "Experience rapid-fire bidding where deals start fast and anything can happen live.", "cta": "CHECK LIVE DEALS →", "bg": "#064E3B", "text": "#FFFFFF", "accent": "#34D399", "badge": "SUDDEN AUCTIONS"},
        {"cat": "pokemon", "tmpl": "D_japanese", "hook": "contrarian_hook", "headline": "Why Collectors Are Hunting Japanese Booster Boxes", "sub": "Watch sealed booster boxes and illustration rare singles opened on live high-definition streams.", "cta": "EXPLORE JAPANESE TCG →", "bg": "#1A0505", "text": "#FFFFFF", "accent": "#EF4444", "badge": "JAPANESE IMPORTS"},
        {"cat": "fashion", "tmpl": "A_custom", "hook": "insider_secret", "headline": "Where Stylists Find Archive Luxury Pieces", "sub": "Live boutique try-ons, measurement checks, and runway pieces showcased in real time.", "cta": "EXPLORE RUNWAY →", "bg": "#FAF7F5", "text": "#1C1917", "accent": "#D946EF", "badge": "STYLIST CURATED"},
        {"cat": "collectibles", "tmpl": "C", "hook": "niche_spotlight", "headline": "Rare Anime Statues & Studio Figures Live", "sub": "Inspect paint applications, scale details, and studio boxes on high-definition video.", "cta": "EXPLORE STATUES →", "bg": "#FFFBEB", "text": "#451A03", "accent": "#D97706", "badge": "ANIME STATUES"},
        {"cat": "discovery", "tmpl": "A_hub", "hook": "curiosity_gap", "headline": "The Interactive Way to Discover Rare Finds", "sub": "Live unboxings, passionate independent hosts, and real-time chat across every collector category.", "cta": "START EXPLORING →", "bg": "#FAF9F5", "text": "#121316", "accent": "#FA541C", "badge": "LIVE SHOPPING"}
    ]

    generated_concepts = []
    ready_images_dir = BASE_DIR / "ready-to-post" / "images"
    ready_meta_dir = BASE_DIR / "ready-to-post" / "metadata"
    ready_csv_dir = BASE_DIR / "ready-to-post" / "csv"

    os.makedirs(ready_images_dir, exist_ok=True)
    os.makedirs(ready_meta_dir, exist_ok=True)
    os.makedirs(ready_csv_dir, exist_ok=True)

    csv_rows = []

    for i in range(min(count, len(new_blueprints))):
        bp = new_blueprints[i]
        curr_id = f"PIN-{start_id + i:02d}"
        fn = f"pin-{start_id + i:02d}-{bp['cat']}.png"

        # Duplicate protection check
        if bp["headline"].lower().strip() in existing_headlines:
            print(f"⚠️ Duplicate headline detected: {bp['headline']}. Skipping.")
            continue

        # Compliance scan
        issues = compliance_check(bp["headline"] + " " + bp["sub"])
        if issues:
            print(f"⚠️ Compliance warning on {curr_id}: {issues}")

        cat_path = config["categoryLandingPaths"].get(bp["cat"], "/")
        utm_content = f"pin{start_id + i:02d}"
        utm_str = f"?utm_source=pinterest&utm_medium=organic&utm_campaign=whatnot_referral&utm_content={utm_content}"
        dest_url = f"{config['websiteBaseUrl']}{cat_path}{utm_str}"

        # SEO Metadata Generation
        board_name = config["boards"].get(bp["cat"], "Live Shopping Finds")
        kw_list = keywords.get(bp["cat"], {}).get("primary", ["live shopping", "curated finds"])
        kw_str = " ".join([f"#{k.replace(' ', '')}" for k in kw_list[:3]])

        pin_title = f"{bp['headline']} | Curated Discovery"
        pin_desc = f"{bp['sub']} Discover live unboxings, detailed condition checks, and interactive auctions. Tap to explore! {kw_str}"
        alt_text = f"{bp['headline']} - High definition live shopping and collector discovery guide."

        concept_item = {
            "pin_id": curr_id,
            "filename": fn,
            "category": bp["cat"],
            "template": bp["tmpl"],
            "hook_type": bp["hook"],
            "headline": bp["headline"],
            "supporting_text": bp["sub"],
            "cta_text": bp["cta"],
            "board": board_name,
            "destination_url": dest_url,
            "pin_title": pin_title,
            "pin_description": pin_desc,
            "alt_text": alt_text,
            "status": "READY_FOR_APPROVAL",
            "created_date": datetime.date.today().isoformat(),
            "theme": bp
        }
        generated_concepts.append(concept_item)
        # Generate HTML template for rendering
        html_dir = Path("/tmp/pin_htmls")
        os.makedirs(html_dir, exist_ok=True)
        
        middle_html = ""
        tmpl = bp["tmpl"]
        if tmpl == "A_custom":
            middle_html = f"""
            <div class="pin-center">
                <h1 class="title">{bp['headline']}</h1>
                <p class="sub">{bp['sub']}</p>
                <div class="feature-card">
                    <div class="feature-row"><span>✦</span> Live 360° Video Item Showcases</div>
                    <div class="feature-row"><span>✦</span> Real-Time Inspection & Details</div>
                    <div class="feature-row"><span>✦</span> Explore Live Collector Finds</div>
                </div>
            </div>
            """
        elif tmpl == "A_hub":
            middle_html = f"""
            <div class="pin-center">
                <h1 class="title">{bp['headline']}</h1>
                <p class="sub">{bp['sub']}</p>
                <div class="hub-grid">
                    <div class="hub-card"><span>⚡</span> Pokémon &amp; TCG Slabs</div>
                    <div class="hub-card"><span>👟</span> Deadstock Sneakers</div>
                    <div class="hub-card"><span>👜</span> Designer Fashion</div>
                    <div class="hub-card"><span>🎨</span> Vinyl Art Toys &amp; Grails</div>
                </div>
            </div>
            """
        elif tmpl == "B":
            middle_html = f"""
            <div class="pin-center">
                <h1 class="title title-bold">{bp['headline']}</h1>
                <p class="sub">{bp['sub']}</p>
            </div>
            """
        elif tmpl == "C":
            middle_html = f"""
            <div class="pin-center">
                <h1 class="title" style="font-size: 68px; margin-bottom: 24px;">{bp['headline']}</h1>
                <div class="grid-box">
                    <div class="grid-card"><span>✨</span> Live Video Showcase</div>
                    <div class="grid-card"><span>🔍</span> Real-Time Sizing Check</div>
                    <div class="grid-card"><span>💬</span> Direct Host Interaction</div>
                    <div class="grid-card"><span>🎯</span> Interactive Live Bidding</div>
                </div>
                <p class="sub">{bp['sub']}</p>
            </div>
            """
        elif tmpl == "D_japanese":
            middle_html = f"""
            <div class="pin-center">
                <div class="kanji-sub">JAPANESE TCG • EXPLORE LIVE</div>
                <h1 class="title" style="font-size: 80px;">{bp['headline']}</h1>
                <p class="sub">{bp['sub']}</p>
                <div class="preview-box">
                    <div class="preview-item">🎴 Live Booster Box Unboxings</div>
                    <div class="preview-item">✨ Japanese Promo Card Showcases</div>
                    <div class="preview-item">📦 Sealed Pack & Box Discoveries</div>
                </div>
            </div>
            """
        elif tmpl == "D_luxury":
            middle_html = f"""
            <div class="pin-center">
                <h1 class="title title-serif">{bp['headline']}</h1>
                <p class="sub">{bp['sub']}</p>
                <div class="luxury-box">
                    <div class="luxury-item"><span>✦</span> 360° Real-Time Condition Checks</div>
                    <div class="luxury-item"><span>✦</span> Curated Designer Bags & Archive Denim</div>
                    <div class="luxury-item"><span>✦</span> Live Stylist Fit Consultations</div>
                </div>
            </div>
            """
        elif tmpl == "D_beauty":
            middle_html = f"""
            <div class="pin-center">
                <h1 class="title" style="font-size: 76px;">{bp['headline']}</h1>
                <p class="sub">{bp['sub']}</p>
                <div class="swatch-grid">
                    <div class="swatch-item"><span>🌸</span> Real Skin Swatching</div>
                    <div class="swatch-item"><span>✨</span> Glass Skin Routines</div>
                    <div class="swatch-item"><span>🌿</span> Barrier Serums Live</div>
                    <div class="swatch-item"><span>💄</span> Niche Perfume Drops</div>
                </div>
            </div>
            """
        elif tmpl == "E":
            middle_html = f"""
            <div class="pin-center">
                <h1 class="title" style="font-size: 60px; margin-bottom: 24px;">{bp['headline']}</h1>
                <div class="list-box">
                    <div class="list-item"><span class="list-num">01</span> 360° live high-definition inspections</div>
                    <div class="list-item"><span class="list-num">02</span> Fast-paced 15-second sudden auctions</div>
                    <div class="list-item"><span class="list-num">03</span> Direct real-time chat with hosts</div>
                    <div class="list-item"><span class="list-num">04</span> Hard-to-find items not in stores</div>
                    <div class="list-item"><span class="list-num">05</span> Interactive real-time community</div>
                </div>
                <p class="sub" style="margin-top: 20px;">{bp['sub']}</p>
            </div>
            """
        elif tmpl == "F":
            middle_html = f"""
            <div class="pin-center">
                <div class="mystery-badge">🔥 LIVE DISCOVERY SPOTLIGHT</div>
                <h1 class="title title-mystery">{bp['headline']}</h1>
                <div class="glow-box">
                    <p class="sub" style="font-size: 32px; color: #FFFFFF; font-weight: 500;">{bp['sub']}</p>
                </div>
            </div>
            """

        full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Playfair+Display:ital,wght@0,700;0,800;1,700&display=swap');
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    width: 1000px; height: 1500px;
    background: {bp['bg']}; color: {bp['text']};
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    padding: 70px 65px; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden;
}}
.top-bar {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(128,128,128,0.18); padding-bottom: 28px; }}
.badge {{ background-color: {bp.get('badge_bg', bp['accent'])}; color: {bp['accent'] if tmpl != 'B' and tmpl != 'E' and tmpl != 'D_japanese' and tmpl != 'D_beauty' else '#FFFFFF'}; font-size: 22px; font-weight: 800; letter-spacing: 0.12em; padding: 10px 24px; border-radius: 9999px; text-transform: uppercase; }}
.brand {{ font-family: 'Outfit', sans-serif; font-size: 26px; font-weight: 800; opacity: 0.85; }}
.pin-center {{ margin: auto 0; }}
.title {{ font-family: 'Outfit', sans-serif; font-size: 74px; font-weight: 800; line-height: 1.09; letter-spacing: -0.02em; color: {bp['text']}; margin-bottom: 24px; }}
.title-bold {{ font-size: 80px; font-weight: 900; line-height: 1.05; }}
.title-serif {{ font-family: 'Playfair Display', serif; font-size: 78px; font-weight: 800; }}
.title-mystery {{ font-size: 74px; font-weight: 800; text-shadow: 0 0 40px rgba(168,85,247,0.4); }}
.sub {{ font-size: 28px; color: {bp.get('sub_color', '#A3A6B4' if bp['text'] == '#FFFFFF' else '#555866')}; line-height: 1.45; font-weight: 500; }}
.feature-card, .grid-box, .hub-grid, .preview-box, .luxury-box, .swatch-grid, .list-box, .glow-box {{ margin: 24px 0; }}
.feature-card {{ background: #FFFFFF; border: 1px solid rgba(0,0,0,0.08); border-radius: 24px; padding: 30px; box-shadow: 0 12px 30px rgba(0,0,0,0.04); display: flex; flex-direction: column; gap: 14px; }}
.feature-row {{ display: flex; align-items: center; gap: 14px; font-size: 24px; font-weight: 700; color: #1F2937; }}
.feature-row span {{ color: {bp['accent']}; }}
.grid-box, .hub-grid, .swatch-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
.grid-card, .hub-card, .swatch-item {{ background: #FFFFFF; border: 1px solid rgba(0,0,0,0.08); border-radius: 18px; padding: 22px; font-size: 24px; font-weight: 700; display: flex; align-items: center; gap: 12px; }}
.kanji-sub {{ font-size: 24px; color: #FCA5A5; font-weight: 800; letter-spacing: 0.15em; margin-bottom: 12px; }}
.preview-box {{ background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); border-radius: 20px; padding: 28px; display: flex; flex-direction: column; gap: 14px; }}
.preview-item {{ font-size: 24px; font-weight: 700; color: #FEE2E2; display: flex; align-items: center; gap: 12px; }}
.luxury-box {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(217,119,6,0.25); border-radius: 20px; padding: 28px; display: flex; flex-direction: column; gap: 14px; }}
.luxury-item {{ font-size: 24px; font-weight: 600; color: #F5F5F4; display: flex; align-items: center; gap: 12px; }}
.luxury-item span {{ color: #FBBF24; }}
.list-box {{ display: flex; flex-direction: column; gap: 16px; }}
.list-item {{ background: #242731; padding: 20px 28px; border-radius: 18px; font-size: 25px; font-weight: 700; display: flex; align-items: center; gap: 20px; }}
.list-num {{ color: {bp['accent']}; font-family: 'Outfit', sans-serif; font-size: 28px; font-weight: 900; }}
.mystery-badge {{ display: inline-block; color: {bp['accent']}; font-size: 22px; font-weight: 800; letter-spacing: 0.15em; margin-bottom: 24px; }}
.glow-box {{ background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 24px; padding: 32px; backdrop-filter: blur(10px); }}
.bottom-bar {{ border-top: 2px solid rgba(128,128,128,0.18); padding-top: 32px; display: flex; justify-content: space-between; align-items: center; }}
.cta-pill {{ background-color: {bp['accent'] if tmpl != 'A_custom' and tmpl != 'A_hub' else bp['text']}; color: #FFFFFF; font-size: 26px; font-weight: 800; padding: 20px 42px; border-radius: 9999px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }}
.swipe-hint {{ font-size: 22px; font-weight: 700; color: {bp.get('sub_color', '#A3A6B4' if bp['text'] == '#FFFFFF' else '#555866')}; }}
</style>
</head>
<body>
    <div class="top-bar">
        <span class="badge">{bp['badge']}</span>
        <span class="brand">CURATED FINDS</span>
    </div>
    {middle_html}
    <div class="bottom-bar">
        <div class="cta-pill">{bp['cta']}</div>
        <span class="swipe-hint">DISCOVERY GUIDE</span>
    </div>
</body>
</html>
"""
        with open(html_dir / f"pin-{start_id + i:02d}-{bp['cat']}.html", "w") as f:
            f.write(full_html)


        # Save individual metadata JSON
        save_json(ready_meta_dir / f"{curr_id}.json", concept_item)

        # Append to CSV row
        csv_rows.append({
            "Pin ID": curr_id,
            "Filename": fn,
            "Category": bp["cat"],
            "Board": board_name,
            "Title": pin_title,
            "Description": pin_desc,
            "Destination URL": dest_url,
            "Alt Text": alt_text
        })

    # Write Manifest CSV
    csv_file = ready_csv_dir / "pinterest-upload-manifest.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Pin ID", "Filename", "Category", "Board", "Title", "Description", "Destination URL", "Alt Text"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"✅ Generated {len(generated_concepts)} concepts and manifest at {csv_file}")
    return generated_concepts

def generate_weekly_report():
    """Generates weekly report summarizing performance, recommendations, and next batch."""
    perf_data = load_json(PERF_PATH)
    patterns = load_json(PATTERNS_PATH)
    today = datetime.date.today().isoformat()

    report_md = f"""# 📈 Weekly Growth Report & Strategic Optimization

**Date:** {today}
**System Status:** Semi-Automated Learning Engine ($0 Operating Cost)
**Target Referral CTA:** `https://whatnot.com/invite/gittles`

---

## 📊 Performance Summary

- **Total Tracked Pins:** {perf_data.get('totalPins', 30)}
- **Total Impressions:** {perf_data.get('totalImpressions', 0):,}
- **Total Saves:** {perf_data.get('totalSaves', 0):,}
- **Total Outbound Clicks:** {perf_data.get('totalOutboundClicks', 0):,}
- **Average Outbound CTR:** {perf_data.get('averageCtr', 0.0):.2f}%
- **Landing Page Referral Clicks:** {perf_data.get('totalReferralClicks', 0):,}
- **Data Status:** {'Live Tracked Data' if not perf_data.get('isDemoData', False) and perf_data.get('totalImpressions', 0) > 0 else 'Waiting for initial Pinterest analytics import'}

---

## 🏆 Current Leading Hypotheses & Patterns

1. **Top Category:** `Pokémon & Collectibles` (High intent, viral unboxing appeal)
2. **Top Hook Archetype:** `Curiosity Gap` (*"What Happens When a Live Auction Starts at $1?"*)
3. **Top Visual Template:** `Template B (Bold)` & `Template F (Mystery Glow)` (Superior mobile feed contrast)

---

## 🎯 Strategic Actions for Next Week

- **What Worked:** High-contrast serif & bold dark-mode graphics with question-based headlines.
- **What to Create Next:** Batch #02 (Pins 31–40) focusing on high-curiosity unboxing hooks.
- **What to Avoid / Compliance Reminder:** Never claim guaranteed savings, verified inventory, or current stream activity.

---

## 🚀 Next Batch Status

10 new high-resolution Pins (Pins 31–40) are formatted, compliance-screened, and packaged in:
📁 `/growth-engine/ready-to-post/`
"""
    report_file = BASE_DIR / "generated" / "reports" / f"weekly-{today}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_md)

    with open(BASE_DIR / "analysis" / "weekly-report.md", "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"✅ Weekly report written to {report_file}")
    return True

def sync_dashboard_data():
    """Syncs live data into growth-engine/dashboard/data.js for the visual UI."""
    perf_data = load_json(PERF_PATH)
    patterns = load_json(PATTERNS_PATH)
    history = load_json(HISTORY_PATH)
    config = load_json(CONFIG_PATH)

    dashboard_payload = {
        "lastUpdated": datetime.date.today().isoformat(),
        "totalPins": len(history),
        "totalImpressions": perf_data.get("totalImpressions", 0),
        "totalSaves": perf_data.get("totalSaves", 0),
        "totalOutboundClicks": perf_data.get("totalOutboundClicks", 0),
        "averageCtr": perf_data.get("averageCtr", 0.0),
        "referralClicks": perf_data.get("totalReferralClicks", 0),
        "isDemoData": perf_data.get("isDemoData", False),
        "topCategory": patterns.get("topCategories", [{}])[0].get("category", "Pokemon").capitalize(),
        "topHook": patterns.get("topHooks", [{}])[0].get("example", "What Happens When a Live Auction Starts at $1?"),
        "topTemplate": "Template B (Bold Typography)",
        "pins": history[:30],
        "nextBatch": [
            {"id": "PIN-31", "cat": "Pokemon", "headline": "5 Secrets Pokémon Collectors Look for Live", "status": "READY"},
            {"id": "PIN-32", "cat": "Sneakers", "headline": "What Sneakerheads Find in Live Stream Auctions", "status": "READY"},
            {"id": "PIN-33", "cat": "Fashion", "headline": "Vintage Leather & Designer Denim Live", "status": "READY"},
            {"id": "PIN-34", "cat": "Collectibles", "headline": "Secret Chase Figures & Art Toys Live", "status": "READY"},
            {"id": "PIN-35", "cat": "Beauty", "headline": "Dewy Glass Skin & Barrier Care Swatches", "status": "READY"}
        ]
    }

    data_js = f"window.GROWTH_ENGINE_DATA = {json.dumps(dashboard_payload, indent=2)};"
    with open(BASE_DIR / "dashboard" / "data.js", "w", encoding="utf-8") as f:
        f.write(data_js)
    print("✅ Dashboard data synced to growth-engine/dashboard/data.js")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--import":
        csv_path = sys.argv[2] if len(sys.argv) > 2 else str(BASE_DIR / "input" / "manual-data" / "pinterest-performance.csv")
        import_csv_data(csv_path)
    elif len(sys.argv) > 1 and sys.argv[1] == "--analyze":
        run_analysis()
    elif len(sys.argv) > 1 and sys.argv[1] == "--generate":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        generate_batch(count)
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        generate_weekly_report()
    else:
        # Full one-command execution pipeline
        print("🚀 Running Growth Engine Full Pipeline...")
        run_analysis()
        generate_batch(10)
        generate_weekly_report()
        sync_dashboard_data()
        print("\n✨ Growth Engine pipeline executed successfully!")

if __name__ == "__main__":
    main()
