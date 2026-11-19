# Agent Service Deployment Guide

Prepared on: 2026-06-23  
Repository: npet-foundry-template

## Table of Contents

1. [Overview of Deployment](#overview-of-deployment)
2. [Deployment Steps](#deployment-steps)
3. [Validation](#validation)

## Overview of Deployment

This guide covers the agent-service pipeline that provisions Foundry projects and project-level access control.

Pipeline and workflow scope:
- Trigger workflow: `Trigger Foundry Setup` (`.github/workflows/iac.yaml`)
- Reusable workflow: `Foundry Project Deployment` (`.github/workflows/agent-capability-deploy.yml`)
- Terraform stack covered:
  - `iac/capability/agent-service`

Deployment responsibilities:
- Creates or updates Foundry project resources.
- Applies project-level role assignments.
- Uses segment-scoped and environment-scoped Terraform variable files.

Important behavior to note:
- `plan` job always runs when this pipeline is selected.
- `apply` job is conditionally gated by branch value `updated-foundry-deployment`.

## Deployment Steps

1. Open GitHub Actions and run `Trigger Foundry Setup`.
2. In input `choice`, select one of:
   - `Deploy Dev Agent Service`
   - `Deploy Prod Agent Service`
3. Select `segment` (for example: `marketing` or `operations`) and `location` (for example: `europe`).
4. The workflow calls `agent-capability-deploy.yml` with environment, segment, and location inputs.
5. Plan job executes in `iac/capability/agent-service`:
   - Azure login (OIDC)
   - `terraform init -backend-config=<environment>/<segment>/backend-config-project.tfvars`
   - `terraform plan -var-file=<environment>/<segment>/agent-service.tfvars -var=project_segment -var=foundry_location -out=tfplan`
   - Uploads `tfplan` artifact
6. If branch is `updated-foundry-deployment`, manual approval job runs.
7. If approved and branch condition matches, apply job executes:
   - Downloads `tfplan`
   - Runs `terraform init` with project backend config
   - Runs `terraform apply tfplan`

## Validation

Use this checklist after pipeline execution:

1. Workflow validation
- Confirm `plan` job succeeded.
- Confirm manual approval job completed when apply is expected.
- Confirm `apply` job executed (or intentionally skipped due to branch condition).

2. Terraform output validation
- Verify `tfplan` artifact was generated and consumed by apply.
- Confirm plan/apply logs show expected project resources and no unresolved errors.

3. Azure resource validation
- Verify Foundry project resources exist under expected Foundry hub.
- Verify IAM role assignments are present at project scope for configured principals.

4. Configuration validation
- Confirm project config and tfvars inputs align with selected segment/environment.
- Confirm OIDC identity variables resolved correctly for the run.

5. Access validation
- Validate that project manager and project user groups can access the project as expected.
- Record project endpoint/readiness status for onboarding handover.
