# Website migration inventory

Status: **PARTIAL SOURCE SNAPSHOT — NOT DEPLOYABLE**.

Source repository: [web-harvest/web-harvest](https://github.com/web-harvest/web-harvest), branch `2.2.x`, source commit `e25296701225f40a0f62b56df0795e5b83290a78`.

Destination branch: `migration/website-source-inventory`.

Tracking issue: [#1 — Migrate the WebHarvest project website and deployment tooling](https://github.com/web-harvest/website/issues/1).

## Current transfer status

- All 115 files under `docs/web/**` now have a destination representation.
- 32 files still have the same Git blob SHA as the source file.
- 83 source files differ on purpose: 79 HTML pages and `css/enterprise.css` now use `<picture>` for the logo and hero assets, and the three PNGs are display-sized fallbacks. The original PNG blobs are in commit `5e0b98d4eb85972cefe4a26eeaab06783b851107`. See `SOURCE-SNAPSHOT.md`.
- The copied snapshot does not preserve per-file commit history. The source commit is recorded. A local `git filter-repo` / `git subtree split` extraction remains the preferred history-preserving alternative.
- No source files have been deleted or changed in the application repository.

## Candidate source paths and decisions

| Source path | Dependency finding | Decision |
|---|---|---|
| `docs/web/**` | Public website pages/assets, including the three PNGs transferred from the local source object database | All 115 files are represented; image fallbacks are optimized and the original blobs stay in Git history |
| `docs/scripts/generate_sitemap.py` | Website-only, but old script hard-codes SourceForge URL and assumes application-root paths | Replaced here by `scripts/generate_sitemap.py`; requires explicit `--base-url` / `WEBSITE_BASE_URL` |
| `docs/scripts/fix_html_examples.py` | Edits only four HTML pages under `docs/web/documentation/` | Adapted and moved to `scripts/fix_html_examples.py`; now site-root-relative and supports `--check` |
| `docs/scripts/fix_javadoc_examples.py` | Edits Java source files across core/database/FTP/mail/browser/ZIP modules | Keep in application repository |
| `docs/scripts/generate_core_plugin_docs.py` | Reads Java plugin source/Javadocs from application modules | Keep in application repository |
| `docs/scripts/generate_external_plugin_docs.py` | Reads Java plugin source/Javadocs from external application modules | Keep in application repository |
| `docs/scripts/generate_plugins_index.py` | Imports `CATEGORIES` and `PLUGIN_NAMES` from `generate_core_plugin_docs.py`; not standalone | Keep for now; later extract shared plugin metadata or emit a stable generated input |
| `docs/scripts/generate_all_plugin_docs.py` | Orchestrates core/external generators and index generation | Keep in application repository |
| `docs/scripts/regenerate_all_with_seo.py` | Orchestrates app-coupled generators plus sitemap; assumes application-root cwd | Keep orchestration in app repo; invoke standalone website tooling as a separate step |
| `SFTP-UPLOAD-INSTRUCTIONS.md` | Legacy SourceForge deployment instructions | Replace after hosting target and domain are selected |
| `upload-docs.sh` | Embeds SourceForge account/host/path and destructive remote sync behavior | Retire only after replacement workflow is approved; do not reuse as-is |
| `sftp-upload.batch` | Legacy SourceForge SFTP commands | Retire after replacement workflow; do not execute |
| `publish-release.sh` | Publishes application JAR artifacts, not website files | Keep in application repo; assess separately during release-tooling cleanup |
| `docs/pom.xml`, `docs/src/main/**` | Maven docs module and app-coupled build | Keep in application repository |
| `webharvest-ide/src/main/resources/webapp/**` | Embedded IDE runtime UI | Keep in application repository |

## Current website-specific tooling

- `scripts/generate_sitemap.py`: standard-library-only generator; scans all HTML pages and downloadable XML examples, requires an explicit canonical base URL, and writes `sitemap.xml`. `lastmod` is omitted because filesystem mtimes are not stable across clean checkouts/build agents and no deterministic substitute has been established yet.
- `scripts/fix_html_examples.py`: adapted website-only repair helper for the four legacy tutorial pages; supports a non-writing `--check` mode.
- `tests/test_generate_sitemap.py`, `tests/test_fix_html_examples.py`, and `tests/test_optimize_images.py`: focused unit tests.
- `scripts/optimize_images.py`: resizes the three transferred PNGs and writes lossless WebP. Requires Pillow with WebP support only when encoding images. HTML rewriting is pure and testable; `--html-only` updates markup without re-encoding binaries. Eager loading is limited to header logos and `hero-visual` imagery; other placements are lazy.

### Picture loading classification (all 86 rewritten occurrences)

Inspected every `<picture>` block after the HTML rewrite pass:

| Placement | Count | `loading` |
|---|---:|---|
| Header logo (`logo.png` / `logo-white-bg.png` inside `<header>`) | 79 | `eager` |
| Hero imagery (`hero-icon.png` inside `.hero-visual`) | 7 | `eager` |
| Below-the-fold / other | 0 | n/a |

No below-the-fold rewritten images exist in the current snapshot, so no `loading="lazy"` attributes were required on live pages. Classification is covered by unit tests with synthetic below-the-fold markup. Homepage hero keeps `fetchpriority="high"`. Explicit width/height and existing alt text are preserved. Image binaries were not re-encoded in this follow-up.

Local validation on 2026-11-12, from this repository root, after commit `3e406a66a3149012ce0f8fc119cfe8697f99ef8f`:

- `python3 -m unittest discover -s tests -v` — 14 tests, OK (includes 7 optimizer HTML tests and sitemap `lastmod` omission/reproducibility coverage).
- `python3 scripts/fix_html_examples.py --check` — 0 pages need repair.
- `git diff --check` — clean.
- Focused `<picture>` check — 86 blocks; all referenced PNG/WebP paths resolve; classification anomalies: 0.
- `python3 scripts/optimize_images.py --html-only` — 0 HTML files changed (markup already matched the classifier).
- Image tree (`images/`) — unchanged in this follow-up.

This was a local run, not CI.

## Findings from source inspection

- The homepage `docs/web/index.html` has canonical, Open Graph, Twitter and structured-data URLs pointing to `https://webharvest.sourceforge.net/`.
- Its download link points to SourceForge Files.
- The old sitemap generator hard-coded the SourceForge canonical URL.
- `fix_html_examples.py` is website-only by its explicit four-file target list; `fix_javadoc_examples.py` modifies Java source.
- `generate_plugins_index.py` imports data from the Java-source documentation generator, so it is not currently a standalone website tool.
- `upload-docs.sh` contains a hard-coded SourceForge user, host, remote path and a destructive sync path. It must not be repurposed without redesign.
- `publish-release.sh` publishes application JARs, not the website.
- The IDE embedded web application is separate from the public website.

## Hosting decision — still open

Do not assume GitHub Pages is the selected production host merely because the source is on GitHub. Before implementing deployment, decide and document:

1. Production hostname and DNS ownership.
2. Hosting target (GitHub Pages or another explicitly selected host).
3. Whether the existing domain is retained and how redirects/canonical URLs are handled.
4. Release/deployment trigger and protected-environment approval requirements.
5. Rollback strategy.

No workflow in this branch deploys or modifies production.

## Migration validation checklist

- [x] Transfer and verify the three missing PNG assets, then keep display-sized PNG fallbacks plus lossless WebP. AVIF was not added: lossy encodes changed alpha, and lossless AVIF was larger than WebP.
- [ ] Decide whether to replace this API snapshot with a local history-preserving extraction.
- [ ] Complete file-level review of generated vs hand-maintained website content.
- [x] Move/adapt website-only helper scripts and add focused tests.
- [ ] Select hosting target and canonical production URL.
- [ ] Replace old SourceForge URLs only after target URL is confirmed.
- [ ] Add clean-checkout preview and complete internal-link validation (one pre-existing missing target remains documented).
- [ ] Add deployment workflow with no embedded credentials and no destructive sync by default.
- [ ] Verify application Maven build no longer packages/depends on the moved public-site tree.
- [ ] Remove migrated website source from the application repository only in a coordinated PR after destination validation.
- [ ] Complete license, NOTICE and secrets review before either repository becomes public.

## History preservation

This API snapshot preserves exact Git blob content for the 112 transferred files, but does not preserve their commit history. The original source commit is recorded in `SOURCE-SNAPSHOT.md`. Prefer a local `git filter-repo` or `git subtree split` extraction if a local checkout is available. Do not rewrite the application repository's shared branch history.
