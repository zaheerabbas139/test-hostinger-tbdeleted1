# Multi-Tier Edge & Origin Architecture Diagram

> **Navigation:** [Documentation Hub](../../README.md) &rsaquo; [Architecture](../../README.md#1-architecture) &rsaquo; [Phase 4: SEO 301 Redirect Mapping](../phase-4-seo-301-redirect-mapping.md) &rsaquo; **Multi-Tier Edge & Origin Architecture**  
> **Source Platform:** WordPress 6.x / LiteSpeed  
> **Target Platform:** Astro 5.x SSG  
> **CDN / Edge Network:** Cloudflare Global Anycast Edge (300+ PoPs)  
> **Origin Web Server:** Hostinger LiteSpeed / Apache (`public_html`)  
> **Date:** October 31, 2026  

---

## 1. Architectural Diagram

```mermaid
flowchart TD
    Client["Client Request\n(Browser / Googlebot / Malicious Scanner)"] --> DNS["Cloudflare Anycast DNS & Edge Network\n(300+ PoPs Globally)"]
    
    subgraph Tier1["Tier 1: Cloudflare Global Edge Layer (<10ms TTFB)"]
        DNS --> CF_WAF{"Security Filter &\nWAF Rules"}
        CF_WAF -- "Scanner Traps\n(/wp-admin, /xmlrpc.php, /wp-login)" --> R410["HTTP 410 Gone\n(Fast Abort + noindex Header)"]
        
        CF_WAF -- "Valid Traffic" --> CF_Redirect{"Edge Routing Engine\n(Worker & Bulk Rules)"}
        CF_Redirect -- "Legacy WP Posts/Pages\n(/digital-transformation... -> /blog/...)" --> R301["HTTP 301 Permanent Redirect\n(Preserve Query Strings)"]
        CF_Redirect -- "Media Uploads\n(/wp-content/uploads/... -> /assets/...)" --> R301_Media["HTTP 301 Permanent Redirect\n(Direct Asset Mapping)"]
        CF_Redirect -- "Legacy WP Query IDs\n(?p=117 -> /blog/...)" --> R301_Query["HTTP 301 Permanent Redirect\n(Strip Legacy WP Params)"]
    end

    CF_Redirect -- "Clean Astro Route\n(/who-we-are, /bridgead, /blog/...)" --> Origin{"Origin Web Server\n(Hostinger LiteSpeed / Apache)"}

    subgraph Tier2["Tier 2: Hostinger Origin Server Fallback Layer"]
        Origin --> H_Rewrite{"Origin .htaccess Engine\n(mod_rewrite & mod_headers)"}
        H_Rewrite -- "Bypassed Legacy / Malicious URL" --> H_Sec["Origin 301 Redirect / 410 Gone\n(Defense-in-Depth Fallback)"]
        H_Rewrite -- "Static HTML / Assets" --> Astro_Static["Astro Static Site Files\n(Pre-compiled dist/index.html)"]
        Astro_Static --> H_Cache["Caching & Security Headers\n(1-Year Assets, 0s HTML, HSTS)"]
    end

    H_Cache --> Client
    R301 --> Client
    R301_Media --> Client
    R301_Query --> Client
    R410 --> Client
```

---

## 2. Layer Responsibilities & Performance Metrics

| Layer | Responsibility | Target Latency / TTFB | Component Implementation |
|---|---|---|---|
| **Tier 1: Cloudflare Edge** | Absorbs all legacy WordPress queries, bot scans, and 301 redirects closest to the user. | `< 15ms` | [`cloudflare/edge-redirects.js`](../../cloudflare/edge-redirects.js)<br>[`cloudflare/bulk-redirects.csv`](../../cloudflare/bulk-redirects.csv) |
| **Tier 2: Hostinger Origin** | Fallback routing authority; serves pre-compiled Astro static files and applies security headers. | `< 60ms` | [`public/.htaccess`](../../public/.htaccess)<br>[`dist/.htaccess`](../../dist/.htaccess) |

---

## 3. Defense-in-Depth Rationale
1. **Zero Origin Compute on Legacy Traffic:** Over 95% of legacy inbound links and crawler traffic terminate at the Cloudflare edge, avoiding Hostinger CPU/PHP overhead entirely.
2. **100% Fail-Safe Redundancy:** If Cloudflare is paused, bypassed, or operating in development mode, the origin `.htaccess` enforces identical 301/410 routing rules without human intervention.
3. **Link Equity Preservation:** 301 Moved Permanently response headers transfer 95-99% of PageRank directly to new Astro routes in Google Search Console and Bing Webmaster Tools.

