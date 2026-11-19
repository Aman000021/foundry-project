from pathlib import Path
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

base = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs")
out_path = base / "Platform_Service_Document_002.docx"
img_dir = base / "screenshots" / "actions" / "cropped"

# Match reference screenshot style (~6 inch width)
TARGET_W_IN = 6.0
MAX_H_IN = 3.2
DPI = 96.0


def set_font(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(11)
    for name in ["Heading 1", "Heading 2", "Heading 3"]:
        if name in doc.styles:
            doc.styles[name].font.name = "Aptos"


def add_title(doc):
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run("MS FOUNDRY")
    r.bold = True
    r.font.size = Pt(22)

    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run("Platform Service Document")
    r.bold = True
    r.font.size = Pt(16)

    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.add_run("Version: 002")


def add_toc(doc):
    doc.add_paragraph("")
    doc.add_heading("Table of Contents", level=1)
    doc.add_paragraph("1. Overview")
    doc.add_paragraph("2. Foundry Resource Creation Steps")
    doc.add_paragraph("3. Other Resource Creation Steps")
    doc.add_paragraph("4. Repository Structure")


def picture_size(path: Path):
    with Image.open(path) as im:
        w_px, h_px = im.size
    w_in = w_px / DPI
    h_in = h_px / DPI
    scale = min(TARGET_W_IN / w_in, MAX_H_IN / h_in)
    return w_in * scale, h_in * scale


def add_screenshot(doc, filename, label):
    path = img_dir / filename
    if not path.exists():
        doc.add_paragraph(f"Screenshot not found: {filename}")
        return

    doc.add_paragraph(label)
    w_in, h_in = picture_size(path)
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run()
    r.add_picture(str(path), width=Inches(w_in), height=Inches(h_in))
    p.paragraph_format.space_after = Pt(10)


doc = Document()
set_font(doc)

# Page 1: Title + TOC + Section 1
add_title(doc)
add_toc(doc)

doc.add_paragraph("")
doc.add_heading("1. Overview", level=1)
doc.add_paragraph("This guide covers platform-side resource deployment for MS Foundry in this repository.")
doc.add_paragraph("It follows the same execution pattern used in the reference deployment guide.")
doc.add_paragraph("Flow:")
doc.add_paragraph("- Pull latest code and create feature branch")
doc.add_paragraph("- Update configuration files")
doc.add_paragraph("- Trigger workflow and review Terraform plan")
doc.add_paragraph("- Validate changes and approve")
doc.add_paragraph("- Merge PR and run apply")
doc.add_paragraph("- Validate resources in Azure portal")

# Page 2: Section 2
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch.")
doc.add_paragraph("2. Checkout to new feature branch with naming: <RITM>/<change-name>.")
doc.add_paragraph("3. Update Foundry resource configuration files.")
doc.add_paragraph("4. Update file: environments/<env>/<segment>/foundry-hub.tfvars.")
doc.add_paragraph("5. Update file: iac/foundry_hub_configs/<segment>/config.yaml.")
doc.add_paragraph("6. Validate foundry index, subnet, and location values.")
doc.add_paragraph("7. Push changes to remote feature branch.")
doc.add_paragraph("8. Open Actions -> Trigger Foundry Setup -> Run Workflow.")
doc.add_paragraph("9. Select platform deployment option for the target environment.")
doc.add_paragraph("10. Monitor Terraform plan and validate changes.")
doc.add_paragraph("11. Validate resource group and foundry resource selection.")
doc.add_paragraph("12. Raise PR approval and merge after verification.")
doc.add_paragraph("13. Approve workflow apply after plan validation.")
doc.add_paragraph("14. Validate Foundry resource and private endpoint creation in Azure portal.")

add_screenshot(doc, "05_trigger_workflow_page_cropped.jpg", "Screenshot: Trigger workflow page")
add_screenshot(doc, "02_run_workflow_inputs_annotated_cropped.png", "Screenshot: Workflow input selection")
add_screenshot(doc, "03_run_summary_graph_annotated_cropped.png", "Screenshot: Plan and apply path")

# Page 3: Section 3
doc.add_page_break()
doc.add_heading("3. Other Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch.")
doc.add_paragraph("2. Checkout to new feature branch.")
doc.add_paragraph("3. Update platform configuration file: environments/<env>/platform.tfvars.")
doc.add_paragraph("4. Validate monitoring and shared platform values.")
doc.add_paragraph("5. Push changes and create PR.")
doc.add_paragraph("6. Trigger workflow with platform option in Actions.")
doc.add_paragraph("7. Validate Terraform plan for platform-hub deployment.")
doc.add_paragraph("8. Approve and apply after reviewer confirmation.")
doc.add_paragraph("9. Validate Log Analytics, App Insights, and Key Vault resources.")

add_screenshot(doc, "01_actions_overview_annotated_cropped.png", "Screenshot: Actions run overview")
add_screenshot(doc, "07_plan_job_page_cropped.jpg", "Screenshot: Terraform plan job validation")

# Page 4: Section 4
doc.add_page_break()
doc.add_heading("4. Repository Structure", level=1)
doc.add_paragraph("Key deployment files:")
doc.add_paragraph("- .github/workflows/iac.yaml")
doc.add_paragraph("- .github/workflows/platform-deploy.yml")
doc.add_paragraph("- .github/workflows/agent-capability-deploy.yml")
doc.add_paragraph("- environments/<env>/platform.tfvars")
doc.add_paragraph("- environments/<env>/<segment>/foundry-hub.tfvars")
doc.add_paragraph("- iac/foundry_hub_configs/<segment>/config.yaml")
doc.add_paragraph("- iac/platform-hub/")
doc.add_paragraph("- iac/capability/foundry-hub/")
doc.add_paragraph("- iac/modules/platform/")
doc.add_paragraph("- iac/modules/foundry-hub/")
doc.add_paragraph("")
doc.add_paragraph("Notes:")
doc.add_paragraph("- Use platform deployment path for platform/foundry resource changes.")
doc.add_paragraph("- Validate plan output before approval in every run.")
doc.add_paragraph("- Keep branch naming and PR validation process consistent.")

add_screenshot(doc, "08_apply_job_page_cropped.jpg", "Screenshot: Apply job success validation")

doc.add_paragraph("")
doc.add_paragraph("------------------------------------------End of document------------------------------------------")

doc.save(str(out_path))
print(str(out_path))
