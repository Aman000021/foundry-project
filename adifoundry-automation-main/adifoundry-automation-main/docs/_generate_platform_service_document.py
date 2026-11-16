from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

output_path = r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs\Platform_Service_Document_001.docx"

doc = Document()

# Global font style
normal_style = doc.styles["Normal"]
normal_style.font.name = "Aptos"
normal_style.font.size = Pt(11)

for style_name in ["Heading 1", "Heading 2", "Heading 3"]:
    if style_name in doc.styles:
        doc.styles[style_name].font.name = "Aptos"

# Title
p = doc.add_paragraph()
p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
r = p.add_run("MS FOUNDRY")
r.bold = True
r.font.size = Pt(22)

p = doc.add_paragraph()
p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
r = p.add_run("Platform Service Document")
r.bold = True
r.font.size = Pt(16)

p = doc.add_paragraph()
p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
p.add_run("Version: 001")

doc.add_paragraph("")

# TOC
doc.add_heading("Table of Contents", level=1)
doc.add_paragraph("1. Overview")
doc.add_paragraph("2. Foundry Resource Creation Steps")
doc.add_paragraph("3. Other Resource Creation Steps")
doc.add_paragraph("4. Repository Structure")

doc.add_paragraph("")

# Section 1
doc.add_heading("1. Overview", level=1)
doc.add_paragraph(
    "This document provides the operational steps to create and manage platform-side resources for Azure AI Foundry "
    "using the npet-foundry-template repository. It is structured to match the deployment expectation shared in the review call: "
    "keep the guide practical, screenshot-driven, and execution-oriented."
)

doc.add_paragraph(
    "Scope covered in this document:")
doc.add_paragraph("- Foundry hub resource creation (platform-side Foundry resources)")
doc.add_paragraph("- Other platform resource creation (monitoring, security, and shared infrastructure)")
doc.add_paragraph("- Repository locations and workflow entry points")

doc.add_paragraph(
    "High-level flow:")
doc.add_paragraph("- Review requirement and required capacity")
doc.add_paragraph("- Create feature branch and update configuration")
doc.add_paragraph("- Raise PR and trigger workflow to validate Terraform plan")
doc.add_paragraph("- Verify plan output, approve, merge, and apply")
doc.add_paragraph("- Validate resources in Azure portal")

doc.add_paragraph(
    "Suggested screenshot checkpoints for this section:")
doc.add_paragraph("- Platform architecture flow diagram")
doc.add_paragraph("- GitHub Actions 'Trigger Foundry Setup' workflow page")

# Section 2
doc.add_heading("2. Foundry Resource Creation Steps", level=1)
doc.add_paragraph(
    "Use this section when creating or updating Foundry hub resources (Microsoft.CognitiveServices/accounts) and related private endpoints. "
    "These actions are executed through the platform pipeline path and must be validated carefully before apply."
)

doc.add_heading("2.1 Pre-checks", level=2)
doc.add_paragraph("- Confirm target environment (dv/pp/pr)")
doc.add_paragraph("- Confirm segment (for example: marketing, finance)")
doc.add_paragraph("- Confirm region input (currently Europe flow in existing setup)")
doc.add_paragraph("- Confirm existing network dependencies (VNet/Subnet) and resource group availability")

doc.add_heading("2.2 Branch and Configuration Update", level=2)
doc.add_paragraph("1. Pull latest code from main branch.")
doc.add_paragraph("2. Create feature branch using naming convention: <RITM>/<use-case-or-change-name>.")
doc.add_paragraph("3. Update Foundry hub configuration files:")
doc.add_paragraph("   - environments/<env>/<segment>/foundry-hub.tfvars")
doc.add_paragraph("   - iac/foundry_hub_configs/<segment>/config.yaml")
doc.add_paragraph("4. Validate naming, subnet mapping, and foundry index details.")

doc.add_heading("2.3 PR and Workflow Validation", level=2)
doc.add_paragraph("1. Push the feature branch and create PR.")
doc.add_paragraph("2. Open GitHub Actions and run 'Trigger Foundry Setup'.")
doc.add_paragraph("3. Select environment option for platform deployment.")
doc.add_paragraph("4. Review Terraform plan output before approval.")
doc.add_paragraph("5. Validate at minimum:")
doc.add_paragraph("   - Correct resource group")
doc.add_paragraph("   - Correct Foundry hub name/index")
doc.add_paragraph("   - Correct private endpoint/subnet mapping")
doc.add_paragraph("   - No unintended deletions")

doc.add_heading("2.4 Apply and Post-deployment Validation", level=2)
doc.add_paragraph("1. Approve workflow after plan validation.")
doc.add_paragraph("2. Merge PR after required approvals.")
doc.add_paragraph("3. Confirm workflow apply job completion.")
doc.add_paragraph("4. Validate in Azure:")
doc.add_paragraph("   - Foundry hub created/updated as expected")
doc.add_paragraph("   - Private endpoint created and connected")
doc.add_paragraph("   - Required access and connectivity checks")

doc.add_paragraph("Suggested screenshot checkpoints:")
doc.add_paragraph("- Updated foundry-hub.tfvars and config.yaml fields")
doc.add_paragraph("- Workflow input selection")
doc.add_paragraph("- Terraform plan summary and apply success")

# Section 3
doc.add_heading("3. Other Resource Creation Steps", level=1)
doc.add_paragraph(
    "Use this section for platform resources other than Foundry hub resources, such as monitoring and shared security components. "
    "Typical resources are provisioned through iac/platform-hub and related modules."
)

doc.add_heading("3.1 Resources in Scope", level=2)
doc.add_paragraph("- Log Analytics Workspace")
doc.add_paragraph("- Application Insights")
doc.add_paragraph("- Key Vault (through reusable module)")
doc.add_paragraph("- Supporting shared platform settings from environment tfvars")

doc.add_heading("3.2 Update Steps", level=2)
doc.add_paragraph("1. Pull latest main and create feature branch.")
doc.add_paragraph("2. Update environment-level platform configuration:")
doc.add_paragraph("   - environments/<env>/platform.tfvars")
doc.add_paragraph("3. If required, update module variables under:")
doc.add_paragraph("   - iac/platform-hub/")
doc.add_paragraph("   - iac/modules/platform/")
doc.add_paragraph("4. Validate Terraform variable consistency (names, IDs, locations).")

doc.add_heading("3.3 PR, Plan, and Apply", level=2)
doc.add_paragraph("1. Create PR and attach change summary.")
doc.add_paragraph("2. Trigger platform workflow through 'Trigger Foundry Setup'.")
doc.add_paragraph("3. Review plan for platform-hub-deployment job.")
doc.add_paragraph("4. Validate created/updated resources and avoid unrelated drift.")
doc.add_paragraph("5. Approve and apply after reviewer sign-off.")

doc.add_heading("3.4 Validation Checklist", level=2)
doc.add_paragraph("- Monitoring resources are created in expected resource group")
doc.add_paragraph("- Naming convention matches environment standards")
doc.add_paragraph("- No accidental destruction of existing shared resources")
doc.add_paragraph("- Workflow completed with successful apply status")

doc.add_paragraph("Suggested screenshot checkpoints:")
doc.add_paragraph("- platform.tfvars updated fields")
doc.add_paragraph("- platform-hub-deployment job summary")
doc.add_paragraph("- Azure portal validation snapshot")

# Section 4
doc.add_heading("4. Repository Structure", level=1)
doc.add_paragraph("Key paths and ownership-relevant files:")

doc.add_heading("4.1 Workflow Entry Points", level=2)
doc.add_paragraph("- .github/workflows/iac.yaml")
doc.add_paragraph("- .github/workflows/platform-deploy.yml")
doc.add_paragraph("- .github/workflows/agent-capability-deploy.yml")

doc.add_heading("4.2 Environment Configuration", level=2)
doc.add_paragraph("- environments/<env>/platform.tfvars")
doc.add_paragraph("- environments/<env>/<segment>/foundry-hub.tfvars")
doc.add_paragraph("- environments/<env>/<segment>/agent-service.tfvars")
doc.add_paragraph("- environments/<env>/<segment>/backend-config-*.tfvars")

doc.add_heading("4.3 IaC Stacks", level=2)
doc.add_paragraph("- iac/platform-hub/  -> platform shared resources")
doc.add_paragraph("- iac/capability/foundry-hub/  -> Foundry hub resources")
doc.add_paragraph("- iac/capability/agent-service/  -> Foundry projects and role assignments")

doc.add_heading("4.4 Modules and Config", level=2)
doc.add_paragraph("- iac/modules/platform/")
doc.add_paragraph("- iac/modules/foundry-hub/")
doc.add_paragraph("- iac/modules/agent-service/")
doc.add_paragraph("- iac/foundry_hub_configs/<segment>/config.yaml")
doc.add_paragraph("- iac/project_configs/<segment>/config.yaml")

doc.add_heading("4.5 Quick Reference", level=2)
doc.add_paragraph("- Trigger workflow: Actions -> Trigger Foundry Setup")
doc.add_paragraph("- Platform path: platform-hub + foundry-hub")
doc.add_paragraph("- Project path: agent-service")

doc.add_paragraph("------------------------------------------End of document------------------------------------------")

doc.save(output_path)
print(output_path)
