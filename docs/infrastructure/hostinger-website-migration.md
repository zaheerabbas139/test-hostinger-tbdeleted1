# Hostinger Website Migration: u715171369 → u797343708

> **Navigation:** [Documentation Hub](../README.md) &rsaquo; [Infrastructure](../README.md#2-infrastructure--operations) &rsaquo; **Cross-Account Migration Runbook**  
> **Related Document:** [Business to Unlimited Plan Migration Plan](business-to-unlimited-migration-plan.md)

Written for: the account owner planning the move, and anyone who runs it with them.

Status: **plan only.** Nothing has been created, imported, detached or deleted.

## 1. Context

| Item | Value |
|---|---|
| Client ID (both accounts) | 1016662687 |
| Source account | u715171369 |
| Target account | u797343708 |

### Sites on the source account (u715171369)

| Domain | Type | Location on server | Notes |
|---|---|---|---|
| pranast.com | WordPress | `/home/u715171369/domains/pranast.com/public_html` | Main site, live traffic |
| uat.pranast.com | WordPress | `.../pranast.com/public_html/uat` | Subdomain, inside the main site's folder |
| dev.pranast.com | WordPress | `.../pranast.com/public_html/dev` | Subdomain, inside the main site's folder |
| test.pranast.com | WordPress | `/home/u715171369/domains/test.pranast.com/public_html` | Addon domain |

### Sites on the target account (u797343708)

| Domain | Type | Created | Notes |
|---|---|---|---|
| deeppink-eland-272195.hostingersite.com | Other | 2026-10-26 | Probably a placeholder |

## 2. Key constraint

**A domain can be attached to only one website at a time.** While `pranast.com` and its subdomains point at u715171369, they can't be created on u797343708. The plan builds the new sites under temporary names, tests them, and then moves the domains in one controlled cutover.

## 3. Preconditions

- [ ] Confirm which sites move (all four, or a subset).
- [ ] Confirm the target account has enough hosting capacity for the sites.
- [ ] Check in hPanel whether Hostinger offers an in-panel website transfer between these accounts. If it does, it may be simpler than the steps below.
- [ ] Choose a low-traffic window for the `pranast.com` cutover.
- [ ] Confirm whether the placeholder site `deeppink-eland-272195.hostingersite.com` can be deleted. Deletion is irreversible, so confirm first.

## 4. Backup (source account)

For each site:

1. **Files:** archive the WordPress root, including `wp-content` and `wp-config.php`.
   - For uat and dev, archive from their own subfolders, not from the `pranast.com` root.
   - Example: `tar -czf pranast-com.tar.gz -C /home/u715171369/domains/pranast.com/public_html .`
2. **Database:** dump each WordPress database.
   - Example: `mysqldump --single-transaction -u USER -p DBNAME > pranast-com.sql`
   - Or use phpMyAdmin in hPanel.
3. **Cron jobs:** list them with `hosting_cron-jobs_list` for `u715171369` and save the output. Cron jobs don't move with the files.
4. **DNS records:** save the current records for each domain.
   ```bash
   dig +short NS pranast.com; dig +short A pranast.com; dig +short MX pranast.com; dig +short TXT pranast.com
   ```
   Keep `MX` and `TXT` records safe. Email and domain verification depend on them.
5. **Email:** note any mailboxes on u715171369. They do not move with the site.

Store backups outside the repository. They contain credentials and site data.

## 5. Build on the target account (under temporary names)

Create each site on a temporary `hostingersite.com` subdomain or a subdomain you control. Don't use `pranast.com` yet.

1. Find the order ID for u797343708 with `hosting_orders_list`.
2. Create each website with `hosting_websites_create` using the order ID and temporary domain.
3. Poll `hosting_websites_list-setups` with the domain every 10 to 15 seconds until `status: completed`. Setups can take a few minutes.

## 6. Import

For each WordPress site:

1. Create a database and user on u797343708 with a strong generated password. Record the name, user, password and host. Do not commit them to the repository.
2. Upload the archive and the dump to the new site.
3. Update `wp-config.php` with the new database name, user and password. Use `localhost` as the host.
4. Import the files and database with `wordpress_installations_import-website`.
5. Poll `wordpress_installations_list` with the domain until the install shows `is_valid: true`.
6. Update the home URL in the database. WordPress stores it there, so links and redirects break if it doesn't match the final domain. Use WP-CLI (`wp search-replace`) or a search-replace tool. Do this after the import, before the cutover.

## 7. Test before cutover

Test on the temporary address, or point only your own machine at the new server:

```bash
curl -sSk --resolve pranast.com:443:NEW_IP -o /dev/null -w "%{http_code}\n" https://pranast.com/
curl -sSk --resolve pranast.com:443:NEW_IP https://pranast.com/ | grep -o "TEXT FROM THE LIVE SITE"
curl -sSk --resolve pranast.com:443:NEW_IP -o /dev/null -w "%{http_code}\n" https://pranast.com/wp-login.php
```

- `-k` is expected: the certificate can only be issued after DNS moves.
- Check the home page, an inner page and `/wp-login.php`.
- Repeat for uat, dev and test.
- For a visual check in a browser, add `NEW_IP pranast.com` to your hosts file, then remove it afterwards.

Fix any problems now, while visitors still see the old site.

## 8. Cutover (visitor-facing)

This is the risky step. Expect a short gap, from minutes to a few hours, depending on DNS caching.

1. Lower the TTL on the `A` records to 300 a day in advance, if you control the DNS.
2. Remove `pranast.com` from u715171369, or detach it, so the domain is free.
3. Attach `pranast.com` to the new website on u797343708.
4. Confirm the `A` record points to the new account's IP.
   - If the nameservers are already Hostinger's, this is automatic.
5. Install SSL once the domain resolves to the new account.
6. Repeat steps 1 to 5 for uat, dev and test, with their own DNS records.
7. Keep every `MX` and `TXT` record from section 4.

## 9. Verification

- [ ] `curl -sSI https://pranast.com/` responds from the new account with `platform: hostinger`.
- [ ] Home page, inner pages and `/wp-login.php` work.
- [ ] Each subdomain works.
- [ ] Email delivers, if mailboxes were moved.
- [ ] Cron jobs recreated with `hosting_cron-jobs_create`.
- [ ] Premium plugins and licences still activate.

## 10. Rollback

- Keep the old sites and databases untouched until the new ones are verified for several days.
- To roll back, reattach the domain to u715171369 and point the `A` record back to the old IP.
- Delete the old sites only after the new ones are confirmed working. Deletion is irreversible.

## 11. Caveats

- **Email** does not move with the site. Recreate mailboxes on the new account or move them to Hostinger Mail, then update `MX` records.
- **Subdomains** need their own domain entries and DNS records on the new account.
- **Staging sites:** if uat or dev are copies of production, decide whether they should keep production database credentials.
- **Premium plugins and licences** may be tied to the domain. Check them after the move.
- **Caching** on the old and new hosts can cause brief inconsistency during the switch.

## 12. Open decisions

- Which sites move in this migration?
- Should `pranast.com` cut over now, or stay where it is while uat and dev move first?
- Should the placeholder `hostingersite.com` site be deleted?
- Is there a maintenance window for the cutover?
