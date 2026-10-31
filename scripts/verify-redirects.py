#!/usr/bin/env python3
"""
Phase 4 Automated SEO & 301 Redirect Mapping Verification Suite

Simulates incoming HTTP requests against:
1. Cloudflare Edge Worker routing engine logic
2. .htaccess Apache/LiteSpeed mod_rewrite regex rules

Validates:
- HTTP 301 status for all 6 blog articles (WP root -> Astro /blog/[slug])
- HTTP 301 status for all case studies (WP root -> Astro /case-studies/[slug])
- HTTP 301 status for legacy page aliases (terms-of-services -> terms-of-service, home -> /)
- HTTP 301 status for ID query parameters (?p=ID, ?page_id=ID)
- HTTP 301 status for media uploads (/wp-content/uploads/YYYY/MM/file -> /assets/images/file)
- HTTP 410 status for security probe endpoints (wp-login.php, xmlrpc.php, /wp-admin/)
- Canonical trailing slash handling
"""

import re
from urllib.parse import urlparse, parse_qs

# Exact Map from Cloudflare / .htaccess
EXACT_MAPPINGS = {
    "/digital-transformation-where-to-start": "/blog/digital-transformation-where-to-start",
    "/the-power-of-microsoft-power-platform": "/blog/the-power-of-microsoft-power-platform",
    "/understanding-zero-trust-security-architecture": "/blog/understanding-zero-trust-security-architecture",
    "/google-sheets-vs-dynamics-365": "/blog/google-sheets-vs-dynamics-365",
    "/why-digital-transformation-projects-fail": "/blog/why-digital-transformation-projects-fail",
    "/the-hidden-security-risks-of-rapid-digital-transformation": "/blog/the-hidden-security-risks-of-rapid-digital-transformation",
    "/globaltech-solutions": "/case-studies/globaltech-solutions",
    "/premier-law-associates": "/case-studies/premier-law-associates",
    "/case-studies": "/case-studies",
    "/terms-of-services": "/terms-of-service",
    "/home": "/",
    "/home-page": "/",
    "/technology-innovation": "/bridgead",
    "/services": "/digital-transformation",
    "/resources": "/blog",
    "/insights": "/blog",
    "/blogs-2": "/blog",
    "/blogs": "/blog",
    "/feed": "/blog",
}

QUERY_P_MAPPINGS = {
    "117": "/blog/digital-transformation-where-to-start",
    "123": "/blog/the-power-of-microsoft-power-platform",
    "129": "/blog/understanding-zero-trust-security-architecture",
    "204": "/blog/google-sheets-vs-dynamics-365",
    "351": "/blog/why-digital-transformation-projects-fail",
    "358": "/blog/the-hidden-security-risks-of-rapid-digital-transformation",
}

QUERY_PAGE_ID_MAPPINGS = {
    "3": "/privacy-policy",
    "9": "/",
    "12": "/contact",
    "21": "/",
    "34": "/who-we-are",
    "44": "/cyber-security",
    "56": "/digital-transformation",
    "67": "/cloud-infrastructure",
    "75": "/it-support-managed-services",
    "104": "/case-studies",
    "135": "/case-studies/globaltech-solutions",
    "142": "/case-studies/premier-law-associates",
    "177": "/faq",
    "326": "/terms-of-service",
    "369": "/bridgead",
}

WP_SECURITY_PATTERNS = [
    re.compile(r"^/wp-admin(?:/.*)?$", re.I),
    re.compile(r"^/wp-includes(?:/.*)?$", re.I),
    re.compile(r"^/wp-content/plugins(?:/.*)?$", re.I),
    re.compile(r"^/wp-json(?:/.*)?$", re.I),
    re.compile(r"^/xmlrpc\.php$", re.I),
    re.compile(r"^/wp-login\.php$", re.I),
    re.compile(r"^/wp-config\.php$", re.I),
    re.compile(r"^/trackback(?:/.*)?$", re.I),
]

def simulate_engine(url_str: str):
    """Simulates the Edge & .htaccess unified resolution pipeline."""
    parsed = urlparse(url_str)
    path = parsed.path
    qs = parse_qs(parsed.query)

    # 1. Security Check (410)
    for p in WP_SECURITY_PATTERNS:
        if p.match(path):
            return 410, "GONE"

    # 2. Query String IDs
    if "p" in qs:
        pid = qs["p"][0]
        if pid in QUERY_P_MAPPINGS:
            return 301, QUERY_P_MAPPINGS[pid]

    if "page_id" in qs:
        pid = qs["page_id"][0]
        if pid in QUERY_PAGE_ID_MAPPINGS:
            return 301, QUERY_PAGE_ID_MAPPINGS[pid]

    # 3. Media rewrite
    media_match = re.match(r"^/wp-content/uploads/(?:.+/)?([^/]+\.(?:jpe?g|png|gif|webp|svg|pdf))$", path, re.I)
    if media_match:
        return 301, f"/assets/images/{media_match.group(1)}"

    # 4. Exact path (normalized without trailing slash)
    norm_path = path.rstrip("/") if len(path) > 1 else path
    if norm_path in EXACT_MAPPINGS:
        return 301, EXACT_MAPPINGS[norm_path]

    # 5. Taxonomies, Feeds, Archives
    if (path.startswith("/category/") or
        path.startswith("/tag/") or
        re.match(r"^/[0-9]{4}(?:/[0-9]{2})?/?$", path) or
        path.endswith("/feed/") or path.endswith("/feed")):
        return 301, "/blog"

    if path.startswith("/author/"):
        return 301, "/who-we-are"

    # 6. Fallthrough to Astro static route
    return 200, path

def run_tests():
    test_cases = [
        # Blog Articles
        ("https://uat.pranast.com/digital-transformation-where-to-start/", 301, "/blog/digital-transformation-where-to-start"),
        ("https://uat.pranast.com/digital-transformation-where-to-start", 301, "/blog/digital-transformation-where-to-start"),
        ("https://uat.pranast.com/the-power-of-microsoft-power-platform/", 301, "/blog/the-power-of-microsoft-power-platform"),
        ("https://uat.pranast.com/understanding-zero-trust-security-architecture/", 301, "/blog/understanding-zero-trust-security-architecture"),
        ("https://uat.pranast.com/google-sheets-vs-dynamics-365/", 301, "/blog/google-sheets-vs-dynamics-365"),
        ("https://uat.pranast.com/why-digital-transformation-projects-fail/", 301, "/blog/why-digital-transformation-projects-fail"),
        ("https://uat.pranast.com/the-hidden-security-risks-of-rapid-digital-transformation/", 301, "/blog/the-hidden-security-risks-of-rapid-digital-transformation"),

        # Case Studies
        ("https://uat.pranast.com/globaltech-solutions/", 301, "/case-studies/globaltech-solutions"),
        ("https://uat.pranast.com/premier-law-associates/", 301, "/case-studies/premier-law-associates"),

        # Pages & Aliases
        ("https://uat.pranast.com/terms-of-services/", 301, "/terms-of-service"),
        ("https://uat.pranast.com/home/", 301, "/"),
        ("https://uat.pranast.com/home-page/", 301, "/"),
        ("https://uat.pranast.com/technology-innovation/", 301, "/bridgead"),
        ("https://uat.pranast.com/services/", 301, "/digital-transformation"),
        ("https://uat.pranast.com/resources/", 301, "/blog"),
        ("https://uat.pranast.com/insights/", 301, "/blog"),

        # Query Parameters
        ("https://uat.pranast.com/?p=117", 301, "/blog/digital-transformation-where-to-start"),
        ("https://uat.pranast.com/?p=123", 301, "/blog/the-power-of-microsoft-power-platform"),
        ("https://uat.pranast.com/?page_id=3", 301, "/privacy-policy"),
        ("https://uat.pranast.com/?page_id=369", 301, "/bridgead"),
        ("https://uat.pranast.com/?page_id=135", 301, "/case-studies/globaltech-solutions"),

        # Media Uploads
        ("https://uat.pranast.com/wp-content/uploads/2026/02/image-23-scaled-1.png", 301, "/assets/images/image-23-scaled-1.png"),
        ("https://uat.pranast.com/wp-content/uploads/2026/01/prana-Logo.png", 301, "/assets/images/prana-Logo.png"),

        # Taxonomies & Feeds
        ("https://uat.pranast.com/category/cyber-security/", 301, "/blog"),
        ("https://uat.pranast.com/category/digital-transformation/", 301, "/blog"),
        ("https://uat.pranast.com/tag/azure/", 301, "/blog"),
        ("https://uat.pranast.com/feed/", 301, "/blog"),
        ("https://uat.pranast.com/author/admin/", 301, "/who-we-are"),

        # Security Probes (410 Gone)
        ("https://uat.pranast.com/wp-admin/", 410, "GONE"),
        ("https://uat.pranast.com/wp-login.php", 410, "GONE"),
        ("https://uat.pranast.com/xmlrpc.php", 410, "GONE"),
        ("https://uat.pranast.com/wp-json/wp/v2/posts", 410, "GONE"),
        ("https://uat.pranast.com/wp-config.php", 410, "GONE"),

        # Native Astro Routes (Passthrough 200)
        ("https://uat.pranast.com/who-we-are", 200, "/who-we-are"),
        ("https://uat.pranast.com/cyber-security", 200, "/cyber-security"),
        ("https://uat.pranast.com/bridgead", 200, "/bridgead"),
        ("https://uat.pranast.com/faq", 200, "/faq"),
    ]

    passed = 0
    failed = 0

    print("================================================================================")
    print("PHASE 4: SEO 301 REDIRECT & EDGE HARDENING VERIFICATION")
    print("================================================================================")

    for url, expected_code, expected_dest in test_cases:
        status, dest = simulate_engine(url)
        if status == expected_code and (dest == expected_dest or expected_dest in dest):
            print(f" [PASS] {url:70} -> HTTP {status} ({dest})")
            passed += 1
        else:
            print(f" [FAIL] {url:70}")
            print(f"        Expected: HTTP {expected_code} -> {expected_dest}")
            print(f"        Received: HTTP {status} -> {dest}")
            failed += 1

    print("================================================================================")
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests.")
    print("================================================================================")
    if failed > 0:
        exit(1)

if __name__ == "__main__":
    run_tests()

