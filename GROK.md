# GROK.md — Pranast Website

> Full agent persona & architectural guidelines: `GEMINI.md` (single source of truth).
> Full architecture map, schema refs, and coding standards: `CLAUDE.md`.

## Commands

```sh
npm run dev      # Astro dev server → http://localhost:4321
npm run build    # SSG build → dist/ + copies to repo root (Hostinger prep)
npm run check    # TypeScript + Astro content schema validation
npm run preview  # Serve built output locally
npm run extract  # python3 scripts/extract-wp-xml.py (WP migration utility)
```

## Stack

- **Astro 7** — `output: 'static'`, Islands architecture, zero-JS by default
- **Tailwind CSS v4** — via `@tailwindcss/vite` plugin; no `tailwind.config.js`
- **TypeScript strict** — `@astrojs/check`; path alias `@/*` → `src/*`
- **Deployment** — GitHub Actions → FTPS → Hostinger `public_html/`

## Directory Map

```
src/content/           ← Markdown source (blog/, case-studies/, pages/)
src/content.config.ts  ← Zod schemas for all 3 collections
src/pages/             ← Astro routes ([...slug].astro, blog/, case-studies/)
src/components/        ← Astro components (Header, Footer, ContactForm, etc.)
src/layouts/           ← BaseLayout.astro (global HTML shell + SEO meta)
src/styles/global.css  ← Tailwind v4 @layer customizations
public/                ← Static assets copied verbatim to dist/
scripts/               ← One-off migration utilities (Python/JS)
docs/                  ← Architecture & infra documentation
dist/                  ← BUILD OUTPUT — never edit manually
astro.config.mjs       ← site, output, vite config
tsconfig.json          ← extends astro/strict; @/* path alias
```

## Content Collections (schema summary)

| Collection    | Required fields                          |
|---------------|------------------------------------------|
| `pages`       | title                                    |
| `blog`        | title, date, category (enum), featured_image |
| `case-studies`| title, client, industry, summary         |

Slug defaults to filename; override via frontmatter `slug` field.

## Coding Standards

- TypeScript strict — no implicit `any`; use `z.infer<>` for collection types
- Astro component props typed via `interface Props`; destructure from `Astro.props`
- CSS: Tailwind utility-first; custom classes in `global.css` under `@layer`
- No client-side JS by default; use `client:` directives only when necessary
- Images: stored in `public/assets/images/`; use Astro `<Image>` for optimization
- Fail fast — no silent error catches; surface errors with explicit messages

## Operational Rules

- **Search before reading** — use `grep`/`rg`/`find` instead of listing entire dirs
- **Targeted reads** — inspect only relevant line ranges of large files
- **Surgical edits** — minimal diffs; do not rewrite files with fewer than 5 changed lines
- **Schema changes** → run `npm run check`
- **Any code change** → run `npm run build`, verify `dist/index.html` exists
- **Never edit** `package-lock.json`, `dist/`, or `.astro/` directly

