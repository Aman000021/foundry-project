from docx import Document


def add_placeholder(doc, title, caption):
    doc.add_paragraph(f"Screenshot Placeholder: [Insert Screenshot Here] - {title}")
    doc.add_paragraph("Capture Guidance: Use rectangular crop, 16:9 ratio, focus only on relevant area.")
    doc.add_paragraph(f"Caption: {caption}")
    doc.add_paragraph("")


def add_table(doc, rows):
    table = doc.add_table(rows=len(rows) + 1, cols=2)
    table.style = "Light Grid Accent 1"
    table.rows[0].cells[0].text = "File / Directory"
    table.rows[0].cells[1].text = "Purpose"
    for idx, (path, purpose) in enumerate(rows, start=1):
        table.rows[idx].cells[0].text = path
        table.rows[idx].cells[1].text = purpose


def build_agent_doc(path):
    doc = Document()
    doc.add_heading("Agent Service Deployment Guide (Call-Aligned, Placeholder Version)", 0)

    doc.add_heading("1. Overview", 1)
    doc.add_paragraph(
        "Purpose: This guide covers only infrastructure onboarding for Agent Service requests. "
        "It does not cover agent application deployment."
    )
    doc.add_paragraph(
        "Flow: Service Now request approved -> Config update -> PR approved and merged -> "
        "Trigger Foundry Setup (Agent Service option) -> Terraform Plan -> Approval -> Terraform Apply -> "
        "Foundry Project and IAM roles created"
    )
    add_placeholder(
        doc,
        "High-level agent onboarding infrastructure flow",
        "Figure 1 - High-Level Agent Service Deployment Flow",
    )

    doc.add_heading("2. Scope and Process Difference", 1)
    doc.add_paragraph("Agent process provisions use-case project infrastructure.")
    doc.add_paragraph("Creates Foundry project and project-level IAM assignments.")
    doc.add_paragraph("This is different from Platform process, which provisions shared platform/hub baseline.")
    add_placeholder(
        doc,
        "Agent infrastructure architecture (Service Now to Terraform apply)",
        "Figure 2 - Agent Service Deployment Architecture",
    )

    doc.add_heading("3. Repository Structure", 1)
    doc.add_paragraph("Key deployment files:")
    add_table(
        doc,
        [
            ("iac/project_configs/marketing/config.yaml", "Project definitions from approved request"),
            (".github/workflows/iac.yaml", "Main trigger workflow (Trigger Foundry Setup)"),
            (".github/workflows/agent-capability-deploy.yml", "Agent deployment workflow"),
            ("environments/dv/marketing/agent-service.tfvars", "Environment-specific variables"),
            ("environments/dv/marketing/backend-config-project.tfvars", "Terraform backend configuration"),
            ("iac/capability/agent-service/", "Terraform code for agent project provisioning"),
        ],
    )
    add_placeholder(
        doc,
        "Repository tree with iac, environments, and workflow files",
        "Figure 3 - Agent Deployment Repository Structure",
    )

    doc.add_heading("4. Prerequisites and Configuration Update", 1)
    doc.add_paragraph("Prerequisites from call discussion:")
    doc.add_paragraph("AD group for Project Manager role", style="List Bullet")
    doc.add_paragraph("AD group for Foundry User role", style="List Bullet")
    doc.add_paragraph("Service Now approved request", style="List Bullet")
    doc.add_paragraph("GitHub repo creation can be separate/optional per process", style="List Bullet")
    doc.add_paragraph("Configuration steps:")
    doc.add_paragraph("1. Update config.yaml with approved project details")
    doc.add_paragraph("2. Raise PR and complete review")
    doc.add_paragraph("3. Merge to deployment branch")
    add_placeholder(
        doc,
        "Config.yaml entry with project_name, segment, index, manager and user IDs",
        "Figure 4 - Agent Project Configuration Entry",
    )

    doc.add_heading("5. Pull Request Process", 1)
    doc.add_paragraph("1. Create PR with config.yaml changes")
    doc.add_paragraph("2. Verify request mapping and group IDs")
    doc.add_paragraph("3. Approve and merge")
    add_placeholder(
        doc,
        "PR creation and approval details",
        "Figure 5 - Agent Pull Request Approval and Merge",
    )

    doc.add_heading("6. Terraform Plan", 1)
    doc.add_paragraph("Trigger workflow with Agent Service option in iac.yaml.")
    doc.add_paragraph("Plan job runs in agent-capability-deploy.yml and uploads tfplan artifact.")
    add_placeholder(
        doc,
        "Workflow trigger input panel (choice, segment, location)",
        "Figure 6 - Agent Workflow Trigger Inputs",
    )
    add_placeholder(
        doc,
        "Terraform plan job execution logs",
        "Figure 7 - Agent Terraform Plan Execution",
    )

    doc.add_heading("7. Terraform Apply", 1)
    doc.add_paragraph("Apply runs only after approval and branch condition checks.")
    doc.add_paragraph("Branch gate: updated-foundry-deployment")
    add_placeholder(
        doc,
        "Environment approval gate",
        "Figure 8 - Agent Deployment Approval Gate",
    )
    add_placeholder(
        doc,
        "Terraform apply job execution",
        "Figure 9 - Agent Terraform Apply Execution",
    )

    doc.add_heading("8. Outcome and Validation", 1)
    doc.add_paragraph("Expected outcomes:")
    doc.add_paragraph("Foundry Project created", style="List Bullet")
    doc.add_paragraph("IAM roles assigned to approved groups", style="List Bullet")
    doc.add_paragraph("Resource group creation follows current agreed process", style="List Bullet")
    add_placeholder(
        doc,
        "Validation in Foundry and Azure IAM",
        "Figure 10 - Agent Deployment Validation",
    )

    doc.save(path)


def build_platform_doc(path):
    doc = Document()
    doc.add_heading("Platform Resources Deployment Guide (Call-Aligned, Placeholder Version)", 0)

    doc.add_heading("1. Overview", 1)
    doc.add_paragraph(
        "Purpose: This guide covers only platform infrastructure deployment. "
        "It does not cover Agent Service project provisioning or application deployment."
    )
    doc.add_paragraph(
        "Flow: Service Now request approved -> Platform/hub config update -> PR approved and merged -> "
        "Trigger Foundry Setup (Platform option) -> Platform-hub Plan/Apply -> Foundry-hub Plan/Apply -> "
        "Shared platform baseline ready"
    )
    add_placeholder(
        doc,
        "High-level platform infrastructure flow",
        "Figure 1 - High-Level Platform Resources Deployment Flow",
    )

    doc.add_heading("2. Scope and Process Difference", 1)
    doc.add_paragraph("Platform process provisions shared baseline infrastructure.")
    doc.add_paragraph("Runs platform-hub and foundry-hub stages in platform workflow.")
    doc.add_paragraph("This is different from Agent process, which provisions use-case project resources.")
    add_placeholder(
        doc,
        "Platform deployment architecture (shared infra only)",
        "Figure 2 - Platform Deployment Architecture",
    )

    doc.add_heading("3. Repository Structure", 1)
    doc.add_paragraph("Key deployment files:")
    add_table(
        doc,
        [
            (".github/workflows/iac.yaml", "Main trigger workflow"),
            (".github/workflows/platform-deploy.yml", "Platform and foundry-hub deployment workflow"),
            ("environments/dv/platform.tfvars", "Platform variables"),
            ("environments/dv/backend-config-platform.tfvars", "Platform backend configuration"),
            ("environments/dv/marketing/foundry-hub.tfvars", "Foundry-hub variables"),
            ("environments/dv/marketing/backend-config-hub.tfvars", "Foundry-hub backend configuration"),
            ("iac/platform-hub/", "Terraform code for platform-hub"),
            ("iac/capability/foundry-hub/", "Terraform code for foundry-hub"),
        ],
    )
    add_placeholder(
        doc,
        "Repository tree with platform and foundry-hub deployment files",
        "Figure 3 - Platform Deployment Repository Structure",
    )

    doc.add_heading("4. Prerequisites and Configuration Update", 1)
    doc.add_paragraph("Prerequisites:")
    doc.add_paragraph("Approved Service Now request for platform onboarding", style="List Bullet")
    doc.add_paragraph("Required segment and location values", style="List Bullet")
    doc.add_paragraph("Configuration steps:")
    doc.add_paragraph("1. Update platform and foundry-hub variable files")
    doc.add_paragraph("2. Raise PR and complete review")
    doc.add_paragraph("3. Merge to deployment branch")
    add_placeholder(
        doc,
        "Platform/foundry-hub config update section",
        "Figure 4 - Platform Configuration Update",
    )

    doc.add_heading("5. Pull Request Process", 1)
    doc.add_paragraph("1. Create PR with platform config changes")
    doc.add_paragraph("2. Validate env, segment, and backend references")
    doc.add_paragraph("3. Approve and merge")
    add_placeholder(
        doc,
        "PR creation and approval for platform flow",
        "Figure 5 - Platform Pull Request Approval and Merge",
    )

    doc.add_heading("6. Terraform Plan", 1)
    doc.add_paragraph("Trigger workflow with Platform option in iac.yaml.")
    doc.add_paragraph("Plan jobs run in platform-deploy.yml for platform-hub and foundry-hub.")
    add_placeholder(
        doc,
        "Workflow trigger input panel (platform choice)",
        "Figure 6 - Platform Workflow Trigger Inputs",
    )
    add_placeholder(
        doc,
        "Plan execution for platform-hub and foundry-hub",
        "Figure 7 - Platform Terraform Plan Execution",
    )

    doc.add_heading("7. Terraform Apply", 1)
    doc.add_paragraph("Apply runs after approval and branch gate checks.")
    doc.add_paragraph("Apply order: platform-hub-apply, then foundry-hub-deployment.")
    add_placeholder(
        doc,
        "Environment approval gate",
        "Figure 8 - Platform Deployment Approval Gate",
    )
    add_placeholder(
        doc,
        "Apply execution for platform and foundry-hub",
        "Figure 9 - Platform Terraform Apply Execution",
    )

    doc.add_heading("8. Outcome and Validation", 1)
    doc.add_paragraph("Expected outcomes:")
    doc.add_paragraph("Platform shared resources created", style="List Bullet")
    doc.add_paragraph("Foundry-hub resources created", style="List Bullet")
    doc.add_paragraph("Baseline ready for downstream use-case onboarding", style="List Bullet")
    add_placeholder(
        doc,
        "Validation in Azure for platform resources",
        "Figure 10 - Platform Deployment Validation",
    )

    doc.save(path)


def main():
    agent_path = r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs\Agent_Service_Deployment_Guide_Updated_v6_PLACEHOLDERS_ONLY.docx"
    platform_path = r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs\Platform_Resources_Deployment_Guide_Updated_v6_PLACEHOLDERS_ONLY.docx"

    build_agent_doc(agent_path)
    build_platform_doc(platform_path)

    print(f"Created: {agent_path}")
    print(f"Created: {platform_path}")


if __name__ == "__main__":
    main()
