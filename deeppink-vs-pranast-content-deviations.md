# Content Parity Report: Deeppink (Astro) vs pranast.com (WordPress)

**Prepared:** 31 Oct 2026
**Source of truth:** https://pranast.com (WordPress + Elementor)
**Target to fix:** https://deeppink-eland-272195.hostingersite.com (Astro static build)

---

## 0. Instructions for the AI that fixes this

1. **pranast.com is the source of truth for all content.** That covers every heading, paragraph, list item, button label, FAQ question and answer, email address, link target and image.
2. **Visual design can stay as it is on Deeppink.** Layout, colours, fonts, spacing, card styles and animations do not need to match. **Text and images must match exactly.**
3. **Do not reword, "improve", expand or summarise any copy.** Copy it exactly as written in this report (Section 9 has the full source text for the most-changed pages).
4. **Remove all content that exists on Deeppink but not on pranast.com.** That includes extra sections, extra CTAs, extra stats, extra FAQ answers and extra filters/search UI that adds text.
5. Strip all leftover Markdown and WordPress artefacts from the rendered HTML: `**`, `[ninja_form id=1]`, and similar.
6. Never use `uat.pranast.com` anywhere. The production email is **info@pranast.com**.
7. After fixing, run the checklist in **Section 10**.

### How this comparison was done
- **pranast.com:** page/post body content was read through the WordPress REST API (`/wp-json/wp/v2/pages` and `/posts`). Header, footer, Elementor background images, post templates, category archives and the live contact form were read from the rendered site.
- **Deeppink:** every route was fetched and its rendered HTML parsed, with header/footer/nav compared separately.
- Text was compared line by line after normalising whitespace, `&`/`and` and punctuation. Images were compared by file name.
- 23 WordPress pages/posts were compared, plus the header, footer, category archives and blog template.

---

## 1. Summary

| # | pranast.com URL | Deeppink URL | Status | Severity |
|---|---|---|---|---|
| 1 | `/` (Home) | `/` | Extra sections and text, hidden content shown, wrong hero background | **High** |
| 2 | `/who-we-are/` | `/who-we-are` | Text matches. Logo image and hero background differ | Medium |
| 3 | `/cyber-security/` | `/cyber-security` | ✅ Text and images match | – |
| 4 | `/digital-transformation/` | `/digital-transformation` | ✅ Text and images match | – |
| 5 | `/cloud-infrastructure/` | `/cloud-infrastructure` | ✅ Text and images match | – |
| 6 | `/it-support-managed-services/` | `/it-support-managed-services` | ✅ Text and images match | – |
| 7 | `/bridgead/` | `/bridgead` | **Heavily rewritten.** 68 lines missing, 46 changed, ~136 extra | **Critical** |
| 8 | `/case-studies/` | `/case-studies` | Extra heading, intro and cards added | Medium |
| 9 | `/globaltech-solutions/` | `/case-studies/globaltech-solutions` | URL changed. Extra CTA | Low |
| 10 | `/premier-law-associates/` | `/case-studies/premier-law-associates` | URL changed. Extra CTA | Low |
| 11 | `/faq/` | `/faq` | **All answers rewritten.** Intro missing, extra UI and sections | **High** |
| 12 | `/contact/` | `/contact` | UAT email, raw shortcode visible, different form fields | **Critical** |
| 13 | `/privacy-policy/` | `/privacy-policy` | UAT email, broken URL, `**` artefacts | **High** |
| 14 | `/terms-of-service/` (WP slug `/terms-of-services/`) | `/terms-of-service` | UAT email, broken URL, `**` artefacts, numbering lost | **High** |
| 15 | 6 blog posts at root (e.g. `/google-sheets-vs-dynamics-365/`) | `/blog/<slug>` | URL changed, `**` artefacts in 3 posts, author box / navigation / related posts missing, extra CTA | **High** |
| 16 | `/category/digital-transformation/` and `/category/cyber-security/` | **404** | Category archives missing (replaced by a single `/blog` page with new text) | **High** |
| 17 | Header (global) | Header | Menu labels and structure differ, different logo file | Medium |
| 18 | Footer (global) | Footer | **Footer content rewritten.** Address, phone, hours and socials missing | **High** |
| 19 | Cookie consent banner (Complianz) | None | Missing (UK GDPR) | **High** |
| 20 | `/home/`, `/services/`, `/insights/` (legacy WP pages, not in the menu) | 404 | Not migrated. Needs a decision, see Section 7 | Low |

---

## 2. Global / site-wide deviations

### 2.1 Header / main navigation

**pranast.com header (exact):**

```
[Logo: Prana-Logo-.png] -> /
Home -> /
Who We are -> /who-we-are/
Services (dropdown, no link)
   Cyber Security -> /cyber-security/
   Digital Transformation -> /digital-transformation/
   Cloud & Infrastructure -> /cloud-infrastructure/
   IT Support & Managed Services -> /it-support-managed-services/
Technology & Innovation (dropdown, no link)
   BridgeAD -> /bridgead/
Resources (dropdown, no link)
   Blog (no link / #)
   Digital Transformation -> /category/digital-transformation/
   Cyber Security -> /category/cyber-security/
   Case Studies -> /case-studies/
   FAQ -> /faq/
Get in touch (button) -> /contact/
```

**Deeppink deviations:**

| Item | pranast.com | Deeppink | Fix |
|---|---|---|---|
| Menu label | `Who We are` | `Who We Are` | Use `Who We are` (exact casing) |
| Menu label | `Technology & Innovation` | `Technology and Innovation` | Use `Technology & Innovation` |
| Menu group | `Resources` dropdown containing Blog, Digital Transformation, Cyber Security, Case Studies, FAQ | No `Resources` group. `Case Studies`, `Blog` and `FAQ` are top-level items | Re-create the `Resources` dropdown with the 5 items above |
| Resources items | `Digital Transformation` and `Cyber Security` link to category archives | Missing | Add both, linking to the category archive pages (see 6.2) |
| CTA label | `Get in touch` | `Get in Touch` | Use `Get in touch` |
| Logo file | `Prana-Logo-.png` | `prana-solutions-logo.png` | See Section 8 |

### 2.2 Footer

**pranast.com footer (exact text):**

```
Prana Solutions Tech
Prana Solutions Tech Limited is an IT consultancy providing managed services, cloud solutions, and digital transformation support.
We help forward-thinking organisations modernise systems, improve efficiency, and scale with confidence.

[Facebook icon]  [X-twitter icon]  [LinkedIn icon -> https://www.linkedin.com/company/prana-solutions-tech-ltd/]

Our Services
  Cyber Security -> /cyber-security/
  Digital Transformation -> /digital-transformation/
  Cloud & Infrastructure -> /cloud-infrastructure/
  IT Support & Managed Services -> /it-support-managed-services/

Company
  Who we are -> /who-we-are/
  Contact -> /contact/

Blog
  Digital Transformation -> /category/digital-transformation/
  Cyber Security -> /category/cyber-security/

Get in Touch
  Porchester Mead, London, BR3 1TN
  United Kingdom
  +44 7345116118
  info@pranast.com
  Mon-Fri: 09:00 – 18:00

© 2026 Prana Solutions Tech Limited | Registered In England
Privacy Policy -> /privacy-policy/     Terms of Service -> /terms-of-service/
```

**Deeppink footer currently contains (all of this should be replaced with the block above):**

- A different company description: *"Premier Microsoft Solutions Partner delivering enterprise cloud infrastructure, cyber security, managed IT services, and digital transformation across the UK and internationally. Registered in England & Wales London, United Kingdom"*
- A "Core Services" column with renamed links: *Cyber Security & Zero Trust, Digital Transformation, Cloud & Azure Infrastructure, Managed IT & 24/7 SLA Support, BridgeAD Migration Platform*
- A "Company" column with extra/renamed links: *Who We Are, Client Case Studies, Insights & Thought Leadership, Frequently Asked Questions, Contact Us*
- `Email: info@pranast.com  Location: United Kingdom` and a `Request Assessment` button. Both are extra.
- `© 2026 Prana Solutions Tech Limited. All rights reserved.` The correct text is `© 2026 Prana Solutions Tech Limited | Registered In England`.
- **Missing:** street address (Porchester Mead, London, BR3 1TN), phone (+44 7345116118), business hours (Mon-Fri: 09:00 – 18:00), Facebook / X / LinkedIn icons, and the "Blog" column.
- Deeppink footer shows an extra logo image `prana-solutions-logo-white.png`. pranast.com's footer has **no logo image**, only the text "Prana Solutions Tech". Remove it, or keep it only if you accept a visual-only difference.

### 2.3 Cookie consent banner — MISSING

pranast.com runs a Complianz cookie banner ("Manage consent", Accept / Deny / View preferences) and a **Cookies Policy**. Deeppink has no consent banner. A UK company needs one under UK GDPR / PECR if any analytics or third-party cookies are set.
**Fix:** add a static-site-compatible consent banner (for example a lightweight JS consent script) with Accept / Deny / Preferences, and the same Cookies Policy text as pranast.com. Copy the full policy text from the live pranast.com banner ("View preferences" → Cookies Policy).

### 2.4 Site-wide text artefacts to remove

| Problem | Where | Fix |
|---|---|---|
| `info@uat.pranast.com` (UAT email) | `/contact`, `/privacy-policy`, `/terms-of-service` | Replace every occurrence with `info@pranast.com` (and `mailto:info@pranast.com`) |
| Literal `**` Markdown symbols rendered as text | `/privacy-policy`, `/terms-of-service`, 3 blog posts (Section 5) | Convert to proper `<strong>` or remove. No `**` may appear in rendered HTML |
| Raw WordPress shortcode `[ninja_form id=1]` visible as text | `/contact` | Delete it |
| Site URL rendered as `/` | Privacy Policy and Terms (`...when you visit / or engage...`, `...govern your use of / .`) | Render the literal text `https://pranast.com/` |

---

## 3. Page-by-page deviations

### 3.1 Home `/`

**Images**

| pranast.com | Deeppink | Action |
|---|---|---|
| Hero background **`image-23-scaled-1.png`** | Uses `Banner-03-1.png` | **Add `image-23-scaled-1.png`** and use it as the home hero background |
| `Screenshot-2026-01-24-140716.png` (Strategic Technology Partner) | Present, but also used a 2nd time in the extra "Our Capabilities" section | Fixed by removing the extra section |
| `Screenshot-2026-01-24-140705.png` (Cyber Security card) | Present ×2 | Same as above |
| `Screenshot-2026-01-24-140651.png` (Digital Transformation & AI card) | Present ×2 | Same as above |
| `Screenshot-2026-01-24-140546.png` (Cloud & Infrastructure card) | Present ×2 | Same as above |

**Text: REMOVE these (present on Deeppink, not on pranast.com)**

1. Hero badge text: `Microsoft Solutions Partner` (above the H1).
2. Hero second button: `Learn More` (-> /who-we-are). pranast.com's hero has only one button, `Get In Touch`.
3. The whole extra section **"Our Capabilities / Enterprise IT Solutions Built for Scale"**, with its 4 rewritten cards and the `Explore service →` links:
   - "Comprehensive protection for your digital assets with the Microsoft Security Stack, ISO 27001 standards, and Zero Trust architecture."
   - "Strategic business process automation and data intelligence using Microsoft Dynamics 365, Power Platform, and AI-driven workflows."
   - "Secure, scalable Microsoft Azure solutions and modernized cloud infrastructure designed for resilient, always-available enterprise workloads."
   - "Proactive 24/7 monitoring, rapid helpdesk resolution, and ITIL-aligned service level agreements to keep your operations running smoothly."
4. The whole extra section **"Take the Next Step / Accelerate Your Digital Transformation"**, including:
   - "Whether you are looking to secure your Microsoft 365 environment, migrate legacy workloads to Azure, or modernize business processes, our solutions architects are ready to assist."
   - ✓ Complimentary IT & Cloud Readiness Assessment / ✓ Direct Access to Certified Microsoft Solutions Architects / ✓ Customized Modernization Roadmap & Cost Optimization
   - The "Send Us a Message" form (Full Name, Email Address, Phone Number, Inquiry Type, Message, Send Message)
5. **"Trusted by leading organisations" logo strip (Microsoft, Cisco, Dell, HP, Sophos) and the "Explore All Industries" link.** These exist in pranast.com's markup but are **hidden (not visible)** on the live site. On Deeppink they are visible. **Hide or remove them** to match what visitors see on pranast.com.

**Correct home page content (exact, in order):** see Appendix 9.1.

### 3.2 Who We are `/who-we-are`

- Text: ✅ exact match.
- Images:
  - Logo in the "Driving Digital Excellence" section: pranast.com uses **`prana-Logo.png`**, Deeppink uses `prana-solutions-logo.png` → **replace with `prana-Logo.png`** (Section 8).
  - Page hero/banner background: pranast.com uses **`photo-1504868584819-f8e8b4b6d7e3-scaled-1.jpg`**, Deeppink uses `Banner-03-1.png` → **replace**.
  - `pexels-yankrukov-7691691-scaled-1.jpg` (Expertise You Can Trust): ✅ match.

### 3.3 Cyber Security, Digital Transformation, Cloud & Infrastructure, IT Support & Managed Services

✅ All text and all inline images match. No action needed.
(Images checked: `img-01.png` to `img-04.png`, `Screenshot-2026-01-28-170529.png`, `-170546.png`, `-170559.png`.)

### 3.4 BridgeAD `/bridgead` — CRITICAL

Deeppink's BridgeAD page is a **rewritten marketing page**, not a copy of pranast.com. Partial edits are not practical here.
**Fix:** rebuild the page body from **Appendix 9.7** (pranast.com's exact text, in order). Keep Deeppink's visual components if you like, but use only this text.

Main problems:

- **H1 changed.** pranast.com: `Intelligent Migration & Digital Transformation Platform`. Deeppink: `Intelligent Active Directory & Microsoft 365 Migration`.
- **Intro changed.** pranast.com: "A technology platform designed to simplify, govern and accelerate Active Directory, Microsoft Entra ID and Microsoft 365 migration programmes."
- **Hero CTA changed.** pranast.com: `Get In Touch`. Deeppink: `Request BridgeAD Demo` / `Explore Workload Matrix`.
- **Invented stats added (remove):** "0 Bytes – Customer Data Retained at Rest", "Up to 60% Faster Discovery & Scoping", "SHA-256 Cryptographic Custody Evidence", "Dual-Mode Azure SaaS or Self-Hosted", "60% Faster Pre-Flight Scoping", "100% Auditable Evidence Chain", "Zero Unmapped Identity Surprises". These claims are **not on pranast.com** and should not be published.
- **Sections missing on Deeppink:** the 4 intro tiles (Cloud decisions / Microsoft workloads / Migration intelligence / Governed delivery), "Inside the application – From connection selection to signed-off evidence" (Select / Preview / Start / Control / Prove), "How it works – four operational phases" (Discover / Plan / Execute / Verify & close), "Operations – Built for delivery teams, not just demos", the full "Workload readiness" table text, "Who you are trusting" (Apqor Technologies Pvt Ltd, Hyderabad), and the closing "Ready to plan your migration? Tell us about your tenants and timeline. We respond within one business day."
- **Rewritten (46 lines)**, for example:
  - pranast.com H2 `Start with the migration you actually need to control.` → Deeppink `Start With the Migration You Need to Control`
  - pranast.com `AD forest consolidation` → Deeppink `Active Directory Forest Consolidation`
  - pranast.com `M&A and divestitures` → Deeppink `M&A and Corporate Divestitures`
  - pranast.com `Tenant-to-tenant planning` → Deeppink `Tenant-to-Tenant Modernization`
  - pranast.com `Mailbox migration - any to any` → Deeppink `Certified Any-to-Any Mailbox Routes`
  - pranast.com `Audit & Compliance` → Deeppink `Cryptographic Audit & Custody`
  - Security bullets rewritten with "✓ End-to-End Encryption:", "✓ Azure Key Vault & DPAPI:", and similar labels
  - All 8 FAQ answers expanded or reworded. For example, the integration answer now names ServiceNow, Jira, Sentinel and Splunk, which pranast.com does not mention.
- **Extra UI/text to remove:** "Interactive Product Tour", "Live Console", "Production Console Preview • Hover to inspect telemetry view", the 5-stage "Operational Governance" stepper (STAGE 01–05, "Enforced Architectural Gates", "Stage Telemetry & Boundary"…), the "Use Cases & Scenarios" block with "Consult on this scenario →", "Cloud-Native Endpoint Conversion" card, the filterable "Workload Readiness Directory" (All Capabilities (12) / Supported (11) / Conditional (1)), FAQ filter chips (All 8 / General 0 / Cloud Solutions 2 …), "Expand All / Collapse All", "No matching questions found…", "Have a question not listed here?", "Contact Our Team", "Accelerate Your Active Directory & M365 Modernization", "Request BridgeAD Demo / Read Client Case Studies".
- Images: `intelligence-dashboard.webp` and `cloud-workloads-dashboard.webp` ✅ match. Deeppink added alt text, which is fine to keep.

### 3.5 Case Studies `/case-studies`

- All pranast.com text is present ✅ (GlobalTech Solutions, Premier Law Associates, MedCare Health Systems, RetailMax Corporation, with their challenges, solutions and results).
- **Remove these extras:**
  - H1 `Client Success Stories` and "Real-world business outcomes delivered through Microsoft cloud innovation, security hardening, and digital workplace modernizations." pranast.com's H1 is **`Our Success Stories`**, followed by "Discover how we've helped businesses transform their IT infrastructure, enhance security, and drive growth through innovative technology solutions."
  - Extra cards: "Technology & Cloud Infrastructure GlobalTech Solutions – Enterprise cloud modernization & Azure infrastructure consolidation – View Full Case Study →" and "Legal Services & Compliance Premier Law Associates – Zero Trust security and legal digital workplace compliance overhaul".
- Link label on pranast.com is `Read Full Case Studies`. Keep that label.
- Banner background `Banner-03-1.png` ✅ match.

### 3.6 Case study detail pages

| pranast.com | Deeppink | Issue |
|---|---|---|
| `/globaltech-solutions/` | `/case-studies/globaltech-solutions` | URL changed (add a redirect, Section 7). Text ✅ match |
| `/premier-law-associates/` | `/case-studies/premier-law-associates` | URL changed (add a redirect). Text ✅ match |

**Remove from both:** "Schedule a technical discovery session with our Microsoft solutions architects." and the `Request IT Assessment` button. These are not on pranast.com.

### 3.7 FAQ `/faq` — HIGH

**Missing on Deeppink:**
- H1 `Frequently Asked Questions`
- Intro: "Get answers to common questions about our services, processes, and how we can help your business."
- Category headings as on pranast.com: General / Cloud Solutions / Pricing & Contracts / Managed IT Services / Security. Each heading has its 2 questions under it.

**All 10 questions and answers are reworded on Deeppink.** Replace them all with Appendix 9.2. Examples:

| pranast.com (correct) | Deeppink (wrong) |
|---|---|
| What services does TechPro Solutions offer? ⚠️ | What services does Prana Solutions Tech offer? |
| How is pricing structured? | How is pricing structured for your services? |
| What is the typical contract length? | What is the typical contract length for managed IT services? |
| What is your response time for support requests? | What is your guaranteed response time for technical support requests? |
| "We guarantee a response time of less than 15 minutes for critical issues and less than 2 hours for standard support requests. Our support team is available 24/7/365." | "…under 15 minutes for critical Priority 1 (business-down) incidents… Network Operations Center (NOC)…" |

> ⚠️ **Source-site issue:** pranast.com's first FAQ question says **"TechPro Solutions"**. That looks like leftover template text. Strict parity means copying it as-is. The better option is to fix it on pranast.com too (to "Prana Solutions Tech"), so both sites stay identical. The site owner needs to decide.

**Remove from Deeppink:** "Expand All", "Collapse All", the filter chips (All 10 / General 2 / Cloud Solutions 2 / Pricing & Contracts 2 / Managed IT Services 2 / Security 2), the category prefix text in front of each question ("General …", "Security …"), "No matching questions found…", "Reset Filters", the "Direct Support / Have a question not listed here? / Contact Our Team" block, and the whole "Enterprise Capabilities / Explore Our Core Service Pillars" section (4 cards with "Learn more →").

**Image:** pranast.com FAQ hero background is **`Screenshot-2026-01-29-180248.png`**, and Deeppink uses `Banner-03-1.png` → **replace**.

### 3.8 Contact `/contact` — CRITICAL

| Issue | Fix |
|---|---|
| Email shown as `info@uat.pranast.com` | `info@pranast.com` |
| Raw text `[ninja_form id=1]` visible on the page | Delete it |
| Extra heading "Send Us a Message" and "Fill out the form below and one of our enterprise technology consultants will be in touch within 24 business hours." | Remove (not on pranast.com) |
| Form fields differ | Match pranast.com exactly (below) |

**pranast.com contact form fields (exact labels, in order):**

```
Name *
Email *
Phone
Subject
Message *
[Send Message]
```

Deeppink currently has: `Full Name *`, `Email Address *`, `Phone Number`, `Inquiry Type` (dropdown: General Inquiry, Cyber Security & Zero Trust, Digital Transformation & AI, Cloud & Microsoft Azure, Managed IT Support, BridgeAD Migration Platform), `Message *`. Rename the labels, replace the "Inquiry Type" dropdown with a free-text **Subject** field, and remove the dropdown.

> ⚠️ **Functional check:** pranast.com's form was Ninja Forms (PHP/MySQL). Deeppink is static Astro, so the form needs its own submission backend: a serverless function, a form service, or Hostinger's form handler. Confirm a test submission reaches **info@pranast.com** before go-live. I did not submit the form during this review.

Rest of the page (Get in Touch intro, Email, Phone +44 7345116118, Office address, Business Hours "Monday - Friday: 9:00 AM - 6:00 PM Saturday - Sunday: Closed") ✅ matches.
Images `email-icon.png`, `phone-icon.png`, `locatiin-icon.png`, `Screenshot-2026-01-28-193312.png` and the banner `Banner-03-1.png` ✅ match.

### 3.9 Privacy Policy `/privacy-policy`

| pranast.com (correct) | Deeppink (wrong) |
|---|---|
| …when you visit **https://pranast.com/** or engage with our services. | …when you visit **/** or engage with our services. |
| 1. Information : We Collect We may collect… | `**1. Information :****We Collect We may collect…` |
| 2. How We Collect Information: Information is collected… (numbered paragraph) | `- How We Collect Information:** …`. The "2." is lost and it is rendered as a bullet |
| 3. to 7. headings | Wrapped in literal `** … : **` |
| 8. Contact Data Controller: Prana Solutions Tech Limited – Email: **info@pranast.com** | `**8. Contact Data Controller: ** … Email: info@uat.pranast.com` |

Replace the whole body with Appendix 9.4.

### 3.10 Terms of Service `/terms-of-service`

| pranast.com (correct) | Deeppink (wrong) |
|---|---|
| These Terms of Service govern your use of **https://pranast.com/** . | …govern your use of **/** . |
| 1. Website: Use You agree to use the website lawfully and responsibly. | `- **Website: ** Use You agree…`. The "1." is lost and it is rendered as a bullet |
| 2. to 7. (numbered paragraphs) | Wrapped in literal `** … : **` |
| 8. Contact Email: **info@pranast.com** Location: London, United Kingdom | `**8. Contact Email: ** info@uat.pranast.com …` |

The heading on pranast.com is `TERMS OF SERVICE`. Replace the whole body with Appendix 9.5.

---

## 4. Contact details: canonical values (use everywhere)

```
Company:  Prana Solutions Tech Limited
Email:    info@pranast.com
Phone:    +44 7345116118
Address:  Porchester Mead, London, BR3 1TN, United Kingdom
Hours:    Mon-Fri: 09:00 – 18:00   (Contact page wording: "Monday - Friday: 9:00 AM - 6:00 PM Saturday - Sunday: Closed")
LinkedIn: https://www.linkedin.com/company/prana-solutions-tech-ltd/
Footer ©: © 2026 Prana Solutions Tech Limited | Registered In England
```

---

## 5. Blog

### 5.1 Posts: body text

All 6 post bodies match word for word ✅. However, **3 posts render literal `**` characters.** Remove them or convert them to bold:

| Post | Broken fragments on Deeppink |
|---|---|
| `/blog/the-hidden-security-risks-of-rapid-digital-transformation` | `security. ** As businesses adopt…`, `Transformation Increases Complexity**` (H2), `**Security teams may struggle to: **`, `**This creates: **` |
| `/blog/why-digital-transformation-projects-fail` | `**Platforms such as: **`, `At Prana Solutions Tech Limited **,** we help…`, `** Contact us today for a free IT assessment**` |
| `/blog/google-sheets-vs-dynamics-365` | `multiple versions.**Different teams…`, `person-dependent** to process-driven`, `manual effort.**Even small delays…`, `Final Thoughts**`, `starting point.**It helps…`, `Prana Solutions Tech Limited**, we help…` |

The root cause is likely the WordPress → Markdown conversion. Fix the converter or the source `.md` files, and check that every post renders with no `**`.

### 5.2 Post template: missing elements (present on every pranast.com post)

1. **Author box.** Format: `Author: <Name>`, then the bio, then "View all posts by <Name> >", with the avatar image.
   - **Manasa Nadaduru** (posts: why-digital-transformation-projects-fail, google-sheets-vs-dynamics-365, the-power-of-microsoft-power-platform, digital-transformation-where-to-start).
     Bio: "Nadaduru Manasa is a Business & Data Analyst and Dynamics 365 CRM Consultant, improves processes through simple and effective digital solutions."
     Avatar: `manasa-nadaduru_avatar.jpeg` (Section 8)
   - **Satish Kumar Balasundaram** (posts: the-hidden-security-risks-of-rapid-digital-transformation, understanding-zero-trust-security-architecture).
     Bio: "Satish B is an Azure Solution Architect and Cybersecurity & Compliance Specialist, driving secure cloud and modern workplace transformations across Microsoft 365, DevSecOps, and cloud infrastructure environments."
     Avatar: `satish-kumar-balasundaram_avatar.jpeg` (Section 8)
2. **Posts navigation.** H2 "Posts navigation", with `< Previous post title` / `Next post title >` (by date order).
3. **Related Posts.** H2 "Related Posts" with 3 posts from the same category (category label, thumbnail and title).
4. **Comment form** ("Leave a Reply", Name / Email / Website / Comment). This needs a backend on a static site. **Decision needed:** either add a comments service or consciously drop it. Flag the decision; don't leave it unmentioned.

### 5.3 Post template: extra elements on Deeppink (remove)

- The CTA box at the end of every post: "**Need help implementing this?** Our Microsoft Solutions Architects can assess your architecture and guide your transformation. **Book Consultation**".
- The featured image at the top of the single post. pranast.com single posts **do not show** the featured image above the content; it appears only in listings and related posts. Remove it, or keep it only if you accept a visual-only difference.

### 5.4 Post author and date in listings

The Deeppink `/blog` listing shows **"Prana Solutions Tech"** as the author for every post. Use the real authors:

| Post | Date | Author | Category |
|---|---|---|---|
| The Hidden Security Risks of Rapid Digital Transformation | 15 May 2026 | Satish Kumar Balasundaram | Cyber Security |
| Why Digital Transformation Projects Fail | 16 Apr 2026 | Manasa Nadaduru | Digital Transformation |
| Google Sheets vs Dynamics 365 | 20 Mar 2026 | Manasa Nadaduru | Digital Transformation |
| Understanding Zero Trust Security Architecture | 19 Feb 2026 | Satish Kumar Balasundaram | Cyber Security |
| The Power of Microsoft Power Platform | 19 Feb 2026 | Manasa Nadaduru | Digital Transformation |
| Digital Transformation: Where to Start | 19 Feb 2026 | Manasa Nadaduru | Digital Transformation |

Featured images match ✅ (`The-Hidden-Security-Risks-of-Rapid-Digital-Transformation.png`, `Why-Digital-Transformation-Projects-Fail.png`, `Google-Sheets-vs-Dynamics-365-comparison.jpg`, `Cyber-Security-2.jpg`, `IT-Services.jpg`, `Digital-Transformation-Blog.png`).

---

## 6. Blog listing / category archives

### 6.1 Deeppink `/blog` has text that is not on pranast.com (remove)

- "Thought Leadership"
- "Insights & Technical Perspectives"
- "Actionable strategies and architectural guidance to help enterprise leaders navigate modern IT modernization, Zero Trust security, and cloud scalability."
- "Read Article →". pranast.com archive cards show the category label, the image, the title and an excerpt only.

### 6.2 Missing pages (404 on Deeppink)

| pranast.com | Content | Fix |
|---|---|---|
| `/category/digital-transformation/` | Heading "Digital Transformation" + 4 post cards: Why Digital Transformation Projects Fail, Google Sheets vs Dynamics 365, The Power of Microsoft Power Platform, Digital Transformation: Where to Start | Create the page at the same path |
| `/category/cyber-security/` | Heading "Cyber Security" + 2 post cards: The Hidden Security Risks of Rapid Digital Transformation, Understanding Zero Trust Security Architecture | Create the page at the same path |

Both are linked from pranast.com's header (Resources) and footer (Blog column).

---

## 7. URL changes and redirects (needed for SEO when the domain switches)

When pranast.com is pointed at the Astro build, these existing, indexed URLs will 404 unless they are recreated or 301-redirected:

| Old pranast.com URL | Status on Deeppink | Required action |
|---|---|---|
| `/digital-transformation-where-to-start/` | 404 | 301 → `/blog/digital-transformation-where-to-start` (or move the posts back to root slugs) |
| `/the-power-of-microsoft-power-platform/` | 404 | 301 → `/blog/the-power-of-microsoft-power-platform` |
| `/understanding-zero-trust-security-architecture/` | 404 | 301 → `/blog/understanding-zero-trust-security-architecture` |
| `/google-sheets-vs-dynamics-365/` | 404 | 301 → `/blog/google-sheets-vs-dynamics-365` |
| `/why-digital-transformation-projects-fail/` | 404 | 301 → `/blog/why-digital-transformation-projects-fail` |
| `/the-hidden-security-risks-of-rapid-digital-transformation/` | 404 | 301 → `/blog/the-hidden-security-risks-of-rapid-digital-transformation` |
| `/globaltech-solutions/` | 404 | 301 → `/case-studies/globaltech-solutions` |
| `/premier-law-associates/` | 404 | 301 → `/case-studies/premier-law-associates` |
| `/terms-of-services/` (WP sitemap slug) | 404 | 301 → `/terms-of-service` |
| `/category/digital-transformation/` | 404 | Create the page (6.2) |
| `/category/cyber-security/` | 404 | Create the page (6.2) |
| `/home/`, `/services/`, `/insights/` | 404 | Legacy pages from Dec 2025, not linked in the menu but still published in the WP sitemap. Recommended: 301 → `/`. If the owner wants them kept, the full source text is in pranast.com's REST API |
| `/author/...` (3 author archives) | 404 | Optional: 301 → `/blog` |

The Astro site also has **no sitemap** (`/sitemap-index.xml` is 404). Add `@astrojs/sitemap` and publish a `robots.txt` that points to it.
Trailing slashes: pranast.com uses them (`/faq/`). Deeppink links mix both forms (`/contact` and `/contact/`). Pick one, set `trailingSlash` in `astro.config`, and use it consistently.

---

## 8. Image actions

Download each file from pranast.com and add it to the Deeppink project (for example `/public/images/` or `src/assets/`), then use it where listed.

| # | Add this image (download from pranast.com) | Use it on Deeppink | Replaces |
|---|---|---|---|
| 1 | `https://pranast.com/wp-content/uploads/2026/02/Prana-Logo-.png` | Header logo (all pages) | `prana-solutions-logo.png` |
| 2 | `https://pranast.com/wp-content/uploads/2026/02/prana-Logo.png` | `/who-we-are` → "Driving Digital Excellence" section logo | `prana-solutions-logo.png` |
| 3 | `https://pranast.com/wp-content/uploads/2026/02/image-23-scaled-1.png` | `/` home hero background | `Banner-03-1.png` |
| 4 | `https://pranast.com/wp-content/uploads/2026/02/photo-1504868584819-f8e8b4b6d7e3-scaled-1.jpg` | `/who-we-are` hero/banner background | `Banner-03-1.png` |
| 5 | `https://pranast.com/wp-content/uploads/2026/03/Screenshot-2026-01-29-180248.png` | `/faq` hero/banner background | `Banner-03-1.png` |
| 6 | `https://pranast.com/wp-content/uploads/2026/03/manasa-nadaduru_avatar-96x96.jpeg` | Author box on Manasa's 4 posts | (new) |
| 7 | `https://pranast.com/wp-content/uploads/2026/03/satish-kumar-balasundaram_avatar-96x96.jpeg` | Author box on Satish's 2 posts | (new) |
| 8 | (none — remove) | Footer white logo `prana-solutions-logo-white.png` | pranast.com footer has no logo image |

**Images already correct on Deeppink (no action):** `Banner-03-1.png` (case-studies, contact), `Screenshot-2026-01-24-140716/140705/140651/140546.png` (home), `pexels-yankrukov-7691691-scaled-1.jpg` (who-we-are), `img-01…04.png` (service pages), `Screenshot-2026-01-28-170529/170546/170559.png` (digital transformation), `email-icon.png`, `phone-icon.png`, `locatiin-icon.png`, `Screenshot-2026-01-28-193312.png` (contact), `intelligence-dashboard.webp`, `cloud-workloads-dashboard.webp` (BridgeAD), and all 6 blog featured images.

---

## 9. Appendix: exact source text from pranast.com

Notation: `H1:`/`H2:`/`H3:` = heading level, `- ` = bullet item, other lines = paragraph, button or label. Copy the text exactly, including British spellings ("organisations", "modernise", "programmes").

### 9.1 Home `/`

```
H1: A Trusted IT Partner for Secure, Scalable Growth
We deliver managed IT support, Microsoft cloud solutions, cyber security, and digital transformation helping organisations stay resilient, compliant, and ready for what's next.
[Button] Get In Touch
H2: Our Commitment
H2: Your Strategic Technology Partner
We deliver enterprise-grade IT solutions that drive efficiency, security, and sustainable growth. As a Microsoft Solutions Partner, we combine technical excellence with a deep understanding of the business landscape to help you navigate an increasingly complex digital world.
H3: Cyber Security
Comprehensive protection for your digital assets with the Microsoft Security Stack and ISO 27001 standards.
H3: Digital Transformation & AI
Strategic innovation using Microsoft Dynamics 365, Power Platform, and AI-driven insights.
H3: Cloud & Infrastructure
Secure, scalable Microsoft Azure solutions and modern infrastructure designed for enterprise resilience.
H3: IT Support & Managed Services
Proactive 24/7 monitoring and helpdesk support to keep your operations running smoothly.
H2: Why Partner With Us
H2: Excellence in Delivery
- Microsoft Solutions Partner for Digital & App Innovation
- Dedicated support team available 24/7
- Proven methodology for digital transformation success
- ISO 27001 & Cyber Essentials Plus certified
- Enterprise-grade security and compliance focus
- Nationwide coverage supporting remote & hybrid teams
H2: Sectors
H2: Industries We Serve
Tailored technology solutions for diverse business sectors
H3: SMBs & Growing Enterprises
H3: Professional Services
H3: Remote & Hybrid Workforce
H3: Technology & Innovation
(HIDDEN on live site — do not display: "Explore All Industries", "Trusted by leading organisations", Microsoft, Cisco, Dell, HP, Sophos)
H1: Ready to Modernise Your IT Environment?
Let's discuss how Prana Solutions can transform your business operations, enhance security, and drive sustainable growth for your organisation.
[Button] Get Started Today -> /contact/
[Button] View Case Studies -> /case-studies/
```

### 9.2 FAQ `/faq`

```
H1: Frequently Asked Questions
Get answers to common questions about our services, processes, and how we can help your business.

H2: General
Q: What services does TechPro Solutions offer?   (see ⚠️ note in 3.7)
A: We offer comprehensive IT services including managed IT support, cloud solutions (Azure, Microsoft 365), cybersecurity, digital transformation with Dynamics 365 and Power Platform, and infrastructure management.
Q: Do you support businesses of all sizes?
A: Yes, we work with small and medium businesses, large enterprises, and everything in between. Our solutions are scalable and tailored to meet the specific needs of your organization.

H2: Cloud Solutions
Q: Can you help migrate our on-premises infrastructure to the cloud?
A: Yes, we specialize in cloud migration services using Microsoft Azure. We assess your current environment, design a migration strategy, and execute the migration with minimal disruption to your operations.
Q: What are the benefits of moving to Microsoft 365?
A: Microsoft 365 provides enterprise-grade productivity tools, advanced security features, anywhere access, automatic updates, scalability, and reduced IT management overhead.

H2: Pricing & Contracts
Q: How is pricing structured?
A: We offer flexible pricing models including monthly managed services contracts, project-based pricing, and hybrid arrangements. Contact us for a customized quote based on your specific needs.
Q: What is the typical contract length?
A: We typically offer 12-month contracts for managed services, but we can accommodate different terms based on your business requirements.

H2: Managed IT Services
Q: What is included in managed IT services?
A: Our managed IT services include 24/7 monitoring, helpdesk support, patch management, backup and disaster recovery, endpoint management, security monitoring, and proactive maintenance.
Q: What is your response time for support requests?
A: We guarantee a response time of less than 15 minutes for critical issues and less than 2 hours for standard support requests. Our support team is available 24/7/365.

H2: Security
Q: How do you protect against cyber threats?
A: We use a multi-layered security approach including Microsoft Security Stack (Defender, Sentinel, Intune), regular security assessments, employee training, security monitoring, and incident response capabilities.
Q: Do you provide compliance support?
A: Yes, we help organizations meet various compliance requirements including GDPR, HIPAA, ISO 27001, and industry-specific regulations through proper security controls and documentation.
```

### 9.3 Contact `/contact`

```
H1: Get in Touch
Have questions about our services? Ready to transform your IT infrastructure? We're here to help. Reach out to our team today.
H2: Contact Information
H3: Email
info@pranast.com
H3: Phone
+44 7345116118
H3: Office
Porchester Mead, London, BR3 1TN United Kingdom
H3: Business Hours
Monday - Friday: 9:00 AM - 6:00 PM
Saturday - Sunday: Closed

FORM: Name * | Email * | Phone | Subject | Message * | [Send Message]
```

### 9.4 Privacy Policy `/privacy-policy`

```
Prana Solutions Tech Limited ("we", "us", "our") is committed to protecting your personal information. This Privacy Policy explains how we collect, use, store, and safeguard personal data when you visit https://pranast.com/ or engage with our services.
This policy is provided for general information purposes only and does not constitute legal advice.
1. Information : We Collect We may collect personal data including name, email address, phone number, business details, technical data such as IP address and browser type, website usage data, and communication details.
2. How We Collect Information: Information is collected when you contact us, submit forms, enquire about IT consulting, staffing, or SaaS services, or automatically through cookies.
3. How We Use Information: We use personal data to respond to enquiries, deliver services, improve our website, communicate service updates, and comply with legal obligations.
4. Legal Basis for Processing: We process data based on contractual necessity, legitimate interests, legal obligations, or consent where required.
5. Data Sharing: We do not sell personal data. Information may be shared with trusted service providers or authorities where legally required.
6. Data Retention Personal: data is retained only as long as necessary for its purpose or legal compliance.
7. Your Rights: You have rights under UK GDPR including access, correction, deletion, restriction, objection, and withdrawal of consent.
8. Contact Data Controller: Prana Solutions Tech Limited – Email: info@pranast.com
```
(The bold labels, for example "1. Information :", may be rendered in `<strong>`. Never as literal `**`.)

### 9.5 Terms of Service `/terms-of-service`

```
H3: TERMS OF SERVICE
These Terms of Service govern your use of https://pranast.com/ . By accessing or using this website, you agree to these Terms.
These terms are provided for general information only and do not replace formal service contracts.
1. Website: Use You agree to use the website lawfully and responsibly.
2. Services Information: The website provides information about IT consulting, technology services, staffing solutions, and SaaS offerings. Website content is informational only.
3. Intellectual Property: All content on this website is owned by or licensed to Prana Solutions Tech Limited.
4. Availability and Accuracy: We aim to keep information accurate but do not guarantee completeness or uninterrupted availability.
5. Limitation of Liability: To the extent permitted by law, we are not liable for indirect or consequential losses arising from website use.
6. External Links: We are not responsible for third-party websites linked from this site.
7. Governing Law: These Terms are governed by the laws of England and Wales.
8. Contact Email: info@pranast.com Location: London, United Kingdom
```

### 9.6 Case Studies `/case-studies` (for reference: Deeppink already has this text, just remove the extras)

```
H1: Our Success Stories
Discover how we've helped businesses transform their IT infrastructure, enhance security, and drive growth through innovative technology solutions.
H2: Proven Results Across Industries
See how we've delivered measurable improvements in efficiency, security, and business outcomes
H2: GlobalTech Solutions
H3: Challenge
Legacy infrastructure causing frequent downtime and limiting scalability for a growing tech company.
H3: Solution
H3: Results
- 99.9% uptime achieved
- 40% reduction in IT costs
- 3x faster deployment times
- Scalable infrastructure for growth
[Link] Read Full Case Studies
H2: Premier Law Associates
Need for secure remote access and document management while maintaining strict compliance requirements.
Deployed Microsoft 365 with advanced security, Azure Virtual Desktop, and comprehensive document management.
- Secure remote work for 100+ attorneys
- Full compliance with legal standards
- 50% improvement in collaboration
- Enhanced client data protection
H2: MedCare Health Systems
Outdated systems and increasing cybersecurity threats in a healthcare environment.
Implemented Microsoft Security Stack with Defender, Sentinel, and comprehensive security policies.
- Zero security breaches post-implementation
- HIPAA compliance achieved
- 60% faster threat detection
- Improved patient data security
H2: RetailMax Corporation
Manual processes and disconnected systems limiting business agility and customer insights.
Digital transformation with Dynamics 365 CRM, Power Platform automation, and Power BI analytics.
- 35% increase in sales efficiency
- 80% reduction in manual tasks
- Real-time customer insights
- Improved customer satisfaction by 45%
```

### 9.7 BridgeAD `/bridgead`: full page text (rebuild from this)

```
H1: Intelligent Migration & Digital Transformation Platform
A technology platform designed to simplify, govern and accelerate Active Directory, Microsoft Entra ID and Microsoft 365 migration programmes.
[Button] Get In Touch
[Tabs] Intelligence | Cloud Workloads   (tab images: intelligence-dashboard.webp, cloud-workloads-dashboard.webp)
H3: Cloud decisions
Assessment, target design, plan and evidence
H3: Microsoft workloads
AD, Entra ID, Exchange, SharePoint and Teams - plus any-to-any mailbox routes
H3: Migration intelligence
Cited answers, failures and reports
H3: Governed delivery
Approvals, validation and audit evidence

H2: Inside the application
H2: From connection selection to signed-off evidence.
BridgeAD is not only a capability catalog. Operators work through named source and destination connections. They preview changes, start bounded jobs, and watch individual items move. They can intervene safely and close each wave with inspectable outputs.
H2: Select
Choose validated source and destination connections, agents, assessed objects, users, sites, mailboxes, or servers.
H2: Preview
Run dry-run or readiness checks, inspect collisions and unsupported items, then revise mappings or scope before writes begin.
H2: Start
Launch a job, wave, cloud-directory run, endpoint conversion, or server operation with the options attached to that run.
H2: Control
See the current item, processed and failed counts, warnings, throughput, and live state; pause, cancel, resume, or retry where supported.
H2: Prove
Review exceptions and validation, record acceptance, and export reports, certificates, transcripts, and audit evidence.

H2: Best-fit programs
H2: Start with the migration you actually need to control.
BridgeAD is designed first for AD-heavy and hybrid programs. In these programs, dependencies, operator control, rollback planning, and evidence matter as much as moving objects.
H2: AD forest consolidation
Discover, map, dry-run, and migrate directory objects through controlled waves.
H2: M&A and divestitures
Coordinate identity scope, approvals, execution, and evidence across environments.
H2: Tenant-to-tenant planning
Assess identity and workload readiness before committing to content- transfer scope.
H2: Regulated self-hosted delivery
Keep the control plane in customer-managed infrastructure with explicit cloud egress.
H2: MSP migration delivery
Standardize assessment, pilot boundaries, operator roles, and evidence across client programs.

H2: BridgeAD product family
H2: Two focused products for different migration responsibilities.
Choose Cloud Workloads for AD and Microsoft 365 migration. Choose Intelligence for cloud assessment, planning, controlled execution, analysis, and reporting.
H3: BridgeAD Cloud Workloads
Assess, scope, execute, reconcile, and prove Active Directory, Entra ID, Exchange, sharePoint, OneDrive, and Teams migrations - plus any-to-any mailbox moves across Gmail, IMAR on-premises Exchange, and archives.
H3: BridgeAD Intelligence
Assess cloud estates, compare target designs, verify plans, govern execution, investigate failures, and prepare cited reports.

H2: Cloud Workloads capabilities
H2: Dedicated engines for identity and Microsoft 365.
H3: Active Directory
Supported discovery, mapping, CSV workflows, collision checks, and dry runs. Topology-specific controlled pilots then cover execution, delta, SID, ACL, password, and rollback workflows.
H3: Mailbox migration - any to any
Certified routes between Exchange Online tenants, Gmail, IMAP hosts, on-premises Exchange (EWS), and PST/EML archives - mail, owned calendars, contacts, and tasks with resumable delta passes, signed fidelity contracts, and offline-verifiable custody evidence.
H3: SharePoint & OneDrive
Assessment-backed site and drive scoping with resumable Graph content transfer. Conflict handling and version depth are configurable. Permissions are mapped, lists are supported, and delta passes end in reconciliation.
H3: Microsoft Teams
Graph reconstruction for team and channel structure, mapped membership, supported settings, tabs, and tags. Microsoft-native channel-message import is conditional.
H3: Microsoft Entra ID
Graph-based users, groups, devices, and memberships with collision protection. Adds governed guest invitations, selected application definitions, and conditional Intune policy definitions.
H3: Audit & Compliance
Supported audit logging with hash-chain verification, correlation IDs, role-change traceability, and exportable operational reports.

H2: Workload readiness
H2: Know what can enter scope before the project starts.
Status applies to the exact scope stated below. Every engagement still depends on tenant state, permissions, connectivity, and identity mappings. Service limits, validation, and owned remediation also apply.
TABLE columns: CAPABILITY | STATUS | CURRENT/DELIVERY BOUNDARY
| AD discovery, mapping, CSV validation, and dry run | Supported | Available for orchestrating when connections and permissions validate. |
| AD migration orchestration and rollback | Supported | Dry-run first with success criteria; per-step rollback, automated rollback rules, and connectivity circuit breakers are built in. |
| SID history and ACL remapping | Supported | Agent-executed with streamed progress and evidence; multi-forest translation follows applied sync and one mapped peer link. |
| Entra users, groups, devices, and memberships | Supported | Configured Graph permissions required; synchronized attributes remain owned by Entra Connect or Cloud Sync. |
| Entra tenant-to-tenant users and static groups | Supported | Preview-first route with UPN transformation, optional update-existing reruns, and membership reconciliation; licenses, mailboxes, and MFA registration remain separate. |
| Google Workspace directory to Entra or AD | Supported | Users and groups only through domain-wide delegation; Gmail, Drive, Calendar, and source passwords are excluded from rollout. |
| Cloud-native device conversion | Supported | AD unjoin, Entra join, Microsoft 365 app reset, and BitLocker escrow verification — dry-run first, using a customer-built provisioning package and a per-device SYSTEM agent. |
| IIS and SQL Server migration | Supported | Agent-executed configuration and credential moves with preview and confirmation gates; TLS keys, TDE prerequisites, and break-glass secrets remain explicit boundary items. |
| Exchange Online mailbox content and cutover evidence | Supported | Microsoft 365 tenant-to-tenant Graph path plus certified any-to-any routes (Gmail, IMAP, EWS, archives); in-place archives and public folders migrate via the certified EWS route, with license assignment for re-guard. |
| SharePoint, OneDrive, and supported list content | Supported | Scoped Graph transfer; full app-fidelity, sharing links, and tenant governance are not implied. |
| Teams structure, membership, settings, tabs, and tags | Supported | Graph reconstruction; files and meetings move through their owning workloads. |
| Teams channel messages | Conditional | Requires Microsoft-protected-API approval and opt-in migration mode; attachments move through SharePoint and reactions are not preserved. |
| Teams private chats | (verify status label on pranast.com) | Re-creates mapped chat shells and walks full-history transport via destination OneDrive; requires secure Chat.Read.All, and history is not replayed into destination threads. |
NOTE: pranast.com's markup prints the STATUS label only on the 1st row ("Supported") and on "Teams channel messages" ("Conditional"). The "Supported" values on the other rows above are INFERRED. Verify every row's status against the live pranast.com/bridgead/ table before publishing.

H2: How it works
H2: From discovery to verification - in four operational phases.
BridgeAD standardises migration delivery so teams can assess risk early, execute in controlled waves, and close with evidence-backed reporting.
H2: Discover
Connect source and destination environments and run read-only discovery. Baseline identity, directory, and workload readiness before scope is committed.
H2: Plan
Build mapping rules, wave strategy, and rollback guardrails. Dry-run validates assumptions. It produces a clear execution plan per migration phase.
H2: Execute
Execute dependency-ordered jobs with retry, resume, and real-time progress telemetry. Pause, resume, cancel, or retry failed items without losing control.
H2: Verify & close
Run reconciliation checks and export audit and job reports. Close with governed handover and operational evidence for client, security, and compliance teams.

H2: Operations
H2: Built for delivery teams, not just demos.
BridgeAD includes the controls and integrations required to run migration programs at enterprise scale.
H3: Assessment & reporting
Pre-migration readiness scoring, finding categorisation, and exportable reports in CSV, Excel, and PDF formats.
H3: Real-time operations
SignalR live dashboards, health checks, metrics endpoints, and alert-ready telemetry for NOC and delivery teams.
H3: API & automation
Comprehensive authenticated APIs and signed webhook notifications. Integrates with ITSM, SIEM, and internal orchestration pipelines.
H3: On-prem execution agent
Outbound-only Windows agent with pairing, heartbeat monitoring, command dispatch, and controlled auto-update workflows.

H2: Security
H2: Security Migration content is streamed, not retained by the control plane.
BridgeAD persists the operational metadata needed to orchestrate and audit work. Mail, file, and message bodies are not retained at rest in BridgeAD infrastructure.
- Customer migration content is streamed source → destination; no mailbox, file, or message body is persisted at rest in BridgeAD infrastructure.
- All Microsoft Graph and Exchange traffic is TLS 1.2+; internal control plane uses TLS termination and mutual authentication.
- Secrets are stored in Azure Key Vault (SaaS) or DPAPI-protected local stores (self-hosted). Access tokens are never logged.
- Multi-tenant deployments enforce per-tenant data isolation via Entity Framework query filters and database-level row filters.
- Five-tier RBAC (Viewer, Migration Operator, Tenant Admin, Platform Admin, Super Admin) with mandatory MFA for all privileged roles.
- Self-hosted edition keeps every byte of customer data inside the customer's own infrastructure.

H2: Deployment
H2: Two deployment models. One orchestration approach.
Use managed SaaS or deploy the control plane in customer-managed infrastructure. Available features and required egress are confirmed during solution design.
H3: SaaS
Multi-tenant managed service hosted on Azure. Region-pinned data residency. Per-seat or per-mailbox licensing. Fastest path to first migration.
H3: Self-hosted
Single-tenant deployment inside the customer's Azure subscription, Kubernetes environment, or Docker host. Microsoft 365 workloads still require approved outbound access to Microsoft APIs.

H2: Who you are trusting
H2: Built and operated by the team you hold accountable.
BridgeAD is a product of Apqor Technologies Pvt Ltd , an engineering company based in Hyderabad, India. There is no reseller layer or outsourced support desk between you and the people who build the platform.
H3: Direct accountability
Migration engineering, security review, and commercial questions route to the team that ships the product. The same engineers who write the orchestration review your controlled-pilot plan.
H3: Claim discipline
Every public capability statement maps to a reviewed claim ledger and a readiness status — Supported, Conditional, Controlled pilot, or Manual. We publish boundaries next to claims rather than behind a sales call.
H3: Deployment control
Run managed SaaS with region-pinned residency, or self-host inside your own subscription, Kubernetes cluster, or Docker host. Your compliance boundary is a first-class design input, not an afterthought.
H3: Evidence over assurance
Assessment findings, dry runs, reconciliation, and sign-off exports are produced as verifiable artifacts. You evaluate us on what the platform records, not on what we promise.

H2: FAQ
H2: Common questions.
Q: Do we need an agent on every user workstation?
A: Not for directory or Microsoft 365 workload migrations: one healthy agent per reachable domain is often sufficient. Device-local workflows such as controlled-pilot cloud-native conversion are different. They require a healthy agent running as SYSTEM on each target Windows device for the conversion window.
Q: Does BridgeAD store our mailbox or file content?
A: No. Migration content is streamed in transit from source to destination. Only metadata required for orchestration (job state, error counts, audit records) is persisted – never bodies of mail, files, or messages.
Q: What is your Microsoft 365 workload migration readiness?
A: Exchange Online mailbox content (including certified any-to-any routes to and from Gmail, IMAP, on-premises Exchange, and PST/EML archives), SharePoint and OneDrive content, and Teams structure reconstruction are supported within their documented prerequisites and exclusions. Teams channel-message import is conditional on Microsoft protected-API approval. See the workload directory for exact scope and manual boundaries.
Q: Where does our data live in the SaaS edition?
A: You pin a primary Azure region at provisioning. All customer-scoped data (audit log, configuration, secrets in Azure Key Vault) stays in that region. Operational telemetry may be processed in additional regions under SCC-equivalent safeguards.
Q: Can we run BridgeAD on-prem or in our own subscription?
A: Yes. The self-hosted edition deploys via Helm chart, raw Kubernetes manifests, or Docker Compose, and runs entirely inside your subscription or data centre. SaaS and self-hosted ship from the same codebase.
Q: How is access controlled?
A: Five-tier RBAC: Viewer, Migration Operator, Tenant Admin, Platform Admin, Super Admin. MFA is mandatory for every privileged role. All sign-ins and privilege changes are recorded to the immutable audit log.
Q: Can BridgeAD integrate with our internal tooling?
A: Yes. BridgeAD exposes authenticated REST APIs and webhook notifications for job events and audit automation. Downstream integrations include ITSM, SIEM, and delivery runbooks.
Q: Do you offer a sandbox or proof-of-concept?
A: Yes. Request a scoped PoC at sales[at]bridgead[dot]in with your source & destination tenant context.

H2: Ready to plan your migration?
Tell us about your tenants and timeline. We respond within one business day.
```

> ⚠️ **Source-site typos (copy as-is for strict parity, or fix on BOTH sites):** "IMAR" should probably be "IMAP"; "sharePoint" should be "SharePoint"; "content- transfer" has a stray space; "re-guard" is unclear; "Security Migration content is streamed…" has the eyebrow text merged into the heading.

---

## 10. Verification checklist (run after fixes)

- [ ] Searching the built `dist/` folder for `uat.` returns **0** results.
- [ ] Searching `dist/` for `**` inside visible text returns **0** results.
- [ ] Searching `dist/` for `[ninja_form` returns **0** results.
- [ ] Privacy and Terms show `https://pranast.com/`, not `/`.
- [ ] Header menu matches 2.1 (labels, casing, Resources dropdown).
- [ ] Footer matches 2.2 word for word (address, phone, hours, socials, © line).
- [ ] Home has no "Our Capabilities", no "Accelerate Your Digital Transformation"/form, and no visible logo strip or "Explore All Industries"; the hero uses `image-23-scaled-1.png`.
- [ ] `/bridgead` text matches Appendix 9.7 line for line, with no invented stats.
- [ ] `/faq` matches Appendix 9.2 and has no filter/search UI text.
- [ ] `/contact` form fields are Name*, Email*, Phone, Subject, Message* and Send Message, and a test submission reaches info@pranast.com.
- [ ] Every blog post has an author box with the correct author and avatar, posts navigation and related posts, and no "Need help implementing this?" box.
- [ ] `/category/digital-transformation` and `/category/cyber-security` exist.
- [ ] All URLs in Section 7 return 200 or 301 (none return 404).
- [ ] The 7 images in Section 8 are added and used in the right places.
- [ ] A cookie consent banner is present.
- [ ] `sitemap-index.xml` and `robots.txt` exist.
