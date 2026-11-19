from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_repo_table(doc):
    table = doc.add_table(rows=12, cols=2)
    table.style = "Light Grid Accent 1"

    headers = table.rows[0].cells
    headers[0].text = "File / Directory"
    headers[1].text = "Purpose"

    data = [
        (".github/workflows/iac.yaml", "Main workflow trigger (Trigger Foundry Setup)"),
        (".github/workflows/platform-deploy.yml", "Reusable Platform deployment workflow"),
        (".github/workflows/agent-capability-deploy.yml", "Reusable workflow for agent capability deployment"),
        ("environments/<env>/platform.tfvars", "Environment-level variables for platform deployment"),
        ("environments/<env>/<segment>/foundry-hub.tfvars", "Segment-level variables for foundry-hub deployment"),
        ("environments/<env>/<segment>/backend-config-hub.tfvars", "Terraform backend state configuration for foundry-hub stack"),
        ("iac/platform-hub/", "Terraform root stack for platform resource deployment"),
        ("iac/capability/foundry-hub/", "Terraform root stack for foundry-hub capability deployment"),
        ("iac/modules/platform/", "Reusable Terraform module implementation for platform resources"),
        ("iac/modules/foundry-hub/", "Reusable Terraform module implementation for foundry-hub resources"),
        ("iac/foundry_hub_configs/<segment>/config.yaml", "Segment configuration metadata used by deployment flows"),
    ]

    for idx, (path, purpose) in enumerate(data, start=1):
        row = table.rows[idx].cells
        row[0].text = path
        row[1].text = purpose


def main():
    doc = Document()

    doc.add_heading("Platform Resources Deployment Guide (Stakeholder Ready)", 0)

    # 1. Overview
    doc.add_heading("1. Overview", 1)
    doc.add_paragraph("This guide covers the Platform Resources deployment pipeline triggered from a Service Now approved request.")
    doc.add_paragraph("")
    doc.add_paragraph(
        "Flow: Service Now Request -> Team Updates Platform Config -> PR Approved & Merged -> "
        "Operator Triggers Pipeline -> Terraform Plan & Apply -> Platform Resources Created"
    )
    doc.add_paragraph("")
    doc.add_paragraph(
        "Outcome: Foundry hub/platform resources, IAM role assignments, and Azure infrastructure are deployed to the target environment."
    )
    doc.add_paragraph("[Insert Screenshot Here] - High-level platform deployment flow diagram")

    # 2. Architecture Diagram
    doc.add_heading("2. Architecture Diagram", 1)
    doc.add_paragraph(
        "Service Now Request Approved -> Platform Config Updated -> GitHub Workflow Triggered -> "
        "Terraform Plan (dv/pp/pr) -> Manual Approval Gate -> Terraform Apply -> Azure Platform Resources Created"
    )
    doc.add_paragraph("[Insert Screenshot Here] - Platform deployment architecture from Service Now to Azure")

    # 3. Repository Structure
    doc.add_heading("3. Repository Structure", 1)
    doc.add_paragraph("Key deployment files:")
    add_repo_table(doc)
    doc.add_paragraph("[Insert Screenshot Here] - Platform repository structure overview")

    # 4. Configuration Update
    doc.add_heading("4. Configuration Update", 1)
    doc.add_paragraph("1. Service Now request is approved with platform details (environment, segment, owners, location)")
    doc.add_paragraph("2. Team updates iac/foundry_hub_configs/marketing/config.yaml with approved values")
    doc.add_paragraph("3. Team creates Pull Request with platform configuration changes")
    doc.add_paragraph("4. Reviewer approves PR")
    doc.add_paragraph("5. Merge to main branch prepares pipeline execution")
    doc.add_paragraph("")
    doc.add_paragraph("Config entry example:")
    doc.add_paragraph("- project_segment: marketing")
    doc.add_paragraph("  foundry_index: 'mkt001'")
    doc.add_paragraph("  location: europe")
    doc.add_paragraph("  owner_group_id: [from_service_now]")
    doc.add_paragraph("  approver_group_id: [from_service_now]")
    doc.add_paragraph("[Insert Screenshot Here] - Platform config file update")

    # 5. Pull Request Process
    doc.add_heading("5. Pull Request Process", 1)
    doc.add_paragraph("1. Team creates PR against main branch with updated platform config")
    doc.add_paragraph("2. PR reviewers verify:")
    doc.add_paragraph("Service Now ticket reference is included", style="List Bullet 2")
    doc.add_paragraph("Platform details match approved request", style="List Bullet 2")
    doc.add_paragraph("IAM and owner groups are correct", style="List Bullet 2")
    doc.add_paragraph("3. Approval -> Merge to main branch")
    doc.add_paragraph("4. Merge confirms configuration is available for deployment")
    doc.add_paragraph("[Insert Screenshot Here] - GitHub PR approval and merge")

    # 6. Terraform Plan
    doc.add_heading("6. Terraform Plan", 1)
    doc.add_paragraph("Trigger: Click 'Trigger Foundry Setup' workflow in GitHub Actions")
    doc.add_paragraph("")
    doc.add_paragraph("Inputs required:")
    doc.add_paragraph("Environment: Choose Dev (dv), Pre-Prod (pp), or Prod (pr)", style="List Bullet")
    doc.add_paragraph("Project Segment: Select 'marketing' (or applicable segment)", style="List Bullet")
    doc.add_paragraph("Location: Select 'europe' (or applicable region)", style="List Bullet")
    doc.add_paragraph("")
    doc.add_paragraph("Pipeline execution:")
    doc.add_paragraph("iac.yaml dispatches to platform-deploy.yml with selected inputs")
    doc.add_paragraph("Workflow reads environment variables from environments/[env]/platform.tfvars")
    doc.add_paragraph("Terraform initializes backend from backend-config-platform.tfvars")
    doc.add_paragraph("Terraform plan executes against iac/platform-hub/")
    doc.add_paragraph("Plan output is stored as tfplan artifact")
    doc.add_paragraph("")
    doc.add_paragraph("Validation: Review plan output for platform resource creation and IAM role changes")
    doc.add_paragraph("[Insert Screenshot Here] - GitHub Actions workflow dispatch")
    doc.add_paragraph("[Insert Screenshot Here] - Terraform plan output")

    # 7. Terraform Apply
    doc.add_heading("7. Terraform Apply", 1)
    doc.add_paragraph("Prerequisites: terraform plan completed successfully AND manual approval provided")
    doc.add_paragraph("Branch condition: Apply only runs if branch = 'updated-foundry-deployment'")
    doc.add_paragraph("")
    doc.add_paragraph("Approval gate:")
    doc.add_paragraph("1. Plan completes -> pipeline waits at environment approval gate")
    doc.add_paragraph("2. Authorized reviewer approves in GitHub Environments")
    doc.add_paragraph("3. Apply starts automatically after approval")
    doc.add_paragraph("")
    doc.add_paragraph("Apply execution:")
    doc.add_paragraph("Terraform downloads tfplan artifact")
    doc.add_paragraph("Applies configuration: terraform apply tfplan")
    doc.add_paragraph("Creates Azure platform resources:", style="List Bullet")
    doc.add_paragraph("Foundry Hub and platform services", style="List Bullet 2")
    doc.add_paragraph("Role assignments for platform owners and groups", style="List Bullet 2")
    doc.add_paragraph("Networking and private endpoints for platform", style="List Bullet 2")
    doc.add_paragraph("Key Vault and foundational service resources", style="List Bullet 2")
    doc.add_paragraph("")
    doc.add_paragraph("Outcome: Platform baseline is created and ready for project onboarding.")
    doc.add_paragraph("[Insert Screenshot Here] - Manual approval gate in GitHub Environments")
    doc.add_paragraph("[Insert Screenshot Here] - Terraform apply job execution")
    doc.add_paragraph("[Insert Screenshot Here] - Azure platform resources creation confirmation")

    output_path = r"c:\Users\XSPriyaGa\Downloads\Platform_Resources_Deployment_Guide_Updated_v3.docx"
    doc.save(output_path)
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
