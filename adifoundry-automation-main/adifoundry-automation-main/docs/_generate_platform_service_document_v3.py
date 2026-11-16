from pathlib import Path
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

base = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs")
out_path = base / "Platform_Service_Document_003.docx"
img_dir = base / "screenshots" / "actions" / "cropped"
rect_dir = img_dir / "rect"
rect_dir.mkdir(parents=True, exist_ok=True)

# Reference-like screenshot format
TARGET_W_IN = 6.0
TARGET_H_IN = 3.2
TARGET_RATIO = TARGET_W_IN / TARGET_H_IN  # 1.875
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
    p.add_run("Version: 003")


def add_toc(doc):
    doc.add_paragraph("")
    doc.add_heading("Table of Contents", level=1)
    doc.add_paragraph("1. Overview")
    doc.add_paragraph("2. Foundry Resource Creation Steps")
    doc.add_paragraph("3. Other Resource Creation Steps")
    doc.add_paragraph("4. Repository Structure")


def make_rect_image(src_name: str):
    src = img_dir / src_name
    if not src.exists():
        return None

    out = rect_dir / f"{Path(src_name).stem}_rect{Path(src_name).suffix}"

    with Image.open(src) as im:
        w, h = im.size
        target_h = int(w / TARGET_RATIO)
        if target_h <= h:
            # Keep top area (where headings and key run info usually appear)
            crop = im.crop((0, 0, w, target_h))
        else:
            # If already short, center-crop width
            target_w = int(h * TARGET_RATIO)
            left = max((w - target_w) // 2, 0)
            crop = im.crop((left, 0, left + target_w, h))

        crop.save(out, quality=92)

    return out


def add_screenshot(doc, src_name, label):
    rect = make_rect_image(src_name)
    if not rect:
        doc.add_paragraph(f"Screenshot not found: {src_name}")
        return

    doc.add_paragraph(label)
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run()
    r.add_picture(str(rect), width=Inches(TARGET_W_IN), height=Inches(TARGET_H_IN))
    p.paragraph_format.space_after = Pt(8)


doc = Document()
set_font(doc)

# PAGE 1
a = add_title(doc)
add_toc(doc)

doc.add_paragraph("")
doc.add_heading("1. Overview", level=1)
doc.add_paragraph("This guide covers platform service deployment steps in MS Foundry.")
doc.add_paragraph("It follows the same sentence style and execution flow used in the reference guide.")
doc.add_paragraph("Flow:")
doc.add_paragraph("- Pull latest code and create feature branch")
doc.add_paragraph("- Update configuration files")
doc.add_paragraph("- Trigger workflow and validate Terraform plan")
doc.add_paragraph("- Request PR approval, merge, and apply")
doc.add_paragraph("- Validate resources after deployment")
add_screenshot(doc, "01_actions_overview_annotated_cropped.png", "Screenshot: Actions overview")

# PAGE 2
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch.")
doc.add_paragraph("2. Checkout with new feature branch: <RITM>/<change-name>.")
doc.add_paragraph("3. Update environments/<env>/<segment>/foundry-hub.tfvars.")
doc.add_paragraph("4. Update iac/foundry_hub_configs/<segment>/config.yaml.")
doc.add_paragraph("5. Validate foundry index, subnet, and location values.")
doc.add_paragraph("6. Push changes to feature branch.")
doc.add_paragraph("7. Go to Actions -> Trigger Foundry Setup -> Run Workflow.")
doc.add_paragraph("8. Select platform deployment option for the target environment.")
doc.add_paragraph("9. Validate Terraform plan and resource selection.")
doc.add_paragraph("10. Approve and merge PR, then approve apply.")
doc.add_paragraph("11. Validate Foundry hub and private endpoint in Azure portal.")
add_screenshot(doc, "02_run_workflow_inputs_annotated_cropped.png", "Screenshot: Foundry workflow input selection")

# PAGE 3
doc.add_page_break()
doc.add_heading("3. Other Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch.")
doc.add_paragraph("2. Checkout with new feature branch.")
doc.add_paragraph("3. Update environments/<env>/platform.tfvars.")
doc.add_paragraph("4. Validate monitoring and shared resource values.")
doc.add_paragraph("5. Push changes and raise PR.")
doc.add_paragraph("6. Trigger workflow with platform option.")
doc.add_paragraph("7. Monitor Terraform plan in platform deployment job.")
doc.add_paragraph("8. Validate no unintended deletions.")
doc.add_paragraph("9. Approve and apply after review.")
doc.add_paragraph("10. Validate Log Analytics, App Insights, and Key Vault.")
add_screenshot(doc, "07_plan_job_page_cropped.jpg", "Screenshot: Platform plan validation")

# PAGE 4
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
doc.add_paragraph("Notes:")
doc.add_paragraph("- Keep configuration updates in feature branches.")
doc.add_paragraph("- Validate Terraform plan before approval in each run.")
doc.add_paragraph("- Use this structure reference for platform-side updates.")
add_screenshot(doc, "08_apply_job_page_cropped.jpg", "Screenshot: Apply job success verification")

doc.add_paragraph("------------------------------------------End of document------------------------------------------")

doc.save(str(out_path))
print(str(out_path))
