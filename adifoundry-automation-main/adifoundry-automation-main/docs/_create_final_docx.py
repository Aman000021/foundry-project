#!/usr/bin/env python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

doc = Document()

# Title Page
title = doc.add_paragraph()
title_run = title.add_run("FOUNDRY ONBOARDING PLATFORM")
title_run.font.size = Pt(28)
title_run.bold = True
title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

subtitle = doc.add_paragraph()
subtitle_run = subtitle.add_run("Deployment Guide")
subtitle_run.font.size = Pt(18)
subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

doc.add_paragraph()

meta = doc.add_paragraph()
meta_run = meta.add_run("Repository: npet-foundry-template\nPrepared: 2026-06-22")
meta.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

doc.add_page_break()

# Helper functions
def h1(text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)

def h2(text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)

def h3(text):
    h = doc.add_heading(text, level=3)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(3)

def para(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    return p

def bullet(text, level=0):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.5 + level*0.25)
    p.paragraph_format.space_after = Pt(3)

def num_item(text):
    doc.add_paragraph(text, style='List Number')

# Content
h1("1. OVERVIEW")
para("This repository provides Infrastructure-as-Code for onboarding use cases onto Azure AI Foundry. It implements a two-stage deployment model:")

doc.add_paragraph("STAGE 1: PLATFORM DEPLOYMENT (one-time, shared)", style='List Bullet')
doc.add_paragraph("Creates shared platform components (observability, security)", style='List Bullet 2')
doc.add_paragraph("Creates Foundry hub resources (AI Foundry accounts)", style='List Bullet 2')
doc.add_paragraph("Executed via: Platform and Foundry Resource Deployment workflow", style='List Bullet 2')

doc.add_paragraph("STAGE 2: ONBOARDING DEPLOYMENT (per use case, repeatable)", style='List Bullet')
doc.add_paragraph("Creates Foundry projects under existing hub resources", style='List Bullet 2')
doc.add_paragraph("Assigns project-level access roles to AD groups", style='List Bullet 2')
doc.add_paragraph("Executed via: Foundry Project Deployment workflow", style='List Bullet 2')

para("The critical architecture principle: Foundry hub resources exist once and are shared across many projects. Each onboarding creates one or more projects within that hub. This prevents accidental recreation or deletion of shared infrastructure.")

h1("2. END-TO-END DEPLOYMENT FLOW")

h2("STEP 1: USE CASE TEAM SUBMITS ONBOARDING REQUEST")
bullet("ServiceNow or Backstage request system")
bullet("Includes: project name, segment (marketing/finance), team AD groups, location")

h2("STEP 2: REPOSITORY AND CONFIG GENERATION")
bullet("Central onboarding platform generates GitHub repository from template")
bullet("Populates environments/<env>/<segment>/*.tfvars with request values")
bullet("Populates iac/project_configs/<segment>/config.yaml with project metadata")

h2("STEP 3: TRIGGER DEPLOYMENT")
bullet("Infrastructure operator opens GitHub Actions")
bullet("Selects: Environment (dv/pp/pr), Segment (marketing/finance), Location (europe)")

h2("STEP 4: TERRAFORM INITIALIZATION")
bullet("Terraform init: download providers and modules")
bullet("Backend configured: separate containers for platform/hub/project state")

h2("STEP 5: TERRAFORM PLAN AND VALIDATE")
bullet("Terraform plan: shows what WILL BE CREATED")
bullet("Human review: infrastructure team approves or rejects changes")

h2("STEP 6: TERRAFORM APPLY - PROJECT CREATION")
bullet("Foundry project resource created")
bullet("Name: glbl-<env>-<projectname>-prj-cgs")

h2("STEP 7: TERRAFORM APPLY - ROLE ASSIGNMENT")
bullet("Two role assignments created: Project Manager and Foundry User")

h2("STEP 8: POST-DEPLOYMENT VALIDATION")
bullet("Verify Terraform success")
bullet("Confirm project visible in Azure portal")
bullet("Confirm roles assigned correctly")

h1("3. TERRAFORM EXECUTION EXPLAINED")

h2("TERRAFORM STACKS AND RESPONSIBILITY")

h3("Stack 1: PLATFORM-HUB")
bullet("Creates: Log Analytics Workspace, Application Insights, Key Vault")
bullet("Executes: Platform pipeline (ONE TIME)")

h3("Stack 2: FOUNDRY-HUB")
bullet("Creates: Foundry hub resources, Private endpoints")
bullet("Executes: Platform pipeline (ONE TIME)")

h3("Stack 3: AGENT-SERVICE (ONBOARDING)")
bullet("Creates: Foundry projects, Project role assignments")
bullet("Executes: Onboarding pipeline (REPEATABLE)")

h2("PLATFORM PIPELINE")
para("Executes both Stack 1 and Stack 2:")
num_item("terraform init → plan → apply (Platform Hub)")
num_item("terraform init → plan → apply (Foundry Hub)")

h2("ONBOARDING PIPELINE")
para("Executes Stack 3 in two jobs:")
num_item("Plan Job: terraform init → plan → upload artifact")
num_item("Apply Job: download artifact → terraform init → apply")

h1("4. RESOURCES CREATED DURING ONBOARDING")

h2("RESOURCE: Foundry Project")
bullet("Type: Microsoft.CognitiveServices/accounts/projects")
bullet("Name: glbl-<environment>-<project_name>-prj-cgs")
bullet("Parent: Existing Foundry hub")

h2("RESOURCE: Foundry Project Manager Role Assignment")
bullet("Assigned to: project_manager_group_id from config.yaml")

h2("RESOURCE: Foundry User Role Assignment")
bullet("Assigned to: project_manager_user_id from config.yaml")

para("SUMMARY: Onboarding creates ONLY projects and role assignments.")

h1("5. PRE-EXISTING PLATFORM COMPONENTS")

h2("PREREQUISITE 1: Azure Subscription and Resource Groups")
bullet("Created and managed by enterprise cloud team")

h2("PREREQUISITE 2: Virtual Network and Subnets")
bullet("Created and managed by enterprise networking team")

h2("PREREQUISITE 3: Storage Account")
bullet("For Terraform remote state")

h2("PREREQUISITE 4: Foundry Hub Resource")
bullet("Created by platform deployment pipeline")
bullet("Shared across all onboarding projects")

h2("PREREQUISITE 5: Azure AD Groups")
bullet("Object IDs provided in config.yaml")

h2("PREREQUISITE 6: Platform Services")
bullet("Log Analytics, Application Insights, Key Vault")
bullet("Created by platform pipeline")

h1("6. INPUTS AND VARIABLES")

h2("REQUIRED INPUTS FROM SERVICENOW")
bullet("project_name")
bullet("segment")
bullet("AD group IDs for Project Manager and Users")
bullet("location")
bullet("environment")

h2("TERRAFORM VARIABLE FILES")
bullet("environments/<env>/platform.tfvars")
bullet("environments/<env>/<segment>/foundry-hub.tfvars")
bullet("environments/<env>/<segment>/agent-service.tfvars")

h2("CONFIGURATION YAML FILES")
bullet("iac/foundry_hub_configs/<segment>/config.yaml")
bullet("iac/project_configs/<segment>/config.yaml")

h1("7. PIPELINE EXECUTION FLOW")

h2("GITHUB WORKFLOWS")

h3("Primary Trigger: .github/workflows/iac.yaml")
bullet("Type: workflow_dispatch (manual)")
bullet("Inputs: environment, segment, location")

h3("Platform Deploy: .github/workflows/platform-deploy.yml")
bullet("Executes: Stacks 1 and 2")
bullet("Frequency: Once per segment")

h3("Agent Deploy: .github/workflows/agent-capability-deploy.yml")
bullet("Executes: Stack 3")
bullet("Frequency: Once per use case")

h2("AUTHENTICATION")
bullet("OIDC login to Azure")
bullet("GitHub federated identity configured in Azure")

h1("8. ROLE ASSIGNMENTS")

h2("FOUNDRY PROJECT MANAGER ROLE")
bullet("Permissions: Can manage project, configure, administer access")
bullet("Assigned to: project_manager_group_id")

h2("FOUNDRY USER ROLE")
bullet("Permissions: Can use project, run experiments")
bullet("Assigned to: project_manager_user_id")

h2("IMPLEMENTATION")
bullet("File: iac/modules/agent-service/roles.tf")
bullet("Uses: Terraform azurerm_role_assignment resources")

h1("9. CONSTRAINTS AND ASSUMPTIONS")

h2("CONSTRAINT 1: Resource Groups Pre-exist")
bullet("Terraform reads via data lookup")

h2("CONSTRAINT 2: AD Groups Pre-exist")
bullet("Object IDs provided in config.yaml")

h2("CONSTRAINT 3: Foundry Hub Resource Pre-exists")
bullet("Created by platform pipeline")

h2("CONSTRAINT 4: Separate State Backends")
bullet("Three containers: tfstate, tfstatehub, tfstateproject")

h2("CONSTRAINT 5: VNet and Subnets Pre-exist")
bullet("For private endpoint connectivity")

h2("CONSTRAINT 6: Storage Account Pre-exists")
bullet("For Terraform state")

h2("CONSTRAINT 7: OIDC Pre-configured")
bullet("GitHub federated identity in Azure")

h1("10. RISKS AND CONSIDERATIONS")

h2("RISK 1: Accidental Foundry Hub Deletion")
para("Mitigation: Use only agent-capability-deploy for onboarding")

h2("RISK 2: Incorrect AD Group Object IDs")
para("Mitigation: Validate IDs before entry; require dual approval")

h2("RISK 3: State Backend Misconfiguration")
para("Mitigation: Use strict naming conventions")

h2("RISK 4: Resource Group Does Not Exist")
para("Mitigation: Validate before pipeline execution")

h2("RISK 5: VNet/Subnet Missing")
para("Mitigation: Network team provides subnet list")

h2("RISK 6: OIDC Misconfigured")
para("Mitigation: Cloud team validates OIDC setup")

h1("11. POST-ONBOARDING STEPS")

h2("STEP 1: VERIFY TERRAFORM SUCCESS")
bullet("Check GitHub workflow logs for success")

h2("STEP 2: CONFIRM PROJECT IN AZURE PORTAL")
bullet("Verify project resource created and Ready")

h2("STEP 3: VERIFY ROLE ASSIGNMENTS")
bullet("Check Access Control (IAM) in Azure portal")

h2("STEP 4: TEST AD GROUP ACCESS")
bullet("Log in with team member account")
bullet("Confirm project visible in Foundry portal")

h2("STEP 5: CONFIRM PROJECT ENDPOINTS")
bullet("Record API endpoint for application team")

h2("STEP 6: VALIDATE PRIVATE ENDPOINT CONNECTIVITY")
bullet("Test network connectivity to endpoint")

h2("STEP 7: NOTIFY APPLICATION TEAM")
bullet("Send project ready notification with endpoint and access info")

h2("STEP 8: CREATE PROJECT DOCUMENTATION")
bullet("Record creation date, purpose, groups, and endpoint")

h2("STEP 9: EXECUTE ACCEPTANCE TESTING")
bullet("Application team validates project access and functionality")

h2("STEP 10: CLOSE SERVICENOW REQUEST")
bullet("Mark request Complete with project ID and endpoint")

# Save
output_path = r'c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs\Foundry_Onboarding_Deployment_Guide_FINAL.docx'
doc.save(output_path)
print(f"Document created: {output_path}")
