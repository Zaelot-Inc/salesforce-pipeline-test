# 🔧 Deployment Manifests

  

- Deployment manifest generated for `{{BRANCH_SAFE}}`

- Package manifest: `{{PKG_PATH}}`

<!-- IF_DESTRUCTIVE -->- Destructive manifest: `{{DEST_PATH}}`<!-- ENDIF_DESTRUCTIVE -->

  

---

  

# 🚀 How to Deploy to Production with the `sf` CLI

  

> Replace `Prod` with your org alias.

  

## A. Validate 

As the deployment happens in PRODUCTION, we need to first validade before trying to deploy the metadata. The validation <ins>must</ins> run all local tests to be valid. 

The command will return the deployment Id, which can be used to quick deploy after it gets validated with success.

<!-- IF_NO_DESTRUCTIVE -->

Run a validation deploy:

  

```bash

sf  project  deploy  validate  --manifest {{PKG_PATH}} --target-org  Prod  --test-level  RunLocalTests  --wait  120  --json > validate.json

```

<!-- ENDIF_NO_DESTRUCTIVE -->

  

<!-- IF_DESTRUCTIVE -->

### A. Validate with destructive changes

  

>  **Note:**  `sf project deploy validate` historically doesn't accept `--pre/--post-destructive-changes`, so use a **check-only** deploy which still produces a Quick-Deployable job id.

  

```bash

sf  project  deploy  start  --manifest {{PKG_PATH}} --pre-destructive-changes {{DEST_PATH}} --check-only  --target-org  Prod  --test-level  RunLocalTests  --wait  120  --json > validate.json

```

<!-- ENDIF_DESTRUCTIVE -->

  

## B. Quick Deploy (within 10 days, unchanged org)

  

```bash

sf  project  deploy  quick  --target-org  Prod  --job-id  <deployment-id> --wait  120  --json

```