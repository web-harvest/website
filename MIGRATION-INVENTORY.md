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

## Internal-link audit (historical scan and follow-up)

The original clean-checkout scan recorded below identified six unique internal-link defects. That classification is **superseded** by the navigation correction recorded in commit `75732458e796a27dced88720272bfbbee5fa6c96`.

The six reported references were rechecked against the current migration branch:

| Formerly reported reference | Current result |
|---|---|
| `about.html` → `index.html#download` | Resolved: `index.html` defines `id="download"` |
| `news.html` → `index.html#download` | Resolved: `index.html` defines `id="download"` |
| `support.html` → `index.html#download` | Resolved: `index.html` defines `id="download"` |
| `documentation/getting-started.html` → `../plugins.html#extensions` | Resolved: `plugins.html` defines `id="extensions"` |
| `plugins.html` → `#database` | Resolved: `plugins.html` defines `id="database"` |
| `documentation/2.2.0/stylesheet.html` → `param.html` | Removed: no replacement page or target was invented |

The old `/documentation/2.2.0/param.html` path still returns 404 in the historical preview check, but the dangling related-processor link was removed. The full 2,261-reference scan below is historical and has **not** been rerun on the current migration head; do not present its counts as current measurements.

### Historical scan (2026-11-12; not current-head verification)

Scanned 79 HTML files and 4 CSS files. Checked 2,261 references:

| Category | Count |
|---|---:|
| HTML `href` / `src` | 2175 |
| HTML `srcset` | 86 |
| CSS `url(...)` / `@import` | 0 |
| Stylesheet links | 454 |
| Script sources | 74 |
| Image `src` + `srcset` | 172 |
| Downloadable XML `href` | 45 (all resolved at scan time) |
| Directory / trailing-slash links | 417 (all resolved at scan time) |
| Same-page anchors checked | 13 |
| Resolving / OK internal targets | 2049 |
| Intentional external links | 105 |
| Legacy SourceForge / old-host URLs | 101 (includes the now-removed checked-in sitemap; current count not recomputed) |

Legacy URLs in website content remain pending the explicit hosting/canonical decision in issue #4. Do not mass-rewrite them to `webharvest.org` before that decision.

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

## Website CI root cause (2026-11-14)

Workflow `.github/workflows/website-ci.yml` is syntactically valid and triggers on PRs targeting `main` as well as pushes to `main` / `migration/website-source-inventory`.

Runs on head `0fd46e839fed073604ee1c0230a42c413fe4cf7d` (and prior heads including `7776cdd`):

| Run | Event | Conclusion | Job steps | Runner |
|---|---|---|---:|---|
| [43581441597](https://github.com/web-harvest/website/actions/runs/43581441597) | `pull_request` | `failure` | 0 | none (`runner_id: 0`) |
| [43581437900](https://github.com/web-harvest/website/actions/runs/43581437900) | `push` | `failure` | 0 | none (`runner_id: 0`) |

Check-run annotation (exact): *"The job was not started because recent account payments have failed or your spending limit needs to be increased."*

This is a **billing/spending-limit blocker** for the private repository. It is not a test failure and does not validate or invalidate local workflow commands. Repository visibility was not changed.

### Local validation on `0fd46e8` (Python 3 via pyenv shim)

| Step | Result |
|---|---|
| `python3 -m unittest discover -s tests -v` | PASS — 14 tests |
| `python3 scripts/fix_html_examples.py --check` | PASS — 0 pages need repair |
| `python3 scripts/optimize_images.py --html-only` | PASS — 0 images / 0 HTML updates |
| `git diff --exit-code -- '*.html'` | PASS |
| Sitemap generate/parse with `https://example.invalid` | PASS — 104 URLs |
| `git diff --check` | PASS |
| `gitleaks detect` (tree + 39 reachable commits) | no leaks found |

Gitleaks was available locally for this pass; earlier audits that lacked it remain historically accurate as tooling-coverage notes for those sessions.

## Content reconciliation vs application `main` (2026-11-14, issue #3)

Comparison baselines (GitHub-only; no SourceForge):

| Tree | Ref | HEAD |
|---|---|---|
| Application `main` | `origin/main` | `3adcd9b5a22004929ca455cd781ae86d9da26b5a` |
| Website migration PR #2 tip (pre-reconcile parent) | `migration/website-source-inventory` | `bcd794108d51e905b35718c2873d7ebfea720b75` |
| Transfer snapshot | `2.2.x` | `e25296701225f40a0f62b56df0795e5b83290a78` (115 `docs/web/**` blobs) |

### Path-level summary (pre-reconcile website tip vs app `main`)

| Class | Count | Decision |
|---|---:|---|
| Identical blob SHA | 22 | RETAIN (already synced) |
| Website intentional post-snapshot edits (`app` still matches snap; website differs) | 88 | RETAIN on website (picture/WebP, nav hygiene, credential placeholders, optimized PNG, sitemap) |
| App drifted after snap; website still held snap | 4 | INCLUDE app `main` content into website |
| All three differ (`body-processor.html`) | 1 | MERGE: keep website picture/nav edits + import app 2.3.x removal callout |
| Only in app | 1 (`examples/database_example.xml`) | INCLUDE sanitized website copy (never publish original unchanged) |
| Only on website site tree | 3 (`.webp` delivery variants) | RETAIN |
| Website meta (scripts/tests/licence/docs/CI) | 23 | RETAIN (website-only / already migrated) |

### App-only / drifted paths investigated

| Source path | Source blob @ `3adcd9b` | Destination | Decision | Notes |
|---|---|---|---|---|
| `docs/web/examples/database_example.xml` | `72ada1d0dff445407159b76948cfda16c11aa56c` | `examples/database_example.xml` (sanitized; new blob) | INCLUDE (sanitized) | Original contained production-shaped placeholders (`prod_user`, `prod_password`, `analytics_user`, `analytics_pass`, `analytics-server`). Not proven live credentials. Original **not** copied. App tree untouched. |
| `docs/web/examples/basic_variables_example.xml` | `1bd0f580a64836b5065c16f8087fcace77f6715e` | `examples/basic_variables_example.xml` | INCLUDE | CDATA wrapping for template XML-like output |
| `docs/web/examples/modern_web_scraping.xml` | `0634b3f41923395ad8bde7ee3deacb6b890930b2` | `examples/modern_web_scraping.xml` | INCLUDE | Simplified `html-to-xml` usage |
| `docs/web/examples/webbrowser_plugin_demo.xml` | `be6d2c017547bf07943fa23408fa18a70862a68d` | `examples/webbrowser_plugin_demo.xml` | INCLUDE + honesty edit | App content is HTTP + `html-to-xml` + XPath, not headless browser. Website comment/index labels corrected. |
| `docs/web/examples/xquery.xml` | `4bdefd1ed542344d966a2650c68fc3b6a5040743` | `examples/xquery.xml` | INCLUDE | Result captured in variable before optional file write |
| `docs/web/documentation/2.2.0/body-processor.html` | `65d4d1a4f7452df0288686adb8ba5844baf44c7e` | `documentation/2.2.0/body-processor.html` | MERGE | Added app callout; retained website `<picture>` changes |

### Security / licensing notes for this pass

- Focused secret-pattern scan of the website candidate tree found only intentional `YOUR_*` placeholders in examples (plus H2 `sa`/empty demo defaults).
- No private keys, personal machine paths, or cloud tokens observed in changed files.
- Original `database_example.xml` values were treated as documentation-shaped, not proven live secrets. No credential rotation attempted.
- Third-party asset provenance (Font Awesome CDN, Google Fonts Inter, brand PNGs beyond owner confirmation already recorded) remains an open publication gate; project BSD does not override third-party terms.
- Application `docs/web/**` was **not** modified.

### Hosting decision prep

The earlier GitHub Pages recommendation in Issue #4 predates the continuity decision in Issue #7 and is superseded. The currently operating SourceForge-hosted public website is to remain available as the legacy endpoint during transition; GitHub Pages is only a possible future option, not an approved host. No hosting, DNS, TLS, canonical URL, redirect, or production deployment changes were made. See [Issue #4](https://github.com/web-harvest/website/issues/4) and [Issue #7](https://github.com/web-harvest/website/issues/7).


### CI coverage

Website CI now runs for pull requests targeting any branch, including this migration branch. The validation workflow is non-deploying and does not change production hosting.
