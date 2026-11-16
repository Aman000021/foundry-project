from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches, Pt

BASE_DIR = Path(__file__).parent
SHOT_DIR = BASE_DIR / "screenshots" / "actions" / "cropped"

PLATFORM_DOCX = BASE_DIR / "Platform_Resources_Deployment_Guide_DETAILED.docx"
AGENT_DOCX = BASE_DIR / "Agent_Service_Deployment_Guide_DETAILED.docx"

PLATFORM_YAML = """# iac/foundry_hub_configs/marketing/config.yaml
- resource_index: "mkt001"
  resource_subnet: "emna-np-g.2-adi-euwe-001-snt"

- resource_index: "mkt002"
  resource_subnet: "emna-np-g.3-adi-euwe-001-snt"

- resource_index: "mkt003"
  resource_subnet: "emna-np-g.3-adi-euwe-001-snt"
""".strip()

AGENT_YAML = """# iac/project_configs/marketing/config.yaml
- project_name: redeploy01
  project_segment: marketing
  foundry_index: "mkt001"
  project_manager_group_id: <aad-group-object-id>
  project_manager_user_id: <aad-user-or-group-object-id>

- project_name: redeploy02
  project_segment: marketing
  foundry_index: "mkt001"
  project_manager_group_id: <aad-group-object-id>
  project_manager_user_id: <aad-user-or-group-object-id>

- project_name: redeploy03
  project_segment: marketing
  foundry_index: "mkt002"
  project_manager_group_id: <aad-group-object-id>
  project_manager_user_id: <aad-user-or-group-object-id>""".strip()


def add_title(doc: Document, title: str, subtitle: str) -> None:
    p = doc.add_paragraph()
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(22)
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    p2 = doc.add_paragraph()
    r2 = p2.add_run(subtitle)
    r2.font.size = Pt(13)
    p2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    meta = doc.add_paragraph()
    meta.add_run(f"Prepared on: {date.today().isoformat()}\\nRepository: npet-foundry-template")
    meta.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


def h1(doc: Document, text: str) -> None:
    doc.add_heading(text, level=1)


def h2(doc: Document, text: str) -> None:
    doc.add_heading(text, level=2)


def bullet(doc: Document, text: str) -> None:
    doc.add_paragraph(text, style="List Bullet")


def num(doc: Document, text: str) -> None:
    doc.add_paragraph(text, style="List Number")


def code_block(doc: Document, text: str) -> None:
    for line in text.splitlines():
        p = doc.add_paragraph()
        run = p.add_run(line)
        run.font.name = "Consolas"
        run.font.size = Pt(9)


def add_screenshot(doc: Document, image_name: str, caption: str) -> None:
    path = SHOT_DIR / image_name
    if path.exists():
        doc.add_picture(str(path), width=Inches(6.3))
        cp = doc.add_paragraph(caption)
        cp.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


def table_of_contents(doc: Document) -> None:
    h1(doc, "Table of Contents")
    num(doc, "Overview of Deployment")
    num(doc, "Deployment Steps")
    num(doc, "Configuration YAML and Input Mapping")
    num(doc, "Validation")


def platform_doc() -> None:
    doc = Document()
    add_title(doc, "Platform Resources Deployment Guide", "Detailed Visual Guide")
    table_of_contents(doc)

    h1(doc, "Overview of Deployment")
    bullet(doc, "Purpose: deploy shared platform resources and Foundry hub resources.")
    bullet(doc, "Trigger: .github/workflows/iac.yaml -> choice = Deploy Dev Platform / Deploy Prod Platform.")
    bullet(doc, "Reusable workflow: .github/workflows/platform-deploy.yml.")
    bullet(doc, "Terraform folders: iac/platform-hub and iac/capability/foundry-hub.")
    bullet(doc, "Branch gate: apply runs when branch is updated-foundry-deployment.")

    add_screenshot(doc, "01_actions_overview_annotated_cropped.png", "GitHub Actions overview with target workflow")
    add_screenshot(doc, "05_trigger_workflow_page_cropped.jpg", "Trigger workflow page")

    h1(doc, "Deployment Steps")
    h2(doc, "Step 1 - Trigger")
    num(doc, "Open GitHub Actions and run Trigger Foundry Setup.")
    num(doc, "Select choice = Deploy Dev Platform or Deploy Prod Platform.")
    num(doc, "Set segment and location.")
    add_screenshot(doc, "02_run_workflow_inputs_annotated_cropped.png", "Required input fields before run")

    h2(doc, "Step 2 - Plan Jobs")
    num(doc, "platform-hub-plan: terraform init + terraform plan with platform tfvars.")
    num(doc, "foundry-hub-plan: terraform init + terraform plan with foundry-hub tfvars and segment/location vars.")
    add_screenshot(doc, "07_plan_job_page_cropped.jpg", "Plan job details")

    h2(doc, "Step 3 - Approval and Apply")
    num(doc, "Manual approval executes for branch-gated deployment.")
    num(doc, "platform-hub-apply runs terraform apply tfplan.")
    num(doc, "foundry-hub-deployment runs terraform apply tfplan.")
    add_screenshot(doc, "08_apply_job_page_cropped.jpg", "Apply job details")

    h2(doc, "Step 4 - End-to-End Run View")
    num(doc, "Verify run graph contains platform and hub sequence.")
    add_screenshot(doc, "03_run_summary_graph_annotated_cropped.png", "Run graph and dependency flow")
    add_screenshot(doc, "06_run_summary_page_cropped.jpg", "Run summary page")

    h1(doc, "Configuration YAML and Input Mapping")
    h2(doc, "Workflow Input to Terraform")
    bullet(doc, "choice, segment, location are captured by iac.yaml.")
    bullet(doc, "segment and location are passed into platform-deploy.yml and then into terraform -var and -var-file.")

    h2(doc, "Foundry Hub YAML")
    bullet(doc, "File: iac/foundry_hub_configs/marketing/config.yaml")
    bullet(doc, "resource_index maps each hub resource key used by Terraform loops.")
    bullet(doc, "resource_subnet maps private endpoint subnet per resource.")
    code_block(doc, PLATFORM_YAML)

    h2(doc, "Full Platform Flow (Config -> Plan -> Apply)")
    num(doc, "Input segment selects environment/<env>/<segment>/foundry-hub.tfvars.")
    num(doc, "YAML entries are read by Terraform locals in module path and iterated in resources.")
    num(doc, "Plan creates delta for platform and hub resources.")
    num(doc, "Apply executes approved tfplan and commits infra changes to state.")

    h1(doc, "Validation")
    num(doc, "Check workflow run is green for platform-hub-plan and foundry-hub-plan.")
    num(doc, "If deployment branch gate applies, confirm approval and apply jobs are green.")
    num(doc, "Confirm resources in Azure: shared platform resources and Foundry hub resources.")
    num(doc, "Confirm private endpoint/subnet mapping matches YAML configuration.")
    num(doc, "Archive run URL, environment, segment, location, and commit for audit.")

    doc.save(str(PLATFORM_DOCX))


def agent_doc() -> None:
    doc = Document()
    add_title(doc, "Agent Service Deployment Guide", "Detailed Visual Guide")
    table_of_contents(doc)

    h1(doc, "Overview of Deployment")
    bullet(doc, "Purpose: deploy Foundry projects and project-level IAM assignments.")
    bullet(doc, "Trigger: .github/workflows/iac.yaml -> choice = Deploy Dev Agent Service / Deploy Prod Agent Service.")
    bullet(doc, "Reusable workflow: .github/workflows/agent-capability-deploy.yml.")
    bullet(doc, "Terraform folder: iac/capability/agent-service.")
    bullet(doc, "Branch gate: apply runs when branch is updated-foundry-deployment.")

    add_screenshot(doc, "01_actions_overview_annotated_cropped.png", "GitHub Actions overview with target workflow")
    add_screenshot(doc, "05_trigger_workflow_page_cropped.jpg", "Trigger workflow page")

    h1(doc, "Deployment Steps")
    h2(doc, "Step 1 - Trigger")
    num(doc, "Open GitHub Actions and run Trigger Foundry Setup.")
    num(doc, "Select choice = Deploy Dev Agent Service or Deploy Prod Agent Service.")
    num(doc, "Set segment and location.")
    add_screenshot(doc, "02_run_workflow_inputs_annotated_cropped.png", "Required input fields before run")

    h2(doc, "Step 2 - Plan Job")
    num(doc, "Run terraform init with backend-config-project.tfvars.")
    num(doc, "Run terraform plan with agent-service.tfvars plus project_segment and foundry_location.")
    num(doc, "Upload tfplan artifact for apply stage.")
    add_screenshot(doc, "07_plan_job_page_cropped.jpg", "Plan job details")

    h2(doc, "Step 3 - Approval and Apply")
    num(doc, "Manual approval executes for branch-gated deployment.")
    num(doc, "Apply job downloads tfplan and runs terraform apply tfplan.")
    add_screenshot(doc, "08_apply_job_page_cropped.jpg", "Apply job details")

    h2(doc, "Step 4 - End-to-End Run View")
    num(doc, "Verify plan -> approval -> apply progression in run graph.")
    add_screenshot(doc, "03_run_summary_graph_annotated_cropped.png", "Run graph and dependency flow")
    add_screenshot(doc, "06_run_summary_page_cropped.jpg", "Run summary page")

    h1(doc, "Configuration YAML and Input Mapping")
    h2(doc, "Workflow Input to Terraform")
    bullet(doc, "segment and location values from iac.yaml are passed into agent-capability-deploy.yml.")
    bullet(doc, "These feed terraform -var=project_segment and -var=foundry_location.")

    h2(doc, "Project YAML")
    bullet(doc, "File: iac/project_configs/marketing/config.yaml")
    bullet(doc, "Each list item creates one Foundry project instance.")
    bullet(doc, "foundry_index maps each project to a specific hub resource.")
    bullet(doc, "project_manager_group_id and project_manager_user_id map IAM principals.")
    code_block(doc, AGENT_YAML)

    h2(doc, "Full Agent-Service Flow (Config -> Plan -> Apply)")
    num(doc, "segment selects environment/<env>/<segment>/agent-service.tfvars and matching project YAML records.")
    num(doc, "Terraform locals parse YAML list and iterate project resources and role assignments.")
    num(doc, "Plan shows project and IAM deltas.")
    num(doc, "Apply creates/updates project resources and role bindings in Azure.")

    h1(doc, "Validation")
    num(doc, "Check plan, approval, and apply jobs are green.")
    num(doc, "Verify Foundry projects exist in target hub based on foundry_index.")
    num(doc, "Verify IAM role assignments for manager and user principals at project scope.")
    num(doc, "Validate project access with both AD principals.")
    num(doc, "Archive run URL, environment, segment, location, and commit for audit.")

    doc.save(str(AGENT_DOCX))


if __name__ == "__main__":
    platform_doc()
    agent_doc()
    print("Generated:")
    print(PLATFORM_DOCX)
    print(AGENT_DOCX)
