from docx import Document


def main():
    out = r"c:\Users\XSPriyaGa\Downloads\Platform_Resources_Deployment_Guide_Updated_v3_STYLE_MATCH.docx"
    doc = Document()

    # Title
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
        "Outcome: Platform baseline resources and Foundry Hub resources are provisioned in Azure for the requested environment and segment."
    )
    doc.add_paragraph("The deployment provisions shared platform resources including:")
    doc.add_paragraph("Azure Key Vault", style="List Bullet")
    doc.add_paragraph("Storage Account", style="List Bullet")
    doc.add_paragraph("Private Endpoints", style="List Bullet")
    doc.add_paragraph("Private DNS Zones", style="List Bullet")
    doc.add_paragraph("Monitoring and Log Analytics components", style="List Bullet")
    doc.add_paragraph("Platform Hub supporting resources", style="List Bullet")
    doc.add_paragraph("[Insert Screenshot Here]")
    doc.add_paragraph("Figure 1 - High-Level Platform Resources Deployment Flow")

    # 2. Architecture Diagram
    doc.add_heading("2. Architecture Diagram", 1)
    doc.add_paragraph(
        "Service Now Request Approved -> Platform Config Updated -> GitHub Workflow Triggered -> "
        "Platform-Hub Terraform Plan/Apply -> Foundry-Hub Terraform Plan/Apply -> Shared Platform Resources Created"
    )
    doc.add_paragraph("[Insert Screenshot Here]")
    doc.add_paragraph("Figure 2 - Platform Resources Deployment Architecture")

    # 3. Repository Structure
    doc.add_heading("3. Repository Structure", 1)
    doc.add_paragraph("")
    doc.add_paragraph("Key deployment files:")

    table = doc.add_table(rows=12, cols=2)
    table.style = "Light Grid Accent 1"
    table.rows[0].cells[0].text = "File / Directory"
    table.rows[0].cells[1].text = "Purpose"
    table.rows[1].cells[0].text = ".github/workflows/iac.yaml"
    table.rows[1].cells[1].text = "Main trigger workflow (Trigger Foundry Setup)"
    table.rows[2].cells[0].text = ".github/workflows/platform-deploy.yml"
    table.rows[2].cells[1].text = "Reusable platform deployment workflow"
    table.rows[3].cells[0].text = ".github/workflows/agent-capability-deploy.yml"
    table.rows[3].cells[1].text = "Reusable workflow for agent capability deployment"
    table.rows[4].cells[0].text = "environments/<env>/platform.tfvars"
    table.rows[4].cells[1].text = "Environment-level variables for platform deployment"
    table.rows[5].cells[0].text = "environments/<env>/<segment>/foundry-hub.tfvars"
    table.rows[5].cells[1].text = "Segment-level variables for foundry-hub deployment"
    table.rows[6].cells[0].text = "environments/<env>/<segment>/backend-config-hub.tfvars"
    table.rows[6].cells[1].text = "Terraform backend state configuration for foundry-hub stack"
    table.rows[7].cells[0].text = "iac/platform-hub/"
    table.rows[7].cells[1].text = "Terraform root stack for platform resource deployment"
    table.rows[8].cells[0].text = "iac/capability/foundry-hub/"
    table.rows[8].cells[1].text = "Terraform root stack for foundry-hub capability deployment"
    table.rows[9].cells[0].text = "iac/modules/platform/"
    table.rows[9].cells[1].text = "Reusable Terraform module implementation for platform resources"
    table.rows[10].cells[0].text = "iac/modules/foundry-hub/"
    table.rows[10].cells[1].text = "Reusable Terraform module implementation for foundry-hub resources"
    table.rows[11].cells[0].text = "iac/foundry_hub_configs/<segment>/config.yaml"
    table.rows[11].cells[1].text = "Segment configuration metadata used by deployment flows"

    doc.add_paragraph("")
    doc.add_paragraph("[Insert Screenshot Here]")
    doc.add_paragraph("Figure 3 - Platform Deployment Repository Structure")
    doc.add_paragraph("")

    # 4. Configuration Update
    doc.add_heading("4. Configuration Update", 1)
    doc.add_paragraph("1. Service Now request is approved with platform details (environment, segment, location)")
    doc.add_paragraph("2. Team updates environment and segment tfvars/backend config files")
    doc.add_paragraph("3. Team creates Pull Request with platform config changes")
    doc.add_paragraph("4. Reviewer approves PR")
    doc.add_paragraph("5. Merge to main branch triggers workflow readiness")
    doc.add_paragraph("")
    doc.add_paragraph("Config entry example:")
    doc.add_paragraph("# environments/dv/platform.tfvars")
    doc.add_paragraph("platform_location = \"westeurope\"")
    doc.add_paragraph("project_segment  = \"marketing\"")
    doc.add_paragraph("")
    doc.add_paragraph("# environments/dv/marketing/foundry-hub.tfvars")
    doc.add_paragraph("resource_index = \"mkt001\"")
    doc.add_paragraph("resource_subnet = \"<approved_subnet>\"")
    doc.add_paragraph("")
    doc.add_paragraph("[Insert Screenshot Here]")
    doc.add_paragraph("Figure 4 - Platform Configuration Update")

    # 5. Pull Request Process
    doc.add_heading("5. Pull Request Process", 1)
    doc.add_paragraph("1. Team creates PR against main branch with updated platform files")
    doc.add_paragraph("2. PR reviewers verify:")
    doc.add_paragraph("Service Now ticket reference is included", style="List Bullet 2")
    doc.add_paragraph("Environment and segment values match approved request", style="List Bullet 2")
    doc.add_paragraph("Backend and tfvars changes are correct", style="List Bullet 2")
    doc.add_paragraph("3. Approval -> Merge to main branch")
    doc.add_paragraph("4. Merge automatically triggers GitHub Actions readiness")
    doc.add_paragraph("5. Config is now available for pipeline consumption")
    doc.add_paragraph("")
    doc.add_paragraph("Figure 5 - Pull Request Creation")

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
    doc.add_paragraph("platform-hub-plan runs using environments/[env]/platform.tfvars")
    doc.add_paragraph("foundry-hub-plan runs using environments/[env]/[segment]/foundry-hub.tfvars")
    doc.add_paragraph("Terraform initializes backends from backend-config-platform.tfvars and backend-config-hub.tfvars")
    doc.add_paragraph("Plan outputs saved as tfplan artifacts for apply stages")
    doc.add_paragraph("")
    doc.add_paragraph("Validation: Review plan outputs for platform and foundry-hub resource changes")
    doc.add_paragraph("")
    doc.add_paragraph("Figure 7 - Workflow Trigger Inputs")
    doc.add_paragraph("")
    doc.add_paragraph("Figure 8 - Terraform Plan Execution")

    # 7. Terraform Apply
    doc.add_heading("7. Terraform Apply", 1)
    doc.add_paragraph("Prerequisites: terraform plan completed successfully AND manual approval provided")
    doc.add_paragraph("Branch condition: Apply only runs if branch = 'updated-foundry-deployment'")
    doc.add_paragraph("")
    doc.add_paragraph("Approval gate:")
    doc.add_paragraph("1. Plan completes -> automatic pause at environment-approval gate")
    doc.add_paragraph("2. Authorized reviewer approves in GitHub Environments UI")
    doc.add_paragraph("3. Apply automatically triggered after approval")
    doc.add_paragraph("")
    doc.add_paragraph("Apply execution:")
    doc.add_paragraph("Terraform downloads tfplan artifacts from plan stages")
    doc.add_paragraph("Applies configuration in order: platform-hub-apply then foundry-hub-deployment")
    doc.add_paragraph("Creates Azure resources:", style="List Bullet")
    doc.add_paragraph("Platform hub baseline resources", style="List Bullet 2")
    doc.add_paragraph("Foundry hub resources for approved segment", style="List Bullet 2")
    doc.add_paragraph("Role assignments and private connectivity components", style="List Bullet 2")
    doc.add_paragraph("Environment-ready shared infrastructure", style="List Bullet 2")
    doc.add_paragraph("")
    doc.add_paragraph("Outcome: Platform resources are provisioned and ready for downstream use-case onboarding.")
    doc.add_paragraph("")
    doc.add_paragraph("Figure 9 - Deployment Approval Gate")
    doc.add_paragraph("")
    doc.add_paragraph("Figure 10 - Terraform Apply Execution")
    doc.add_paragraph("")
    doc.add_paragraph("Figure 11 - Azure Resources Created")

    doc.save(out)
    print(f"Created: {out}")


if __name__ == "__main__":
    main()
