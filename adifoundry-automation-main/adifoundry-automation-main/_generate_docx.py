from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import date

output_path = r"c:\\Users\\XSPriyaGa\\Downloads\\npet-foundry-template\\docs\\Foundry_Onboarding_Deployment_Guide.docx"

doc = Document()

# Title
p = doc.add_paragraph()
r = p.add_run("Foundry Onboarding Deployment Guide")
r.bold = True
r.font.size = Pt(20)
p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

meta = doc.add_paragraph()
meta.add_run(f"Prepared on: {date.today().isoformat()}\\nRepository: npet-foundry-template")
meta.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

doc.add_paragraph("")

def h(text, level=1):
    doc.add_heading(text, level=level)

def para(text):
    doc.add_paragraph(text)

def bullets(items):
    for i in items:
        doc.add_paragraph(i, style='List Bullet')

def nums(items):
    for i in items:
        doc.add_paragraph(i, style='List Number')

h("1. Overview", 1)
para("This repository is an onboarding accelerator for Azure AI Foundry deployments. It manages onboarding in two layers:")
nums([
    "Platform layer (shared monitoring, observability, and security components)",
    "Foundry layer (Foundry hub resources, Foundry projects, and project-level access control)",
])
para("Deployment is triggered manually from GitHub Actions and executed with Terraform using environment- and segment-specific configurations.")

h("2. Step-by-Step Flow", 1)
nums([
    "Use case team submits request through ServiceNow/Backstage onboarding process.",
    "Repository and environment configuration files are generated from onboarding request inputs.",
    "Operator triggers the GitHub workflow: Trigger Foundry Setup.",
    "Workflow routes to reusable deployment flows (platform/hub or project deployment).",
    "Terraform runs init, plan, and apply using selected environment and segment values.",
    "Azure resources are created/updated in target resource groups and subscription.",
    "Post-deployment validation confirms project access, networking, and readiness.",
])

h("3. Terraform Flow and Structure", 1)
h("3.1 Entry Points", 2)
para("Primary Terraform stack entry points:")
bullets([
    "iac/platform-hub/main.tf",
    "iac/capability/foundry-hub/main.tf",
    "iac/capability/agent-service/main.tf",
])

h("3.2 Standard Stack Layout", 2)
para("Each stack follows a standard Terraform layout:")
bullets([
    "backend.tf: remote state backend configuration",
    "provider.tf: provider and authentication model (OIDC)",
    "variables.tf: input variable contract",
    "main.tf: module invocation and stack orchestration",
])

h("3.3 Module Organization", 2)
para("Reusable modules are organized under iac/modules:")
bullets([
    "platform",
    "foundry-hub",
    "agent-service",
])
para("Module internals include resource definitions (main.tf), data lookups (data.tf), variable contracts (variables.tf), helper locals (locals.tf), and role assignments (roles.tf for agent-service).")

h("4. Foundry Deployment Logic", 1)
h("4.1 Does the Repo Create Foundry Resource or Only Foundry Project?", 2)
para("The repository creates both:")
nums([
    "Foundry hub resources (Microsoft.CognitiveServices/accounts)",
    "Foundry projects (Microsoft.CognitiveServices/accounts/projects)",
])

h("4.2 Module Handling Foundry Project Creation", 2)
para("Foundry project creation is handled by module iac/modules/agent-service using azapi resource type Microsoft.CognitiveServices/accounts/projects.")

h("4.3 Segmentation Model (Marketing, Finance, etc.)", 2)
para("Segmentation is implemented through workflow inputs and segment-scoped files:")
bullets([
    "Workflow input: segment",
    "Segment tfvars path: environments/<environment>/<segment>/...",
    "Foundry hub config: iac/foundry_hub_configs/<segment>/config.yaml",
    "Project config: iac/project_configs/<segment>/config.yaml",
])
para("Current repository data is fully populated for marketing. Finance scaffolding exists but sample finance tfvars content is currently empty.")

h("5. Inputs and Variables", 1)
para("Expected onboarding/deployment inputs include:")
bullets([
    "environment_name",
    "segment",
    "location",
    "resource_group_name",
    "solution_name",
    "storage_account",
    "storage_container_name",
    "shared_subnet_name",
    "vnet_name",
    "vnet_resource_group_name",
    "project_manager_group_id (AD Object ID)",
    "project_manager_user_id (AD Object ID)",
])

h("5.1 Where Variables Are Defined", 2)
bullets([
    "Terraform variable contracts: variables.tf in each stack/module",
    "Environment values: environments/<env>/*.tfvars",
    "Segment values: environments/<env>/<segment>/*.tfvars",
    "Project/segment mapping: iac/project_configs and iac/foundry_hub_configs YAML files",
    "Runtime inputs: .github/workflows/iac.yaml",
])

h("6. Pipeline Execution Flow", 1)
h("6.1 Trigger Type", 2)
para("Top-level trigger is manual (workflow_dispatch). Reusable workflows use workflow_call.")

h("6.2 Terraform Execution in Pipelines", 2)
para("Platform and Foundry Resource Deployment flow:")
nums([
    "Run in iac/platform-hub",
    "terraform init with backend-config-platform.tfvars",
    "terraform plan with platform.tfvars",
    "terraform apply",
    "Run foundry-hub job after platform job",
    "Run in iac/capability/foundry-hub",
    "terraform init with backend-config-hub.tfvars",
    "terraform plan with foundry-hub.tfvars plus project_segment and foundry_location",
    "terraform apply",
])

para("Foundry Project Deployment flow:")
nums([
    "Run in iac/capability/agent-service",
    "Plan job: terraform init + terraform plan + upload tfplan artifact",
    "Apply job: download tfplan + terraform init + terraform apply",
])

h("6.3 Authentication Model", 2)
para("GitHub OIDC authentication is used with environment variables/secrets, including TENANT_ID, SUBSCRIPTION_ID, and client IDs (PLATFORM_CLIENT_ID / AGENT_CLIENT_ID).")

h("7. ServiceNow Integration (Visible in Repository)", 1)
h("7.1 What Is Visible", 2)
bullets([
    "Repository/environment artifacts are generated from request context.",
    "Template placeholders in environments/env indicate mapping from request fields to tfvars.",
    "Onboarding documentation references ServiceNow and Backstage request channels.",
])

h("7.2 What Is Not Visible", 2)
bullets([
    "No direct runtime ServiceNow API calls in GitHub workflow files.",
    "No active JSON transform script for request payload in this repository.",
    "Some potential request fields are present only as commented workflow inputs (e.g., snow_ticket, project_name, explicit group IDs).",
])

h("8. Role Assignments and Access Control", 1)
para("Project-level access control is handled via Terraform role assignments in iac/modules/agent-service/roles.tf.")
bullets([
    "Foundry Project Manager role",
    "Foundry User role",
])
para("Role principals are sourced from per-project config YAML values (group/user object IDs).")

h("9. Resource Creation Scope", 1)
h("9.1 Created by This Repository", 2)
bullets([
    "Platform observability and key management components (Log Analytics, App Insights, Key Vault module)",
    "Foundry hub resources (accounts)",
    "Private endpoints for Foundry hub resources",
    "Foundry projects",
    "Foundry project role assignments",
])

h("9.2 Not Created by This Repository", 2)
bullets([
    "Resource groups",
    "VNets and subnets",
    "Existing storage accounts",
    "Azure AD groups",
    "ServiceNow records or runtime ServiceNow orchestration",
])
para("These are expected to pre-exist or be provisioned by upstream enterprise platform processes.")

h("10. Deployment Sequence (ServiceNow to Azure)", 1)
nums([
    "ServiceNow/Backstage request submitted",
    "Repository and environment files generated",
    "GitHub workflow manually triggered",
    "Terraform Platform stack deployed",
    "Terraform Foundry hub stack deployed",
    "Terraform Foundry project stack deployed",
    "Project roles assigned and validations completed",
])

h("11. Important Constraints and Risks", 1)
nums([
    "Segment support mismatch: workflow input currently emphasizes marketing while finance is only partially scaffolded.",
    "Recreation risk: changing key identifiers (project_name, foundry_index, resource_index) can cause replacement.",
    "Naming dependency: resources are naming-derived from environment, segment/index, solution, and location mapping.",
    "State dependency: platform/hub/project use separate state backends; misconfiguration can impact deployment integrity.",
    "RBAC quality dependency: wrong AD object IDs can fail access assignment or grant access to wrong principals.",
])

h("12. Post-Onboarding Steps", 1)
nums([
    "Validate terraform apply completion and Azure resource health.",
    "Confirm Foundry project visibility and access for expected groups.",
    "Validate private endpoint connectivity and DNS behavior.",
    "Validate project endpoints and application integration readiness.",
    "Apply governance for high-impact fields (project_name, foundry_index, resource_index).",
    "Assign operations ownership for support, enhancement, rollback, and decommission lifecycle.",
])

h("13. Appendix: Key File Map", 1)
bullets([
    "Workflow trigger: .github/workflows/iac.yaml",
    "Platform workflow: .github/workflows/platform-deploy.yml",
    "Project workflow: .github/workflows/agent-capability-deploy.yml",
    "Platform stack: iac/platform-hub",
    "Foundry hub stack: iac/capability/foundry-hub",
    "Agent project stack: iac/capability/agent-service",
    "Platform module: iac/modules/platform",
    "Foundry hub module: iac/modules/foundry-hub",
    "Agent project module: iac/modules/agent-service",
    "Environment tfvars: environments/dv/... and environments/env/...",
    "Segment/project mappings: iac/foundry_hub_configs/marketing/config.yaml and iac/project_configs/marketing/config.yaml",
])

doc.save(output_path)
print(output_path)
