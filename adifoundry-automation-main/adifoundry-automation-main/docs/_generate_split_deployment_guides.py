from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt

BASE_DIR = Path(__file__).parent


def _add_title(doc: Document, title: str) -> None:
    p = doc.add_paragraph()
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(20)
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    meta = doc.add_paragraph()
    meta.add_run(f"Prepared on: {date.today().isoformat()}\nRepository: npet-foundry-template")
    meta.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    doc.add_paragraph("")


def _h1(doc: Document, text: str) -> None:
    doc.add_heading(text, level=1)


def _num(doc: Document, text: str) -> None:
    doc.add_paragraph(text, style="List Number")


def _bullet(doc: Document, text: str) -> None:
    doc.add_paragraph(text, style="List Bullet")


def build_platform_doc() -> None:
    doc = Document()
    _add_title(doc, "Platform Resources Deployment Guide")

    _h1(doc, "Table of Contents")
    _num(doc, "Overview of Deployment")
    _num(doc, "Deployment Steps")
    _num(doc, "Validation")

    _h1(doc, "Overview of Deployment")
    doc.add_paragraph(
        "This guide covers the platform pipeline that provisions and updates shared infrastructure required for Foundry onboarding."
    )
    _bullet(doc, "Trigger workflow: Trigger Foundry Setup (.github/workflows/iac.yaml)")
    _bullet(doc, "Reusable workflow: Platform and Foundry Resource Deployment (.github/workflows/platform-deploy.yml)")
    _bullet(doc, "Terraform stacks: iac/platform-hub and iac/capability/foundry-hub")
    _bullet(doc, "Plan jobs always run for this pipeline selection")
    _bullet(doc, "Apply jobs are gated by branch value: updated-foundry-deployment")

    _h1(doc, "Deployment Steps")
    _num(doc, "Run Trigger Foundry Setup in GitHub Actions.")
    _num(doc, "Select Deploy Dev Platform or Deploy Prod Platform in the choice input.")
    _num(doc, "Provide segment and location inputs.")
    _num(doc, "Pipeline runs platform-hub terraform init/plan and uploads tfplan artifact.")
    _num(doc, "Pipeline runs foundry-hub terraform init/plan and uploads tfplan artifact.")
    _num(doc, "If branch is updated-foundry-deployment, manual approval and apply jobs execute.")
    _num(doc, "Apply uses the uploaded tfplan artifacts to deploy platform and foundry hub changes.")

    _h1(doc, "Validation")
    _num(doc, "Confirm platform-hub and foundry-hub plan jobs succeeded.")
    _num(doc, "Confirm approval and apply jobs executed when branch condition is met.")
    _num(doc, "Verify tfplan artifacts were uploaded and consumed successfully.")
    _num(doc, "Validate platform and foundry hub resources in Azure portal.")
    _num(doc, "Verify private endpoint and connectivity status for the selected segment.")

    out = BASE_DIR / "Platform_Resources_Deployment_Guide.docx"
    doc.save(str(out))


def build_agent_doc() -> None:
    doc = Document()
    _add_title(doc, "Agent Service Deployment Guide")

    _h1(doc, "Table of Contents")
    _num(doc, "Overview of Deployment")
    _num(doc, "Deployment Steps")
    _num(doc, "Validation")

    _h1(doc, "Overview of Deployment")
    doc.add_paragraph(
        "This guide covers the agent-service pipeline that provisions Foundry projects and project-level role assignments."
    )
    _bullet(doc, "Trigger workflow: Trigger Foundry Setup (.github/workflows/iac.yaml)")
    _bullet(doc, "Reusable workflow: Foundry Project Deployment (.github/workflows/agent-capability-deploy.yml)")
    _bullet(doc, "Terraform stack: iac/capability/agent-service")
    _bullet(doc, "Plan job always runs for this pipeline selection")
    _bullet(doc, "Apply job is gated by branch value: updated-foundry-deployment")

    _h1(doc, "Deployment Steps")
    _num(doc, "Run Trigger Foundry Setup in GitHub Actions.")
    _num(doc, "Select Deploy Dev Agent Service or Deploy Prod Agent Service in the choice input.")
    _num(doc, "Provide segment and location inputs.")
    _num(doc, "Plan job runs terraform init/plan and uploads tfplan artifact.")
    _num(doc, "If branch is updated-foundry-deployment, manual approval job runs.")
    _num(doc, "Apply job downloads tfplan artifact and runs terraform apply tfplan.")

    _h1(doc, "Validation")
    _num(doc, "Confirm plan job succeeded and tfplan artifact exists.")
    _num(doc, "Confirm approval and apply jobs executed when branch condition is met.")
    _num(doc, "Verify Foundry project resources were created/updated in Azure.")
    _num(doc, "Verify project IAM role assignments are present for expected principals.")
    _num(doc, "Validate project access with manager and user groups.")

    out = BASE_DIR / "Agent_Service_Deployment_Guide.docx"
    doc.save(str(out))


if __name__ == "__main__":
    build_platform_doc()
    build_agent_doc()
    print("Generated split deployment guides:")
    print(BASE_DIR / "Platform_Resources_Deployment_Guide.docx")
    print(BASE_DIR / "Agent_Service_Deployment_Guide.docx")
