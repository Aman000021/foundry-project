from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

base = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs")
out_path = base / "Platform_Service_Document_007.docx"

img = {
    "flow_pipeline": base / "diagrams" / "platform_pipeline_flow_enterprise.png",
    "flow_arch": base / "diagrams" / "platform_architecture_deployment_only_enterprise.png",
    "iac_trigger": base / "diagrams" / "iac_snapshots" / "01_trigger_workflow_yaml.png",
    "iac_platform_wf": base / "diagrams" / "iac_snapshots" / "02_platform_pipeline_yaml.png",
    "iac_platform_module": base / "diagrams" / "iac_snapshots" / "04_platform_module_main_tf.png",
    "iac_foundry_module": base / "diagrams" / "iac_snapshots" / "05_foundry_hub_module_main_tf.png",
    "iac_hub_cfg": base / "diagrams" / "iac_snapshots" / "08_hub_config_yaml.png",
    "run_input": base / "screenshots" / "actions" / "cropped" / "02_run_workflow_inputs_annotated_cropped.png",
    "run_plan": base / "screenshots" / "actions" / "cropped" / "07_plan_job_page_cropped.jpg",
    "run_apply": base / "screenshots" / "actions" / "cropped" / "08_apply_job_page_cropped.jpg",
}


def set_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(11)
    for s in ["Heading 1", "Heading 2", "Heading 3"]:
        if s in doc.styles:
            doc.styles[s].font.name = "Aptos"


def center_title(doc, text, size, bold=True):
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)


def add_img(doc, path, caption, w=5.8, h=1.85):
    if not path.exists():
        doc.add_paragraph(f"Screenshot not found: {path.name}")
        return
    c = doc.add_paragraph(caption)
    c.runs[0].bold = True
    c.paragraph_format.space_after = Pt(2)
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.add_run().add_picture(str(path), width=Inches(w), height=Inches(h))
    p.paragraph_format.space_after = Pt(6)


doc = Document()
set_styles(doc)

# PAGE 1
center_title(doc, "MS FOUNDRY", 22, True)
center_title(doc, "Platform Service Document", 16, True)
center_title(doc, "Version: 007", 11, False)

doc.add_paragraph("")
doc.add_heading("Table of Contents", level=1)
doc.add_paragraph("1. Overview")
doc.add_paragraph("2. Foundry Resource Creation Steps")
doc.add_paragraph("3. Other Resource Creation Steps")
doc.add_paragraph("4. Repository Structure")

doc.add_paragraph("")
doc.add_heading("1. Overview", level=1)
doc.add_paragraph("This guide covers platform service deployment steps for Foundry-related platform resources.")
doc.add_paragraph("This document follows the same practical format used in the referenced guide.")
doc.add_paragraph("Flow:")
doc.add_paragraph("- Pull latest code and create feature branch")
doc.add_paragraph("- Update config and validate inputs")
doc.add_paragraph("- Trigger workflow and check Terraform plan")
doc.add_paragraph("- Approve, merge, and apply")
doc.add_paragraph("- Validate resources in Azure")
add_img(doc, img["flow_pipeline"], "Screenshot: Platform deployment flow", 5.9, 1.7)

# PAGE 2
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch.")
doc.add_paragraph("2. Checkout to feature branch: <RITM>/<change-name>.")
doc.add_paragraph("3. Update environments/<env>/<segment>/foundry-hub.tfvars.")
doc.add_paragraph("4. Update iac/foundry_hub_configs/<segment>/config.yaml.")
doc.add_paragraph("5. Validate foundry index, subnet, and location values.")
doc.add_paragraph("6. Push changes to remote feature branch.")
add_img(doc, img["iac_hub_cfg"], "Screenshot: Foundry hub config values", 5.8, 1.8)
add_img(doc, img["iac_foundry_module"], "Screenshot: Foundry hub module (main.tf)", 5.8, 1.8)

# PAGE 3
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps (continued)", level=2)
doc.add_paragraph("7. Go to Actions and run Trigger Foundry Setup.")
doc.add_paragraph("8. Select platform deployment option and required inputs.")
doc.add_paragraph("9. Validate Terraform plan for intended changes only.")
doc.add_paragraph("10. Raise PR approval and merge after review.")
doc.add_paragraph("11. Approve apply and validate deployment status.")
add_img(doc, img["run_input"], "Screenshot: Workflow input selection", 5.8, 1.85)
add_img(doc, img["run_plan"], "Screenshot: Terraform plan validation", 5.8, 1.85)

# PAGE 4
doc.add_page_break()
doc.add_heading("3. Other Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest code and checkout feature branch.")
doc.add_paragraph("2. Update environments/<env>/platform.tfvars.")
doc.add_paragraph("3. Validate platform monitoring and shared values.")
doc.add_paragraph("4. Push updates and create PR.")
doc.add_paragraph("5. Trigger workflow and monitor platform plan.")
doc.add_paragraph("6. Validate there are no unintended destroy changes.")
doc.add_paragraph("7. Approve and apply after reviewer sign-off.")
add_img(doc, img["iac_trigger"], "Screenshot: Trigger workflow YAML", 5.8, 1.7)
add_img(doc, img["iac_platform_wf"], "Screenshot: Platform deployment workflow YAML", 5.8, 1.7)

# PAGE 5
doc.add_page_break()
doc.add_heading("3. Other Resource Creation Steps (continued)", level=2)
doc.add_paragraph("8. Validate platform resource status in Azure after apply completion.")
doc.add_paragraph("9. Confirm expected resources are created in target resource groups.")
doc.add_paragraph("10. Re-run plan if any mismatch is identified.")
add_img(doc, img["flow_arch"], "Screenshot: Platform deployment architecture", 5.9, 1.9)
add_img(doc, img["iac_platform_module"], "Screenshot: Platform module (main.tf)", 5.8, 1.7)
add_img(doc, img["run_apply"], "Screenshot: Terraform apply validation", 5.8, 1.7)

# PAGE 6
doc.add_page_break()
doc.add_heading("4. Repository Structure", level=1)
doc.add_paragraph("Key deployment files:")
doc.add_paragraph("- .github/workflows/iac.yaml")
doc.add_paragraph("- .github/workflows/platform-deploy.yml")
doc.add_paragraph("- .github/workflows/agent-capability-deploy.yml")
doc.add_paragraph("- environments/<env>/platform.tfvars")
doc.add_paragraph("- environments/<env>/<segment>/foundry-hub.tfvars")
doc.add_paragraph("- environments/<env>/<segment>/backend-config-hub.tfvars")
doc.add_paragraph("- iac/platform-hub/")
doc.add_paragraph("- iac/capability/foundry-hub/")
doc.add_paragraph("- iac/modules/platform/")
doc.add_paragraph("- iac/modules/foundry-hub/")
doc.add_paragraph("- iac/foundry_hub_configs/<segment>/config.yaml")
doc.add_paragraph("Notes:")
doc.add_paragraph("- Use feature branch updates with plan validation before apply.")
doc.add_paragraph("- Keep workflow selection aligned with platform deployment path.")
doc.add_paragraph("------------------------------------------End of document------------------------------------------")

doc.save(str(out_path))
print(str(out_path))
