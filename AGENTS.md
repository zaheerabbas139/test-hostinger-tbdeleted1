# AGENTS.md — Pranast Website (Codex / OpenAI)

> Full agent persona & architectural guidelines: `GEMINI.md` (single source of truth).
> Detailed Claude-specific instructions: `CLAUDE.md` (architecture map, schema refs, etc.).

## Commands

```sh
npm run dev          # Astro dev server (localhost:4321)
npm run build        # SSG build → dist/; also copies to repo root
npm run check        # TS + Astro content schema validation
npm run preview      # Preview built output locally
npm run extract      # python3 scripts/extract-wp-xml.py
```

## Stack (quick ref)

- **Astro 7** — `output: 'static'`, Islands architecture, zero client-JS by default
- **Tailwind CSS v4** — via `@tailwindcss/vite`; no `tailwind.config.js`
- **TypeScript strict** — `@astrojs/check`; path alias `@/*` → `src/*`
- **Deploy** — GitHub Actions → FTPS → Hostinger `public_html/`

## Directory Map

```
src/content/        ← Markdown source (blog/, case-studies/, pages/)
src/content.config.ts ← Zod schemas for all 3 collections
src/pages/          ← Astro routes ([...slug].astro, blog/, case-studies/)
src/components/     ← Astro components (Header, Footer, ContactForm, etc.)
src/layouts/        ← BaseLayout.astro (global shell + SEO meta)
src/styles/         ← global.css (Tailwind @layer customizations)
public/             ← Static assets (images, favicon)
scripts/            ← One-off migration utilities (Python/JS)
docs/               ← Architecture & infra documentation
dist/               ← BUILD OUTPUT — never edit manually
```

## Agent Operational Rules

- **Search before reading** — use `grep`/`rg`/`find -name` rather than reading full dirs
- **Read targeted line ranges** — never load an entire large file when only a block is needed
- **Surgical edits** — minimal diffs only; do not rewrite files that need <5 line changes
- **After schema changes** → run `npm run check`
- **After any code change** → run `npm run build`, verify `dist/index.html` exists
- **Never edit** `package-lock.json`, `dist/`, or `.astro/` directly
- **Content edits** → modify `.md` in `src/content/`; never touch generated output
- **No lockfile creation** — this project uses npm (`package-lock.json`); do not generate `yarn.lock` or `pnpm-lock.yaml`

