# Local Development & Execution Guide

This guide provides instructions and technical details for running, developing, and testing the **Pranast Platform** website locally.

---

## 📋 System Prerequisites

Ensure your local development environment meets the following baseline requirements:

| Dependency | Minimum Version | Recommended Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Node.js** | `>= 18.17.1` or `>= 20.3.0` | `20.x LTS` or `22.x LTS` | Astro runtime & build engine |
| **npm** | `>= 9.x` | Latest bundled with Node | Package dependency management |
| **PHP** *(Optional)* | `>= 8.0` | `8.2+` | Testing legacy connectivity probe (`index.php`) |
| **Python 3** *(Optional)* | `>= 3.9` | `3.10+` | Content extraction script (`extract-wp-xml.py`) |

---

## 🚀 Quick Start

### 1. Clone & Install Dependencies

From the repository root directory:

```bash
# Clean install of all project dependencies
npm install
# or for an exact lockfile-matched install:
npm ci
```

---

### 2. Start the Local Development Server

Run the local Astro development server with active Hot Module Replacement (HMR):

```bash
npm run dev
```

- **Local URL:** [http://localhost:4321](http://localhost:4321)
- **Network URL (optional):** To expose the dev server over your local network for mobile/tablet testing:
  ```bash
  npx astro dev --host
  ```

Changes made to files in [`src/pages/`](../src/pages), [`src/components/`](../src/components), or [`src/content/`](../src/content) will automatically recompile and refresh in your browser.

---

### 3. Build & Preview the Production Static Output

To verify the production build behavior locally before deploying or opening a Pull Request:

```bash
# 1. Compile static production bundle
npm run build

# 2. Start local static preview server
npm run preview
```

- **Preview URL:** [http://localhost:4321](http://localhost:4321)
- The build outputs optimized static HTML, CSS, and JS to the [`dist/`](../dist/) directory and root deployment targets.

---

## 🛠️ Developer Scripts Reference

All primary build and validation commands are defined in [`package.json`](../package.json):

```bash
# Start Astro development server (hot reload enabled)
npm run dev

# Alias for npm run dev
npm start

# Run Astro compiler checks & TypeScript schema validation
npm run check

# Compile production-ready static site
npm run build

# Preview the compiled production build
npm run preview

# Direct CLI wrapper for Astro tools
npm run astro -- [options]

# Re-extract WordPress XML content into Markdown collections
npm run extract
```

---

## 🔍 Validation & Type-Checking

Before committing changes, execute the Astro validator to confirm strict typing across all components and Zod content collections:

```bash
npm run check
```

This verifies:
- Frontmatter schemas against [`src/content.config.ts`](../src/content.config.ts) (Astro Content Layer API)
- TypeScript typings in `.astro` and `.ts` files
- Component prop constraints

---

## 🌐 Running the Legacy PHP Connectivity Probe

If you need to verify legacy Hostinger PHP connectivity probe behaviors locally:

```bash
php -S localhost:8000
```

Access the PHP test page at [http://localhost:8000](http://localhost:8000).

---

## ❓ Troubleshooting & Common Issues

### Port 4321 Already in Use
If port 4321 is occupied by another process:
```bash
npx astro dev --port 3000
```

### Stale Build Cache
If you encounter unexpected layout glitches or stale content:
```bash
# Clean Astro build cache and dist folder
rm -rf .astro dist
npm run dev
```

### Node.js Version Incompatibility
If you see errors regarding unsupported Node versions or syntax, verify your active Node version:
```bash
node -v
```
Use [nvm](https://github.com/nvm-sh/nvm) to switch to an LTS release if needed:
```bash
nvm use 20
```

