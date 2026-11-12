# Source snapshot manifest

This repository's initial website content snapshot is extracted from:

- Source repository: `web-harvest/web-harvest`
- Source ref: `2.2.x`
- Source commit: `e25296701225f40a0f62b56df0795e5b83290a78`
- Source path: `docs/web/**`
- Snapshot date: 2026-11-12

## Transfer integrity

The textual website files were transferred through the Git data API. For every unchanged file, the destination Git blob SHA matches the source tree. The three large PNGs were transferred later from the local Git object database at the source commit above, after verifying each blob SHA, and then replaced in the working tree by display-sized fallbacks. The original blobs remain in commit `5e0b98d4eb85972cefe4a26eeaab06783b851107`.

| Source path | Original bytes | Source blob | Working-tree output |
|---|---:|---|---|
| `docs/web/images/hero-icon.png` | 1,509,376 | `f388b7c169fac584ed1963722eaf801586c5a390` | `images/hero-icon.png` (640×640 PNG, 225,077 bytes, `4f23dc5f8941d72d6e194eaecf1b27117285c8a5`) and `images/hero-icon.webp` (167,094 bytes) |
| `docs/web/images/logo-white-bg.png` | 1,137,188 | `8a86e8afc8e10bef92f03ccb466231456f8291d6` | `images/logo-white-bg.png` (168×168 PNG, 19,662 bytes, `aa69256eecb4999e23b2b177722438bc2e97a29d`) and `images/logo-white-bg.webp` (13,702 bytes) |
| `docs/web/images/logo.png` | 1,530,115 | `0827741939532c392f4d288af3bf80b3a2ebd491` | `images/logo.png` (168×168 PNG, 20,755 bytes, `4b018ecd1b22715302c713fee3d1e5039333703f`) and `images/logo.webp` (14,328 bytes) |

`logo.png` is the transparent flower-in-circle mark. `logo-white-bg.png` is the same mark on an opaque near-white field and is used only by `cli.html`. `hero-icon.png` is the flower without the circular badge. They are not interchangeable. No AVIF files were added. Do not delete the source copies.

## History

The copied blobs preserve exact file content and blob identity, but this API-based snapshot does **not** preserve per-file commit history. A local history-preserving extraction using `git filter-repo` or `git subtree split` remains preferred if local access is available. The source commit above is retained as the authoritative snapshot reference.

## Important limitations

- This is a source snapshot, not a production-ready deployment.
- Canonical URLs, download links, and SEO metadata still refer to the old hosting arrangement and require an explicit hosting/domain decision.
- Website-only helper scripts that have been moved are tracked in `MIGRATION-INVENTORY.md`. Application-coupled generators remain in the application repository.
- No production deployment workflow is configured.
