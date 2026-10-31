export type ThemeId = 'classic' | 'editorial' | 'modern-saas';

export interface ThemeConfig {
  id: ThemeId;
  name: string;
  description: string;
  badge?: string;
}

export const THEMES: readonly ThemeConfig[] = [
  {
    id: 'classic',
    name: 'Classic Corporate',
    description: 'Current baseline: Centered dark hero, single-column reading container, standard card grids',
    badge: 'Baseline',
  },
  {
    id: 'editorial',
    name: 'Editorial Magazine',
    description: 'Publication layout: Sticky Table of Contents, pinned author bio, rich reading typography',
    badge: 'New',
  },
  {
    id: 'modern-saas',
    name: 'Modern SaaS / Bento',
    description: 'Tech layout: Split-hero, reading progress bar, bento-grid related insights',
    badge: 'Experimental',
  },
] as const;

export const DEFAULT_THEME: ThemeId = 'classic';

// Single-flag production activation: allows build-time env var or config flag
export const ACTIVE_THEME: ThemeId = (typeof process !== 'undefined' && (process.env?.THEME as ThemeId)) || DEFAULT_THEME;

export function isValidTheme(theme: unknown): theme is ThemeId {
  return typeof theme === 'string' && THEMES.some((t) => t.id === theme);
}

/**
 * Resolves the active theme based on URL query parameter (?theme=<name>),
 * the ACTIVE_THEME configuration, with defensive fallback to DEFAULT_THEME ('classic').
 */
export function resolveTheme(url?: URL | string): ThemeId {
  if (url) {
    try {
      const parsedUrl = typeof url === 'string' ? new URL(url, 'http://localhost') : url;
      const queryTheme = parsedUrl.searchParams.get('theme');
      if (isValidTheme(queryTheme)) {
        return queryTheme;
      }
    } catch {
      // In case of malformed URL, gracefully fall back
    }
  }

  return isValidTheme(ACTIVE_THEME) ? ACTIVE_THEME : DEFAULT_THEME;
}

