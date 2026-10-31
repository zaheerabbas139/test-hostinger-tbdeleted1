# Tech Stack Analysis: uat.pranast.com

> **Navigation:** [Documentation Hub](../README.md) &rsaquo; [Architecture](../README.md#1-architecture) &rsaquo; **Current Tech Stack Analysis**  
> **Related Document:** [WordPress to Astro Migration Blueprint](wordpress-to-astro-migration-plan.md)

This document details the complete technology stack used to develop, power, and host **uat.pranast.com**, based on live HTTP/REST API inspection and Hostinger hosting configurations.

---

## 1. Overview & Architecture Summary

| Layer | Technology | Details |
|---|---|---|
| **CMS Platform** | WordPress | Core content management and REST API framework |
| **Hosting Provider** | Hostinger | Business Web Hosting plan (`u715171369`) |
| **Runtime & Language** | PHP 8.5.x | Server-side execution environment |
| **Web Server & Cache** | LiteSpeed Server + LiteSpeed Cache | In-memory page caching, delayed JS, QUIC.cloud |
| **CDN / Edge Network** | Hostinger CDN (`hcdn`) | Global caching and edge request routing |
| **Page Builder** | Elementor & Elementor AI | Drag-and-drop layout builder with AI generation |
| **Theme** | Prespa | Base layout, typography, and styling presets |
| **Form Management** | Ninja Forms | Interactive lead capture and submission system |
| **Privacy / Compliance** | Complianz | Cookie banner, legal consent, GDPR compliance |
| **Marketing & Analytics** | Google Site Kit / GTM | Google Tag Manager, Search Console, Analytics |

---

## 2. In-Depth Breakdown of Each Tool

### A. CMS & Core Platform
- **WordPress**
  - **What it is:** The world's most widely adopted open-source content management system (CMS).
  - **Role on this site:** Powers all posts, pages, media management, user roles, security, and provides the REST API (`/wp-json/`) used to serve structured content.

### B. Hosting, Server & Performance Infrastructure
- **Hostinger Web Hosting & hPanel**
  - **What it is:** Web hosting platform with a custom control panel (hPanel).
  - **Role on this site:** Hosts the source files and database. On the server, `uat.pranast.com` resides as a subdomain inside `/home/u715171369/domains/pranast.com/public_html/uat`.
- **Hostinger CDN (`hcdn`)**
  - **What it is:** Hostinger's edge Content Delivery Network.
  - **Role on this site:** Distributes static assets (images, CSS, JS) to edge nodes closer to visitors (e.g. `mum-edge8`), reducing latency and server load.
- **PHP 8.5 (Server Runtime)**
  - **What it is:** The backend scripting language that executes WordPress code and communicates with the MySQL/MariaDB database.
  - **Role on this site:** Compiles themes and plugins dynamically on each non-cached request.
- **LiteSpeed Cache (LSCache) & LiteSpeed Web Server**
  - **What it is:** An enterprise-grade, all-in-one site acceleration plugin and web server module.
  - **Role on this site:**
    - Caches full HTML pages (`x-litespeed-cache: hit`).
    - Performs script minification, image lazy loading, and delayed JavaScript execution (`litespeed_load_delayed_js`).
    - Uses guest mode optimization and QUIC.cloud UCSS for faster Core Web Vitals.

### C. Design, Theme & Page Building
- **Elementor Website Builder**
  - **What it is:** A visual drag-and-drop page builder for WordPress.
  - **Role on this site:** Used by designers and developers to construct custom responsive pages without writing raw HTML/CSS.
- **Elementor AI & Elementor MCP Composer**
  - **What it is:** Elementor's integrated generative AI and component composer features.
  - **Role on this site:** Assists in generating marketing copy, custom CSS snippets, and modular page layouts.
- **Elementor Header & Footer Builder (`hfe`)**
  - **What it is:** An extension for Elementor that allows creating bespoke headers, footers, and sticky navigation blocks across the site.
- **Prespa Theme**
  - **What it is:** A lightweight WordPress starter theme designed for modern page builders.
  - **Role on this site:** Provides base CSS variables, responsive typography scales, color palettes, and container structures.

### D. Forms & Customer Engagement
- **Ninja Forms (`ninja-forms`)**
  - **What it is:** A flexible form-building framework for WordPress.
  - **Role on this site:** Handles contact forms, inquiry submissions, and validation with dedicated submission and view endpoints.
- **NPS Survey (`nps-survey`)**
  - **What it is:** A Net Promoter Score feedback mechanism.
  - **Role on this site:** Collects user satisfaction ratings and feedback.

### E. Privacy, Legal & Analytics
- **Complianz GDPR/CCPA (`complianz`)**
  - **What it is:** A privacy suite that automates cookie policy generation and user consent management.
  - **Role on this site:** Manages cookie consent banners and blocks scripts until user permission is granted, maintaining compliance with global privacy regulations.
- **Site Kit by Google (`google-site-kit`)**
  - **What it is:** Google's official WordPress plugin.
  - **Role on this site:** Connects Google services directly to the site, including Google Tag Manager, Google Analytics 4, and Google Search Console.

