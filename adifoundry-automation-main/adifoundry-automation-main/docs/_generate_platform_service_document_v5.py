from pathlib import Path
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

base = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs")
out_path = base / "Platform_Service_Document_005.docx"
img_dir = base / "screenshots" / "actions" / "cropped"

IMG_W = 5.9
IMG_H = 2.25
RATIO = IMG_W / IMG_H


def set_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(11)
    for s in ["Heading 1", "Heading 2", "Heading 3"]:
        if s in doc.styles:
            doc.styles[s].font.name = "Aptos"


def c_line(doc, text, size=12, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)


def bullet(doc, text):
    doc.add_paragraph(text, style="List Bullet")


def crop_ratio(src: Path, out_name: str):
    out_dir = img_dir / "rect_v5"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / out_name
    with Image.open(src) as im:
        w, h = im.size
        target_h = int(w / RATIO)
        if target_h <= h:
            crop = im.crop((0, 0, w, target_h))
        else:
            target_w = int(h * RATIO)
            left = max((w - target_w) // 2, 0)
            crop = im.crop((left, 0, left + target_w, h))
        crop.save(out, quality=92)
    return out


def add_img(doc, filename, caption):
    src = img_dir / filename
    if not src.exists():
        doc.add_paragraph(f"Screenshot not found: {filename}")
        return
    rect = crop_ratio(src, f"{src.stem}_rect_v5{src.suffix}")
    cp = doc.add_paragraph(caption)
    cp.runs[0].bold = True
    cp.paragraph_format.space_after = Pt(2)
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.add_run().add_picture(str(rect), width=Inches(IMG_W), height=Inches(IMG_H))
    p.paragraph_format.space_after = Pt(6)


doc = Document()
set_styles(doc)

# Page 1
c_line(doc, "MS FOUNDRY", 22, True)
c_line(doc, "Platform Service Document", 16, True)
c_line(doc, "Version: 005", 11, False)

doc.add_paragraph("")
doc.add_heading("Table of Contents", level=1)
doc.add_paragraph("1. Overview")
doc.add_paragraph("2. Foundry Resource Creation Steps")
doc.add_paragraph("3. Other Resource Creation Steps")
doc.add_paragraph("4. Repository Structure")

doc.add_paragraph("")
doc.add_heading("1. Overview", level=1)
doc.add_paragraph("This guide explains platform service deployment in MS Foundry using this repository.")
doc.add_paragraph("It follows the same practical sentence style used in the reference document.")
doc.add_paragraph("Flow:")
bullet(doc, "Pull latest code and checkout to feature branch")
bullet(doc, "Update configuration and push changes")
bullet(doc, "Trigger workflow and validate Terraform plan")
bullet(doc, "Raise PR approval, merge, and approve apply")
bullet(doc, "Validate resources in Azure portal")
add_img(doc, "01_actions_overview_annotated_cropped.png", "Screenshot: Actions overview")

# Page 2
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch.")
doc.add_paragraph("2. Checkout with new feature branch naming: <RITM>/<change-name>.")
doc.add_paragraph("3. Update environments/<env>/<segment>/foundry-hub.tfvars.")
doc.add_paragraph("4. Update iac/foundry_hub_configs/<segment>/config.yaml.")
doc.add_paragraph("5. Validate foundry index, subnet, and location values.")
doc.add_paragraph("6. Push changes to remote feature branch.")
doc.add_paragraph("7. Go to Actions -> Trigger Foundry Setup -> Run Workflow.")
doc.add_paragraph("8. Select platform deployment option and submit.")
add_img(doc, "05_trigger_workflow_page_cropped.jpg", "Screenshot: Trigger workflow page")

# Page 3
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps (continued)", level=2)
doc.add_paragraph("9. Monitor the workflow and open Terraform plan job.")
doc.add_paragraph("10. Validate the plan shows only intended Foundry resource changes.")
doc.add_paragraph("11. Check resource group, foundry name, and private endpoint mapping.")
doc.add_paragraph("12. Request PR approval and merge after plan validation.")
doc.add_paragraph("13. Approve workflow apply after reviewer sign-off.")
doc.add_paragraph("14. Validate Foundry resource creation in Azure portal.")
add_img(doc, "02_run_workflow_inputs_annotated_cropped.png", "Screenshot: Workflow input selection")
add_img(doc, "03_run_summary_graph_annotated_cropped.png", "Screenshot: Plan and apply flow")

# Page 4
doc.add_page_break()
doc.add_heading("3. Other Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch and create feature branch.")
doc.add_paragraph("2. Update environments/<env>/platform.tfvars.")
doc.add_paragraph("3. Validate shared platform values for monitoring and security resources.")
doc.add_paragraph("4. Push updates and raise PR.")
doc.add_paragraph("5. Trigger workflow with platform deployment option.")
doc.add_paragraph("6. Validate Terraform plan output before approval.")
doc.add_paragraph("7. Ensure no unintended destroy actions are included.")
doc.add_paragraph("8. Approve apply and validate resources after completion.")
add_img(doc, "07_plan_job_page_cropped.jpg", "Screenshot: Platform plan job")

# Page 5
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
doc.add_paragraph("Quick understanding:")
bullet(doc, "platform-hub path is for shared platform resources")
bullet(doc, "foundry-hub path is for Foundry hub resources")
bullet(doc, "workflow trigger remains common through Trigger Foundry Setup")
add_img(doc, "08_apply_job_page_cropped.jpg", "Screenshot: Apply job success")

doc.add_paragraph("------------------------------------------End of document------------------------------------------")

doc.save(str(out_path))
print(str(out_path))
