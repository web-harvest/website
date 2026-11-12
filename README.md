# WebHarvest Website

This repository is the canonical source for the public WebHarvest project website and its website-specific publishing tooling.

The application and IDE source code lives in [web-harvest](https://github.com/web-harvest/web-harvest).

## Migration status

The repository is being initialized as part of the website separation tracked in [Issue #1](https://github.com/web-harvest/website/issues/1).

The current website source is being audited in the application repository under `docs/web/`. No bulk copy or deployment workflow has been committed yet. Until the migration is reviewed and completed, the application repository remains the source of the existing published-site files.

## Intended ownership

- Public website pages and assets (HTML, CSS, JavaScript, images).
- Website-specific SEO metadata, sitemap and robots configuration.
- Website-only build, preview, validation and deployment scripts.
- Website deployment documentation.

## Explicitly out of scope

- Java application modules, Maven reactor and runtime tests.
- The embedded IDE web application under `webharvest-ide/src/main/resources/webapp/`.
- Maven-coupled documentation generators that require application source or compiled classes.

## Development

Build, preview and deployment commands will be documented after the source migration and build dependencies have been audited. No production deployment is configured by this bootstrap commit.

## Security

Do not commit credentials, private keys, personal machine paths or host-specific secrets. Deployment credentials, if needed, must be supplied through protected GitHub environments/secrets or an equivalent external secret store.

## License

The applicable project and third-party licensing/NOTICE files will be added as part of the publication-readiness review. Do not assume that this repository's license is settled until that review is complete.
