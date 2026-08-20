# 📌 Pinterest Quick-Start Guide (Step-by-Step)

This guide is designed for non-developers to publish their first Pinterest pins and start generating referral signups immediately.

---

## 🏁 Step 1: Create or Finish Your Pinterest Business Account
1. Go to [pinterest.com/business/create/](https://www.pinterest.com/business/create/) (it's 100% free).
2. Set your business name (e.g. *Curated Shopping Finds* or *Live Collector Discoveries*).
3. Set your website to your live URL (`https://yourusername.github.io/`).

---

## 🗂️ Step 2: Create Your 8 Pinterest Boards
In Pinterest, click **Saved** &rarr; **+ (Create Board)** and create these 8 themed boards:
1. `Pokémon Cards & TCG Live Breaks`
2. `Sneaker Grails & Streetwear Auctions`
3. `Vintage Fashion & Designer Thrifting`
4. `Art Toys & Collectibles Discovery`
5. `K-Beauty Swatches & Skincare Deals`
6. `Vintage Clothing & Retro Finds`
7. `Live Shopping Deals & $1 Auctions`
8. `Cool Things to Buy & Live Shopping`

---

## 📤 Step 3: Upload Your First Pins (Batch #01)
1. Open your images folder: [`pins/exports/`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/pins/exports/) (or unzip [`pins/whatnot-pinterest-30-pins.zip`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/pins/whatnot-pinterest-30-pins.zip)).
2. On Pinterest, click **Create &rarr; Create Pin**.
3. Drag & drop `pin-01-pokemon.png` into the upload box.

---

## ✍️ Step 4: Copy Titles, Descriptions & Destination Links
Open the manifest table at [`pins/exports/README.md`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/pins/exports/README.md):
- **Title:** `Pokémon Cards You Need to See Live`
- **Description:** `Discover where collectors watch vintage booster packs and rare cards opened live on stream. 360° video condition checks and interactive auctions. #pokemoncards #tcgbreak`
- **Link:** `https://yourusername.github.io/pokemon/?utm_source=pinterest&utm_medium=organic&utm_campaign=whatnot_referral&utm_content=pin01`
- **Board:** Select `Pokémon Cards & TCG Live Breaks`.
- Click **Publish** (or schedule for later).

---

## 📦 Step 5: Where to Find the Next Batch (Pins 31–40)
When you are ready for more pins, Batch #02 is waiting for you in:
- **Images:** [`growth-engine/ready-to-post/images/`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/ready-to-post/images/)
- **Copy & Links CSV:** [`growth-engine/ready-to-post/csv/pinterest-upload-manifest.csv`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/ready-to-post/csv/pinterest-upload-manifest.csv)

---

## 📊 Step 6: How to Export Pinterest Analytics
After your pins have been live for 5–7 days:
1. In Pinterest, go to **Analytics &rarr; Overview**.
2. Select date range: **Last 7 days** or **Last 14 days**.
3. Click **Export** (top right) to download your performance CSV.

---

## 📥 Step 7: Where to Put the Analytics CSV
1. Save your exported numbers into:
   [`growth-engine/input/manual-data/pinterest-performance.csv`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/input/manual-data/pinterest-performance-template.csv)
*(The importer accepts Pin ID, Impressions, Saves, and Outbound Clicks).*

---

## ⚡ Step 8: How to Run the Growth Engine
Open your terminal and run:
```bash
./growth-engine/run.sh
```
*The engine will automatically analyze your data, identify winning categories and hooks, create new concepts, and render graphics for your next batch.*

---

## 🖥️ Step 9: How to Review Your Dashboard
Open [`growth-engine/dashboard/index.html`](file:///Users/jake/.gemini/antigravity-ide/scratch/whatnot-pinterest-landing/growth-engine/dashboard/index.html) in any web browser to see:
- Real-time CTR and referral clicks
- Your top-performing category, hook, and visual template
- The review queue for upcoming pins

---

## ✅ Step 10: How to Approve the Next Pins
Review the generated images in `growth-engine/ready-to-post/images/contact_sheet.jpg`. Once you approve them, upload them to Pinterest using the generated manifest CSV!
