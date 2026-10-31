# CLAUDE.md — Pranast Website

> Agent persona & architectural guidelines: see `GEMINI.md` (single source of truth — do NOT duplicate here).

## Commands

```sh
npm run dev          # Astro dev server (localhost:4321)
npm run build        # astro build + copies dist/* to root (Hostinger deploy prep)
npm run check        # astro check (TS + content schema validation)
npm run preview      # preview SSG output locally
npm run extract      # python3 scripts/extract-wp-xml.py (WP XML → MD migration)
```

## Architecture

```
pranast-website/
├── src/
│   ├── content/           # Astro Content Collections (Markdown source of truth)
│   │   ├── blog/          # 6 blog posts; schema: title,date,category,featured_image
│   │   ├── case-studies/  # 2 case studies; schema: client,industry,summary
│   │   └── pages/         # 12 static pages (home,services,legal,etc.)
│   ├── pages/             # Astro route files
│   │   ├── index.astro    # Home (manual, rich layout)
│   │   ├── [...slug].astro# Dynamic catch-all for pages collection
│   │   ├── blog/          # Blog index + [slug].astro
│   │   ├── case-studies/  # Case studies index + [slug].astro
│   │   ├── bridgead.astro # BridgeAD product page (interactive tabs)
│   │   └── faq.astro      # FAQ with accordion
│   ├── components/        # Astro components (Header, Footer, ContactForm,
│   │                      #   FaqAccordion, BridgeADTabs, BridgeADLifecycle,
│   │                      #   WorkloadReadinessMatrix)
│   ├── layouts/
│   │   └── BaseLayout.astro  # Root HTML shell, Tailwind, global SEO meta
│   ├── styles/global.css  # Tailwind v4 base + custom utilities
│   └── content.config.ts  # Zod schemas for all 3 collections
├── public/                # Static assets copied verbatim to dist/
├── scripts/               # One-off Python/JS migration utilities
├── docs/                  # Architecture & infra docs (read these, not duplicated here)
├── astro.config.mjs       # output:'static', site:'https://pranast.com', Tailwind v4 via Vite, @astrojs/sitemap
├── tsconfig.json          # extends astro/strict; path alias @/* → src/*
└── .github/workflows/     # CI (ci.yml) + FTP deploy to Hostinger (deploy-hostinger.yml)
```

**Build output:** `dist/` (SSG). `npm run build` also copies output to repo root for Hostinger flat-file serving.

## Stack

- **Astro 7** — SSG, Islands architecture, zero-JS by default
- **Tailwind CSS v4** — via `@tailwindcss/vite` plugin (no tailwind.config.js)
- **TypeScript** — strict mode; `@astrojs/check` for type validation
- **Deployment** — GitHub Actions → FTPS → Hostinger `public_html/`
- **No framework adapters** — pure `.astro` components only

## Content Collections Schema (quick ref)

| Collection    | Key fields                                         |
|---------------|----------------------------------------------------|
| `pages`       | title, description?, slug?, nav_order?             |
| `blog`        | title, date, category (enum), featured_image, draft|
| `case-studies`| title, client, industry, summary, challenge?       |

Collection IDs default to filename (sans `.md`); override with frontmatter `slug`.

## Coding Standards

- **TypeScript strict**: no implicit `any`; use `z.infer<>` for collection types
- **Astro components**: props typed via `interface Props`; destructure with `Astro.props`
- **CSS**: Tailwind utility-first; custom classes in `global.css` with `@layer`
- **No client-side JS** unless necessary; use `client:load` / `client:idle` sparingly
- **Images**: reference from `public/assets/images/`; use Astro `<Image>` for optimization
- **Error handling**: fail fast with explicit error messages; no silent catches
- **Content edits**: modify `.md` files in `src/content/`; never edit generated `dist/`

## Claude Operational Rules

- **Never glob/read entire directories** — use `rg`, `grep`, or targeted `find` with `-name`
- **Read only relevant line ranges** — pass `StartLine`/`EndLine` when inspecting large files
- **Surgical edits only** — use the `edit_file` tool with minimal Target/Replacement; never rewrite whole files unless the file is <30 lines
- **Schema changes** → always run `npm run check` to validate
- **Build changes** → always run `npm run build` and confirm `dist/index.html` exists
- **Path alias**: use `@/` for imports from `src/` (configured in tsconfig)
- **No lockfile edits** — never manually edit `package-lock.json`

