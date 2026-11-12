# WebHarvest Website

This repository is the canonical source for the public WebHarvest project website and its website-specific publishing tooling.

The application and IDE source code lives in [web-harvest](https://github.com/web-harvest/web-harvest).

## Migration status

The website source migration is in progress and tracked in [Issue #1](https://github.com/web-harvest/website/issues/1).

A partial source snapshot from `web-harvest/web-harvest:2.2.x` is present on the migration branch. It contains 112 of 115 files from `docs/web/**`; three large PNG assets remain to be transferred. See [SOURCE-SNAPSHOT.md](SOURCE-SNAPSHOT.md) and [MIGRATION-INVENTORY.md](MIGRATION-INVENTORY.md) for exact provenance and limitations.

The application repository remains the source of truth for any website files not yet transferred. No source files have been deleted there.

## Intended ownership

- Public website pages and assets (HTML, CSS, JavaScript, images).
- Website-specific SEO metadata, sitemap and robots configuration.
- Website-only build, preview, validation and deployment scripts.
- Website deployment documentation.

## Explicitly out of scope

- Java application modules, Maven reactor and runtime tests.
- The embedded IDE web application under `webharvest-ide/src/main/resources/webapp/`.
- Maven-coupled documentation generators that require application source or compiled classes.
- Application artifact release publishing.

## Local sitemap generation

The standard-library-only generator requires an explicit canonical URL:

```sh
python3 scripts/generate_sitemap.py --base-url https://example.invalid
```

Replace the example URL only after the production hostname has been selected. The generator also accepts `WEBSITE_BASE_URL`.

The website-only legacy example repair helper supports a safe check mode:

\`\`\`sh
python3 scripts/fix_html_examples.py --check
\`\`\`

Run its tests from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

## Deployment

No production deployment is configured. Hosting, canonical hostname, approval requirements and rollback must be decided before a deployment workflow is added.

## Security

Do not commit credentials, private keys, personal machine paths or host-specific secrets. Deployment credentials, if needed, must be supplied through protected GitHub environments/secrets or an equivalent external secret store.

## License

The applicable project and third-party licensing/NOTICE files will be added as part of the publication-readiness review. Do not assume that this repository's license is settled until that review is complete.
