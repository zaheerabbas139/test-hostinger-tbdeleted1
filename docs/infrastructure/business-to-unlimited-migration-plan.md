# Business to Unlimited Hosting Migration Plan

> **Navigation:** [Documentation Hub](../README.md) &rsaquo; [Infrastructure](../README.md#2-infrastructure--operations) &rsaquo; **Hosting Plan Migration Plan**  
> **Related Document:** [Cross-Account Hostinger Migration Runbook](hostinger-website-migration.md)

**Prepared:** October 31, 2026  
**Source plan:** Business Web Hosting, `pranast.com`  
**Destination plan:** Unlimited Web Hosting, `deeppink-eland-272195.hostingersite.com`

## Important outcome

This is an internal move between two Hostinger hosting plans in the same account. The Business plan currently contains five active websites:

### WordPress websites

- `pranast.com`
- `dev.pranast.com`
- `test.pranast.com`
- `uat.pranast.com`

### Agentic mode website

- `mediumblue-armadillo-498453.hostingersite.com`

The migration method depends on the website type. Do not delete any source site until its destination copy has been tested and confirmed.

## Recommended order

1. Record the current domains, DNS records, SSL status, email arrangements, scheduled jobs, and WordPress settings.
2. Back up every website and its databases.
3. Move and test the WordPress websites first, one at a time.
4. Duplicate or recreate the Agentic mode website using its supported flow.
5. Connect the original domains only after testing the destination copies.
6. Keep the Business plan active until every site, domain, email service and backup has been verified.

## Part 1: Prepare the destination plan

1. Open **Websites** in hPanel.
2. Confirm that the Unlimited Web Hosting plan is active and has enough available storage, databases and other resources.
3. Do not create destination websites using the final production domains until the migration flow requests it. Automated WordPress migration normally creates a temporary destination copy first.
4. Confirm that the destination has the required PHP version, SSL capability and database capacity.

## Part 2: Back up everything before moving

For each WordPress site:

1. Open **Websites → Manage → Backups** for the Business plan.
2. Download a recent **Files backup**.
3. Download the matching **Database backup**.
4. Keep a separate local copy of each backup and label it with the domain and date.
5. Confirm the database used by each site from its WordPress configuration before importing or restoring anything.
6. Export important WordPress items separately if needed, including media, forms, plugin settings, theme settings and WooCommerce data.

Also record:

- DNS records and nameservers
- SSL certificates and HTTPS behavior
- Email accounts, aliases and forwarding rules
- Cron jobs and scheduled tasks
- FTP accounts and SSH keys
- CDN, cache and object-cache settings
- Payment gateways, webhooks and third-party integrations
- WordPress administrator access and active plugins

Email mailboxes, FTP accounts and SSH keys should be treated as separate items. They are not automatically included in a normal WordPress site copy.

## Part 3: Move the WordPress websites

Because Business and Unlimited are different hosting plans, the supported automated WordPress path is a **paid Automated Migration**, normally started from **Websites → Migrations**. The migration fee shown in hPanel is charged per site.

Repeat the following process for each WordPress site:

1. Open **Websites → Migrations**.
2. Start a migration for the WordPress site.
3. Select the Unlimited plan as the destination.
4. Use the temporary destination domain provided by Hostinger.
5. Complete the WordPress migration details requested by hPanel.
6. Wait for the destination copy to be prepared.
7. Test the temporary destination copy before changing the production domain.
8. Check the homepage, internal pages, images, CSS, JavaScript, forms, login, admin dashboard, plugins and database-driven features.
9. For `pranast.com`, also test checkout, orders, payment callbacks and email notifications if it is an online store.
10. When the destination is confirmed, remove the original site from Business only when hPanel requires this to release the domain.
11. Use **Connect domain** on the destination site and reconnect the original domain.
12. Recheck SSL, HTTPS redirects, DNS, forms and email delivery.

### WordPress migration sequence

Use this order unless one site is more business-critical:

1. `dev.pranast.com`
2. `uat.pranast.com`
3. `test.pranast.com`
4. `pranast.com`

Moving staging and testing sites first lets you validate the destination plan before moving the production site.

## Free manual fallback for WordPress or PHP/HTML

If you do not want to use paid Automated Migration, use the manual backup and restore method:

1. Download the website files and the correct database backup from Business.
2. Create the destination website on Unlimited.
3. Upload the files into the destination `public_html` directory.
4. Create a new database and database user on Unlimited.
5. Import the database backup using phpMyAdmin. Large databases may require an alternative import method.
6. Update the website configuration with the new database name, username and password. For WordPress, this is normally `wp-config.php`.
7. Test the site using its temporary destination address.
8. Remove the old site only after the destination is working and the backup has been verified.
9. Connect the original domain to the destination and recheck SSL and DNS.

## Part 4: Move the Agentic mode website

The Agentic mode site `mediumblue-armadillo-498453.hostingersite.com` does not use the WordPress migration path. A direct move is not supported.

Use the Agentic mode website duplication flow if it is available in hPanel:

1. Open **Websites**.
2. Find the Agentic mode website.
3. Open the three-dot menu and choose **Duplicate website**.
4. Select the Unlimited plan as the destination if hPanel offers it.
5. Review the preview domain assigned to the duplicate.
6. Check the duplicate site carefully before removing the original.
7. Reconnect the intended domain and publish the duplicate.

If hPanel does not offer Unlimited as a destination, recreate the site on the destination plan instead. Confirm all pages, forms, images, buttons, integrations and settings manually.

## Data that requires special verification

Do not assume that every service moves with the website files. Verify these separately:

- Business Email mailboxes and mailbox contents
- Email aliases, forwarders and DNS mail records
- Databases and database users
- Cron jobs
- FTP accounts and SSH keys
- SSL certificates
- CDN and cache settings
- Payment gateways and webhooks
- Contact forms and notification delivery
- Analytics, search-console and third-party integrations
- Scheduled backups
- Online-store products, orders and settings

For an AI Builder site, store content and settings may not be copied by duplication. Export or record store data before proceeding if the site contains an online store.

## Final testing checklist

For every migrated domain, confirm:

- [ ] The domain opens over HTTPS.
- [ ] The correct destination site is displayed.
- [ ] The homepage and all important pages load.
- [ ] Images, fonts, CSS and JavaScript work.
- [ ] WordPress admin login works.
- [ ] Forms submit successfully and notifications arrive.
- [ ] Database-driven features work.
- [ ] Payments, orders and webhooks work where applicable.
- [ ] Email sending and receiving work.
- [ ] Redirects and canonical URLs are correct.
- [ ] No mixed-content warnings appear.
- [ ] Search-engine settings and robots rules are correct.
- [ ] Backups are enabled on Unlimited.
- [ ] The site is using the intended PHP version.

## DNS and propagation

After connecting a domain to the destination website, DNS and caching changes may take time to propagate. Test from more than one network and confirm that the destination IP is being used before declaring the move complete.

## When to cancel or delete the old Business websites

Do not delete the Business websites at the beginning of the migration. Keep the original plan and its backups available until:

1. Every website has been tested on Unlimited.
2. Every production domain reaches the Unlimited copy.
3. Email and integrations are confirmed.
4. You have a local copy of the final backups.
5. You have confirmed that no remaining domain, mailbox or service still depends on Business.

Only then should you consider removing the old websites or changing the Business plan. The plan itself should not be cancelled until you have confirmed that all required services have moved successfully.