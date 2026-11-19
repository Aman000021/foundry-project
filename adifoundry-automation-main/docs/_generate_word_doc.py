from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import date

out_path = r"c:\\Users\\XSPriyaGa\\Downloads\\npet-foundry-template\\docs\\Foundry_Onboarding_Deployment_Guide.docx"

doc = Document()

# Title
p = doc.add_paragraph()
r = p.add_run("Foundry Onboarding Deployment Guide")
r.bold = True
r.font.size = Pt(20)
p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

meta = doc.add_paragraph()
meta.add_run(f"Prepared on: {date.today().isoformat()}\n").bold = True
meta.add_run("Repository: npet-foundry-template")

doc.add_paragraph()

def h1(text):
    doc.add_heading(text, level=1)

def h2(text):
    doc.add_heading(text, level=2)

def bullet(text):
    doc.add_paragraph(text, style='List Bullet')

def num(text):
    doc.add_paragraph(text, style='List Number')

h1("1. Executive Overview")
doc.add_paragraph(
    "This repository provides infrastructure-as-code for onboarding use cases onto Azure AI Foundry. "
    "It orchestrates deployments through GitHub Actions and Terraform, using environment and segment-specific "
    "configuration files generated during onboarding."
)
doc.add_paragraph(
    "Deployment is separated into three Terraform stacks to improve control and state isolation:"
)
bullet("Platform stack for shared observability and security components.")
bullet("Foundry Hub stack for AI Foundry accounts (hub resources) and private endpoints.")
bullet("Agent Service stack for Foundry projects and project-level role assignments.")

h1("2. End-to-End Deployment Sequence")
num("ServiceNow / Backstage request is submitted by the use case team.")
num("Repository and environment folders are generated with onboarding-specific values.")
num("Operator triggers the manual GitHub workflow Trigger Foundry Setup.")
num("Workflow routes to reusable deployment workflows based on selected action.")
num("Terraform init, plan, and apply execute against Azure using OIDC authentication.")
num("Foundry hub resources are provisioned first, then Foundry projects are provisioned.")
num("Role assignments are applied so AD groups can manage/use project resources.")
num("Post-deployment validation is completed for access, networking, and readiness.")

h1("3. Terraform Flow and Structure")
h2("Entry points")
bullet("iac/platform-hub/main.tf")
bullet("iac/capability/foundry-hub/main.tf")
bullet("iac/capability/agent-service/main.tf")

doc.add_paragraph(
    "Each stack contains backend.tf, provider.tf, variables.tf, and main.tf. Main entry points call reusable modules "
    "under iac/modules."
)

h2("Module composition")
bullet("iac/modules/platform: platform resources such as Log Analytics, Application Insights, and Key Vault module integration.")
bullet("iac/modules/foundry-hub: AI Foundry account creation, storage container provisioning, private endpoint provisioning.")
bullet("iac/modules/agent-service: Foundry project creation and role assignments.")

h2("Terraform execution pattern in pipelines")
num("terraform init with backend-config tfvars")
num("terraform plan with var-file and selected runtime variables")
num("terraform apply using tfplan")

doc.add_paragraph(
    "Remote state is hosted on Azure Storage. Separate backend container names are used to keep platform, hub, "
    "and project state isolated."
)

h1("4. Foundry Deployment Logic")
h2("Does this repo create Foundry resource or only Foundry project?")
doc.add_paragraph("It creates both:")
num("Foundry hub resources (Microsoft.CognitiveServices/accounts)")
num("Foundry projects under those hubs (Microsoft.CognitiveServices/accounts/projects)")

h2("Foundry project creation ownership")
doc.add_paragraph(
    "Foundry project creation is implemented in module iac/modules/agent-service through azapi resource "
    "type Microsoft.CognitiveServices/accounts/projects."
)

h2("Segmentation behavior")
bullet("Segment is received from workflow input.")
bullet("Segment-specific tfvars are loaded from environments/<environment>/<segment>/...")
bullet("Segment-specific YAML config is read from iac/foundry_hub_configs/<segment>/config.yaml and iac/project_configs/<segment>/config.yaml")
bullet("Marketing is currently populated end-to-end in this repository.")
bullet("Finance scaffolding exists but requires completion before production use.")

h1("5. Inputs and Variable Sources")
h2("Typical onboarding inputs")
bullet("environment_name")
bullet("segment (for example marketing, finance)")
bullet("location (for example europe)")
bullet("resource_group_name")
bullet("solution_name")
bullet("storage_account")
bullet("storage_container_name")
bullet("shared_subnet_name")
bullet("vnet_name")
bullet("vnet_resource_group_name")
bullet("project_manager_group_id")
bullet("project_manager_user_id")

h2("Where inputs are defined")
bullet("Stack variable definitions in iac/platform-hub/variables.tf, iac/capability/foundry-hub/variables.tf, iac/capability/agent-service/variables.tf")
bullet("Environment tfvars in environments/<env>/ and segment tfvars in environments/<env>/<segment>/")
bullet("Project and hub mapping YAML files under iac/project_configs and iac/foundry_hub_configs")
bullet("Pipeline runtime inputs in .github/workflows/iac.yaml")

h1("6. Pipeline Execution Flow")
h2("How workflows run")
bullet("Top-level trigger is manual workflow_dispatch in .github/workflows/iac.yaml")
bullet("Reusable deployment workflows are workflow_call based")
bullet("Platform deployment workflow runs platform-hub then foundry-hub")
bullet("Agent capability deployment workflow runs plan and apply in separate jobs using an uploaded tfplan artifact")

h2("How variables are injected")
bullet("-var-file is used for environment and segment tfvars")
bullet("-var is used for runtime values such as project_segment and foundry_location")
bullet("GitHub Environment variables and secrets provide authentication context")

h2("Manual vs automated")
doc.add_paragraph(
    "Current orchestration is manual at trigger level (workflow_dispatch). It is not on push/schedule by default "
    "for production onboarding actions."
)

h1("7. ServiceNow Integration View")
h2("Visible in this repository")
bullet("Repository/environment generation is described as originating from ServiceNow onboarding request context")
bullet("Template placeholder files under environments/env show request-to-tfvars mapping model")
bullet("Use case documentation references Backstage and ServiceNow request links")

h2("Not visible in this repository")
bullet("No active runtime ServiceNow API integration in GitHub workflows")
bullet("No active JSON-to-Terraform transformation script executed during workflow runtime")
bullet("Commented workflow inputs (snow_ticket, explicit group IDs, project_name) indicate potential future/legacy integration points")

h1("8. Role Assignments and Access Control")
doc.add_paragraph(
    "Access control is enforced at Foundry project scope using role assignments in iac/modules/agent-service/roles.tf."
)
bullet("Role: Foundry Project Manager")
bullet("Role: Foundry User")
bullet("Principal IDs are read from project config YAML, not created in Terraform")

h1("9. Resource Creation Scope")
h2("Created by this repository")
bullet("Log Analytics Workspace")
bullet("Log Analytics Solution")
bullet("Application Insights")
bullet("Key Vault (via shared module)")
bullet("Foundry hub resources")
bullet("Foundry private endpoints")
bullet("Foundry projects")
bullet("Project role assignments")

h2("Not created by this repository")
bullet("Resource groups")
bullet("Virtual networks and subnets")
bullet("Existing storage accounts")
bullet("Azure AD groups themselves")
bullet("ServiceNow records and runtime ServiceNow orchestration")

h1("10. Important Constraints and Risks")
num("Segment readiness risk: Workflow options currently emphasize marketing while finance appears partially scaffolded.")
num("Recreation risk: Changing project_name, foundry_index, or resource_index can trigger replacement behavior.")
num("Naming dependency risk: Resource naming is derived from environment, solution, segment/index, and location maps.")
num("State integrity risk: Wrong backend config can cross-contaminate state between platform, hub, and project stacks.")
num("RBAC quality risk: Wrong AD object IDs can fail deployment or grant incorrect access.")

h1("11. Post-Onboarding Operational Steps")
num("Validate Terraform success and reconcile with Azure portal inventory.")
num("Confirm Foundry projects are accessible by intended AD groups.")
num("Validate private endpoint networking and DNS path.")
num("Validate project endpoints and application integration readiness.")
num("Establish change governance for high-impact naming/index fields.")
num("Define support ownership for enhancement, rollback, and decommissioning.")

h1("12. Key File Map")
bullet("Workflow trigger: .github/workflows/iac.yaml")
bullet("Platform deployment workflow: .github/workflows/platform-deploy.yml")
bullet("Project deployment workflow: .github/workflows/agent-capability-deploy.yml")
bullet("Platform stack: iac/platform-hub")
bullet("Foundry hub stack: iac/capability/foundry-hub")
bullet("Agent project stack: iac/capability/agent-service")
bullet("Platform module: iac/modules/platform")
bullet("Foundry hub module: iac/modules/foundry-hub")
bullet("Agent project module: iac/modules/agent-service")
bullet("Environment values: environments/dv/... and environments/env/...")
bullet("Segment/project mappings: iac/foundry_hub_configs/marketing/config.yaml and iac/project_configs/marketing/config.yaml")

doc.save(out_path)
print(out_path)
