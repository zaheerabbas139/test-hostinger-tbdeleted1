---
title: "BridgeAD"
description: "A technology platform designed to simplify, govern and accelerate Active Directory, Microsoft Entra ID and Microsoft 365 migration programmes."
slug: "bridgead"
date: "2026-09-02"
modified: "2026-09-02"
featured_image: "/assets/images/intelligence-dashboard.webp"
---

# Intelligent Migration & Digital Transformation Platform

A technology platform designed to simplify, govern and accelerate Active Directory, Microsoft Entra ID and Microsoft 365 migration programmes.

## Product Engines

### BridgeAD Cloud Workloads
Dedicated execution engines for identity and Microsoft 365. Assess, scope, execute, reconcile, and prove Active Directory, Entra ID, Exchange, SharePoint, OneDrive, and Teams migrations — plus any-to-any mailbox moves across Gmail, IMAP, on-premises Exchange, and archives.

### BridgeAD Intelligence
Assess cloud estates, compare target designs, verify plans, govern execution, investigate failures, and prepare cited reports.

## Inside the Application

From connection selection to signed-off evidence:

1. **Select**: Choose validated source and destination connections, agents, assessed objects, users, sites, mailboxes, or servers.
2. **Preview**: Run dry-run or readiness checks, inspect collisions and unsupported items, then revise mappings or scope before writes begin.
3. **Start**: Launch a job, wave, cloud-directory run, endpoint conversion, or server operation with the options attached to that run.
4. **Control**: See the current item, processed and failed counts, warnings, throughput, and live state; pause, cancel, resume, or retry where supported.
5. **Prove**: Review exceptions and validation, record acceptance, and export reports, certificates, transcripts, and audit evidence.

## Best-Fit Programs

- **AD Forest Consolidation**: Discover, map, dry-run, and migrate directory objects through controlled waves.
- **M&A and Divestitures**: Coordinate identity scope, approvals, execution, and evidence across environments.
- **Tenant-to-Tenant Planning**: Assess identity and workload readiness before committing to content-transfer scope.
- **Regulated Self-Hosted Delivery**: Keep the control plane in customer-managed infrastructure with explicit cloud egress.
- **MSP Migration Delivery**: Standardize assessment, pilot boundaries, operator roles, and evidence across client programs.

## Security & Architecture

- **Zero Data Retained at Rest**: Customer migration content is streamed source to destination; no mailbox, file, or message body is persisted at rest in BridgeAD infrastructure.
- **Encryption in Transit**: All Microsoft Graph and Exchange traffic is TLS 1.2+; internal control plane uses TLS termination and mutual authentication.
- **Secrets Management**: Secrets are stored in Azure Key Vault (SaaS) or DPAPI-protected local stores (self-hosted). Access tokens are never logged.
- **Data Isolation**: Multi-tenant deployments enforce per-tenant data isolation via Entity Framework query filters and database-level row filters.
- **Five-Tier RBAC**: Viewer, Migration Operator, Tenant Admin, Platform Admin, and Super Admin with mandatory MFA for all privileged roles.

## Deployment Models

- **Managed Azure SaaS**: Multi-tenant managed service hosted on Azure with region-pinned data residency and per-seat or per-mailbox licensing.
- **Customer Self-Hosted**: Single-tenant deployment inside the customer's Azure subscription, Kubernetes cluster, or Docker host.
