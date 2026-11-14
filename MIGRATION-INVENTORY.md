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

## Clean-checkout validation (2026-11-12)

Branch verified: `migration/website-source-inventory` at `3003642bdbe3a700f82c888fe6999242b287c4e9`, tracking `origin/migration/website-source-inventory`, clean working tree after `git fetch` + `git pull --ff-only`.

Genuine clean checkout (temporary clone, not this working tree):

```sh
git clone --branch migration/website-source-inventory --single-branch \
  https://github.com/web-harvest/website.git /tmp/website-clean-checkout-*/website
cd /tmp/website-clean-checkout-*/website
git rev-parse HEAD   # 3003642bdbe3a700f82c888fe6999242b287c4e9
```

Commands and exit codes from that checkout:

| Command | Exit code | Result |
|---|---:|---|
| `python3 -m unittest discover -s tests -v` | 0 | 14 tests, OK |
| `python3 scripts/fix_html_examples.py --check` | 0 | 0 pages need repair |
| `git diff --check` | 0 | clean |
| `python3 scripts/optimize_images.py --html-only` | 0 | 0 images / 0 HTML files changed |
| Focused `<picture>` path + loading check | 0 | 86 blocks; missing paths 0; anomalies 0 |
| `python3 -m http.server 8765 --bind 127.0.0.1` smoke (`/`, `/examples/`, `/examples/simple_test.xml`, `/documentation/2.2.0/stylesheet.html`, `/css/enterprise.css`, `/images/logo.webp`) | 0 | HTTP 200 |
| Same preview for `/documentation/2.2.0/param.html` | 0 | HTTP 404 (expected; see link audit) |

Website tests and helpers used only this repository tree. No Maven reactor, Java classes, or application-root paths were required for the clean-checkout checks. `scripts/optimize_images.py` needs Pillow with WebP only when re-encoding binaries; `--html-only` and the unit tests do not.

## Internal-link audit (clean checkout)

Scanned 79 HTML files and 4 CSS files. Checked **2261** references:

| Category | Count |
|---|---:|
| HTML `href` / `src` | 2175 |
| HTML `srcset` | 86 |
| CSS `url(...)` / `@import` | 0 (no such references in current CSS) |
| Stylesheet links | 454 |
| Script sources | 74 |
| Image `src` + `srcset` | 172 |
| Downloadable XML `href` | 45 (all resolve) |
| Directory / trailing-slash links | 417 (all resolve via `index.html`) |
| Same-page anchors checked | 13 |
| Resolving / OK internal targets | 2049 |
| Intentional external links | 105 |
| Legacy SourceForge / old-host URLs | 101 |
| Unresolved / defective internal references | 6 unique |

### Classified unresolved references

| Classification | Count | References |
|---|---:|---|
| Confirmed defect | 5 | `about.html` → `#download`; `news.html` → `#download`; `support.html` → `#download`; `documentation/getting-started.html` → `../plugins.html#external`; `plugins.html` → `documentation/2.2.0/#database` |
| Source snapshot defect | 1 | `documentation/2.2.0/stylesheet.html` → `param.html` |
| Intentional external | 105 | CDN / fonts / third-party (not defects) |
| Legacy URL awaiting hosting decision | 101 | `sourceforge.net` / `webharvest.sourceforge.net` canonicals, downloads, footers, sitemap locs |
| False positive | 0 | — |

Notes:

- `index.html` and `plugins.html` both define `id="download"`; the three confirmed `#download` failures are header CTAs on pages that never define that section. Present identically in the application `docs/web` tree.
- `plugins.html#external` and `documentation/2.2.0/#database` point at real pages that lack those fragment ids. Present identically in the application tree.
- `examples/nytimes.xml` exists, is listed in `sitemap.xml`, and returns HTTP 200, but `examples/index.html` links `improved_nytimes.xml` instead. This is not a broken href; it is an unlinked example file retained in the snapshot.
- No replacement was invented for missing targets.

### `stylesheet.html` → `param.html`

- The related-link `<a href="param.html">` is present in both this repository and application `docs/web/documentation/2.2.0/stylesheet.html`.
- No `param.html` exists under website `documentation/2.2.0/` or application `docs/web/documentation/2.2.0/`.
- Application core plugins include `HttpParamPlugin`, `CallParamPlugin`, and `XQParamPlugin` only. There is no `ParamPlugin` Java class and no `param` entry in `docs/scripts/generate_core_plugin_docs.py` `PLUGIN_NAMES`.
- `StylesheetPlugin` javadoc lists `{@code <param>}` under Related Processors; the generator emits `href="{rel}.html"` from that list, which produced the dangling `param.html` link.
- Correct target from available website source: **none**. Do not invent a page or retarget to `http-param` / `call-param` / `xq-param` without an explicit content decision outside this gate.

## Application / Maven dependency findings

Inspected a local application checkout (`web-harvest-git`) without modifying or deleting anything.

Remaining dependencies if `docs/web/**` were removed from the application repository before a coordinated cutover:

| Dependency | Finding | Decision |
|---|---|---|
| Root reactor `pom.xml` `<module>docs</module>` | Docs module still part of the Maven reactor | Keep until cutover PR |
| `docs/pom.xml` `maven-resources-plugin` `copy-web-docs` | Copies `docs/web` → `${project.build.directory}/site` during `generate-resources` | Moving `docs/web` would break this packaging step |
| `docs/src/main/assembly/docs.xml` | Packages `${project.build.directory}/site` and also `web/` as `/source` | Docs assembly ZIP/tar still requires `docs/web` |
| `upload-docs.sh` | `DOCS_DIR="docs/web"` | Legacy upload path; retire only after replacement hosting workflow |
| `docs/scripts/generate_*plugin*.py`, `regenerate_all_with_seo.py`, old sitemap/fix helpers | Read/write under `docs/web/...` and/or Java sources | Keep in application repository |
| Java modules (`webharvest-core`, IDE, etc.) | No compile/package dependency on `docs/web` files found; IDE comments mention docs styling only | Application JAR builds are not blocked by website-repo independence |
| This website repository tests/helpers | No Maven/Java/application-root path usage | Website clean-checkout validation is independent |

Conclusion: the website repository can be validated independently, but the application docs module **still packages and uploads `docs/web`**. Do not remove `docs/web` from the application repository yet.

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
- [x] Baseline clean-checkout preview and internal-link audit completed at `3003642bdbe3a700f82c888fe6999242b287c4e9`.
- [x] Six navigation/source-snapshot defects from that baseline were corrected in website commit `75732458e796a27dced88720272bfbbee5fa6c96`.
- [ ] Rerun the complete test suite, clean-checkout preview, and internal-link audit on the current PR HEAD. The non-deploying CI workflow exists, but run `43306213169` and one retry both failed before reporting any steps/logs; the failure is inconclusive and requires runner/account-level resolution.
- [ ] Add deployment workflow with no embedded credentials and no destructive sync by default.
- [ ] Verify application Maven build no longer packages/depends on the moved public-site tree (inspection shows it still does; cutover not started).
- [ ] Remove migrated website source from the application repository only in a coordinated PR after destination validation.
- [ ] Complete a full secrets/history review and file-level review of independently authored/third-party website assets before either repository becomes public. Credential-like defaults in the current website examples were replaced with explicit placeholders: Yahoo Mail (`YOUR_YAHOO_EMAIL` / `YOUR_YAHOO_PASSWORD`), REST API (`YOUR_API_KEY`), FTP (`YOUR_FTP_PASSWORD`), SMTP (`YOUR_SMTP_APP_PASSWORD`), and the legacy New York Times example (`YOUR_NYTIMES_USERNAME` / `YOUR_NYTIMES_PASSWORD`). Relevant commits: `ada6806`, `08010aa`, `ad39e85`, `b13c0b7`, `8e88aa6`. This is a targeted current-tree hygiene pass, not a complete secrets review. The old values remain in Git history; verify that they were only dummy/example values and rotate any real credentials before publication. Do not rewrite shared history without explicit approval. Project-level BSD LICENSE, upstream NOTICE and the upstream `licences/` texts have been added; this does not establish the license of every embedded asset.

### Next-phase recommendation

- Navigation defect triage is complete for the website snapshot: the five confirmed broken destinations and the `param.html` source-snapshot link were corrected in commit `75732458e796a27dced88720272bfbbee5fa6c96`. The application-side JavaDoc/generator source remains unchanged.
- **GO** for one final exact-HEAD validation pass (14 focused tests, helper checks, clean-checkout preview, and full internal-link audit), followed by a concise publication-readiness review.
- **STOP** for deployment, production hosting assumptions, repository visibility changes, merging PR #2, and deletion of application `docs/web/**`. Hosting and canonical URL are undecided; file-level third-party asset provenance and secrets review remain incomplete. Project-level BSD LICENSE and NOTICE documentation has been added.

## History preservation

This API snapshot preserves exact Git blob content for the 112 transferred files, but does not preserve their commit history. The original source commit is recorded in `SOURCE-SNAPSHOT.md`. Prefer a local `git filter-repo` or `git subtree split` extraction if a local checkout is available. Do not rewrite the application repository's shared branch history.

## Application `main` reconciliation (2026-11-14)

Coordinated with application umbrella [#84](https://github.com/web-harvest/web-harvest/issues/84) from a separate worktree on `origin/main` @ `436cd50b159a5a22fc9e040663ebd323c5cdfa52`.

| Check | Result |
|---|---|
| Application still contains `docs/web/**` | Yes (116 files under `docs/web` on that SHA) |
| Website branch still builds/tests locally | `python3 -m unittest discover -s tests -v` → 14 tests OK on this campaign tip |
| Domain `webharvest.org` | Parked Porkbun page over HTTP; HTTPS handshake failed in inspection; documented in `DOMAIN.md` |
| Delete application `docs/web/**`? | **No** — Maven docs packaging still depends on it; cutover remains blocked |
| Production deploy / DNS change? | **No** |

Expected intentional drift remains: website HTML uses `<picture>`/WebP optimizations and navigation/placeholder hygiene that the application `docs/web` tree may not yet mirror. The application tree remains the pre-cutover packaging source.

## Source file-count audit — 115 vs 116 (2026-11-14)

Git-only comparison (no SourceForge). Object type counted: regular file blobs (`100644` / `100755`); directories excluded.

| Tree | Commit | Regular files under `docs/web/**` |
|---|---|---:|
| Transfer source (`2.2.x` snapshot recorded in `SOURCE-SNAPSHOT.md`) | `e25296701225f40a0f62b56df0795e5b83290a78` | **115** |
| Application `main` (PR-coordination baseline) | `436cd50b159a5a22fc9e040663ebd323c5cdfa52` | **116** |

**Path present on `main` @ `436cd50` but absent from transfer source `e252967`:**

- `docs/web/examples/database_example.xml` (blob `72ada1d0dff445407159b76948cfda16c11aa56c`; introduced on the application line after the website snapshot, first seen via `cc2b7cf`)

**Website destination vs transfer source `e252967` (relative paths at website repo root):**

| Class | Count | Notes |
|---|---:|---|
| Source paths present in website tree | 115 | No omitted source path |
| Blob SHA identical | 26 | Unchanged content |
| Blob SHA differs (intentional) | 89 | Optimized PNG fallbacks (3); HTML `<picture>`/navigation edits; credential placeholders in examples; `css/enterprise.css`; regenerated `sitemap.xml` |
| Missing source path | 0 | — |
| Extra content-like paths not in source | 3 | `images/hero-icon.webp`, `images/logo-white-bg.webp`, `images/logo.webp` (delivery variants; originals remain in history at `5e0b98d`) |
| `examples/database_example.xml` on website | Absent | Expected: never part of the `e252967` transfer set |

**Conclusion:** The 115 figure is correct for the recorded transfer commit. The 116 figure is correct for application `main` @ `436cd50` and differs by exactly one post-snapshot file. Do not force numeric equality across those commits. Any future cutover must decide whether `database_example.xml` (and later `docs/web` changes on `main`) are imported separately.


## Navigation defect closure (2026-11-12)

Applied in commit `75732458e796a27dced88720272bfbbee5fa6c96`:

- The About, News, and Support header Download CTAs now target the existing homepage download section (`index.html#download`).
- The Getting Started extension link now targets the explicit `#extensions` section on `plugins.html`.
- The Database module documentation CTA now targets the existing Database card anchor on `plugins.html`, rather than a non-existent fragment in the core plugin index.
- Removed the dangling `param.html` related-processor link from the website snapshot. No replacement page or target was invented.

A post-commit content check confirmed all six destination references/targets. This is a source-snapshot correction: the application-side JavaDoc/generator source was not changed, so a future regeneration from the application repository must preserve this omission or correct the generator separately. Application `docs/web/**` remains untouched.

These checks validate the exact changed references only; the full 14-test suite and clean-checkout link audit must be rerun before the migration PR can be considered complete.


## Project license documentation (2026-11-12)

Added in commit `96d9e0ac95dae2c3ce6d6848a4bf13ecf37691dd`:

- Root `LICENSE`: verbatim copy of the WebHarvest BSD license from `web-harvest/web-harvest:2.2.x/licences/webharvest_licence.txt`.
- Root `NOTICE`: upstream project attribution and third-party component notice.
- `licences/`: all nine license texts present in the upstream `2.2.x/licences/` directory.
- `README.md`: states the project-level BSD license and clarifies that separate third-party asset terms remain controlling.

Evidence: the upstream `2.2.x/pom.xml` declares BSD License, and its `NOTICE` identifies the BSD license and the third-party components. This closes the missing project-level license-documentation gap. It does **not** complete a file-level review of all website images, icons, fonts, or other independently sourced material, nor the secrets review.

The full website test suite and clean-checkout link audit have not been rerun on the current branch HEAD. A non-deploying workflow was added in commit `7369fd0c74d0abc960ed8c1742c96d8e04ca1bc0`. Run `43306213169` was retried once; both attempts ended with a failed job, an empty job-step list, and `BlobNotFound` from the job-log endpoint. This is a runner/account-level execution blocker, not evidence of a failing test or a passing validation. A successful runner execution remains outstanding. The repository is still private; changing visibility is a separate owner decision and was not performed.
