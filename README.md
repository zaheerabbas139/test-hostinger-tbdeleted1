# Pranast Platform: Astro 7 SSG & Infrastructure Hub

This repository serves as the central codebase and technical knowledge hub for the **Pranast Digital Platform**:

1. **Modernized Astro 7 Static Platform:** High-performance, zero-JS by default static site built with **Astro 7.4+** and **Tailwind CSS v4**, replacing the legacy WordPress/Elementor runtime with type-safe Content Collections and sub-second page generation.
2. **Architecture & Infrastructure Knowledge Base:** Centralized technical repository housing system audits, target modernization blueprints, and operational hosting cutover runbooks in [`docs/`](docs/).
3. **Automated FTPS & Edge Deployment:** Automated GitHub Actions workflows for continuous integration (`astro check`, schema validation, static build) and continuous deployment to Hostinger web roots via secure FTPS.

---

## ⚡ Tech Stack Architecture

| Layer | Technology | Specification / Role |
| :--- | :--- | :--- |
| **Framework** | **Astro 7.4.x** | Static Site Generation (`output: 'static'`), zero-JS default, islands architecture |
| **Styling** | **Tailwind CSS 4.3.x** | Native Vite integration via `@tailwindcss/vite`, CSS-first tokens in `src/styles/global.css` |
| **Content Engine** | **Astro Content Layer API** | Typed markdown collections defined in `src/content.config.ts` using `glob` loader and Zod |
| **Language & Tooling**| **TypeScript 5.9.x** / `@astrojs/check` | Strict frontmatter type safety, AST checking, compile-time validation |
| **Deployment Target** | **Hostinger Web Hosting** | Automated FTPS deployment to `public_html` |
| **Edge CDN & DNS** | **Cloudflare** | Edge redirects (Bulk CSV / Workers), SSL/TLS Full (Strict), WAF security |

---

## 🔄 Recent Upgrades: Astro 7 & Tailwind CSS v4

The codebase was recently modernized to **Astro 7** and **Tailwind CSS v4**:

* **Vite-Native Tailwind Integration:** Dropped `@astrojs/tailwind` (which reached end-of-life for Astro 7) and `tailwind.config.mjs`. Integrated `@tailwindcss/vite` directly inside `astro.config.mjs`.
* **CSS-First Theme Tokens:** Brand colors (`brand-50` through `brand-900`) and theme settings are now configured directly in `src/styles/global.css` via `@theme` and `@import "tailwindcss";`. Layouts consume them via `@reference`.
* **Content Layer API Migration:** Migrated content configuration from legacy `src/content/config.ts` to modern root `src/content.config.ts` utilizing `glob` loaders (`astro/loaders`) with deterministic slug-based identifiers (`generateSlugId`).
* **Modern Content Rendering API:** Dynamic page templates (`[...slug].astro`, `blog/[slug].astro`, `case-studies/[slug].astro`) use `render(entry)` from `astro:content` and query entries by `entry.id`.

---

## 📚 Technical Documentation Hub

All system architecture specifications and operational migration guides are structured under [`docs/`](docs/):

- **[Documentation Portal & Index (`docs/README.md`)](docs/README.md)** — Master overview, lifecycle roadmap, and document matrix.
- **Architecture Blueprints (`docs/architecture/`):**
  - [As-Is Tech Stack Analysis (`docs/architecture/uat-pranast-tech-stack.md`)](docs/architecture/uat-pranast-tech-stack.md) — Comprehensive audit of WordPress, PHP 8.5, LiteSpeed, and Elementor.
  - [Target-State Astro Blueprint (`docs/architecture/wordpress-to-astro-migration-plan.md`)](docs/architecture/wordpress-to-astro-migration-plan.md) — Architectural roadmap for static site modernization with Astro & Markdown.
  - [Phase Reports (`docs/architecture/`)](docs/README.md#🗺️-documentation-matrix) — Detailed Phase 1–7 execution reports (content schema, scaffolding, UI components, SEO 301 redirects, decommissioning, edge cutover, and post-cutover verification).
- **Infrastructure Runbooks (`docs/infrastructure/`):**
  - [Cross-Account Hostinger Migration (`docs/infrastructure/hostinger-website-migration.md`)](docs/infrastructure/hostinger-website-migration.md) — Cutover runbook between Hostinger client accounts.
  - [Business to Unlimited Plan Move (`docs/infrastructure/business-to-unlimited-migration-plan.md`)](docs/infrastructure/business-to-unlimited-migration-plan.md) — Step-by-step tier migration strategy.
  - [GitHub Actions CI/CD Specification (`docs/infrastructure/github-actions-ci-cd.md`)](docs/infrastructure/github-actions-ci-cd.md) — Production pipeline for automated validation, static building, and FTPS deployment.

---

## 🚀 CI/CD & Automated Deployment

The repository uses enterprise-grade GitHub Actions workflows:

- **Continuous Integration (`.github/workflows/ci.yml`):**
  - Triggers on Pull Requests and Pushes to `main`.
  - Enforces type safety and Zod Content Schema validation via `npm run check` (`astro check`).
  - Audits dependencies with `npm audit`.
  - Validates static compilation (`npm run build`) and uploads build artifacts.
- **Continuous Deployment (`.github/workflows/deploy-hostinger.yml`):**
  - Deploys pre-compiled static assets (`dist/`) directly to Hostinger web roots via secure FTPS.
  - Controlled by GitHub repository secrets (`HOSTINGER_FTP_SERVER`, `HOSTINGER_FTP_USERNAME`, `HOSTINGER_FTP_PASSWORD`).

---

## 💻 Local Development & Build Commands

For a full step-by-step walkthrough, prerequisites, and troubleshooting, see the [**Local Development Guide (`docs/local-development.md`)](docs/local-development.md)**.

```bash
# Install dependencies
npm ci

# Start local Astro 7 development server (http://localhost:4321)
npm run dev

# Validate TypeScript & Astro Content Layer Schemas (src/content.config.ts)
npm run check

# Build production static site (outputs to dist/ and mirrors to root for web serving)
npm run build

# Preview production build locally
npm run preview

# (Optional) Re-extract WordPress XML into Markdown collections
npm run extract
```

---

## 🌐 Legacy PHP Connectivity Probe

If testing legacy Hostinger PHP connectivity probe behaviors locally:
```bash
php -S localhost:8000
```
Then navigate to [http://localhost:8000](http://localhost:8000).
