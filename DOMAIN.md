# Domain and hosting status — webharvest.org

**Status updated:** 2026-11-14  
**Decision record:** [website#4](https://github.com/web-harvest/website/issues/4)  
**Transition policy:** [website#7](https://github.com/web-harvest/website/issues/7)

## Current decision

**No production host, canonical hostname, DNS change, TLS change, redirect, or cutover is approved.**

The currently operating SourceForge-hosted public website is to remain available as the legacy/continuity endpoint during the transition. It is not a development source, upstream, mirror, or authority for code or documentation.

GitHub is the sole source of truth for application code, collaboration, CI and releases. The `web-harvest/website` repository is the canonical source for website content and publishing tooling.

The earlier GitHub Pages / `https://webharvest.org/` / `www`-to-apex proposal is superseded by the transition decision in #7. GitHub Pages remains a possible future option only; it is not selected.

## Historical DNS/HTTP observation

The read-only inspection recorded on 2026-11-14 reported:

| Check | Observed result | Classification |
|---|---|---|
| DNS nameservers | Porkbun nameservers | Historical observation |
| Apex and `www` A records | `207.207.210.107`, `207.207.210.229` | Historical observation |
| HTTP | Porkbun parked “Coming Soon” page | Historical observation |
| HTTPS | TLS handshake failed in the inspection environment | Historical observation |
| Repository deployment | Domain was not serving this repository | Historical observation |

These are a dated snapshot, not live verification and not authorization to change anything. Re-check DNS and hosting directly before any future launch decision.

## Future launch prerequisites

A separate explicit maintainer decision is required before selecting a host or canonical hostname, configuring custom domains/DNS/TLS, deploying, redirecting, or replacing public URLs.

Before that decision:
- Inventory all routes, assets, downloads, sitemap, robots directives and canonical URLs.
- Verify the candidate host supports the required routes, custom domain and HTTPS.
- Validate a staging deployment and a tested rollback path.
- Prepare an exact DNS change list; preserve MX/TXT, email and domain-verification records.
- Prepare an old-URL-to-new-URL map and SEO continuity checks.

## Guardrails

- Keep the currently operating public website available.
- Do not access, fetch, compare, synchronize, overwrite, redirect, or otherwise interact with SourceForge as part of development or migration.
- Do not change Porkbun DNS, registrar settings, hosting, TLS, GitHub Pages settings, canonical URLs, redirects, or production deployment.
- Do not infer launch approval from merging a content or source-migration PR.
- No DNS or production change without explicit maintainer approval.


## Validation workflow

The website validation workflow runs for pull requests targeting any branch, including migration and documentation branches. It is a non-deploying validation workflow; it does not publish the site or alter production hosting.
