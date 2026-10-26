<?php
declare(strict_types=1);

$siteName    = 'Test Hostinger Site for PranaST';
$tagline     = 'GitHub to Hostinger connectivity check';
$serverTime  = date('Y-m-d H:i:s T');
$phpVersion  = PHP_VERSION;
$serverHost  = $_SERVER['HTTP_HOST'] ?? 'unknown';
$deployedAt  = gmdate('Y-m-d H:i:s') . ' UTC';
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= htmlspecialchars($siteName, ENT_QUOTES, 'UTF-8') ?></title>
    <style>
        body {
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 0 16px;
            background: #f5f6f8;
            color: #1f2933;
            line-height: 1.5;
        }
        main {
            max-width: 720px;
            margin: 48px auto;
            background: #ffffff;
            border-radius: 8px;
            padding: 32px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        }
        h1 { margin-top: 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 16px; }
        th, td { text-align: left; padding: 8px; border-bottom: 1px solid #e4e7eb; }
        th { width: 40%; color: #52606d; font-weight: 600; }
        footer { margin-top: 24px; font-size: 0.875rem; color: #7b8794; }
    </style>
</head>
<body>
    <main>
        <h1><?= htmlspecialchars($siteName, ENT_QUOTES, 'UTF-8') ?></h1>
        <p><?= htmlspecialchars($tagline, ENT_QUOTES, 'UTF-8') ?></p>

        <table>
            <tr><th>Host</th><td><?= htmlspecialchars($serverHost, ENT_QUOTES, 'UTF-8') ?></td></tr>
            <tr><th>PHP version</th><td><?= htmlspecialchars($phpVersion, ENT_QUOTES, 'UTF-8') ?></td></tr>
            <tr><th>Server time</th><td><?= htmlspecialchars($serverTime, ENT_QUOTES, 'UTF-8') ?></td></tr>
            <tr><th>Source</th><td>GitHub repository <code>test-hostinger-tbdeleted</code></td></tr>
        </table>

        <footer>Rendered at <?= htmlspecialchars($deployedAt, ENT_QUOTES, 'UTF-8') ?></footer>
    </main>
</body>
</html>
