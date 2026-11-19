from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement

DOC_PATH = Path(r"c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_v3.docx")
OUT_PATH = Path(r"c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_v3_with_real_screenshots.docx")
ROOT = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template")


def insert_paragraph_after(paragraph, text=""):
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = paragraph._parent.add_paragraph(text)
    new_p.addnext(new_para._p)
    return new_para


# Placeholder -> (image path, width cm, caption)
replacements = {
    "[Insert Screenshot Here] - High-level deployment flow diagram": (
        ROOT / "docs/diagrams/agent_pipeline_flow_enterprise.png",
        16,
        "Figure 1 - High-Level Agent Service Deployment Flow",
    ),
    "[Insert Screenshot Here] - Deployment architecture from Service Now to Azure": (
        ROOT / "docs/diagrams/agent_architecture_deployment_only_enterprise.png",
        16,
        "Figure 2 - Agent Service Deployment Architecture",
    ),
    "[Insert Screenshot Here] - Repository structure overview": (
        ROOT / "docs/screenshots/actions/04_actions_overview_current.jpg",
        15,
        "Figure 3 - Deployment Repository Structure",
    ),
    "[Insert Screenshot Here] - Config file update": (
        ROOT / "docs/diagrams/iac_snapshots/09_project_config_yaml.png",
        15,
        "Figure 4 - Sample Project Configuration Entry",
    ),
    "[Insert Screenshot Here] - GitHub PR approval and merge": (
        ROOT / "docs/screenshots/actions/01_actions_overview_annotated.png",
        15,
        "Figure 5 - Pull Request Approval and Merge",
    ),
    "[Insert Screenshot Here] - GitHub Actions workflow dispatch": (
        ROOT / "docs/screenshots/actions/cropped/02_run_workflow_inputs_annotated_cropped.png",
        15,
        "Figure 7 - Workflow Trigger Inputs",
    ),
    "[Insert Screenshot Here] - Terraform plan output": (
        ROOT / "docs/screenshots/actions/cropped/07_plan_job_page_cropped.jpg",
        15,
        "Figure 8 - Terraform Plan Execution",
    ),
    "[Insert Screenshot Here] - Manual approval gate in GitHub Environments": (
        ROOT / "docs/screenshots/actions/cropped/06_run_summary_page_cropped.jpg",
        15,
        "Figure 9 - Deployment Approval Gate",
    ),
    "[Insert Screenshot Here] - Terraform apply job execution": (
        ROOT / "docs/screenshots/actions/cropped/08_apply_job_page_cropped.jpg",
        15,
        "Figure 10 - Terraform Apply Execution",
    ),
    "[Insert Screenshot Here] - Azure resource creation confirmation": (
        ROOT / "docs/screenshots/actions/cropped/03_run_summary_graph_annotated_cropped.png",
        15,
        "Figure 11 - Azure Resources Created",
    ),
}


def main():
    doc = Document(str(DOC_PATH))
    replaced = 0
    missing = []

    for para in list(doc.paragraphs):
        txt = para.text.strip()
        if txt in replacements:
            image_path, width_cm, caption = replacements[txt]
            if not image_path.exists():
                missing.append((txt, str(image_path)))
                continue

            # Replace placeholder text with image, center aligned.
            para.clear()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run()
            run.add_picture(str(image_path), width=Cm(width_cm))

            # Add caption directly below image.
            cap_para = insert_paragraph_after(para, caption)
            cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if cap_para.runs:
                cap_para.runs[0].font.size = Pt(10)
                cap_para.runs[0].italic = True
            cap_para.paragraph_format.space_before = Pt(4)
            cap_para.paragraph_format.space_after = Pt(10)

            replaced += 1

    doc.save(str(OUT_PATH))

    print(f"Replaced placeholders: {replaced}")
    print(f"Output: {OUT_PATH}")
    if missing:
        print("Missing images:")
        for item, path in missing:
            print(f"- {item} -> {path}")


if __name__ == "__main__":
    main()
