/**
 * Cloudflare Edge Worker: SEO 301 Redirects & WordPress Decommissioning Hardening
 *
 * Architecture:
 * - Sub-10ms global edge execution across 300+ Cloudflare PoPs.
 * - Terminates legacy WordPress traffic before hitting Hostinger origin server.
 * - HTTP 410 Gone for legacy WordPress security attack surface.
 * - Clean HTTP 301 Permanent Redirects for link equity & PageRank preservation.
 * - Regex media rewrites for /wp-content/uploads/ -> /assets/images/.
 * - Legacy query parameter lookup (?p=ID, ?page_id=ID).
 */

// 1. Master Exact Path Mappings (Trailing slash normalized internally)
const EXACT_REDIRECTS = new Map([
  // Legacy Blog Posts (WP root URL -> Astro /blog/ subpath)
  ['/digital-transformation-where-to-start', '/blog/digital-transformation-where-to-start'],
  ['/the-power-of-microsoft-power-platform', '/blog/the-power-of-microsoft-power-platform'],
  ['/understanding-zero-trust-security-architecture', '/blog/understanding-zero-trust-security-architecture'],
  ['/google-sheets-vs-dynamics-365', '/blog/google-sheets-vs-dynamics-365'],
  ['/why-digital-transformation-projects-fail', '/blog/why-digital-transformation-projects-fail'],
  ['/the-hidden-security-risks-of-rapid-digital-transformation', '/blog/the-hidden-security-risks-of-rapid-digital-transformation'],

  // Legacy Case Studies (WP root URL -> Astro /case-studies/ subpath)
  ['/globaltech-solutions', '/case-studies/globaltech-solutions'],
  ['/premier-law-associates', '/case-studies/premier-law-associates'],
  ['/case-studies', '/case-studies'],

  // Legacy Pages & Slug Corrections
  ['/terms-of-services', '/terms-of-service'],
  ['/home', '/'],
  ['/home-page', '/'],
  ['/technology-innovation', '/bridgead'],
  ['/services', '/digital-transformation'],
  ['/resources', '/blog'],
  ['/insights', '/blog'],
  ['/blogs-2', '/blog'],
  ['/blogs', '/blog'],
  ['/feed', '/blog'],
]);

// 2. Query Parameter Mappings (?p=ID and ?page_id=ID)
const QUERY_P_REDIRECTS = new Map([
  ['117', '/blog/digital-transformation-where-to-start'],
  ['123', '/blog/the-power-of-microsoft-power-platform'],
  ['129', '/blog/understanding-zero-trust-security-architecture'],
  ['204', '/blog/google-sheets-vs-dynamics-365'],
  ['351', '/blog/why-digital-transformation-projects-fail'],
  ['358', '/blog/the-hidden-security-risks-of-rapid-digital-transformation'],
]);

const QUERY_PAGE_ID_REDIRECTS = new Map([
  ['3', '/privacy-policy'],
  ['9', '/'],
  ['12', '/contact'],
  ['21', '/'],
  ['34', '/who-we-are'],
  ['44', '/cyber-security'],
  ['56', '/digital-transformation'],
  ['67', '/cloud-infrastructure'],
  ['75', '/it-support-managed-services'],
  ['104', '/case-studies'],
  ['135', '/case-studies/globaltech-solutions'],
  ['142', '/case-studies/premier-law-associates'],
  ['177', '/faq'],
  ['326', '/terms-of-service'],
  ['369', '/bridgead'],
]);

// 3. Security Decommission Blacklist: Return 410 Gone immediately
const WP_SECURITY_PATTERNS = [
  /^\/wp-admin(?:\/.*)?$/i,
  /^\/wp-includes(?:\/.*)?$/i,
  /^\/wp-content\/plugins(?:\/.*)?$/i,
  /^\/wp-json(?:\/.*)?$/i,
  /^\/xmlrpc\.php$/i,
  /^\/wp-login\.php$/i,
  /^\/wp-config\.php$/i,
  /^\/trackback(?:\/.*)?$/i,
];

// Helper to construct 301 response with standard security headers
function create301Response(targetUrl) {
  return new Response(null, {
    status: 301,
    statusText: 'Moved Permanently',
    headers: {
      Location: targetUrl,
      'Cache-Control': 'public, max-age=86400, s-maxage=604800',
      'X-Content-Type-Options': 'nosniff',
      'X-Redirect-Engine': 'Cloudflare-Edge-Worker',
    },
  });
}

// Helper to construct 410 Gone response
function create410Response() {
  const body = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>410 Gone - Endpoint Decommissioned</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; text-align: center; padding: 100px 20px; background: #0f172a; color: #f8fafc; }
    h1 { font-size: 2.5rem; margin-bottom: 0.5rem; color: #ef4444; }
    p { font-size: 1.1rem; color: #94a3b8; max-width: 600px; margin: 0 auto 2rem; }
    a { color: #3b82f6; text-decoration: none; font-weight: 600; }
  </style>
</head>
<body>
  <h1>410 - Endpoint Decommissioned</h1>
  <p>The legacy WordPress backend has been permanently decommissioned and migrated to a modern Astro edge architecture.</p>
  <a href="/">&larr; Return to Pranast Homepage</a>
</body>
</html>`;

  return new Response(body, {
    status: 410,
    statusText: 'Gone',
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'public, max-age=604800',
      'X-Robots-Tag': 'noindex, nofollow, noarchive',
    },
  });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    // STEP 1: HTTPS Redirection
    if (url.protocol === 'http:') {
      url.protocol = 'https:';
      return Response.redirect(url.toString(), 301);
    }

    // STEP 2: WP Security Hardening (Fast 410 Gone)
    for (const pattern of WP_SECURITY_PATTERNS) {
      if (pattern.test(pathname)) {
        return create410Response();
      }
    }

    // STEP 3: Legacy Query Parameters (?p=ID, ?page_id=ID)
    if (url.searchParams.has('p')) {
      const pId = url.searchParams.get('p');
      if (QUERY_P_REDIRECTS.has(pId)) {
        const dest = QUERY_P_REDIRECTS.get(pId);
        return create301Response(`${url.origin}${dest}`);
      }
    }

    if (url.searchParams.has('page_id')) {
      const pageId = url.searchParams.get('page_id');
      if (QUERY_PAGE_ID_REDIRECTS.has(pageId)) {
        const dest = QUERY_PAGE_ID_REDIRECTS.get(pageId);
        return create301Response(`${url.origin}${dest}`);
      }
    }

    // STEP 4: Media Asset Mapping (/wp-content/uploads/YYYY/MM/file -> /assets/images/file)
    const mediaMatch = pathname.match(/^\/wp-content\/uploads\/(?:.+\/)?([^/]+\.(?:jpe?g|png|gif|webp|svg|pdf))$/i);
    if (mediaMatch) {
      const filename = mediaMatch[1];
      return create301Response(`${url.origin}/assets/images/${filename}`);
    }

    // STEP 5: Exact Path Redirects (strip trailing slash for dictionary lookup)
    const normalizedPath = pathname.length > 1 && pathname.endsWith('/') ? pathname.slice(0, -1) : pathname;

    if (EXACT_REDIRECTS.has(normalizedPath)) {
      const targetPath = EXACT_REDIRECTS.get(normalizedPath);
      // Preserve incoming query string if present (except WP IDs already handled)
      const query = url.search;
      return create301Response(`${url.origin}${targetPath}${query}`);
    }

    // STEP 6: Pattern-Based Redirects (Taxonomies, Feeds, Authors, Archives)
    if (/^\/category(?:\/.*)?$/i.test(normalizedPath) ||
        /^\/tag(?:\/.*)?$/i.test(normalizedPath) ||
        /^\/[0-9]{4}(?:\/[0-9]{2})?$/i.test(normalizedPath) ||
        /^(?:.*\/)?feed(?:\/(?:rss|rss2|atom))?$/i.test(normalizedPath)) {
      return create301Response(`${url.origin}/blog`);
    }

    if (/^\/author(?:\/.*)?$/i.test(normalizedPath)) {
      return create301Response(`${url.origin}/who-we-are`);
    }

    // STEP 7: Passthrough to Origin Server (Hostinger)
    const response = await fetch(request);

    // Clone and append enterprise security headers to response
    const modifiedHeaders = new Headers(response.headers);
    modifiedHeaders.set('X-Content-Type-Options', 'nosniff');
    modifiedHeaders.set('X-Frame-Options', 'SAMEORIGIN');
    modifiedHeaders.set('Referrer-Policy', 'strict-origin-when-cross-origin');

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: modifiedHeaders,
    });
  },
};

