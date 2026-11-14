# Domain and hosting status — webharvest.org

**Inspected:** 2026-11-14  
**Related:** [website#1](https://github.com/web-harvest/website/issues/1), application [web-harvest#84](https://github.com/web-harvest/web-harvest/issues/84)

This document records observable DNS/HTTP facts. **No DNS, hosting, TLS, or routing changes were made.**

## Intended identity

`webharvest.org` is the intended public project identity for the migrated website in this repository.

## Observed configuration

| Check | Result | Classification |
|---|---|---|
| DNS NS | Porkbun nameservers (`curitiba` / `fortaleza` / `maceio` / `salvador`.ns.porkbun.com) | FACT |
| DNS A (`webharvest.org`, `www`) | `207.207.210.107`, `207.207.210.229` | FACT |
| HTTP `http://webharvest.org` | `200 OK`, openresty/pixie parking page titled “webharvest.org — Coming Soon”, analytics path `/parked` | FACT |
| HTTPS `https://webharvest.org` | TLS handshake failure (`sslv3 alert handshake failure`) in the inspection environment | FACT |
| This repository | Contains website source + local preview/CI validation tooling; **no production deploy workflow** | FACT |

## Implications

- The purchased domain is **not** yet serving this repository’s website content.
- Canonical hostname selection, TLS certificate issuance, and deployment approval remain **open deployment decisions**.
- Do not replace documentation/base URLs with `https://webharvest.org` as a live canonical until HTTPS and hosting serve this site successfully.
- Sitemap generation must continue to require an explicit `--base-url` / `WEBSITE_BASE_URL`.

## Non-actions (guardrails)

- No DNS record edits
- No registrar or hosting panel changes
- No production deployment
- No repository visibility change
