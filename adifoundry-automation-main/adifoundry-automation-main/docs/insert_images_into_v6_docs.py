from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template")

AGENT_IN = ROOT / "docs/Agent_Service_Deployment_Guide_Updated_v6_PLACEHOLDERS_ONLY.docx"
AGENT_OUT = ROOT / "docs/Agent_Service_Deployment_Guide_Updated_v7_IMAGES.docx"
PLATFORM_IN = ROOT / "docs/Platform_Resources_Deployment_Guide_Updated_v6_PLACEHOLDERS_ONLY.docx"
PLATFORM_OUT = ROOT / "docs/Platform_Resources_Deployment_Guide_Updated_v7_IMAGES.docx"


def apply_images(doc_in: Path, doc_out: Path, mapping: dict):
    doc = Document(str(doc_in))
    replaced = 0

    for para in doc.paragraphs:
        txt = para.text.strip()
        if txt.startswith("Screenshot Placeholder:"):
            key = txt.replace("Screenshot Placeholder: [Insert Screenshot Here] - ", "").strip()
            if key in mapping:
                img_path, width_cm = mapping[key]
                if img_path.exists():
                    para.clear()
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = para.add_run()
                    run.add_picture(str(img_path), width=Cm(width_cm))
                    replaced += 1

        if txt.startswith("Caption:"):
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if para.runs:
                para.runs[0].font.size = Pt(10)
                para.runs[0].italic = True
            para.paragraph_format.space_before = Pt(3)
            para.paragraph_format.space_after = Pt(8)

    doc.save(str(doc_out))
    return replaced


def main():
    agent_map = {
        "High-level agent onboarding infrastructure flow": (ROOT / "docs/diagrams/agent_pipeline_flow_enterprise.png", 16),
        "Agent infrastructure architecture (Service Now to Terraform apply)": (ROOT / "docs/diagrams/agent_architecture_deployment_only_enterprise.png", 16),
        "Repository tree with iac, environments, and workflow files": (ROOT / "docs/screenshots/actions/04_actions_overview_current.jpg", 15),
        "Config.yaml entry with project_name, segment, index, manager and user IDs": (ROOT / "docs/diagrams/iac_snapshots/09_project_config_yaml.png", 15),
        "PR creation and approval details": (ROOT / "docs/screenshots/actions/01_actions_overview_annotated.png", 15),
        "Workflow trigger input panel (choice, segment, location)": (ROOT / "docs/screenshots/actions/cropped/02_run_workflow_inputs_annotated_cropped.png", 15),
        "Terraform plan job execution logs": (ROOT / "docs/screenshots/actions/cropped/07_plan_job_page_cropped.jpg", 15),
        "Environment approval gate": (ROOT / "docs/screenshots/actions/cropped/06_run_summary_page_cropped.jpg", 15),
        "Terraform apply job execution": (ROOT / "docs/screenshots/actions/cropped/08_apply_job_page_cropped.jpg", 15),
        "Validation in Foundry and Azure IAM": (ROOT / "docs/screenshots/actions/cropped/03_run_summary_graph_annotated_cropped.png", 15),
    }

    platform_map = {
        "High-level platform infrastructure flow": (ROOT / "docs/diagrams/platform_pipeline_flow_enterprise.png", 16),
        "Platform deployment architecture (shared infra only)": (ROOT / "docs/diagrams/platform_architecture_deployment_only_enterprise.png", 16),
        "Repository tree with platform and foundry-hub deployment files": (ROOT / "docs/diagrams/iac_snapshots/02_platform_pipeline_yaml.png", 15),
        "Platform/foundry-hub config update section": (ROOT / "docs/diagrams/iac_snapshots/08_hub_config_yaml.png", 15),
        "PR creation and approval for platform flow": (ROOT / "docs/screenshots/actions/01_actions_overview_annotated.png", 15),
        "Workflow trigger input panel (platform choice)": (ROOT / "docs/screenshots/actions/cropped/02_run_workflow_inputs_annotated_cropped.png", 15),
        "Plan execution for platform-hub and foundry-hub": (ROOT / "docs/screenshots/actions/cropped/07_plan_job_page_cropped.jpg", 15),
        "Environment approval gate": (ROOT / "docs/screenshots/actions/cropped/06_run_summary_page_cropped.jpg", 15),
        "Apply execution for platform and foundry-hub": (ROOT / "docs/screenshots/actions/cropped/08_apply_job_page_cropped.jpg", 15),
        "Validation in Azure for platform resources": (ROOT / "docs/screenshots/actions/cropped/03_run_summary_graph_annotated_cropped.png", 15),
    }

    a = apply_images(AGENT_IN, AGENT_OUT, agent_map)
    p = apply_images(PLATFORM_IN, PLATFORM_OUT, platform_map)

    print(f"Agent images inserted: {a}")
    print(f"Platform images inserted: {p}")
    print(f"Created: {AGENT_OUT}")
    print(f"Created: {PLATFORM_OUT}")


if __name__ == "__main__":
    main()
