# Foundry Onboarding Deployment Guide

Prepared on: 2026-06-22
Repository: npet-foundry-template

## Overview

This repository is an onboarding accelerator for Azure AI Foundry deployments. It manages onboarding in two layers:

1. Platform layer (shared monitoring and security components)
2. Foundry layer
   - Foundry hub resources (AI Foundry accounts and private endpoints)
   - Foundry projects inside those hubs
   - Project-level access roles for AD groups

This deployment is triggered manually from GitHub Actions and then executed via Terraform.

## Step-by-step flow

1. Use case team submits request through ServiceNow/Backstage process.
2. Repository and environment configuration files are generated from onboarding request data.
3. Operator triggers the GitHub workflow "Trigger Foundry Setup".
4. Workflow routes to one of two reusable deployment flows:
   - Platform and Foundry Resource Deployment
   - Foundry Project Deployment
5. Terraform runs init, plan, apply using environment and segment-specific files.
6. Azure resources are provisioned in the target subscription/resource groups.
7. Post-deployment validation is performed (roles, connectivity, project readiness).

## Terraform execution explanation

### Terraform entry points

The main Terraform stack entry points are:

- iac/platform-hub/main.tf
- iac/capability/foundry-hub/main.tf
- iac/capability/agent-service/main.tf

Each stack follows a standard pattern:

- backend.tf (remote state on Azure Storage)
- provider.tf (OIDC-authenticated providers)
- variables.tf (input contract)
- main.tf (module invocation)

### Module structure

Reusable modules are under iac/modules:

- platform
- foundry-hub
- agent-service

These modules contain:

- resources (main.tf)
- data lookups (data.tf)
- variable contract (variables.tf)
- helper mappings (locals.tf)
- role assignments (roles.tf in agent-service)

### Terraform command flow in pipeline

All deployment workflows follow:

1. terraform init with backend-config tfvars
2. terraform plan with var-file and explicit -var inputs
3. terraform apply using generated tfplan

### Variable injection path

Terraform variables are injected from:

1. Workflow dispatch inputs (environment, segment, location)
2. Environment tfvars files under environments/<env>/...
3. Segment/project YAML configs under iac/project_configs and iac/foundry_hub_configs
4. GitHub Environment variables/secrets for cloud authentication

## Resources created

### Created by this repository

Platform stack creates:

- Log Analytics Workspace
- Log Analytics Solution (ApplicationInsights)
- Application Insights
- Key Vault (through shared external module)

Foundry hub stack creates:

- AI Foundry hub resources (Microsoft.CognitiveServices/accounts)
- Private Endpoints for Foundry hubs
- Foundry-related storage container

Agent service stack creates:

- Foundry projects (Microsoft.CognitiveServices/accounts/projects)
- Role assignments for project-level access

### Access control and role assignments

Project role assignments are applied using Azure role assignment resources:

- Foundry Project Manager
- Foundry User

Principal IDs are sourced from project config YAML (project manager group ID and project user group ID).

## Foundry deployment logic

### Does this repo create Foundry resource or only Foundry project?

It creates both:

1. Foundry hub resources (accounts)
2. Foundry projects under those resources

### Which module handles Foundry project creation?

Project creation is handled by module iac/modules/agent-service using azapi resource type:

- Microsoft.CognitiveServices/accounts/projects

### How segmentation is handled

Segmentation is handled by:

- workflow input: segment
- segment-specific tfvars path: environments/<env>/<location>/<segment>/...
- segment-specific config files:
  - environments/<env>/<location>/<segment>/foundry_resource_configs/config.yaml
  - environments/<env>/<location>/<segment>/project_configs/config.yaml

The DV Europe environment has `marketing` (`mkt`) and `finance` (`fin`)
segment folders. Finance uses the same per-segment file layout under
`environments/dv/europe/finance` as marketing does under
`environments/dv/europe/marketing`. Finance configuration is currently
scaffolded only for DV Europe.

Before deploying finance Foundry resources, populate the finance-specific
account reader/owner IDs and approved managed-subnet/resource entries in
`foundry-resource.tfvars` and `foundry_resource_configs/config.yaml`. Also
configure the GitHub Environment variable `fin_foundry_index` for project
deployments; do not reuse marketing access groups or resource indexes.

## Inputs and variables

Expected onboarding inputs include:

- environment_name
- project segment (for example: marketing, finance)
- location (for example: europe)
- resource_group_name
- solution_name
- storage_account
- storage_container_name
- shared_subnet_name
- vnet_name
- vnet_resource_group_name
- project_manager_group_id (AD object ID)
- project_manager_user_id (AD object ID used for user role assignment)

Variable sources:

- Terraform variable definitions: variables.tf files in stack folders
- Environment values: environments/<env>/*.tfvars and environments/<env>/<segment>/*.tfvars
- Segment/project mappings: config YAML files in iac/project_configs and iac/foundry_hub_configs
- Pipeline runtime inputs: .github/workflows/iac.yaml

## Pipeline execution flow

### Trigger mode

Pipeline is manual at top level (workflow_dispatch):

- Trigger Foundry Setup

Reusable workflows are called internally (workflow_call):

- Platform and Foundry Resource Deployment
- Foundry Project Deployment

### How terraform runs

Platform deployment workflow:

1. Runs in iac/platform-hub
2. terraform init with backend-config-platform.tfvars
3. terraform plan with platform.tfvars
4. terraform apply

Then Foundry hub deployment workflow job runs:

1. Runs in iac/capability/foundry-hub
2. terraform init with backend-config-hub.tfvars
3. terraform plan with foundry-hub.tfvars plus project_segment and foundry_location inputs
4. terraform apply

Foundry project deployment workflow:

1. Runs in iac/capability/agent-service
2. Plan job: init + plan + upload tfplan artifact
3. Apply job: download tfplan + init + apply

### Authentication model

Uses OIDC login with GitHub environment variables:

- TENANT_ID
- SUBSCRIPTION_ID
- PLATFORM_CLIENT_ID / AGENT_CLIENT_ID

## ServiceNow integration (visible scope)

### What is visible in this repository

- Repository and environment artifacts are generated from ServiceNow request context.
- Template placeholders in environments/env show how request data maps into generated tfvars.
- Onboarding document references Backstage and ServiceNow request paths.

### What is not visible here

- No direct runtime ServiceNow API call in GitHub workflows.
- No active JSON payload transformation script in this repository.
- Commented workflow inputs suggest future/legacy fields (snow ticket, explicit group IDs, project name), but they are not currently active.

## Resource creation scope

### In scope (created)

- Platform observability and key management resources
- Foundry hub resources
- Foundry projects
- Foundry project role assignments

### Out of scope (not created)

- Resource groups
- VNets and subnets
- Existing storage accounts
- AD groups themselves
- ServiceNow records or runtime ServiceNow orchestration

These are assumed to exist or be provided by upstream onboarding/platform processes.

## Deployment sequence (enterprise view)

1. ServiceNow/Backstage Request
2. Repository + environment config generation
3. Manual pipeline trigger in GitHub Actions
4. Terraform Platform deployment
5. Terraform Foundry hub deployment
6. Terraform Foundry project deployment
7. Role assignment and post-deployment validation

## Important constraints and risks

1. Segment support mismatch risk
   - Workflow options currently show marketing, while finance exists only as partial scaffolding.

2. Recreation risk from key-field changes
   - Changing foundry index, project name, or resource index can trigger resource replacement.

3. Naming dependency risk
   - Resource names are derived from environment, solution, segment/index, and location mappings.

4. State isolation dependency
   - Separate state containers are used for platform, hub, and project stacks; backend misconfiguration can impact deployment integrity.

5. RBAC data quality dependency
   - Incorrect AD object IDs in project config will break role assignment or grant wrong access.

## Post-onboarding steps

1. Validate Terraform apply output and verify all resources in Azure portal.
2. Confirm Foundry projects are visible and accessible by expected user groups.
3. Confirm private endpoint connectivity and DNS behavior for Foundry hubs.
4. Validate project API endpoints and integration readiness for application teams.
5. Establish change governance for high-impact fields:
   - project_name
   - foundry_index
   - resource_index
6. Document support ownership for lifecycle operations (enhancement, rollback, decommission).

## Appendix: Key file map

- Workflow trigger: .github/workflows/iac.yaml
- Platform workflow: .github/workflows/platform-deploy.yml
- Project workflow: .github/workflows/agent-capability-deploy.yml
- Platform stack: iac/platform-hub
- Foundry hub stack: iac/capability/foundry-hub
- Agent project stack: iac/capability/agent-service
- Platform module: iac/modules/platform
- Foundry hub module: iac/modules/foundry-hub
- Agent project module: iac/modules/agent-service
- Environment values: environments/dv/... and environments/env/...
- Segment/project mappings:
  - iac/foundry_hub_configs/marketing/config.yaml
  - iac/project_configs/marketing/config.yaml
