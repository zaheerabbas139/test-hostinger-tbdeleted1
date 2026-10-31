# Phase 6: Edge CDN & Production Cutover Runbook

> **Navigation:** [Documentation Hub](../README.md) &rsaquo; [Architecture](../README.md#1-architecture) &rsaquo; **Phase 6 Edge CDN & Cutover**  
> **Edge Network:** Cloudflare Global Anycast Edge (DNS, WAF, Edge Workers, Bulk Redirects)  
> **Origin Host:** Hostinger LiteSpeed Web Server (`public_html`)  
> **Automation:** GitHub Actions FTPS Pipeline (`.github/workflows/deploy-hostinger.yml`)  
> **Target Domains:** `uat.pranast.com` / `pranast.com`  
> **Date:** October 31, 2026  
> **Status:** Operational Runbook (Ready for Execution)  

---

## 1. Executive Summary & Objective

Phase 6 governs the live production cutover: synchronizing pre-compiled static Astro assets to the Hostinger origin, deploying edge redirection and security rules across Cloudflare's global Anycast network, and configuring DNS routing for zero-downtime traffic transfer.

---

## 2. Step 1: Cloudflare Edge Network Deployment

### 2.1. Cloudflare SSL/TLS Configuration
1. In Cloudflare Dashboard, select domain `pranast.com`.
2. Navigate to **SSL/TLS &rarr; Overview**.
3. Set encryption mode to **Full (Strict)**.
4. Under **Edge Certificates**:
   - Ensure **Always Use HTTPS** is enabled.
   - Set **Minimum TLS Version** to `TLS 1.2` (or `TLS 1.3`).
   - Enable **Opportunistic Encryption** and **Automatic HTTPS Rewrites**.

### 2.2. Edge Redirection Deployment
Deploy redirects via one of the two verified architectural options:

#### Option A: Cloudflare Bulk Redirects (Dashboard Import)
1. In Cloudflare Dashboard, go to **Manage Account &rarr; Configurations &rarr; Bulk Redirects**.
2. Click **Create List** &rarr; Name: `pranast_legacy_301_mapping`.
3. Upload [`cloudflare/bulk-redirects.csv`](../../cloudflare/bulk-redirects.csv).
4. Go to **Rules &rarr; Redirect Rules &rarr; Bulk Redirects**.
5. Create Rule referencing `pranast_legacy_301_mapping`, enabling `Preserve Query String: True`.

#### Option B: Cloudflare Edge Worker (Programmatic Deployment)
Using the pre-built Worker in [`cloudflare/edge-redirects.js`](../../cloudflare/edge-redirects.js):
```bash
# Authenticate Cloudflare Wrangler
npx wrangler login

# Deploy Edge Worker directly to production routes
cd cloudflare
npx wrangler deploy
```

---

## 3. Step 2: Hostinger Static Web Root Deployment via CI/CD

Static assets are compiled locally or via GitHub Actions and synchronized via secure FTPS:

### 3.1. Configure GitHub Actions Secrets
In GitHub repository settings (**Settings &rarr; Secrets and variables &rarr; Actions**):
* `HOSTINGER_FTP_SERVER` &rarr; e.g. `ftp.pranast.com`
* `HOSTINGER_FTP_USERNAME` &rarr; e.g. `u715171369@pranast.com`
* `HOSTINGER_FTP_PASSWORD` &rarr; `<Hostinger-FTP-Password>`

### 3.2. Automated Pipeline Trigger
Every push to `main` executes `.github/workflows/deploy-hostinger.yml`:
1. `npm ci` installs clean dependencies.
2. `npm run check` validates TypeScript and Astro Zod Content Collections.
3. `npm run build` compiles 21 static routes to `dist/`.
4. Copies [`public/.htaccess`](../../public/.htaccess) to `dist/.htaccess`.
5. Deploys `dist/` directly to Hostinger's web root via FTPS.

---

## 4. Step 3: DNS Routing & Cloudflare Proxy Activation

1. In Cloudflare Dashboard, navigate to **DNS &rarr; Records**.
2. Ensure records are proxied through Cloudflare (**Proxy status: Proxied / Orange Cloud**):
   | Type | Name | Target / IP Value | Proxy Status | TTL |
   |---|---|---|---|---|
   | `A` | `pranast.com` | Hostinger Server IP (`145.223.x.x`) | Proxied (Orange) | Auto |
   | `CNAME` | `www` | `pranast.com` | Proxied (Orange) | Auto |
   | `A` | `uat` | Hostinger Server IP (`145.223.x.x`) | Proxied (Orange) | Auto |
3. Under **Speed &rarr; Optimization**:
   - Enable **Brotli Compression**.
   - Enable **Early Hints (103)**.
   - Enable **Auto Minify** for HTML, CSS, and JS.

---

## 5. Step 4: Edge Cache Invalidation & Pre-Warming

Immediately following cutover, purge all stale WordPress cache objects from Cloudflare:
1. In Cloudflare Dashboard, navigate to **Caching &rarr; Configuration**.
2. Click **Purge Everything**.
3. Warm the edge cache for high-priority pages:
   ```bash
   curl -s -o /dev/null https://uat.pranast.com/
   curl -s -o /dev/null https://uat.pranast.com/bridgead
   curl -s -o /dev/null https://uat.pranast.com/blog
   curl -s -o /dev/null https://uat.pranast.com/faq
   curl -s -o /dev/null https://uat.pranast.com/who-we-are
   ```
