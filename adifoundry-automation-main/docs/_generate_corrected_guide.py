#!/usr/bin/env python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def shade_cell(cell, color):
    """Apply background color to cell"""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color)
    cell._element.get_or_add_tcPr().append(shading_elm)

doc = Document()

# Title Page
title = doc.add_paragraph()
title_run = title.add_run("FOUNDRY ONBOARDING")
title_run.font.size = Pt(32)
title_run.bold = True
title_run.font.color.rgb = RGBColor(0, 51, 102)
title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
title.paragraph_format.space_after = Pt(12)

subtitle = doc.add_paragraph()
subtitle_run = subtitle.add_run("Deployment and Configuration Guide")
subtitle_run.font.size = Pt(20)
subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
subtitle.paragraph_format.space_after = Pt(24)

doc.add_paragraph()

meta = doc.add_paragraph()
meta_run = meta.add_run("Repository: npet-foundry-template")
meta_run.font.size = Pt(11)
meta.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
meta.paragraph_format.space_after = Pt(3)

meta2 = doc.add_paragraph()
meta2_run = meta2.add_run("Version: Final (Aligned to Platform Architecture)")
meta2_run.font.size = Pt(11)
meta2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
meta2.paragraph_format.space_after = Pt(3)

meta3 = doc.add_paragraph()
meta3_run = meta3.add_run("Date: 2026-06-22")
meta3_run.font.size = Pt(11)
meta3.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

doc.add_page_break()

# Helper functions
def h1(text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(18)
    h.paragraph_format.space_after = Pt(10)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 51, 102)

def h2(text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(8)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 102, 153)

def h3(text):
    h = doc.add_heading(text, level=3)
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(6)

def para(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    return p

def emphasis(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(8)
    for run in p.runs:
        run.bold = True
    return p

def bullet(text, level=0):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.5 + level*0.25)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    return p

def num_item(text):
    p = doc.add_paragraph(text, style='List Number')
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15

def box_text(title, text):
    """Create a highlighted box with title and text"""
    p = doc.add_paragraph()
    p_format = p.paragraph_format
    p_format.left_indent = Inches(0.3)
    p_format.right_indent = Inches(0.3)
    p_format.space_before = Pt(6)
    p_format.space_after = Pt(6)
    
    # Add border
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for border_name in ('top', 'left', 'bottom', 'right'):
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '12')
        border.set(qn('w:space'), '1')
        border.set(qn('w:color'), '3366CC')
        pBdr.append(border)
    pPr.append(pBdr)
    
    # Add shading
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), 'E8F0F8')
    pPr.append(shading)
    
    run = p.add_run(f"{title}\n")
    run.bold = True
    run.font.color.rgb = RGBColor(0, 51, 102)
    p.add_run(text)

# ===== SECTION 1: OVERVIEW =====
h1("1. OVERVIEW")

para("This repository provides Infrastructure-as-Code (Terraform) for onboarding use cases onto Microsoft Azure AI Foundry. It automates the creation of Foundry projects and the assignment of access permissions to your teams.")

para("The repository implements a two-stage deployment model:")

bullet("STAGE 1 — PLATFORM DEPLOYMENT (one-time, already complete)")
bullet("Creates shared platform infrastructure (observability, security)", level=1)
bullet("Creates Foundry hub resources (AI Foundry accounts)", level=1)
bullet("Status: Already deployed and managed separately", level=1)

bullet("STAGE 2 — ONBOARDING DEPLOYMENT (per use case, repeatable)")
bullet("Creates Foundry projects under pre-existing hubs", level=1)
bullet("Assigns project-level access roles to AD groups", level=1)
bullet("Status: Triggered for each new use case", level=1)

box_text(
    "CRITICAL PRECONDITION:",
    "Platform infrastructure and Foundry hub resources are PRE-EXISTING when onboarding begins. Onboarding does NOT create or modify Foundry hubs. This design prevents accidental deletion of shared infrastructure."
)

h1("2. SIMPLIFIED WORKING MODEL")

para("For business stakeholders, here is how the system works:")

box_text(
    "The Five-Step Onboarding Journey:",
    "Step 1: Your team requests a Foundry project via ServiceNow\n" +
    "Step 2: Infrastructure team configures the project details and settings\n" +
    "Step 3: Infrastructure team clicks a button in GitHub to deploy\n" +
    "Step 4: Terraform automatically creates your project and sets permissions\n" +
    "Step 5: Your team logs in and starts using the project"
)

para("What you need to provide:")
bullet("Project name (e.g., 'customer-analytics-platform')")
bullet("Which team owns the project (marketing, finance, etc.)")
bullet("Who manages the project (Project Manager AD group)")
bullet("Who uses the project (Users AD group)")

para("What gets created automatically:")
bullet("One Foundry project with a unique Azure identifier")
bullet("Access permissions configured for your teams")
bullet("Network connectivity through private endpoints")
bullet("Monitoring and logging integration")

para("What is NOT created:")
bullet("Resource groups (pre-existing)")
bullet("Virtual networks or subnets (pre-existing)")
bullet("Azure AD groups (must already exist)")
bullet("Foundry hub resources (already deployed)")

h1("3. END-TO-END DEPLOYMENT FLOW")

h2("PHASE 1: REQUEST AND CONFIGURATION")

h3("Step 1: Use Case Team Submits Request")
bullet("Team submits onboarding request through ServiceNow or Backstage")
bullet("Request includes:")
doc.add_paragraph("Project name and business purpose", style='List Bullet 2')
doc.add_paragraph("Segment/cost center (marketing, finance, etc.)", style='List Bullet 2')
doc.add_paragraph("Team AD group for Project Manager role", style='List Bullet 2')
doc.add_paragraph("Team AD group for User access role", style='List Bullet 2')
doc.add_paragraph("Target environment (development, staging, production)", style='List Bullet 2')
doc.add_paragraph("Deployment region", style='List Bullet 2')

h3("Step 2: Infrastructure Team Generates Configuration")
para("Central onboarding platform processes the request:")
bullet("Creates a new GitHub repository from this template")
bullet("Populates environment configuration files (tfvars) with team inputs")
bullet("Populates project configuration YAML with project metadata")
bullet("Configuration includes:")
doc.add_paragraph("Project name (for Foundry resource naming)", style='List Bullet 2')
doc.add_paragraph("AD group object IDs (for access control)", style='List Bullet 2')
doc.add_paragraph("Which Foundry hub this project belongs to", style='List Bullet 2')
doc.add_paragraph("Network settings (subnets for private endpoints)", style='List Bullet 2')

para("Infrastructure team receives GitHub repository link and reviews configuration.")

h2("PHASE 2: DEPLOYMENT EXECUTION")

h3("Step 3: Trigger GitHub Deployment Pipeline")
bullet("Infrastructure operator opens GitHub Actions in the repository")
bullet("Selects 'Run Workflow' on the Foundry Project Deployment")
bullet("Workflow inputs:")
doc.add_paragraph("Environment: dv (development), pp (pre-prod), pr (production)", style='List Bullet 2')
doc.add_paragraph("Segment: marketing, finance, or other", style='List Bullet 2')
doc.add_paragraph("Location: europe or other region", style='List Bullet 2')
bullet("Workflow begins and connects to Azure")

h3("Step 4: Terraform Initialization")
bullet("Terraform reads configuration files from repository")
bullet("Terraform downloads required Terraform modules and Azure providers")
bullet("Terraform connects to Azure remote state backend (Azure Storage account)")
bullet("State files are stored in separate containers:")
doc.add_paragraph("tfstateproject: State for this onboarding project", style='List Bullet 2')
doc.add_paragraph("(tfstate and tfstatehub are for platform deployment only)", style='List Bullet 2')

h3("Step 5: Terraform Plan and Validation")
bullet("Terraform plan: Generates a detailed list of resources to be created")
bullet("Output shows:")
doc.add_paragraph("Project resource details", style='List Bullet 2')
doc.add_paragraph("Role assignment details", style='List Bullet 2')
doc.add_paragraph("Network configuration", style='List Bullet 2')
bullet("Infrastructure team reviews the plan")
bullet("Team approves or rejects the changes in GitHub")

h3("Step 6: Terraform Apply - Project Creation")
bullet("If approved, Terraform creates the Foundry project")
bullet("Project details:")
doc.add_paragraph("Name: glbl-<environment>-<projectname>-prj-cgs", style='List Bullet 2')
doc.add_paragraph("Type: Microsoft.CognitiveServices/accounts/projects", style='List Bullet 2')
doc.add_paragraph("Parent: Pre-existing Foundry hub", style='List Bullet 2')
doc.add_paragraph("Status: Immediately ready for use", style='List Bullet 2')

h3("Step 7: Terraform Apply - Role Assignment")
bullet("Terraform creates TWO role assignments at the project scope:")
bullet("Role 1: Foundry Project Manager", level=1)
doc.add_paragraph("Assigned to: Project Manager AD group", style='List Bullet 3')
doc.add_paragraph("Permissions: Manage project, configure settings", style='List Bullet 3')
bullet("Role 2: Foundry User", level=1)
doc.add_paragraph("Assigned to: User/Team AD group", style='List Bullet 3')
doc.add_paragraph("Permissions: Use project, create models, run experiments", style='List Bullet 3')
bullet("Result: Team members gain immediate access via their AD accounts")

h3("Step 8: Deployment Validation")
bullet("Terraform apply completes and reports success")
bullet("GitHub workflow logs show all resources created")
bullet("Infrastructure team verifies:")
doc.add_paragraph("Project visible in Azure portal", style='List Bullet 2')
doc.add_paragraph("Role assignments correctly configured", style='List Bullet 2')
doc.add_paragraph("Network endpoints accessible", style='List Bullet 2')

h1("4. TERRAFORM EXECUTION EXPLAINED")

h2("THREE TERRAFORM STACKS (NOT ALL USED FOR ONBOARDING)")

h3("Stack 1: PLATFORM-HUB (Not Used During Onboarding)")
para("Purpose: Create shared platform infrastructure (one-time)")
bullet("Location in repo: iac/platform-hub")
bullet("Execution: ONLY via Platform Deployment pipeline")
bullet("Creates:")
doc.add_paragraph("Log Analytics Workspace (monitoring)", style='List Bullet 2')
doc.add_paragraph("Application Insights (observability)", style='List Bullet 2')
doc.add_paragraph("Key Vault (secrets management)", style='List Bullet 2')
bullet("State stored in: tfstate container")
bullet("Status during onboarding: Already complete")

h3("Stack 2: FOUNDRY-HUB (Not Used During Onboarding)")
para("Purpose: Create Foundry hub resources (one-time per segment)")
bullet("Location in repo: iac/capability/foundry-hub")
bullet("Execution: ONLY via Platform Deployment pipeline")
bullet("Creates:")
doc.add_paragraph("Foundry hub resources (AI Foundry accounts)", style='List Bullet 2')
doc.add_paragraph("Private endpoints for secure connectivity", style='List Bullet 2')
doc.add_paragraph("Storage containers for hub data", style='List Bullet 2')
bullet("State stored in: tfstatehub container")
bullet("Status during onboarding: Already complete and pre-existing")
box_text(
    "KEY POINT:",
    "When onboarding runs, the Foundry hub ALREADY EXISTS. Onboarding finds it and uses it as the parent for the new project. Onboarding never creates or modifies the hub."
)

h3("Stack 3: AGENT-SERVICE (USED FOR ONBOARDING)")
para("Purpose: Create Foundry projects and role assignments (repeatable per use case)")
bullet("Location in repo: iac/capability/agent-service")
bullet("Execution: Triggered via Onboarding Deployment pipeline")
bullet("Creates:")
doc.add_paragraph("Foundry projects (Microsoft.CognitiveServices/accounts/projects)", style='List Bullet 2')
doc.add_paragraph("Project Manager role assignment", style='List Bullet 2')
doc.add_paragraph("User role assignment", style='List Bullet 2')
bullet("Does NOT create:")
doc.add_paragraph("Foundry hubs (hub is pre-existing)", style='List Bullet 2')
doc.add_paragraph("Resource groups (pre-existing)", style='List Bullet 2')
doc.add_paragraph("Virtual networks (pre-existing)", style='List Bullet 2')
doc.add_paragraph("AD groups (pre-existing)", style='List Bullet 2')
bullet("State stored in: tfstateproject container")
bullet("Frequency: Once per new project")

h2("HOW STACKS WORK TOGETHER")

para("Pipeline Execution Order:")

num_item("PLATFORM DEPLOYMENT (Stage 1) — Runs once:")
doc.add_paragraph("Stack 1: Platform Hub → Creates infra", style='List Bullet 2')
doc.add_paragraph("Stack 2: Foundry Hub → Creates hub", style='List Bullet 2')

num_item("ONBOARDING DEPLOYMENT (Stage 2) — Runs for each project:")
doc.add_paragraph("Stack 3: Agent Service → Finds existing hub → Creates project", style='List Bullet 2')

para("Separation Principle: Platform stacks create foundational resources. Onboarding stack builds on top by creating projects. Stacks never overlap or recreate each other's resources.")

h2("TERRAFORM MODULES")

para("Stack 3 uses two key modules:")

h3("Module 1: iac/modules/agent-service/main.tf")
bullet("Input: Project names and configuration from YAML")
bullet("Output: Creates Foundry project resources")
bullet("Logic:")
doc.add_paragraph("Loops through project_configs/<segment>/config.yaml", style='List Bullet 2')
doc.add_paragraph("For each project, looks up the parent Foundry hub", style='List Bullet 2')
doc.add_paragraph("Creates a project resource under that hub", style='List Bullet 2')

h3("Module 2: iac/modules/agent-service/roles.tf")
bullet("Input: Project resources and AD group object IDs")
bullet("Output: Role assignments for project access")
bullet("Logic:")
doc.add_paragraph("Assigns Foundry Project Manager role to manager group", style='List Bullet 2')
doc.add_paragraph("Assigns Foundry User role to user group", style='List Bullet 2')

h1("5. RESOURCES CREATED DURING ONBOARDING")

para("When the Onboarding pipeline executes, the following Azure resources are created:")

h2("RESOURCE 1: FOUNDRY PROJECT")

para("Azure Resource Type: Microsoft.CognitiveServices/accounts/projects")
para("Naming Convention: glbl-<environment>-<projectname>-prj-cgs")

bullet("Example: glbl-dv-customer-analytics-prj-cgs")
bullet("Parent: Pre-existing Foundry hub (shared infrastructure)")
bullet("Created by: Terraform module iac/modules/agent-service/main.tf")
bullet("Quantity: One per entry in project_configs/<segment>/config.yaml")
bullet("Lifespan: Persists for the life of the use case")
bullet("Endpoints: Automatically generated for API access")

h2("RESOURCE 2: PROJECT MANAGER ROLE ASSIGNMENT")

para("Azure Resource Type: Azure Role Assignment")
para("Role: Foundry Project Manager")
para("Assigned to: AD group from config YAML (project_manager_group_id)")

bullet("Scope: The specific Foundry project resource")
bullet("Created by: Terraform resource iac/modules/agent-service/roles.tf")
bullet("Permissions:")
doc.add_paragraph("Manage project settings", style='List Bullet 2')
doc.add_paragraph("Configure access control", style='List Bullet 2')
doc.add_paragraph("Delete or modify project", style='List Bullet 2')

h2("RESOURCE 3: USER ROLE ASSIGNMENT")

para("Azure Resource Type: Azure Role Assignment")
para("Role: Foundry User")
para("Assigned to: AD group from config YAML (project_manager_user_id)")

bullet("Scope: The specific Foundry project resource")
bullet("Created by: Terraform resource iac/modules/agent-service/roles.tf")
bullet("Permissions:")
doc.add_paragraph("Use the project", style='List Bullet 2')
doc.add_paragraph("Create experiments and models", style='List Bullet 2')
doc.add_paragraph("Run deployments", style='List Bullet 2')

box_text(
    "ONBOARDING CREATES ONLY:",
    "✓ One Foundry project\n" +
    "✓ Two role assignments\n\n" +
    "Onboarding does NOT create:\n" +
    "✗ Foundry hubs (pre-existing)\n" +
    "✗ Storage accounts (pre-existing)\n" +
    "✗ Virtual networks (pre-existing)\n" +
    "✗ Resource groups (pre-existing)"
)

h1("6. PRE-EXISTING PLATFORM COMPONENTS")

para("The following components must already exist BEFORE the onboarding pipeline runs. These are created and managed separately, outside this repository.")

h2("PREREQUISITE 1: AZURE SUBSCRIPTION AND RESOURCE GROUPS")

bullet("What: Azure resource groups that organize resources")
bullet("Created by: Enterprise cloud team (one-time)")
bullet("Used by: Terraform to place all resources")
bullet("Requirement: Resource group must exist and be specified in tfvars")
bullet("How Terraform uses it: data.azurerm_resource_group lookup")

h2("PREREQUISITE 2: VIRTUAL NETWORK AND SUBNETS")

bullet("What: Azure Virtual Network with delegated subnets")
bullet("Created by: Enterprise networking team (one-time)")
bullet("Used by: Private endpoints for secure Foundry connectivity")
bullet("Requirement: Specific subnets must exist with available IP space")
bullet("How Terraform uses it: Creates private endpoint resources in these subnets")

h2("PREREQUISITE 3: STORAGE ACCOUNT FOR TERRAFORM STATE")

bullet("What: Azure Storage account with containers for Terraform state")
bullet("Created by: Enterprise infrastructure team (one-time)")
bullet("Used by: Terraform to store .tfstate files")
bullet("Containers needed:")
doc.add_paragraph("tfstate: Platform stack state", style='List Bullet 2')
doc.add_paragraph("tfstatehub: Foundry hub stack state", style='List Bullet 2')
doc.add_paragraph("tfstateproject: Onboarding stack state", style='List Bullet 2')
bullet("Requirement: Account must exist with all three containers")

h2("PREREQUISITE 4: FOUNDRY HUB RESOURCE")

bullet("What: Microsoft.CognitiveServices/accounts (Foundry hub)")
bullet("Created by: Platform Deployment pipeline (one-time per segment)")
bullet("Used by: Onboarding pipeline as parent for projects")
bullet("Naming: glbl-<environment>-<solution>-<index>-<location>-cgs")
bullet("Example: glbl-dv-marketing-mkt001-euwe-cgs")
bullet("Requirement: Hub must exist before onboarding projects are created")
bullet("How Terraform uses it: data.azapi_resource lookup to find hub by name")

box_text(
    "CRITICAL:",
    "During onboarding, Terraform looks up the pre-existing Foundry hub and uses it as the parent for the new project. It does NOT create the hub. If the hub does not exist, Terraform will fail."
)

h2("PREREQUISITE 5: AZURE AD GROUPS")

bullet("What: Azure AD (Entra ID) security groups")
bullet("Created by: Enterprise IAM team (one-time)")
bullet("Used by: Role assignments to grant access")
bullet("Groups needed:")
doc.add_paragraph("Project Manager group (manages the project)", style='List Bullet 2')
doc.add_paragraph("User/Team group (uses the project)", style='List Bullet 2')
bullet("Requirement: Groups must exist, and object IDs must be in config.yaml")
bullet("How Terraform uses it: Assigns roles to group object IDs")

h2("PREREQUISITE 6: PLATFORM SERVICES")

bullet("What: Log Analytics Workspace, Application Insights, Key Vault")
bullet("Created by: Platform Deployment pipeline (one-time)")
bullet("Used by: Application team for monitoring and secrets")
bullet("Requirement: Must exist before projects are created")

h2("PREREQUISITE 7: GITHUB SECRETS FOR OIDC")

bullet("What: Azure authentication credentials for GitHub Actions")
bullet("Created by: Azure cloud team (one-time)")
bullet("Used by: GitHub workflow to authenticate to Azure")
bullet("Secrets needed:")
doc.add_paragraph("AZURE_SUBSCRIPTION_ID", style='List Bullet 2')
doc.add_paragraph("AZURE_TENANT_ID", style='List Bullet 2')
doc.add_paragraph("AZURE_CLIENT_ID (service principal)", style='List Bullet 2')

box_text(
    "READY-TO-USE ASSUMPTION:",
    "When you receive this repository and are asked to run the onboarding pipeline, you should be able to assume that all seven prerequisites above already exist and are properly configured. If anything is missing, the Terraform execution will fail with a clear error message."
)

h1("7. INPUTS AND VARIABLES")

h2("INPUT SOURCE 1: SERVICENOW REQUEST FORM")

para("When a team requests a Foundry project, they provide:")

bullet("Project Name: Descriptive name of the use case")
bullet("Business Segment: Segment/cost center (marketing, finance, etc.)")
bullet("Project Manager Group: Which AD group manages the project (with object ID)")
bullet("User Group: Which AD group uses the project (with object ID)")
bullet("Target Environment: dv (dev), pp (pre-prod), pr (production)")
bullet("Deployment Location: Region (europe, etc.)")

h2("INPUT SOURCE 2: GITHUB WORKFLOW DISPATCH")

para("When infrastructure operator triggers the pipeline, they select:")

bullet("Environment: dv | pp | pr")
bullet("Segment: marketing | finance | other")
bullet("Location: europe | other regions")

para("These values are passed as environment variables to Terraform.")

h2("INPUT SOURCE 3: TERRAFORM VARIABLE FILES (.tfvars)")

para("Configuration files that specify deployment details:")

h3("File: environments/<env>/platform.tfvars")
para("Used by: Platform deployment (not onboarding)")
bullet("Contains: Resource group, VNet, storage account, shared services")

h3("File: environments/<env>/<segment>/agent-service.tfvars")
para("Used by: Onboarding deployment")
bullet("Contains:")
doc.add_paragraph("environment_name: e.g., 'dv'", style='List Bullet 2')
doc.add_paragraph("solution_name: e.g., 'marketing'", style='List Bullet 2')
doc.add_paragraph("resource_group_name: Where to place resources", style='List Bullet 2')
doc.add_paragraph("storage_account: For state storage", style='List Bullet 2')
doc.add_paragraph("shared_subnet_name: For private endpoints", style='List Bullet 2')

h2("INPUT SOURCE 4: YAML CONFIGURATION FILES")

h3("File: iac/foundry_hub_configs/<segment>/config.yaml")
para("Used by: Platform deployment (hub creation)")
bullet("Defines which Foundry hubs exist")
bullet("Specifies network subnets for each hub")

h3("File: iac/project_configs/<segment>/config.yaml")
para("Used by: Onboarding deployment (project creation)")
bullet("Defines which projects to create")
bullet("Example structure:")

doc.add_paragraph()
p = doc.add_paragraph("projects:")
p.paragraph_format.left_indent = Inches(0.3)
p = doc.add_paragraph("analytics-platform:", style='List Bullet')
p.paragraph_format.left_indent = Inches(0.5)
p = doc.add_paragraph("project_name: analytics-platform", style='List Bullet')
p.paragraph_format.left_indent = Inches(0.75)
p = doc.add_paragraph("foundry_index: mkt001", style='List Bullet')
p.paragraph_format.left_indent = Inches(0.75)
p = doc.add_paragraph("project_manager_group_id: <AD group object ID>", style='List Bullet')
p.paragraph_format.left_indent = Inches(0.75)
p = doc.add_paragraph("project_manager_user_id: <AD group object ID>", style='List Bullet')
p.paragraph_format.left_indent = Inches(0.75)

para("Variables in the YAML are read by Terraform and used in 'for_each' loops to create multiple projects or perform bulk operations.")

h1("8. PIPELINE EXECUTION FLOW")

h2("GITHUB ACTIONS WORKFLOWS")

h3("Workflow 1: .github/workflows/iac.yaml (Main Trigger)")

bullet("Type: Manual trigger (workflow_dispatch)")
bullet("Purpose: Routes user to the correct deployment pipeline")
bullet("Inputs:")
doc.add_paragraph("environment, segment, location", style='List Bullet 2')
bullet("Action: Calls the appropriate reusable workflow below")

h3("Workflow 2: .github/workflows/platform-deploy.yml (NOT used for onboarding)")

bullet("Purpose: Deploy platform infrastructure and Foundry hubs")
bullet("When triggered: Once per segment (e.g., marketing, finance)")
bullet("Jobs:")
doc.add_paragraph("platform-hub-deployment: Creates infra", style='List Bullet 2')
doc.add_paragraph("foundry-hub-deployment: Creates hubs", style='List Bullet 2')
bullet("Status: Already complete before onboarding begins")

h3("Workflow 3: .github/workflows/agent-capability-deploy.yml (USED for onboarding)")

bullet("Purpose: Deploy Foundry projects and role assignments")
bullet("When triggered: For each new use case")
bullet("Jobs:")

h4_para = doc.add_paragraph("plan_job: Terraform plan and artifact upload", style='List Number')
doc.add_paragraph("terraform init → terraform plan", style='List Bullet 2')
doc.add_paragraph("Plan output uploaded as GitHub artifact", style='List Bullet 2')

h4_para = doc.add_paragraph("apply_job: Manual approval then terraform apply", style='List Number')
doc.add_paragraph("Waits for manual approval from infrastructure team", style='List Bullet 2')
doc.add_paragraph("Downloads artifact → terraform apply", style='List Bullet 2')
doc.add_paragraph("Creates all resources", style='List Bullet 2')

h2("OIDC AUTHENTICATION FLOW")

para("Each workflow performs the following authentication steps:")

num_item("Checkout: Pull repository code from GitHub")
num_item("Azure Login: Use OIDC token to authenticate to Azure")
doc.add_paragraph("GitHub federated identity pre-configured in Azure", style='List Bullet 2')
doc.add_paragraph("No passwords or secrets transmitted", style='List Bullet 2')
num_item("Terraform Connect: Inherit Azure CLI credentials for Terraform")
num_item("Resource Operations: Terraform can now create resources in Azure")

h2("SEPARATION AND SAFETY")

para("The two deployment pipelines are completely separate:")

bullet("Platform Pipeline (platform-deploy.yml):")
doc.add_paragraph("Creates infrastructure and Foundry hubs", style='List Bullet 2')
doc.add_paragraph("Runs one time per segment", style='List Bullet 2')
doc.add_paragraph("Higher risk (affects shared infrastructure)", style='List Bullet 2')

bullet("Onboarding Pipeline (agent-capability-deploy.yml):")
doc.add_paragraph("Creates projects and role assignments only", style='List Bullet 2')
doc.add_paragraph("Runs one time per project", style='List Bullet 2')
doc.add_paragraph("Lower risk (affects single project)", style='List Bullet 2')

box_text(
    "SAFETY GUARANTEE:",
    "The onboarding pipeline can NEVER create or modify Foundry hubs. The Terraform configuration for onboarding uses only 'azapi_resource' for projects (creates) and 'azurerm_role_assignment' for roles (creates). It does not include any resources that would modify hubs. This is enforced by the repository structure and code review."
)

h1("9. ROLE ASSIGNMENTS")

h2("FOUNDRY PROJECT ROLES")

h3("Role 1: Foundry Project Manager")

para("Permissions granted:")
bullet("Manage project settings and configuration")
bullet("Add or remove team members")
bullet("Delete the project")
bullet("Configure access control")

para("Assigned to: Project Manager AD group")
para("Typical members: Use case lead, project manager, DevOps lead")

h3("Role 2: Foundry User")

para("Permissions granted:")
bullet("Use the project to create models")
bullet("Run experiments and deployments")
bullet("Access datasets and resources")
bullet("Cannot modify project settings or delete")

para("Assigned to: User/Team AD group")
para("Typical members: Data scientists, developers, analysts")

h2("HOW ROLES ARE ASSIGNED")

para("File: iac/modules/agent-service/roles.tf")

para("Terraform creates two azurerm_role_assignment resources:")

h3("Assignment 1: Project Manager")
bullet("Scope: The Foundry project resource")
bullet("Role: 'Foundry Project Manager'")
bullet("Principal: project_manager_group_id from config.yaml")
bullet("Effect: Everyone in the manager group gains Project Manager permissions")

h3("Assignment 2: User")
bullet("Scope: The Foundry project resource")
bullet("Role: 'Foundry User'")
bullet("Principal: project_manager_user_id from config.yaml")
bullet("Effect: Everyone in the user group gains User permissions")

h2("TIMELINE: WHEN ROLES TAKE EFFECT")

bullet("Terraform apply completes: Role assignments created in Azure")
bullet("Within minutes: Azure updates role caches")
bullet("Within 5-10 minutes: Users can log in and see the project")
bullet("First login: User authenticates with corporate credentials (no special setup needed)")

h1("10. CONSTRAINTS AND ASSUMPTIONS")

para("The following constraints define what this onboarding system can and cannot do:")

h2("CONSTRAINT 1: RESOURCE GROUPS PRE-EXIST")

para("Assumption: Azure resource groups already exist in your subscription.")
bullet("Impact: Terraform cannot create resource groups")
bullet("Solution: Enterprise cloud team creates and provides group names")
bullet("Error if violated: Terraform will fail: 'Resource group not found'")

h2("CONSTRAINT 2: AZURE AD GROUPS PRE-EXIST")

para("Assumption: AD groups (Project Manager and Users) already exist in your tenant.")
bullet("Impact: Terraform cannot create AD groups")
bullet("Solution: Enterprise IAM team creates groups and provides object IDs")
bullet("Error if violated: Role assignment will fail or assign to wrong group")

h2("CONSTRAINT 3: FOUNDRY HUB RESOURCE PRE-EXISTS")

para("Assumption: The Foundry hub resource must already exist before onboarding.")
bullet("Impact: Onboarding finds the hub and creates projects under it")
bullet("Solution: Platform pipeline creates hubs one-time per segment")
bullet("Error if violated: Terraform will fail: 'Cannot find parent Foundry hub'")

h2("CONSTRAINT 4: VIRTUAL NETWORKS AND SUBNETS PRE-EXIST")

para("Assumption: VNets and subnets for private endpoints already exist.")
bullet("Impact: Terraform uses these to create private endpoints")
bullet("Solution: Enterprise networking team provides subnet names")
bullet("Error if violated: Private endpoint creation will fail")

h2("CONSTRAINT 5: STORAGE ACCOUNT FOR STATE PRE-EXISTS")

para("Assumption: Azure storage account with state containers exists.")
bullet("Impact: Terraform stores state in remote backend")
bullet("Solution: Cloud team creates storage and provides account details in tfvars")
bullet("Error if violated: Terraform init will fail immediately")

h2("CONSTRAINT 6: SEPARATE STATE BACKENDS")

para("Assumption: Three separate containers for state isolation (tfstate, tfstatehub, tfstateproject).")
bullet("Impact: Prevents state corruption and enables independent rollback")
bullet("Solution: Enforce correct backend configuration in each stack")
bullet("Error if violated: Multiple stacks could interfere with each other")

h2("CONSTRAINT 7: OIDC AUTHENTICATION CONFIGURED")

para("Assumption: GitHub federated identity is configured in Azure.")
bullet("Impact: GitHub Actions can authenticate without passwords")
bullet("Solution: Azure cloud team configures OIDC one-time")
bullet("Error if violated: Workflow will fail during Azure login")

h2("CONSTRAINT 8: CONFIGURATION FILES COMPLETE")

para("Assumption: All tfvars and YAML files are populated for the target segment.")
bullet("Impact: Terraform has all variables needed to create resources")
bullet("Solution: Central onboarding platform auto-generates config files")
bullet("Error if violated: Terraform will fail: 'Missing required variable'")

h1("11. RISKS AND CONSIDERATIONS")

h2("CRITICAL RISK 1: FOUNDRY RESOURCE RE-CREATION")

box_text(
    "THE RISK:",
    "If the wrong pipeline is triggered or configuration is incorrect, Terraform might attempt to recreate the Foundry hub resource. This would DELETE all existing projects under that hub, causing total data loss."
)

para("Why this happens:")
bullet("Terraform State tracks which resources exist")
bullet("If state gets out of sync with reality, Terraform may plan to recreate")
bullet("Deleting a hub deletes all its projects and data")

para("How to prevent:")
bullet("ONLY use agent-capability-deploy.yml for onboarding")
bullet("NEVER run platform-deploy.yml during onboarding")
bullet("Code review: Verify terraform plan before approving apply")
bullet("State backup: Keep backups of Azure storage state files")
bullet("Documentation: Team members aware of the separation principle")

para("What to do if it happens:")
bullet("STOP the Terraform apply immediately")
bullet("Restore state from backup")
bullet("Investigate what caused the plan to include hub resources")
bullet("Require post-incident review before retry")

h2("RISK 2: INCORRECT AD GROUP OBJECT IDS")

para("The Risk: Wrong object ID assigned → wrong people get access")
bullet("Likelihood: Medium (manual entry error)")
bullet("Impact: Security issue; team cannot access project, or wrong team gains access")

para("Prevention:")
bullet("Validate AD group object IDs before entry into config.yaml")
bullet("Use Azure AD portal to copy correct IDs")
bullet("Code review for config changes")
bullet("Test roles after Terraform apply")

h2("RISK 3: STATE BACKEND MISCONFIGURATION")

para("The Risk: Incorrect storage container name → Terraform overwrites wrong state")
bullet("Likelihood: Low (checked at init)")
bullet("Impact: State file corruption; deployed resources become unmanageable")

para("Prevention:")
bullet("Use consistent naming: tfstate, tfstatehub, tfstateproject")
bullet("Validate backend config during code review")
bullet("Never manually edit backend config")
bullet("Test storage account access before deployment")

h2("RISK 4: RESOURCE GROUP DOES NOT EXIST")

para("The Risk: tfvars points to non-existent resource group → deployment fails")
bullet("Likelihood: Low (should be pre-created)")
bullet("Impact: Terraform fails immediately, no resources created")

para("Prevention:")
bullet("Checklist: Verify resource group exists before triggering pipeline")
bullet("Terraform output: terraform plan shows which RG will be used")

h2("RISK 5: PRIVATE ENDPOINT SUBNET MISSING")

para("The Risk: Specified subnet does not have available IP space → endpoint fails")
bullet("Likelihood: Low (networking team coordinates)")
bullet("Impact: Private endpoint creation fails; Foundry not accessible")

para("Prevention:")
bullet("Network team validates subnet availability")
bullet("Test connectivity after deployment")

h2("RISK 6: OIDC TOKEN EXPIRATION")

para("The Risk: GitHub federated identity expires → authentication fails")
bullet("Likelihood: Very low (long expiration)")
bullet("Impact: Pipeline cannot authenticate to Azure; manual intervention needed")

para("Prevention:")
bullet("Monitor OIDC token expiration dates")
bullet("Rotate credentials before expiration")

h1("12. POST-ONBOARDING STEPS")

h2("STEP 1: VERIFY TERRAFORM SUCCESS")

para("Check that Terraform apply completed successfully:")
bullet("Open GitHub Actions")
bullet("Find the workflow run for your project")
bullet("Look for: '✓ apply succeeded' or 'Apply complete'")
bullet("Expected output:")
doc.add_paragraph("Applied 3 resource(s): 1 project + 2 role assignments", style='List Bullet 2')

h2("STEP 2: CONFIRM PROJECT IN AZURE PORTAL")

para("Navigate to Azure portal and verify the project was created:")
bullet("Search for 'Cognitive Services' or 'AI Foundry'")
bullet("Look for resource: glbl-<env>-<projectname>-prj-cgs")
bullet("Verify: Resource status is 'Ready'")
bullet("Check: Resource group is correct")

h2("STEP 3: VERIFY ROLE ASSIGNMENTS")

para("Verify that roles were assigned correctly:")
bullet("In Azure portal: Open the project resource")
bullet("Go to Access Control (IAM)")
bullet("Check for TWO role assignments:")
doc.add_paragraph("Foundry Project Manager (assigned to manager group)", style='List Bullet 2')
doc.add_paragraph("Foundry User (assigned to user group)", style='List Bullet 2')
bullet("Verify: Each assignment shows the correct AD group name")

h2("STEP 4: TEST AD GROUP ACCESS")

para("Test that team members can access the project:")
bullet("Log out of Azure portal")
bullet("Log back in with a test user account from the User AD group")
bullet("Go to https://ai.azure.com/ (Azure AI Foundry portal)")
bullet("Look for: Project appears in 'My Projects' list")
bullet("Note: May take 5-10 minutes for role propagation")
bullet("If not visible: Verify user is in the correct AD group")

h2("STEP 5: CONFIRM PROJECT API ENDPOINTS")

para("Retrieve project endpoints for application team:")
bullet("In Foundry portal: Open the project")
bullet("Go to Project Settings → API Endpoints")
bullet("Copy: Project endpoint URL")
bullet("Record: Endpoint in project documentation")

h2("STEP 6: VALIDATE PRIVATE ENDPOINT CONNECTIVITY")

para("Ensure private endpoint connectivity works:")
bullet("From a machine in the authorized network: Test endpoint connectivity")
bullet("Verify: Private endpoint routes traffic correctly")
bullet("Check: Network routing is functional")

h2("STEP 7: NOTIFY APPLICATION TEAM")

para("Send project ready notification to the requesting team:")

num_item("Email template:")
doc.add_paragraph("Subject: Foundry Project Ready - [ProjectName]", style='List Bullet 2')
doc.add_paragraph("Your Foundry project is now ready to use.", style='List Bullet 2')
doc.add_paragraph("Project Name: [ProjectName]", style='List Bullet 2')
doc.add_paragraph("Project ID: glbl-[env]-[projectname]-prj-cgs", style='List Bullet 2')
doc.add_paragraph("Foundry Portal: https://ai.azure.com/", style='List Bullet 2')
doc.add_paragraph("Project Manager Group: [GroupName]", style='List Bullet 2')
doc.add_paragraph("User Group: [GroupName]", style='List Bullet 2')
doc.add_paragraph("Support Contact: [Infrastructure Team]", style='List Bullet 2')

h2("STEP 8: CREATE PROJECT DOCUMENTATION")

para("Update internal documentation:")
bullet("Record project creation date")
bullet("Document business purpose and use case")
bullet("Record resource group and subscription")
bullet("List segment, environment, and region")
bullet("Document project managers and user groups")
bullet("Store API endpoint")

h2("STEP 9: EXECUTE ACCEPTANCE TESTING")

para("Application team validates the project:")
bullet("Can team members log in? ✓")
bullet("Can they create experiments in the project? ✓")
bullet("Can they access shared resources? ✓")
bullet("Do role permissions work as expected? ✓")
bullet("Can they run models and deployments? ✓")

h2("STEP 10: CLOSE SERVICENOW REQUEST")

para("Mark the onboarding request as complete:")
bullet("Update ServiceNow status to 'Completed'")
bullet("Record project ID and endpoint in request")
bullet("Add link to project documentation")
bullet("Notify requesting team that project is ready")

# ===== END OF CONTENT =====

# Save document
output_path = r'c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs\Foundry_Onboarding_Deployment_Guide_CORRECTED.docx'
doc.save(output_path)
print(f"✓ Corrected guide created: {output_path}")
print(f"✓ File ready for stakeholder distribution")
