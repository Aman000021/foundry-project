# Platform Resources Deployment Guide

Prepared on: 2026-06-23  
Repository: npet-foundry-template

## Table of Contents

1. [Overview of Deployment](#overview-of-deployment)
2. [Deployment Steps](#deployment-steps)
3. [Validation](#validation)

## Overview of Deployment

This guide covers the platform pipeline that provisions and updates shared infrastructure required for Foundry onboarding.

Pipeline and workflow scope:
- Trigger workflow: `Trigger Foundry Setup` (`.github/workflows/iac.yaml`)
- Reusable workflow: `Platform and Foundry Resource Deployment` (`.github/workflows/platform-deploy.yml`)
- Terraform stacks covered:
  - `iac/platform-hub`
  - `iac/capability/foundry-hub`

Deployment responsibilities:
- Deploys shared platform resources (for observability/security foundations).
- Deploys Foundry hub resources and related connectivity components.
- Produces plan artifacts before apply.

Important behavior to note:
- `plan` jobs always run when this pipeline is selected.
- `apply` jobs are conditionally gated by branch value `updated-foundry-deployment`.

### Key Deployment Files

| File / Directory | Purpose |
|---|---|
| `.github/workflows/iac.yaml` | Entry workflow to trigger infrastructure deployment flows. |
| `.github/workflows/platform-deploy.yml` | Reusable workflow that deploys platform and hub infrastructure. |
| `.github/workflows/agent-capability-deploy.yml` | Reusable workflow for agent capability infrastructure deployment. |
| `environments/<env>/platform.tfvars` | Environment-level platform variables used during Terraform plan/apply. |
| `environments/<env>/<segment>/foundry-hub.tfvars` | Segment-level hub variables for Foundry hub deployment. |
| `environments/<env>/<segment>/backend-config-hub.tfvars` | Terraform backend state configuration for hub stack per env/segment. |
| `iac/platform-hub/` | Terraform root stack for platform-hub resource deployment. |
| `iac/capability/foundry-hub/` | Terraform root stack for foundry-hub capability resources. |
| `iac/modules/platform/` | Shared Terraform module definitions for platform resources. |
| `iac/modules/foundry-hub/` | Shared Terraform module definitions for foundry-hub resources. |
| `iac/foundry_hub_configs/<segment>/config.yaml` | Segment onboarding/config metadata consumed by deployment flows. |

## Deployment Steps

1. Open GitHub Actions and run `Trigger Foundry Setup`.
2. In input `choice`, select one of:
   - `Deploy Dev Platform`
   - `Deploy Prod Platform`
3. Select `segment` (for example: `marketing`) and `location` (for example: `europe`).
4. The workflow calls `platform-deploy.yml` with environment, segment, and location inputs.
5. Platform stack plan executes in `iac/platform-hub`:
   - Azure login (OIDC)
   - `terraform init -backend-config=<environment>/backend-config-platform.tfvars`
   - `terraform plan -var-file=<environment>/platform.tfvars -out=tfplan`
   - Uploads `tfplan` artifact
6. Foundry hub stack plan executes in `iac/capability/foundry-hub`:
   - Azure login (OIDC)
   - `terraform init -backend-config=<environment>/<segment>/backend-config-hub.tfvars`
   - `terraform plan -var-file=<environment>/<segment>/foundry-hub.tfvars -var=project_segment -var=foundry_location -out=tfplan`
   - Uploads `tfplan` artifact
7. If branch is `updated-foundry-deployment`, manual approval jobs run.
8. If approved and branch condition matches, apply jobs execute:
   - `terraform apply tfplan` in `iac/platform-hub`
   - `terraform apply tfplan` in `iac/capability/foundry-hub`

## Validation

Use this checklist after pipeline execution:

1. Workflow validation
- Confirm both plan jobs completed successfully.
- Confirm approval jobs completed when apply is expected.
- Confirm apply jobs executed (or intentionally skipped due to branch condition).

2. Terraform artifact validation
- Verify `tfplan` artifact was uploaded and consumed by apply jobs.
- Confirm no drift/error messages in plan and apply logs.

3. Azure resource validation
- In Azure portal, verify shared platform resources are present and healthy.
- Verify Foundry hub resources are present for the selected segment.
- Verify private endpoint resources and network links are in expected state.

4. Configuration validation
- Confirm correct tfvars files were used for selected environment and segment.
- Confirm OIDC identity values (`TENANT_ID`, `SUBSCRIPTION_ID`, client IDs) resolved correctly.

5. Handover validation
- Capture deployment summary (environment, segment, location, commit/branch).
- Share outcome with agent-service deployment owner if project onboarding is next.
