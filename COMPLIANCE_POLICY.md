# 🛡️ Whatnot Finds — Compliance Policy & Advertising Standards

**Effective Date:** 2026-08-21  
**Account Positioning:** Independent Fan & Discovery Guide ("Whatnot Finds")  
**Primary Referral URL:** `https://whatnot.com/invite/gittles`

---

## 1. Core Principles

1. **Independent Positioning:**
   - This account, website, and promotional pins are independent community discovery guides.
   - We are NOT Whatnot Inc., and we do not represent official Whatnot corporate customer service, official management, or direct corporate endorsement.
   - Standard disclosure: *"Independent fan content — not affiliated with Whatnot."*

2. **Zero False Claims (Strictly Prohibited):**
   - ❌ **NO Guarantees of Authenticity:** Never claim "100% authentic guaranteed" or "guaranteed real." Use *"Inspect condition and items live on high-definition video."*
   - ❌ **NO Price or Savings Guarantees:** Never claim "lowest price anywhere" or "guaranteed under market." Use *"Rapid-fire auctions starting at $1."*
   - ❌ **NO Fake Scarcity or Urgency:** Never use fake countdown timers or fake live viewer numbers on static pages.
   - ❌ **NO Vetting Misrepresentations:** Never claim all sellers are personally vetted by us. Use *"Card streamers and curators showcase pieces live."*
   - ❌ **NO Fake Buyer Protection:** Never promise absolute refund guarantees. Refer to *"Whatnot platform buyer policies for qualifying orders."*

3. **Truthful, Evergreen Marketing:**
   - Focus on unique live shopping mechanics: 360° video inspections, real-time chat with hosts, sudden-death auctions, and collector unboxings.
   - All product references and category examples must reflect genuine platform categories.

---

## 2. Automated Compliance Rules (Engine Check)

The Growth Engine runs automated regex scans on all pin copy and HTML before staging. Flagged patterns:
- `\b100%\b`
- `\bguarantee(d)?\b`
- `\bverified seller(s)?\b`
- `\bzero damage\b`
- `\bofficial whatnot\b`
- `\bauthentic(ity)? guaranteed\b`

Any pin triggering these rules is immediately blocked in `QA_CHECK` until remediated.
