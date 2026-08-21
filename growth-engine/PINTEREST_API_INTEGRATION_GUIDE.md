# 🔌 Pinterest API v5 Integration Architecture & Setup Guide

This guide outlines the official, fully compliant integration pathway for connecting the Growth Engine directly to the **Pinterest API v5** for programmatic pin publishing and automated analytics retrieval.

---

## 🛡️ Anti-Scraping & Account Protection Policy

- **No Scraping:** We strictly prohibit web scrapers, headless browser automation on pinterest.com, or bypassing CAPTCHAs.
- **No Stored Credentials:** Never store Pinterest passwords or session cookies.
- **Official API Only:** All programmatic actions must use Pinterest's official REST API v5 with developer token authorization.
- **Human Review Preserved:** Automatic posting must still respect the `HUMAN APPROVAL` gate before scheduling pins.

---

## 🔑 1. Obtaining Official Pinterest API v5 Access

1. Log into the [Pinterest Developers Portal](https://developers.pinterest.com/).
2. Click **Create App** and name it `Whatnot Growth Engine`.
3. Request standard access permissions:
   - `boards:read` / `boards:write`
   - `pins:read` / `pins:write`
   - `user_accounts:read`
   - `ads:read` (for organic & campaign analytics)
4. Generate your **OAuth 2.0 Client ID**, **Client Secret**, and **Access Token**.

---

## 🔒 2. Configuring Environment Variables

Store your credentials in your local shell environment (or `.env` file excluded by `.gitignore`):

```bash
export PINTEREST_APP_ID="your_pinterest_app_id"
export PINTEREST_APP_SECRET="your_pinterest_app_secret"
export PINTEREST_ACCESS_TOKEN="pina_your_access_token_here"
```

*The growth engine will read these directly via `os.environ.get("PINTEREST_ACCESS_TOKEN")`.*

---

## 🌐 3. Supported Endpoints & Workflows

### A. Pin Publishing (`POST /v5/pins`)
```json
{
  "link": "https://thequadguy.github.io/whatnot-finds/pokemon/?utm_source=pinterest&utm_medium=organic&utm_campaign=whatnot_referral&utm_content=pin01",
  "title": "Pokémon Cards You Need to See Live",
  "description": "Discover where collectors watch vintage booster packs opened live on stream.",
  "board_id": "YOUR_BOARD_ID",
  "media_source": {
    "source_type": "image_base64",
    "content_type": "image/png",
    "data": "<BASE64_ENCODED_IMAGE>"
  }
}
```

### B. Analytics Retrieval (`GET /v5/user_account/analytics`)
Fetches daily impressions, pin clicks, outbound clicks, and saves directly into `performance-data.json`.

---

## 🔄 4. Hybrid Operation (CSV Fallback)

If API access is pending or unconfigured, the Growth Engine operates in **Hybrid CSV Mode**:
- Drop your weekly CSV export into `growth-engine/input/manual-data/pinterest-performance.csv`.
- Run `./growth-engine/run.sh` to update analytics and rankings.
