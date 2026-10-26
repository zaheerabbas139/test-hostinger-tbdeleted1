# test-hostinger-tbdeleted

A minimal PHP website used to test GitHub → Hostinger connectivity.

## Contents

- `index.php` — landing page showing basic site information and server details (PHP version, server time, host).
- `.gitignore` — ignores OS files, editor folders, dependencies, and local env files.

## Deploying to Hostinger

1. In hPanel, open **Websites → Git** (or the Git integration for your site) and connect this repository.
2. Set the branch to `main` and the deploy target to the site's `public_html` directory.
3. Push a commit to `main`; the site should serve `index.php` at your domain.

## Local preview

```bash
php -S localhost:8000
```

Then open http://localhost:8000.
