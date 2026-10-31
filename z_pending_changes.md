I've implemented the report's fixes and the site builds cleanly (`astro check`: 0 errors, `npm run build`: `dist/index.html` produced). Nothing is committed. Several items need your decision or an external step before go-live.

## What changed

- **Global:** Header labels, the Resources dropdown, the `Prana-Logo-.png` logo and "Get in touch" CTA. Footer rewritten to the section 2.2 text. Cookie consent banner added (Manage consent / Accept / Deny / View preferences, with the Cookies Policy text taken from the live page).
- **Home:** Hero uses `image-23-scaled-1.png`. Extra sections, the logo strip and the Learn More button removed. Body copy matches 9.1.
- **BridgeAD:** Rebuilt from 9.7, with no invented stats and no filter/search UI. Workload table statuses are taken from the live page, so Teams private chats is **Conditional**. Three unused components were deleted.
- **FAQ:** The accordion is now plain, with category headings and the 9.2 copy. Hero uses `Screenshot-2026-01-29-180248.png`.
- **Contact:** Six-field form (Name, Email, Phone, Subject, Message, Send Message). Shortcode and UAT email removed.
- **Privacy and Terms:** Bodies rewritten from 9.4/9.5 with `https://pranast.com/` and `info@pranast.com`. No `**` in the rendered HTML.
- **Blog:** Fixed the broken bold markers and set real authors. Single posts now have the author box (exact bios and avatars), Posts navigation and Related Posts. The CTA and featured image are gone. Added `/category/digital-transformation/` and `/category/cyber-security/`.
- **Case studies:** Hub uses "Our Success Stories" with the extra cards removed. Detail-page CTA removed. UAT links repointed.
- **SEO and routing:** `site` is `https://pranast.com`. `trailingSlash: 'always'` to match pranast.com, with internal links updated. `@astrojs/sitemap` added, plus `robots.txt`. Section 7 301s added to `public/.htaccess`.
- **Images:** Downloaded the two author avatars. The other section 8 images were already in the repo.

## Verified

Against the built `dist/`: no `uat.` URLs, no `[ninja_form`, no rendered `**`, the footer, contact labels and header labels match the report, and the sitemap and robots files exist.

## Needs your decision or an external step

1. **Contact form won't deliver yet.** It still uses the Web3Forms placeholder key `YOUR_ACCESS_KEY_HERE`. Add the real key and run a test submission to info@pranast.com. I did not submit the form.
2. **Blog comments** (5.2 item 4) are not implemented. Choose a comments service or drop it.
3. **Source-site wording copied as-is** for strict parity: the FAQ's "TechPro Solutions" question, and the BridgeAD typos ("IMAR", "sharePoint", "content- transfer", "Apqor Technologies Pvt Ltd ,"). Fix on both sites or accept the mismatch.
4. **MedCare and RetailMax "Read Full Case Studies" links** point to `/medcare-health-systems/` and `/retailmax-…/`, which don't exist in this repo. They will 404 unless those pages are created.

## Judgment calls to check

- Blog cards show the date and author. Section 5.4 asks for real authors in the listing, but 6.1 lists only category, image, title and excerpt.
- Generic page heroes no longer repeat the description, since it duplicated the body text.
- "Back to Insights" and the "PS" placeholder were removed from posts.
- Facebook and X icons are unlinked, matching the live site, which has no link targets for them.
- The footer year is hard-coded to 2026 to match the exact text.
- Some appendix H1s became H2s to avoid duplicate H1s.
- `faq.md` and `bridgead.md` were deleted because their pages now carry the copy in the `.astro` files.

## Not verified

- The redirects are untested. I have no way to run Hostinger's Apache here.
- The cookie banner and the layout haven't been checked in a browser.
- The root HTML files changed because `npm run build` copies `dist/` to the repo root, as the project's deploy step does.