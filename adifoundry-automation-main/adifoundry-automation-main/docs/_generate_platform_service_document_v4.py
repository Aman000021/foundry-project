from pathlib import Path
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

base = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs")
out_path = base / "Platform_Service_Document_004.docx"
img_dir = base / "screenshots" / "actions" / "cropped"

# Consistent screenshot format (same style family as reference)
IMG_W = 6.0
IMG_H = 2.55
RATIO = IMG_W / IMG_H


def set_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(11)
    for s in ["Heading 1", "Heading 2", "Heading 3"]:
        if s in doc.styles:
            doc.styles[s].font.name = "Aptos"


def add_center_line(doc, text, size=12, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold


def add_bullet(doc, text):
    doc.add_paragraph(text, style="List Bullet")


def crop_to_ratio(src: Path, out_name: str):
    out_dir = img_dir / "rect_v4"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / out_name

    with Image.open(src) as im:
        w, h = im.size
        target_h = int(w / RATIO)
        if target_h <= h:
            # Keep upper region where key context appears
            crop = im.crop((0, 0, w, target_h))
        else:
            target_w = int(h * RATIO)
            left = max((w - target_w) // 2, 0)
            crop = im.crop((left, 0, left + target_w, h))
        crop.save(out, quality=92)
    return out


def add_image(doc, filename, caption):
    src = img_dir / filename
    if not src.exists():
        doc.add_paragraph(f"Screenshot not found: {filename}")
        return
    rect = crop_to_ratio(src, f"{src.stem}_rect_v4{src.suffix}")
    cp = doc.add_paragraph(caption)
    cp.runs[0].bold = True
    cp.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    cp.paragraph_format.space_after = Pt(3)

    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    r = p.add_run()
    r.add_picture(str(rect), width=Inches(IMG_W), height=Inches(IMG_H))
    p.paragraph_format.space_after = Pt(8)


doc = Document()
set_styles(doc)

# PAGE 1
add_center_line(doc, "MS FOUNDRY", size=22, bold=True)
add_center_line(doc, "Platform Service Document", size=16, bold=True)
add_center_line(doc, "Version: 004", size=11, bold=False)

doc.add_paragraph("")
doc.add_heading("Table of Contents", level=1)
doc.add_paragraph("1. Overview")
doc.add_paragraph("2. Foundry Resource Creation Steps")
doc.add_paragraph("3. Other Resource Creation Steps")
doc.add_paragraph("4. Repository Structure")

doc.add_paragraph("")
doc.add_heading("1. Overview", level=1)
doc.add_paragraph("This guide covers the platform service deployment flow to create and manage Foundry platform resources in this repository.")
doc.add_paragraph("This document follows the same working pattern used in the reference guide: practical steps, screenshot checkpoints, and clear validation points.")
doc.add_paragraph("Flow:")
add_bullet(doc, "Pull latest changes and checkout to feature branch")
add_bullet(doc, "Update configuration files for the target environment")
add_bullet(doc, "Trigger workflow and validate Terraform plan")
add_bullet(doc, "Request approvals, merge PR, and run apply")
add_bullet(doc, "Validate resources in Azure portal")
add_image(doc, "01_actions_overview_annotated_cropped.png", "Screenshot: Actions overview (Trigger Foundry Setup runs)")

# PAGE 2
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch.")
doc.add_paragraph("2. Checkout with new feature branch naming convention: <RITM>/<change-name>.")
doc.add_paragraph("3. Update Foundry hub tfvars in environments/<env>/<segment>/foundry-hub.tfvars.")
doc.add_paragraph("4. Update Foundry hub configuration in iac/foundry_hub_configs/<segment>/config.yaml.")
doc.add_paragraph("5. Validate foundry index, subnet mapping, and region values before push.")
doc.add_paragraph("6. Push changes to remote feature branch.")
doc.add_paragraph("7. Go to Actions -> Trigger Foundry Setup -> Run Workflow.")
doc.add_paragraph("8. Select deployment option for platform flow and choose required segment/location.")
add_image(doc, "05_trigger_workflow_page_cropped.jpg", "Screenshot: Trigger workflow page")

# PAGE 3
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps (continued)", level=2)
doc.add_paragraph("9. Monitor the workflow and open Terraform Plan job.")
doc.add_paragraph("10. Validate that plan shows intended Foundry resource changes only.")
doc.add_paragraph("11. Check correct resource group and Foundry hub name selection.")
doc.add_paragraph("12. Check private endpoint and subnet are mapped correctly.")
doc.add_paragraph("13. Raise PR approval request and merge after reviewer sign-off.")
doc.add_paragraph("14. Approve workflow apply only after plan validation is complete.")
doc.add_paragraph("15. Once completed, validate Foundry hub and endpoint status in Azure portal.")
add_image(doc, "02_run_workflow_inputs_annotated_cropped.png", "Screenshot: Workflow inputs for Foundry resource creation")
add_image(doc, "03_run_summary_graph_annotated_cropped.png", "Screenshot: Plan and apply execution path")

# PAGE 4
doc.add_page_break()
doc.add_heading("3. Other Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch and create feature branch.")
doc.add_paragraph("2. Update platform-level tfvars in environments/<env>/platform.tfvars.")
doc.add_paragraph("3. Verify values for Log Analytics, Application Insights, and Key Vault related inputs.")
doc.add_paragraph("4. Push changes and create PR with a clear change summary.")
doc.add_paragraph("5. Trigger the same workflow with platform deployment option.")
doc.add_paragraph("6. Validate Terraform plan output before approval.")
doc.add_paragraph("7. Confirm there are no unrelated destroy actions in the plan.")
doc.add_paragraph("8. Approve and apply after mandatory review.")
doc.add_paragraph("9. Validate resource creation/update from Azure portal.")
add_image(doc, "07_plan_job_page_cropped.jpg", "Screenshot: Terraform plan job validation")

# PAGE 5
doc.add_page_break()
doc.add_heading("3. Other Resource Creation Steps (continued)", level=2)
doc.add_paragraph("Validation checklist after apply:")
add_bullet(doc, "Log Analytics workspace is created/updated in correct resource group")
add_bullet(doc, "Application Insights is linked and healthy")
add_bullet(doc, "Key Vault deployment status is successful")
add_bullet(doc, "Workflow run status is successful for plan and apply")
add_bullet(doc, "No drift-inducing changes are pending")
doc.add_paragraph("If any mismatch is found, revert incorrect changes in feature branch and rerun plan before apply.")
add_image(doc, "08_apply_job_page_cropped.jpg", "Screenshot: Apply job success verification")

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

doc.add_paragraph("Quick understanding:")
add_bullet(doc, "platform-hub path controls shared platform resources")
add_bullet(doc, "foundry-hub path controls Foundry hub resources")
add_bullet(doc, "workflow trigger remains common through Trigger Foundry Setup")

doc.add_paragraph("------------------------------------------End of document------------------------------------------")

doc.save(str(out_path))
print(str(out_path))
