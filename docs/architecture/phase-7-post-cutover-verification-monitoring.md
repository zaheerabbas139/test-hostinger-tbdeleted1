# Phase 7: Post-Cutover Verification & Monitoring Runbook

> **Navigation:** [Documentation Hub](../README.md) &rsaquo; [Architecture](../README.md#1-architecture) &rsaquo; **Phase 7 Verification & Monitoring**  
> **Target Platform:** Astro 5.x Static Site Generation (SSG)  
> **Monitoring Scope:** SEO Crawlers, Core Web Vitals, Edge Redirects, Form Delivery, Security  
> **Date:** October 31, 2026  
> **Status:** Operational Runbook (Ready for Execution)  

---

## 1. Executive Summary & Objective

Phase 7 establishes post-launch quality assurance, automated smoke testing, and continuous monitoring protocols to guarantee zero regressions across organic traffic, Core Web Vitals, and lead generation forms.

---

## 2. Step 1: Automated Live Smoke Testing

Execute this CLI verification script immediately following DNS and CDN cutover:

```bash
# 1. Verify Core Routes return HTTP 200 with gzip/brotli
for path in "" "who-we-are" "bridgead" "blog" "faq" "contact" "cyber-security" "digital-transformation" "cloud-infrastructure" "it-support-managed-services"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" https://uat.pranast.com/$path)
  echo "Route: /$path -> Status: $status"
done

# 2. Verify 301 Redirects resolve properly
curl -I https://uat.pranast.com/digital-transformation-where-to-start/
# Expected: Location: https://uat.pranast.com/blog/digital-transformation-where-to-start

curl -I https://uat.pranast.com/terms-of-services/
# Expected: Location: https://uat.pranast.com/terms-of-service

# 3. Verify WP Attack Surface returns 410 Gone
curl -I https://uat.pranast.com/wp-login.php
# Expected: HTTP/2 410

curl -I https://uat.pranast.com/xmlrpc.php
# Expected: HTTP/2 410

# 4. Verify Security Headers
curl -I https://uat.pranast.com/ | grep -E "x-content-type-options|x-frame-options|strict-transport-security"
```

---

## 3. Step 2: Search Console & Sitemap Submission

### 3.1. Google Search Console (GSC)
1. In GSC, select property `uat.pranast.com` (or `pranast.com`).
2. Navigate to **Indexing &rarr; Sitemaps**.
3. Submit the static sitemap endpoint:
   `https://uat.pranast.com/sitemap-index.xml` (or `/sitemap-0.xml`).
4. Perform **URL Inspection** on core routes (`/`, `/bridgead`, `/blog/digital-transformation-where-to-start`):
   - Click **Test Live URL**.
   - Confirm Googlebot successfully crawls and renders static HTML without JavaScript rendering delays.

### 3.2. Bing Webmaster Tools
1. Under **Sitemaps**, submit the live sitemap URL.
2. Run **SEO Site Scan** to verify zero broken links (404 errors) or missing canonical meta tags.

---

## 4. Step 3: Core Web Vitals & Lighthouse Profiling

Run automated Lighthouse audits across core pages. Target performance metrics:

| Metric | Target SLA | WordPress Baseline | Astro Target Result |
|---|---|---|---|
| **Lighthouse Performance Score** | `> 95 / 100` | 54 / 100 | **99-100 / 100** |
| **First Contentful Paint (FCP)** | `< 0.8s` | 2.4s | **< 0.4s** |
| **Largest Contentful Paint (LCP)** | `< 1.2s` | 4.8s | **< 0.8s** |
| **Cumulative Layout Shift (CLS)** | `0.00` | 0.28 | **0.00** |
| **Total Blocking Time (TBT)** | `< 50ms` | 890ms | **0ms (Zero-JS)** |

```bash
# Execute local Lighthouse CLI test (if installed)
npx lighthouse https://uat.pranast.com --preset=desktop --view
```

---

## 5. Step 4: Serverless Contact Form Smoke Test

Verify the decommissioned Ninja Form replacement (`src/components/ContactForm.astro`):
1. Navigate to `https://uat.pranast.com/contact`.
2. Fill out test submission:
   - Name: `Migration Verification Test`
   - Email: `dev@pranast.com`
   - Subject: `Cutover Verification`
   - Message: `Automated testing of serverless submission endpoint.`
3. Click **Send Message**.
4. Confirm successful redirect to thank-you state and delivery of inquiry email to team inbox.
5. Verify honeypot field rejects automated spam bot injections.

---

## 6. Step 5: Continuous 14-Day Monitoring Runbook

| Monitoring Vector | Frequency | Action / Threshold |
|---|---|---|
| **Cloudflare Analytics** | Daily (First 7 Days) | Monitor 301 volume, confirm 410 rate limits bot traffic, verify zero 5xx server errors. |
| **GSC Coverage Report** | Daily (First 14 Days) | Inspect "Page with redirect" vs "Not found (404)". Resolve any unmapped legacy 404s. |
| **Hostinger Server Logs** | Every 48 Hours | Check `/public_html/error_log` for any unexpected internal rewrite loop errors. |
| **Uptime Monitoring** | Real-time (1-minute ping) | Configure UptimeRobot or BetterStack monitoring for 99.99% edge availability. |

---

## 7. Sign-Off Protocol & Project Handover

At the conclusion of the 14-day observation window:
- [ ] 0 crawl errors reported in Google Search Console.
- [ ] 100% of legacy traffic successfully transferred to Astro routes via 301.
- [ ] WordPress MySQL database and PHP execution permanently purged.
- [ ] Sub-100ms global TTFB established across Cloudflare and Hostinger origin.
- [ ] Final sign-off from Chief Technology Officer & Principal Solutions Architect.
