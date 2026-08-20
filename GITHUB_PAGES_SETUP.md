# 🌐 GitHub Pages Deployment Guide ($0 Free Hosting)

This guide walks you through deploying your Whatnot referral landing site to GitHub Pages in under 2 minutes.

---

## 📌 Current Repository Status

- **Local Git Repository:** Initialized and committed on branch `main`.
- **Remote:** None configured yet (no remote credentials or secrets required from you).
- **Files Ready:** `index.html`, 7 category hubs, CSS/JS, 40 Pin graphics, and growth engine.

---

## 🚀 3 Simple Steps to Publish

### Step 1: Create a New Repository on GitHub
1. Go to [github.com/new](https://github.com/new).
2. Name your repository (e.g. `whatnot-finds` or `whatnot-referral-guide`).
3. Set visibility to **Public** (required for free GitHub Pages).
4. Do **not** initialize with a README (this repository already has everything).
5. Click **Create repository**.

### Step 2: Link & Push Your Local Repository
In your terminal, run the following two commands (replace `YOUR_USERNAME` and `YOUR_REPO_NAME`):

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 3: Enable GitHub Pages in Repository Settings
1. On your GitHub repository page, click **Settings** (top tab).
2. On the left sidebar, click **Pages**.
3. Under **Build and deployment &rarr; Source**, select **Deploy from a branch**.
4. Set branch to **`main`** and folder to **`/(root)`**.
5. Click **Save**.

---

## 🔗 Your Live URL Structure

Within 1–2 minutes, your website will be live at:
`https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

All sub-pages and Pinterest destination routes will map automatically:
- **Main Hub:** `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`
- **Pokémon Hub:** `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/pokemon/`
- **Sneakers Hub:** `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/sneakers/`
- **Fashion Hub:** `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/fashion/`
- **Collectibles Hub:** `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/collectibles/`
- **Beauty Hub:** `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/beauty/`
- **Vintage Hub:** `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/vintage/`
- **Deals Hub:** `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/deals/`

*(Optional)* If you name your repository `YOUR_USERNAME.github.io`, your site will be hosted directly at the root: `https://YOUR_USERNAME.github.io/`.
