# Pranast Platform & Hostinger Deployment

This repository serves dual purposes:
1. **Connectivity Probe & Deploy Target:** A lightweight PHP verification site used to test and validate automated GitHub → Hostinger Git deployments.
2. **Architecture & Infrastructure Knowledge Base:** The centralized technical repository housing system audits, target modernization blueprints, and operational hosting cutover runbooks in [`docs/`](docs/).

---

## 📚 Technical Documentation Hub

All system architecture specifications and operational migration guides are structured under [`docs/`](docs/):

- **[Documentation Portal & Index (`docs/README.md`)](docs/README.md)** — Master overview, lifecycle roadmap, and document matrix.
- **Architecture Blueprints (`docs/architecture/`):**
  - [As-Is Tech Stack Analysis (`docs/architecture/uat-pranast-tech-stack.md`)](docs/architecture/uat-pranast-tech-stack.md) — Comprehensive audit of WordPress, PHP 8.5, LiteSpeed, and Elementor.
  - [Target-State Astro Blueprint (`docs/architecture/wordpress-to-astro-migration-plan.md`)](docs/architecture/wordpress-to-astro-migration-plan.md) — Architectural roadmap for static site modernization with Astro & Markdown.
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

```bash
# Install dependencies
npm ci

# Start local Astro development server
npm run dev

# Validate TypeScript & Astro Content Schemas
npm run check

# Build production static site
npm run build

# Preview production build locally
npm run preview
```

---

## 🚀 Deployment & Local Testing

### Deploying to Hostinger
1. In hPanel, navigate to **Websites → Git** and connect this repository.
2. Set the deployment branch to `main` and target destination to `public_html`.
3. Pushes to `main` automatically deploy `index.php` to serve the connectivity probe.

### Local Preview
To test the local PHP probe:
```bash
php -S localhost:8000
```
Then navigate to [http://localhost:8000](http://localhost:8000).
