# Phase 5: WordPress Decommissioning & Database Detachment Runbook

> **Navigation:** [Documentation Hub](../README.md) &rsaquo; [Architecture](../README.md#1-architecture) &rsaquo; **Phase 5 WordPress Decommissioning**  
> **Source Platform:** WordPress 6.x (PHP 8.5 + LiteSpeed + MySQL/MariaDB + Elementor)  
> **Target Platform:** Pure Static HTML/CSS via Astro 5.x SSG  
> **Hosting Environment:** Hostinger Web Root (`public_html/uat` or `public_html`)  
> **Date:** October 31, 2026  
> **Status:** Operational Runbook (Ready for Execution)  

---

## 1. Executive Summary & Objective

Phase 5 executes the controlled, zero-risk decommissioning of the legacy WordPress installation on Hostinger. By permanently removing the dynamic PHP application layer and detaching the MySQL database, the platform eliminates:
1. **100% of WordPress CVE Security Vulnerabilities:** Shuts down plugin vulnerabilities (Elementor, forms, LiteSpeed Cache), PHP deserialization exploits, and admin credential stuffing.
2. **Server Resource Overhead:** Reclaims origin RAM and CPU by terminating persistent MySQL database connections and dynamic PHP-FPM processes.
3. **Database Concurrency Bottlenecks:** Eradicates database query latency, pool exhaustion, and table lock overhead.

> [!CAUTION]
> Decommissioning must only be executed after verifying that Phase 2 (Extraction), Phase 3 (UI Components), and Phase 4 (SEO/Redirects) have been verified and built cleanly.

---

## 2. Step 1: Pre-Decommissioning Safety Archival Snapshots

Before deleting any server files or database tables, create offline archival snapshots:

### 2.1. File System Backup via Hostinger hPanel
1. Log into **Hostinger hPanel**.
2. Navigate to **Websites &rarr; Manage &rarr; Files &rarr; Backups**.
3. Select **Files backups** and click **Prepare Backup**.
4. Select the website document root (e.g., `uat.pranast.com`).
5. Download the resulting archive: `uat_pranast_files_2026-10-31.tar.gz`.
6. Store this file in secure long-term cold storage (e.g., AWS S3 glacier / enterprise Google Drive).

### 2.2. MySQL Database Dump via phpMyAdmin / SSH
1. In Hostinger hPanel, go to **Databases &rarr; Management**.
2. Identify the active WordPress database (e.g., `u715171369_uat_wp`).
3. Click **Enter phpMyAdmin**.
4. Navigate to **Export &rarr; Method: Custom &rarr; Format: SQL**.
5. Ensure `Add DROP TABLE / VIEW / PROCEDURE / FUNCTION` is checked.
6. Export the database dump: `uat_pranast_db_2026-10-31.sql`.
7. Verify file integrity and non-zero byte size locally.

---

## 3. Step 2: WordPress File System Decommissioning

### 3.1. Files to Permanently Eradicate from Web Root
Using Hostinger File Manager or SSH (`ssh -p 65002 u715171369@uat.pranast.com`):

```bash
# Navigate to web root
cd /home/u715171369/domains/pranast.com/public_html/uat/

# 1. Eradicate WordPress Core Folders
rm -rf wp-admin/
rm -rf wp-includes/
rm -rf wp-content/plugins/
rm -rf wp-content/themes/
rm -rf wp-content/cache/
rm -rf wp-content/upgrade/

# 2. Eradicate WordPress Dynamic Core Scripts
rm -f wp-config.php
rm -f wp-login.php
rm -f xmlrpc.php
rm -f wp-activate.php
rm -f wp-blog-header.php
rm -f wp-comments-post.php
rm -f wp-cron.php
rm -f wp-links-opml.php
rm -f wp-load.php
rm -f wp-mail.php
rm -f wp-settings.php
rm -f wp-signup.php
rm -f wp-trackback.php
rm -f index.php
```

### 3.2. Preservation of Media Uploads
* The `wp-content/uploads/` directory can either:
  - Be retained temporarily on the server as an emergency fallback, OR
  - Be removed once [`public/.htaccess`](../../public/.htaccess) 301 redirects all media queries to `/assets/images/`.

---

## 4. Step 3: MySQL Database Detachment & Deletion

1. In Hostinger hPanel, go to **Databases &rarr; Management**.
2. Locate the database `u715171369_uat_wp`.
3. Click the three dots (`...`) action menu next to the database and select **Delete**.
4. Confirm deletion.
5. In **Database Users**, delete the associated database user (`u715171369_uat_user`).

---

## 5. Step 4: Verification of Complete Decommissioning

Execute the following verification commands to verify no PHP execution remains:

```bash
# 1. Verify WP Login returns 410 Gone (via .htaccess / Cloudflare)
curl -I https://uat.pranast.com/wp-login.php
# Expected: HTTP/2 410 (Gone)

# 2. Verify XML-RPC returns 410 Gone
curl -I https://uat.pranast.com/xmlrpc.php
# Expected: HTTP/2 410 (Gone)

# 3. Verify Admin returns 410 Gone
curl -I https://uat.pranast.com/wp-admin/
# Expected: HTTP/2 410 (Gone)

# 4. Verify no PHP-FPM processes remain active for this domain
ps aux | grep php
```

---

## 6. Rollback & Disaster Recovery Protocol

If an unforeseen blocker requires rolling back to the legacy WordPress state prior to final DNS switchover:
1. Extract `uat_pranast_files_2026-10-31.tar.gz` back into `/public_html/uat/`.
2. Re-create the MySQL database in Hostinger hPanel.
3. Import `uat_pranast_db_2026-10-31.sql` via phpMyAdmin.
4. Update `wp-config.php` with the new database credentials.
5. Re-enable WordPress `.htaccess` permalink rules.
