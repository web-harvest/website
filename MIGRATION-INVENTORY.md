# Website migration inventory

Status: **PARTIAL SOURCE SNAPSHOT — NOT DEPLOYABLE**.

Source repository: [web-harvest/web-harvest](https://github.com/web-harvest/web-harvest), branch `2.2.x`, source commit `e25296701225f40a0f62b56df0795e5b83290a78`.

Destination branch: `migration/website-source-inventory`.

Tracking issue: [#1 — Migrate the WebHarvest project website and deployment tooling](https://github.com/web-harvest/website/issues/1).

## Current transfer status

- 112 of 115 files under `docs/web/**` have been copied into this repository.
- Every copied file has the same Git blob SHA as the source file.
- Three PNG assets larger than 1 MB could not be retrieved through the text-only GitHub file-content interface. They are listed in `SOURCE-SNAPSHOT.md`; no placeholder files were created.
- The copied snapshot does not preserve per-file commit history. The source commit is recorded. A local `git filter-repo` / `git subtree split` extraction remains the preferred history-preserving alternative.
- No source files have been deleted or changed in the application repository.

## Candidate source paths and decisions

| Source path | Dependency finding | Decision |
|---|---|---|
| `docs/web/**` | Public website pages/assets; currently includes three large PNGs not transferred | Move all 115 files; finish binary transfer before considering snapshot complete |
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

- `scripts/generate_sitemap.py`: standard-library-only generator; scans all HTML pages and downloadable XML examples, requires an explicit canonical base URL, and writes `sitemap.xml`.
- `scripts/fix_html_examples.py`: adapted website-only repair helper for the four legacy tutorial pages; supports a non-writing `--check` mode.
- `tests/test_generate_sitemap.py` and `tests/test_fix_html_examples.py`: focused unit tests added; not yet executed in a clean local checkout.

The tests have been added but have **not yet been executed in a clean local checkout**. Do not claim CI or test success.

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

- [ ] Transfer and verify the three missing PNG assets.
- [ ] Decide whether to replace this API snapshot with a local history-preserving extraction.
- [ ] Complete file-level review of generated vs hand-maintained website content.
- [ ] Move/adapt website-only helper scripts and add tests.
- [ ] Select hosting target and canonical production URL.
- [ ] Replace old SourceForge URLs only after target URL is confirmed.
- [ ] Add clean-checkout preview and internal-link validation.
- [ ] Add deployment workflow with no embedded credentials and no destructive sync by default.
- [ ] Verify application Maven build no longer packages/depends on the moved public-site tree.
- [ ] Remove migrated website source from the application repository only in a coordinated PR after destination validation.
- [ ] Complete license, NOTICE and secrets review before either repository becomes public.

## History preservation

This API snapshot preserves exact Git blob content for the 112 transferred files, but does not preserve their commit history. The original source commit is recorded in `SOURCE-SNAPSHOT.md`. Prefer a local `git filter-repo` or `git subtree split` extraction if a local checkout is available. Do not rewrite the application repository's shared branch history.
