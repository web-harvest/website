# Website migration inventory

Status: initial static inventory; not yet a completed migration.

Source repository: [web-harvest/web-harvest](https://github.com/web-harvest/web-harvest), branch `2.2.x`.

Destination repository: this repository.

Tracking issue: [#1 — Migrate the WebHarvest project website and deployment tooling](https://github.com/web-harvest/website/issues/1).

## Candidate source paths

| Source path | Initial classification | Action |
|---|---|---|
| `docs/web/**` | Public website source and generated HTML/assets | Move after identifying generated files and build inputs |
| `docs/scripts/generate_sitemap.py` | Website utility; currently hard-codes the old SourceForge canonical host | Move and parameterize canonical site URL |
| `docs/scripts/generate_plugins_index.py` | Potentially generated website output | Inspect imports, inputs and generated output before moving |
| `docs/scripts/generate_core_plugin_docs.py` | Application-coupled documentation generator | Keep with application unless proven independent |
| `docs/scripts/generate_external_plugin_docs.py` | Application-coupled documentation generator | Keep with application unless proven independent |
| `docs/scripts/generate_all_plugin_docs.py` | Orchestrator for the two application-coupled generators and index generator | Keep with application or split after dependency analysis |
| `docs/scripts/regenerate_all_with_seo.py` | Orchestrator; invokes generators and sitemap script from application-root-relative paths | Do not move unchanged; split website-only and application-coupled steps |
| `SFTP-UPLOAD-INSTRUCTIONS.md` | Legacy website deployment documentation | Replace with current hosting/deployment guide; do not carry forward SourceForge credentials/paths |
| `upload-docs.sh` | Legacy website uploader; embeds SourceForge user, host, path and SSH key path; has destructive remote sync behavior | Replace with safe, non-destructive deployment workflow after hosting target is chosen |
| `sftp-upload.batch` | Legacy SourceForge SFTP commands | Archive only if historically useful; otherwise retire after replacement |
| `publish-release.sh` | Application artifact publisher to SourceForge FRS (not website deployment) | Keep release-artifact publishing concern separate; redesign in application repo, not website repo |
| `docs/pom.xml` | Maven docs module | Keep in application repository |
| `docs/src/main/**` | Maven-coupled documentation implementation/resources | Keep unless dependency analysis proves a separable website-only part |
| `webharvest-ide/src/main/resources/webapp/**` | Embedded IDE runtime UI | Keep in application repository; not the public website |

## Findings from initial source inspection

- The existing homepage `docs/web/index.html` contains canonical, Open Graph, Twitter and structured-data URLs pointing to `https://webharvest.sourceforge.net/`.
- The homepage's download link points to SourceForge Files.
- `generate_sitemap.py` hard-codes `https://webharvest.sourceforge.net` and writes to `docs/web/sitemap.xml`.
- `regenerate_all_with_seo.py` assumes it is run from the application repository root and invokes several documentation generators. Moving it unchanged would break those path assumptions.
- `upload-docs.sh` contains hard-coded SourceForge account/host/remote path and a remote sync path that can delete destination files. It must not be repurposed as a GitHub Pages deployment script without a clean redesign.
- `publish-release.sh` publishes application JARs, not the public website. It is intentionally not classified as website tooling.
- The IDE embedded web application is separate from the public website and must not be moved as part of this migration.

## Hosting decision — still open

Do not assume GitHub Pages is the selected production host merely because the source is on GitHub. Before implementing deployment, decide and document:

1. Production hostname and DNS ownership.
2. Hosting target (GitHub Pages or another explicitly selected host).
3. Whether the existing domain is retained and how redirects/canonical URLs are handled.
4. Release/deployment trigger and protected-environment approval requirements.
5. Rollback strategy.

No workflow in this branch deploys or modifies production.

## Migration validation checklist

- [ ] Complete file-level inventory of `docs/web/**`, including generated vs hand-maintained content.
- [ ] Trace every script's inputs, outputs, imports and working-directory assumptions.
- [ ] Identify application-derived documentation generation and keep it reproducible.
- [ ] Select hosting target and canonical production URL.
- [ ] Move website source with a source-to-destination path map.
- [ ] Replace SourceForge URLs in the website only after target URL is confirmed.
- [ ] Add clean-checkout build/preview and link validation.
- [ ] Add deployment workflow with no embedded credentials and no destructive sync by default.
- [ ] Verify application Maven build no longer packages/depends on the moved public-site tree.
- [ ] Remove the migrated website source from the application repository in a coordinated PR only after this repository's PR is reviewed and accepted.
- [ ] Complete license, NOTICE and secrets review before either repository becomes public.

## History preservation

Prefer a history-preserving Git move where feasible. If repository history constraints make that impractical, record each original path and source commit in a migration manifest and retain the source commit reference. Do not rewrite the application repository's existing shared branch history.
