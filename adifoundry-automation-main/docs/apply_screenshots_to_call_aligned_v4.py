from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement

ROOT = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template")


AGENT_DOC = Path(r"c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_v4.docx")
AGENT_OUT = Path(r"c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_v5_with_screenshots.docx")

PLATFORM_DOC = Path(r"c:\Users\XSPriyaGa\Downloads\Platform_Resources_Deployment_Guide_Updated_v4.docx")
PLATFORM_OUT = Path(r"c:\Users\XSPriyaGa\Downloads\Platform_Resources_Deployment_Guide_Updated_v5_with_screenshots.docx")


def remove_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)


def insert_paragraph_after(paragraph, text=""):
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = paragraph._parent.add_paragraph(text)
    new_p.addnext(new_para._p)
    return new_para


def apply_mapping(doc_path, out_path, mapping):
    doc = Document(str(doc_path))
    replacements = 0

    i = 0
    while i < len(doc.paragraphs):
        para = doc.paragraphs[i]
        text = para.text.strip()

        if text.startswith("SCREENSHOT PLACEHOLDER "):
            code = text.split(":", 1)[0].replace("SCREENSHOT PLACEHOLDER", "").strip()
            if code in mapping:
                image_path, width_cm, caption = mapping[code]
                if image_path.exists():
                    para.clear()
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = para.add_run()
                    run.add_picture(str(image_path), width=Cm(width_cm))

                    cap = insert_paragraph_after(para, caption)
                    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    if cap.runs:
                        cap.runs[0].font.size = Pt(10)
                        cap.runs[0].italic = True
                    cap.paragraph_format.space_before = Pt(4)
                    cap.paragraph_format.space_after = Pt(10)
                    replacements += 1

                    # Remove metadata helper lines immediately after placeholder block.
                    # These are explicit lines added in v4 docs.
                    j = i + 2
                    while j < len(doc.paragraphs):
                        t = doc.paragraphs[j].text.strip()
                        if (
                            t.startswith("Source:")
                            or t.startswith("Capture:")
                            or t.startswith("Highlight:")
                            or t.startswith("Size:")
                            or t.startswith("Caption:")
                            or t == ""
                        ):
                            remove_paragraph(doc.paragraphs[j])
                            continue
                        break
        i += 1

    doc.save(str(out_path))
    return replacements


def main():
    agent_map = {
        "A1": (ROOT / "docs/diagrams/agent_pipeline_flow_enterprise.png", 16, "Figure 1 - High-Level Agent Service Infra Deployment Flow"),
        "A2": (ROOT / "docs/screenshots/actions/04_actions_overview_current.jpg", 15, "Figure 2 - Agent Deployment Repository Structure"),
        "A3": (ROOT / "docs/diagrams/iac_snapshots/09_project_config_yaml.png", 15, "Figure 3 - Agent Project Configuration Entry"),
        "A4": (ROOT / "docs/screenshots/actions/cropped/02_run_workflow_inputs_annotated_cropped.png", 15, "Figure 4 - Agent Workflow Trigger Inputs"),
        "A5": (ROOT / "docs/screenshots/actions/cropped/07_plan_job_page_cropped.jpg", 15, "Figure 5 - Agent Terraform Plan Execution"),
        "A6": (ROOT / "docs/screenshots/actions/cropped/06_run_summary_page_cropped.jpg", 15, "Figure 6 - Agent Deployment Approval Gate"),
        "A7": (ROOT / "docs/screenshots/actions/cropped/08_apply_job_page_cropped.jpg", 15, "Figure 7 - Agent Terraform Apply Execution"),
        "A8": (ROOT / "docs/screenshots/actions/cropped/03_run_summary_graph_annotated_cropped.png", 15, "Figure 8 - Agent Infra Validation"),
    }

    platform_map = {
        "P1": (ROOT / "docs/diagrams/platform_pipeline_flow_enterprise.png", 16, "Figure 1 - High-Level Platform Resources Deployment Flow"),
        "P2": (ROOT / "docs/diagrams/iac_snapshots/02_platform_pipeline_yaml.png", 15, "Figure 2 - Platform Deployment Repository Structure"),
        "P3": (ROOT / "docs/diagrams/iac_snapshots/08_hub_config_yaml.png", 15, "Figure 3 - Platform Configuration Update"),
        "P4": (ROOT / "docs/screenshots/actions/cropped/02_run_workflow_inputs_annotated_cropped.png", 15, "Figure 4 - Platform Workflow Trigger Inputs"),
        "P5": (ROOT / "docs/screenshots/actions/cropped/07_plan_job_page_cropped.jpg", 15, "Figure 5 - Platform and Foundry-Hub Plan Execution"),
        "P6": (ROOT / "docs/screenshots/actions/cropped/06_run_summary_page_cropped.jpg", 15, "Figure 6 - Platform Deployment Approval Gate"),
        "P7": (ROOT / "docs/screenshots/actions/cropped/08_apply_job_page_cropped.jpg", 15, "Figure 7 - Platform Terraform Apply Execution"),
        "P8": (ROOT / "docs/screenshots/actions/cropped/03_run_summary_graph_annotated_cropped.png", 15, "Figure 8 - Platform Infrastructure Validation"),
    }

    a = apply_mapping(AGENT_DOC, AGENT_OUT, agent_map)
    p = apply_mapping(PLATFORM_DOC, PLATFORM_OUT, platform_map)

    print(f"Agent placeholders replaced: {a}")
    print(f"Platform placeholders replaced: {p}")
    print(f"Created: {AGENT_OUT}")
    print(f"Created: {PLATFORM_OUT}")


if __name__ == "__main__":
    main()
