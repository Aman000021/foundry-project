from docx import Document
from docx.shared import Pt


def add_placeholder(doc, code, title, source, capture, highlight, size, caption):
    doc.add_paragraph(f"SCREENSHOT PLACEHOLDER {code}: {title}")
    doc.add_paragraph(f"Source: {source}", style="List Bullet")
    doc.add_paragraph(f"Capture: {capture}", style="List Bullet")
    doc.add_paragraph(f"Highlight: {highlight}", style="List Bullet")
    doc.add_paragraph(f"Size: {size}", style="List Bullet")
    doc.add_paragraph(f"Caption: {caption}", style="List Bullet")
    doc.add_paragraph("")


def add_repo_table(doc, rows):
    table = doc.add_table(rows=len(rows) + 1, cols=2)
    table.style = "Light Grid Accent 1"
    table.rows[0].cells[0].text = "File / Directory"
    table.rows[0].cells[1].text = "Purpose"
    for idx, (path, purpose) in enumerate(rows, start=1):
        table.rows[idx].cells[0].text = path
        table.rows[idx].cells[1].text = purpose


def build_agent_doc(path):
    doc = Document()
    doc.add_heading("Agent Service Infrastructure Deployment Guide (Call-Aligned)", 0)

    doc.add_heading("1. Scope and Overview", 1)
    doc.add_paragraph(
        "This document is only for Terraform infrastructure provisioning related to Agent Service onboarding. "
        "It does not cover agent application deployment or hello-world app deployment."
    )
    doc.add_paragraph(
        "Call alignment: Agent infra flow creates Foundry Project and IAM role assignments after approved request and pipeline execution."
    )
    doc.add_paragraph(
        "Flow: Service Now approved request -> config update -> PR review and merge -> Trigger Foundry Setup (Deploy Dev/Prod Agent Service) -> Terraform plan -> approval gate -> Terraform apply -> Foundry Project and IAM created"
    )
    add_placeholder(
        doc,
        "A1",
        "High-level Agent Infra Flow",
        "draw.io or architecture tool",
        "Only onboarding infra flow blocks from Service Now to Terraform apply",
        "Trigger workflow, plan/apply, Foundry Project, IAM",
        "16 cm x 8 cm",
        "Figure 1 - High-Level Agent Service Infra Deployment Flow",
    )

    doc.add_heading("2. Prerequisites (from call)", 1)
    doc.add_paragraph("Mandatory prerequisites before onboarding request:")
    doc.add_paragraph("AD group for Project Manager role", style="List Bullet")
    doc.add_paragraph("AD group for Foundry User role", style="List Bullet")
    doc.add_paragraph("Service Now approved onboarding request", style="List Bullet")
    doc.add_paragraph("GitHub repository request can be optional/manual based on process", style="List Bullet")

    doc.add_heading("3. Repository and Workflow Files", 1)
    add_repo_table(
        doc,
        [
            ("iac/project_configs/marketing/config.yaml", "Project entries used for Foundry project provisioning"),
            (".github/workflows/iac.yaml", "Manual trigger workflow: Trigger Foundry Setup"),
            (".github/workflows/agent-capability-deploy.yml", "Agent infra reusable deployment workflow"),
            ("environments/dv/marketing/agent-service.tfvars", "Environment and segment values"),
            ("environments/dv/marketing/backend-config-project.tfvars", "Backend state config for agent project deployment"),
            ("iac/capability/agent-service/", "Terraform root for Foundry project and IAM resources"),
        ],
    )
    add_placeholder(
        doc,
        "A2",
        "Agent Repo Structure",
        "GitHub repository tree",
        "Root tree with iac/, environments/, .github/workflows/",
        "config.yaml, iac.yaml, agent-capability-deploy.yml",
        "15 cm x 8 cm",
        "Figure 2 - Agent Deployment Repository Structure",
    )

    doc.add_heading("4. Configuration Update Process", 1)
    doc.add_paragraph("1. Add approved use-case/project row in config.yaml")
    doc.add_paragraph("2. Ensure segment, foundry index, and manager IDs match approved request")
    doc.add_paragraph("3. Raise PR and complete reviewer approval")
    doc.add_paragraph("4. Merge to deployment branch/process branch")
    add_placeholder(
        doc,
        "A3",
        "Agent Config Entry",
        "iac/project_configs/marketing/config.yaml",
        "Only one project entry block",
        "project_name, project_segment, foundry_index, project_manager_group_id, project_manager_user_id",
        "15 cm x 4 cm",
        "Figure 3 - Agent Project Configuration Entry",
    )

    doc.add_heading("5. Pipeline Trigger and Plan", 1)
    doc.add_paragraph("Trigger workflow: .github/workflows/iac.yaml")
    doc.add_paragraph("Choice: Deploy Dev Agent Service or Deploy Prod Agent Service")
    doc.add_paragraph("Plan uses agent-capability-deploy.yml and creates tfplan artifact")
    add_placeholder(
        doc,
        "A4",
        "Workflow Trigger Inputs",
        "GitHub Actions - Trigger Foundry Setup",
        "Run workflow panel for Agent Service option",
        "choice, segment, location",
        "15 cm x 6 cm",
        "Figure 4 - Agent Workflow Trigger Inputs",
    )
    add_placeholder(
        doc,
        "A5",
        "Terraform Plan Job",
        "GitHub Actions job page",
        "Plan job logs",
        "terraform init, terraform plan, success",
        "15 cm x 6 cm",
        "Figure 5 - Agent Terraform Plan Execution",
    )

    doc.add_heading("6. Approval and Apply", 1)
    doc.add_paragraph("Apply runs only when branch condition matches updated-foundry-deployment and environment approval is granted.")
    add_placeholder(
        doc,
        "A6",
        "Environment Approval Gate",
        "GitHub Environments",
        "Pending deployment approval screen",
        "approval action and approver",
        "15 cm x 6 cm",
        "Figure 6 - Agent Deployment Approval Gate",
    )
    add_placeholder(
        doc,
        "A7",
        "Terraform Apply Job",
        "GitHub Actions apply job",
        "Apply stage logs",
        "download artifact, terraform apply, success",
        "15 cm x 6 cm",
        "Figure 7 - Agent Terraform Apply Execution",
    )

    doc.add_heading("7. Outcomes and Validation", 1)
    doc.add_paragraph("Expected outcome after apply:")
    doc.add_paragraph("Foundry Project created for requested segment/use case", style="List Bullet")
    doc.add_paragraph("IAM role assignments created for manager/user groups", style="List Bullet")
    doc.add_paragraph("Resource group creation may be pipeline-driven or separate request, pending final confirmation", style="List Bullet")
    add_placeholder(
        doc,
        "A8",
        "Validation in Azure / Foundry",
        "Azure Portal and Foundry Portal",
        "Created project/resources and IAM assignments",
        "new project name, role assignments",
        "15 cm x 6 cm",
        "Figure 8 - Agent Infra Validation",
    )

    doc.save(path)


def build_platform_doc(path):
    doc = Document()
    doc.add_heading("Platform Resources Deployment Guide (Call-Aligned)", 0)

    doc.add_heading("1. Scope and Overview", 1)
    doc.add_paragraph(
        "This document is for platform and foundry-hub infrastructure deployment only. "
        "It is different from Agent Service project provisioning flow."
    )
    doc.add_paragraph(
        "Call alignment: platform deployment is infra-only and separate from agent app deployment owned by another team."
    )
    doc.add_paragraph(
        "Flow: Service Now approved platform request -> platform/hub config update -> PR review and merge -> Trigger Foundry Setup (Deploy Dev/Prod Platform) -> platform-hub plan/apply -> foundry-hub plan/apply -> platform baseline ready"
    )
    add_placeholder(
        doc,
        "P1",
        "High-level Platform Infra Flow",
        "draw.io or architecture tool",
        "Platform and foundry-hub deployment chain",
        "platform-hub and foundry-hub stages, approvals, apply",
        "16 cm x 8 cm",
        "Figure 1 - High-Level Platform Resources Deployment Flow",
    )

    doc.add_heading("2. Process Difference vs Agent Guide", 1)
    doc.add_paragraph("Platform process provisions shared infra baseline (platform-hub and foundry-hub).", style="List Bullet")
    doc.add_paragraph("Agent process provisions use-case Foundry projects and IAM per request.", style="List Bullet")
    doc.add_paragraph("Neither guide includes agent application deployment steps.", style="List Bullet")

    doc.add_heading("3. Repository and Workflow Files", 1)
    add_repo_table(
        doc,
        [
            (".github/workflows/iac.yaml", "Manual trigger workflow"),
            (".github/workflows/platform-deploy.yml", "Reusable platform and foundry-hub deployment workflow"),
            ("environments/dv/platform.tfvars", "Platform variables"),
            ("environments/dv/backend-config-platform.tfvars", "Platform terraform backend config"),
            ("environments/dv/marketing/foundry-hub.tfvars", "Foundry hub variables for segment"),
            ("environments/dv/marketing/backend-config-hub.tfvars", "Foundry hub backend config"),
            ("iac/platform-hub/", "Terraform root for platform-hub"),
            ("iac/capability/foundry-hub/", "Terraform root for foundry-hub"),
        ],
    )
    add_placeholder(
        doc,
        "P2",
        "Platform Repo Structure",
        "GitHub repository tree",
        "Root tree and workflow files",
        "platform-deploy.yml, platform tfvars, foundry-hub tfvars",
        "15 cm x 8 cm",
        "Figure 2 - Platform Deployment Repository Structure",
    )

    doc.add_heading("4. Configuration Update Process", 1)
    doc.add_paragraph("1. Update platform and foundry-hub tfvars/config with approved values")
    doc.add_paragraph("2. Create PR with clear change summary")
    doc.add_paragraph("3. Complete review and merge")
    add_placeholder(
        doc,
        "P3",
        "Platform Config Update",
        "environments and iac config files",
        "Only changed keys relevant to deployment",
        "segment, location, indices, backend references",
        "15 cm x 4 cm",
        "Figure 3 - Platform Configuration Update",
    )

    doc.add_heading("5. Pipeline Trigger and Plan", 1)
    doc.add_paragraph("Trigger workflow: .github/workflows/iac.yaml")
    doc.add_paragraph("Choice: Deploy Dev Platform or Deploy Prod Platform")
    doc.add_paragraph("platform-deploy.yml runs plan in two tracks: platform-hub-plan and foundry-hub-plan")
    add_placeholder(
        doc,
        "P4",
        "Platform Workflow Trigger Inputs",
        "GitHub Actions - Trigger Foundry Setup",
        "Run workflow panel for Platform option",
        "choice, segment, location",
        "15 cm x 6 cm",
        "Figure 4 - Platform Workflow Trigger Inputs",
    )
    add_placeholder(
        doc,
        "P5",
        "Platform Plan Jobs",
        "GitHub Actions jobs",
        "platform-hub-plan and foundry-hub-plan logs",
        "terraform init and terraform plan status",
        "15 cm x 6 cm",
        "Figure 5 - Platform and Foundry-Hub Plan Execution",
    )

    doc.add_heading("6. Approval and Apply", 1)
    doc.add_paragraph("Apply runs after approval gates when branch condition is updated-foundry-deployment.")
    doc.add_paragraph("Apply order in workflow: platform-hub-apply first, then foundry-hub-deployment.")
    add_placeholder(
        doc,
        "P6",
        "Platform Approval Gate",
        "GitHub Environments",
        "Pending approval for platform/foundry-hub",
        "approval status and approver",
        "15 cm x 6 cm",
        "Figure 6 - Platform Deployment Approval Gate",
    )
    add_placeholder(
        doc,
        "P7",
        "Platform Apply Jobs",
        "GitHub Actions apply jobs",
        "platform-hub-apply and foundry-hub-deployment logs",
        "download artifact, terraform apply, success",
        "15 cm x 6 cm",
        "Figure 7 - Platform Terraform Apply Execution",
    )

    doc.add_heading("7. Outcomes and Validation", 1)
    doc.add_paragraph("Expected outcome after apply:")
    doc.add_paragraph("Platform hub baseline resources created", style="List Bullet")
    doc.add_paragraph("Foundry hub resources created for segment", style="List Bullet")
    doc.add_paragraph("Shared infra ready for downstream use-case onboarding", style="List Bullet")
    add_placeholder(
        doc,
        "P8",
        "Platform Validation in Azure",
        "Azure Portal",
        "Resource groups/resources created by platform and foundry-hub apply",
        "new platform resources and hub resources",
        "15 cm x 6 cm",
        "Figure 8 - Platform Infrastructure Validation",
    )

    doc.save(path)


def main():
    agent_out = r"c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_v4.docx"
    platform_out = r"c:\Users\XSPriyaGa\Downloads\Platform_Resources_Deployment_Guide_Updated_v4.docx"

    build_agent_doc(agent_out)
    build_platform_doc(platform_out)

    print(f"Created: {agent_out}")
    print(f"Created: {platform_out}")


if __name__ == "__main__":
    main()
