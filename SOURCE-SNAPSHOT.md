# Source snapshot manifest

This repository's initial website content snapshot is extracted from:

- Source repository: `web-harvest/web-harvest`
- Source ref: `2.2.x`
- Source commit: `e25296701225f40a0f62b56df0795e5b83290a78`
- Source path: `docs/web/**`
- Snapshot date: 2026-11-12

## Transfer integrity

The textual website files were transferred through the Git data API. For every transferred file, the destination Git blob SHA was checked against the source tree's blob SHA. This proves byte-for-byte identity for those files.

The GitHub file-content connector returned empty content for three large PNG files (all larger than 1 MB), so they are intentionally not represented by placeholders:

| Source path | Size | Source blob |
|---|---:|---|
| `docs/web/images/hero-icon.png` | 1,509,376 bytes | `f388b7c169fac584ed1963722eaf801586c5a390` |
| `docs/web/images/logo-white-bg.png` | 1,137,188 bytes | `8a86e8afc8e10bef92f03ccb466231456f8291d6` |
| `docs/web/images/logo.png` | 1,530,115 bytes | `0827741939532c392f4d288af3bf80b3a2ebd491` |

These assets must be transferred from a local Git clone (or another binary-safe path) before this snapshot can be considered complete. Do not delete the source copies.

## History

The copied blobs preserve exact file content and blob identity, but this API-based snapshot does **not** preserve per-file commit history. A local history-preserving extraction using `git filter-repo` or `git subtree split` remains preferred if local access is available. The source commit above is retained as the authoritative snapshot reference.

## Important limitations

- This is a source snapshot, not a production-ready deployment.
- Canonical URLs, download links, and SEO metadata still refer to the old hosting arrangement and require an explicit hosting/domain decision.
- Website scripts have not yet been moved; their dependencies are tracked in `MIGRATION-INVENTORY.md`.
- No production deployment workflow is configured.
