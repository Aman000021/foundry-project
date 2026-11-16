from pathlib import Path
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

base = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs")
out_path = base / "Platform_Service_Document_006.docx"

# Source screenshots (reference-like mix: flow + code + workflow evidence)
imgs = {
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

prepared_dir = base / "screenshots" / "platform_doc_v6"
prepared_dir.mkdir(parents=True, exist_ok=True)


def set_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(11)
    for s in ["Heading 1", "Heading 2", "Heading 3"]:
        if s in doc.styles:
            doc.styles[s].font.name = "Aptos"


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
    p.add_run("Version: 006")


def add_toc(doc):
    doc.add_heading("Table of Contents", level=1)
    doc.add_paragraph("1. Overview")
    doc.add_paragraph("2. Foundry Resource Creation Steps")
    doc.add_paragraph("3. Other Resource Creation Steps")
    doc.add_paragraph("4. Repository Structure")


def prep_image(name, src: Path):
    if not src.exists():
        return None
    out = prepared_dir / f"{name}{src.suffix}"
    with Image.open(src) as im:
        w, h = im.size
        # For wide code screenshots, crop to useful left content region for readability.
        if "iac_" in name and w > 2200:
            cw = int(w * 0.60)
            ch = int(h * 0.80)
            im = im.crop((0, 0, cw, ch))
        # For flow diagrams, keep full frame.
        im.save(out, quality=92)
    return out


def add_image(doc, path: Path, caption: str, width=6.0):
    if not path or not path.exists():
        doc.add_paragraph(f"Screenshot not found: {caption}")
        return
    cap = doc.add_paragraph(caption)
    cap.runs[0].bold = True
    cap.paragraph_format.space_after = Pt(3)

    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.add_run().add_picture(str(path), width=Inches(width))
    p.paragraph_format.space_after = Pt(8)


prepared = {k: prep_image(k, v) for k, v in imgs.items()}

doc = Document()
set_styles(doc)

# Page 1
add_title(doc)
doc.add_paragraph("")
add_toc(doc)
doc.add_paragraph("")
doc.add_heading("1. Overview", level=1)
doc.add_paragraph("This guide covers platform service deployment for MS Foundry resources using this repository.")
doc.add_paragraph("The structure and sentence style follow the same pattern used in the referenced deployment guide.")
doc.add_paragraph("Flow:")
doc.add_paragraph("- Review request and prepare branch")
doc.add_paragraph("- Update config files and validate values")
doc.add_paragraph("- Run workflow and check terraform plan")
doc.add_paragraph("- Request approval, merge, and apply")
doc.add_paragraph("- Validate resources in Azure")
add_image(doc, prepared["flow_pipeline"], "Screenshot: Platform deployment flow diagram", width=6.2)

# Page 2
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main branch.")
doc.add_paragraph("2. Checkout with feature branch naming convention: <RITM>/<change-name>.")
doc.add_paragraph("3. Update environments/<env>/<segment>/foundry-hub.tfvars.")
doc.add_paragraph("4. Update iac/foundry_hub_configs/<segment>/config.yaml.")
doc.add_paragraph("5. Validate foundry index, subnet, and location details.")
doc.add_paragraph("6. Push changes to remote feature branch.")
add_image(doc, prepared["iac_hub_cfg"], "Screenshot: Foundry hub config fields", width=5.8)
add_image(doc, prepared["iac_foundry_module"], "Screenshot: Foundry hub Terraform module", width=5.8)

# Page 3
doc.add_page_break()
doc.add_heading("2. Foundry Resource Creation Steps (continued)", level=2)
doc.add_paragraph("7. Go to Actions and trigger 'Trigger Foundry Setup'.")
doc.add_paragraph("8. Select platform deployment option, segment, and location.")
doc.add_paragraph("9. Monitor Terraform Plan and validate intended changes.")
doc.add_paragraph("10. Raise PR approval and merge after validation.")
doc.add_paragraph("11. Approve apply and validate resource creation.")
add_image(doc, prepared["run_input"], "Screenshot: Workflow input selection", width=6.0)
add_image(doc, prepared["run_plan"], "Screenshot: Terraform plan job validation", width=6.0)
add_image(doc, prepared["run_apply"], "Screenshot: Terraform apply job validation", width=6.0)

# Page 4
doc.add_page_break()
doc.add_heading("3. Other Resource Creation Steps", level=1)
doc.add_paragraph("1. Pull latest changes from main and create feature branch.")
doc.add_paragraph("2. Update environments/<env>/platform.tfvars with required values.")
doc.add_paragraph("3. Validate monitoring resources and security resource settings.")
doc.add_paragraph("4. Push changes and raise PR for review.")
doc.add_paragraph("5. Trigger workflow and verify platform-hub and foundry-hub sequence.")
doc.add_paragraph("6. Validate no unintended destroy actions in plan.")
doc.add_paragraph("7. Approve and apply after reviewer sign-off.")
add_image(doc, prepared["iac_trigger"], "Screenshot: Trigger workflow YAML (iac.yaml)", width=5.8)
add_image(doc, prepared["iac_platform_wf"], "Screenshot: Platform deploy workflow YAML", width=5.8)

# Page 5
doc.add_page_break()
doc.add_heading("3. Other Resource Creation Steps (continued)", level=2)
doc.add_paragraph("8. Validate platform resources in Azure after apply completion.")
doc.add_paragraph("9. Confirm expected components are available in target resource groups.")
doc.add_paragraph("10. Re-run plan if any drift or mismatch is identified.")
add_image(doc, prepared["flow_arch"], "Screenshot: Platform deployment architecture diagram", width=6.2)
add_image(doc, prepared["iac_platform_module"], "Screenshot: Platform module Terraform code", width=5.8)

# Page 6
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
doc.add_paragraph("- Keep platform resource updates in dedicated feature branches.")
doc.add_paragraph("- Validate Terraform plan before every approval.")
doc.add_paragraph("- Use this structure as the quick reference for platform-side changes.")
doc.add_paragraph("------------------------------------------End of document------------------------------------------")

doc.save(str(out_path))
print(str(out_path))
