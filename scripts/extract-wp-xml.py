#!/usr/bin/env python3
"""
Pranast WordPress XML to Astro Content Collections Extractor
Extracts pages, posts, case studies, and media metadata from WordPress WXR XML export.
Produces type-safe Markdown files with YAML frontmatter aligned with Phase 1 Content Schema.
"""

import os
import re
import html
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from datetime import datetime

# XML Namespaces
NS = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
}

XML_FILE = 'pranasolutionstechlimited.WordPress.2026-10-31.xml'
BASE_CONTENT_DIR = 'src/content'
PAGES_DIR = os.path.join(BASE_CONTENT_DIR, 'pages')
BLOG_DIR = os.path.join(BASE_CONTENT_DIR, 'blog')
CASE_STUDIES_DIR = os.path.join(BASE_CONTENT_DIR, 'case-studies')
MEDIA_MANIFEST = 'scripts/media-manifest.json'

def clean_text(text):
    if not text:
        return ''
    # Replace non-breaking spaces and other weird unicode whitespace
    text = text.replace('\xa0', ' ').replace('&nbsp;', ' ')
    # Decode HTML entities
    text = html.unescape(text)
    return text.strip()

def html_to_markdown(html_content, attachment_map=None):
    if not html_content:
        return ''

    # Clean HTML entities and common WP artifacts
    text = html_content
    # Remove Gutenberg comments
    text = re.sub(r'<!--\s*/?wp:[^>]*-->', '', text)

    # Remove decorative SVGs that Elementor dumps inline into lists/buttons
    text = re.sub(r'<svg[^>]*>.*?</svg>', '', text, flags=re.DOTALL)

    # Normalize internal URLs
    text = re.sub(r'https?://uat\.pranast\.com/', '/', text)
    text = re.sub(r'https?://pranast\.com/', '/', text)

    # Replace local image URLs to Astro public assets path
    def replace_img_src(match):
        img_tag = match.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag)
        if not src_match:
            return ''
        src = src_match.group(1)
        alt = alt_match.group(1) if alt_match else ''
        filename = os.path.basename(urlparse(src).path)
        # Rewrite to local assets
        local_path = f"/assets/images/{filename}"
        return f"\n\n![{alt}]({local_path})\n\n"

    text = re.sub(r'<img[^>]+>', replace_img_src, text)

    # Convert headings
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n\n# \1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n\n### \1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n\n#### \1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<h5[^>]*>(.*?)</h5>', r'\n\n##### \1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<h6[^>]*>(.*?)</h6>', r'\n\n###### \1\n\n', text, flags=re.DOTALL)

    # Convert links
    def replace_link(match):
        href = match.group(1)
        label = match.group(2).strip()
        if not label:
            return ''
        return f'[{label}]({href})'
    text = re.sub(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', replace_link, text, flags=re.DOTALL)

    # Convert bold / strong
    text = re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', r'**\1**', text, flags=re.DOTALL)
    # Convert italic / em
    text = re.sub(r'<(?:em|i)[^>]*>(.*?)</(?:em|i)>', r'*\1*', text, flags=re.DOTALL)

    # Convert unordered lists
    def replace_ul(match):
        ul_content = match.group(1)
        items = re.findall(r'<li[^>]*>(.*?)</li>', ul_content, flags=re.DOTALL)
        res = []
        for item in items:
            clean_item = re.sub(r'<[^>]+>', '', item).strip()
            clean_item = ' '.join(clean_item.split())
            if clean_item:
                res.append(f"- {clean_item}")
        return '\n\n' + '\n'.join(res) + '\n\n'

    text = re.sub(r'<ul[^>]*>(.*?)</ul>', replace_ul, text, flags=re.DOTALL)

    # Convert ordered lists
    def replace_ol(match):
        ol_content = match.group(1)
        items = re.findall(r'<li[^>]*>(.*?)</li>', ol_content, flags=re.DOTALL)
        res = []
        for idx, item in enumerate(items, 1):
            clean_item = re.sub(r'<[^>]+>', '', item).strip()
            clean_item = ' '.join(clean_item.split())
            if clean_item:
                res.append(f"{idx}. {clean_item}")
        return '\n\n' + '\n'.join(res) + '\n\n'

    text = re.sub(r'<ol[^>]*>(.*?)</ol>', replace_ol, text, flags=re.DOTALL)

    # Convert paragraphs and blockquotes
    text = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'\n\n> \1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\n\1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)

    # Strip remaining HTML tags (like div, span, button, section)
    text = re.sub(r'<[^>]+>', '', text)

    # Clean whitespace and multiple blank lines
    lines = [line.strip() for line in text.split('\n')]
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        if not line:
            if not prev_blank:
                cleaned_lines.append('')
                prev_blank = True
        else:
            cleaned_lines.append(line)
            prev_blank = False

    result = '\n'.join(cleaned_lines).strip()
    return html.unescape(result)

def extract():
    print(f"Loading {XML_FILE}...")
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    channel = root.find('channel')
    items = channel.findall('item')
    print(f"Found {len(items)} items in XML.")

    # 1. Catalog Attachments
    attachments = {} # id -> dict(url, title, filename)
    all_media_urls = []

    for item in items:
        pt = item.find('wp:post_type', NS)
        if pt is not None and pt.text == 'attachment':
            pid = item.find('wp:post_id', NS).text
            title = clean_text(item.find('title').text)
            url = item.find('wp:attachment_url', NS).text
            filename = os.path.basename(urlparse(url).path)
            attachments[pid] = {
                'id': pid,
                'title': title,
                'url': url,
                'filename': filename,
                'local_path': f"/assets/images/{filename}"
            }
            all_media_urls.append(url)

    print(f"Cataloged {len(attachments)} media attachments.")

    # Save media manifest
    os.makedirs('scripts', exist_ok=True)
    import json
    with open(MEDIA_MANIFEST, 'w') as f:
        json.dump(attachments, f, indent=2)
    print(f"Saved media manifest to {MEDIA_MANIFEST}")

    # Ensure Astro content collection directories exist
    os.makedirs(PAGES_DIR, exist_ok=True)
    os.makedirs(BLOG_DIR, exist_ok=True)
    os.makedirs(CASE_STUDIES_DIR, exist_ok=True)

    # 2. Extract Blog Posts
    posts_extracted = 0
    for item in items:
        pt = item.find('wp:post_type', NS)
        status = item.find('wp:status', NS)
        if pt is not None and pt.text == 'post' and status is not None and status.text == 'publish':
            pid = item.find('wp:post_id', NS).text
            title = clean_text(item.find('title').text)
            slug = item.find('wp:post_name', NS).text
            date_raw = item.find('wp:post_date', NS).text
            date = date_raw.split(' ')[0] if date_raw else '2026-01-01'
            modified_raw = item.find('wp:post_modified', NS).text
            modified = modified_raw.split(' ')[0] if modified_raw else date

            # Category
            categories = [c.text for c in item.findall('category') if c.get('domain') == 'category']
            # Fallback category to match Zod schema: 'Digital Transformation' or 'Cyber Security'
            category = 'Digital Transformation'
            for c in categories:
                if 'Cyber' in c or 'Security' in c:
                    category = 'Cyber Security'
                    break
                elif 'Digital' in c or 'Transformation' in c:
                    category = 'Digital Transformation'

            # Featured Image
            featured_image = '/assets/images/IT-Services.jpg'
            featured_image_alt = title
            for meta in item.findall('wp:postmeta', NS):
                k = meta.find('wp:meta_key', NS).text
                if k == '_thumbnail_id':
                    thumb_id = meta.find('wp:meta_value', NS).text
                    if thumb_id in attachments:
                        featured_image = attachments[thumb_id]['local_path']
                        featured_image_alt = attachments[thumb_id]['title'] or title

            content_raw = item.find('content:encoded', NS).text or ''
            markdown_body = html_to_markdown(content_raw, attachments)

            # Generate description / excerpt
            excerpt_el = item.find('excerpt:encoded', NS)
            excerpt = clean_text(excerpt_el.text) if excerpt_el is not None and excerpt_el.text else ''
            if not excerpt:
                # Take first non-empty paragraph
                paras = [p for p in markdown_body.split('\n\n') if p and not p.startswith('#') and not p.startswith('!')]
                excerpt = paras[0][:160] + '...' if paras else f"Insights and best practices for {title}."

            safe_title = title.replace('"', '\\"')
            safe_desc = excerpt.replace('"', '\\"').replace('\n', ' ')

            file_content = f"""---
title: "{safe_title}"
description: "{safe_desc}"
slug: "{slug}"
date: "{date}"
modified: "{modified}"
category: "{category}"
featured_image: "{featured_image}"
featured_image_alt: "{featured_image_alt.replace('"', '\\"')}"
author: "Prana Solutions Tech"
draft: false
---

{markdown_body}
"""
            post_filename = os.path.join(BLOG_DIR, f"{slug}.md")
            with open(post_filename, 'w', encoding='utf-8') as f:
                f.write(file_content)
            print(f"Extracted Blog Post [{pid}] -> {post_filename}")
            posts_extracted += 1

    # 3. Extract Case Studies & Pages
    # Target production pages:
    # 21: Home page (route '/')
    # 34: Who We are
    # 44: Cyber Security
    # 56: Digital Transformation
    # 67: Cloud & Infrastructure
    # 75: IT Support & Managed Services
    # 369: BridgeAD
    # 104: Case Studies (Hub)
    # 135: GlobalTech Solutions (Case Study)
    # 142: Premier Law Associates (Case Study)
    # 177: FAQ
    # 12: Contact
    # 3: Privacy Policy
    # 326: TERMS OF SERVICE

    legacy_page_ids = {'9', '10', '11'}
    case_study_ids = {'135', '142'}

    pages_extracted = 0
    case_studies_extracted = 0

    for item in items:
        pt = item.find('wp:post_type', NS)
        status = item.find('wp:status', NS)
        if pt is not None and pt.text == 'page' and status is not None and status.text == 'publish':
            pid = item.find('wp:post_id', NS).text
            if pid in legacy_page_ids:
                print(f"Skipping legacy starter page [{pid}] ({item.find('title').text})")
                continue

            title = clean_text(item.find('title').text)
            slug = item.find('wp:post_name', NS).text
            date_raw = item.find('wp:post_date', NS).text
            date = date_raw.split(' ')[0] if date_raw else '2026-01-01'
            modified_raw = item.find('wp:post_modified', NS).text
            modified = modified_raw.split(' ')[0] if modified_raw else date

            # Normalize slug for key pages
            if pid == '21':
                slug = 'home'
                title = 'Home'
            elif pid == '326':
                slug = 'terms-of-service'
                title = 'Terms of Service'

            content_raw = item.find('content:encoded', NS).text or ''
            markdown_body = html_to_markdown(content_raw, attachments)

            # Check for featured image
            featured_image = ''
            for meta in item.findall('wp:postmeta', NS):
                k = meta.find('wp:meta_key', NS).text
                if k == '_thumbnail_id':
                    thumb_id = meta.find('wp:meta_value', NS).text
                    if thumb_id in attachments:
                        featured_image = attachments[thumb_id]['local_path']

            paras = [p for p in markdown_body.split('\n\n') if p and not p.startswith('#') and not p.startswith('!')]
            description = paras[0][:160] + '...' if paras else f"Prana Solutions Tech - {title}"

            safe_title = title.replace('"', '\\"')
            safe_desc = description.replace('"', '\\"').replace('\n', ' ')

            # Case Study handling
            if pid in case_study_ids:
                client = 'GlobalTech Solutions' if pid == '135' else 'Premier Law Associates'
                industry = 'Technology & Cloud Infrastructure' if pid == '135' else 'Legal Services & Compliance'
                summary = (
                    "Enterprise cloud modernization & Azure infrastructure consolidation"
                    if pid == '135' else
                    "Zero Trust security and legal digital workplace compliance overhaul"
                )

                file_content = f"""---
title: "{safe_title}"
client: "{client}"
industry: "{industry}"
summary: "{summary}"
slug: "{slug}"
date: "{date}"
featured_image: "{featured_image}"
---

{markdown_body}
"""
                cs_filename = os.path.join(CASE_STUDIES_DIR, f"{slug}.md")
                with open(cs_filename, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                print(f"Extracted Case Study [{pid}] -> {cs_filename}")
                case_studies_extracted += 1
            else:
                # Standard Page handling
                file_content = f"""---
title: "{safe_title}"
description: "{safe_desc}"
slug: "{slug}"
date: "{date}"
modified: "{modified}"
featured_image: "{featured_image}"
---

{markdown_body}
"""
                page_filename = os.path.join(PAGES_DIR, f"{slug}.md")
                with open(page_filename, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                print(f"Extracted Page [{pid}] -> {page_filename}")
                pages_extracted += 1

    print("\nExtraction Summary:")
    print(f"- Blog Posts Extracted: {posts_extracted}")
    print(f"- Pages Extracted: {pages_extracted}")
    print(f"- Case Studies Extracted: {case_studies_extracted}")
    print(f"- Media Assets Cataloged: {len(attachments)}")

if __name__ == '__main__':
    extract()

