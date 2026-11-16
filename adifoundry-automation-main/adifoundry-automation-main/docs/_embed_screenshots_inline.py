from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

BASE = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs")
INPUT_DOC = BASE / "Foundry_Onboarding_Deployment_Guide_CORRECTED.docx"
OUTPUT_DOC = BASE / "Foundry_Onboarding_Deployment_Guide_CORRECTED_INLINE_SCREENSHOTS.docx"
IMG = BASE / "screenshots" / "actions" / "cropped"


def insert_paragraph_after(paragraph, text="", style=None):
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    if text:
        new_para.add_run(text)
    if style:
        new_para.style = style
    return new_para


def find_paragraph(doc, needle):
    for p in doc.paragraphs:
        if p.text.strip() == needle:
            return p
    return None


def add_image_block(anchor_paragraph, image_path, caption):
    cap = insert_paragraph_after(anchor_paragraph, caption)
    cap.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    if cap.runs:
        cap.runs[0].bold = True
    cap.paragraph_format.space_before = Pt(6)
    cap.paragraph_format.space_after = Pt(4)

    img_para = insert_paragraph_after(cap)
    img_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = img_para.add_run()
    run.add_picture(str(image_path), width=Inches(6.2))
    img_para.paragraph_format.space_after = Pt(12)
    return img_para


doc = Document(str(INPUT_DOC))

# Ordered placements: screenshot appears directly below relevant section content.
placements = [
    (
        "8. PIPELINE EXECUTION FLOW",
        [
            (
                IMG / "04_actions_overview_current_cropped.jpg",
                "Figure 1. GitHub Actions overview for this repository",
            ),
            (
                IMG / "01_actions_overview_annotated_cropped.png",
                "Figure 2. Actions run list with Trigger Foundry Setup highlighted",
            ),
        ],
    ),
    (
        "Step 3: Trigger GitHub Deployment Pipeline",
        [
            (
                IMG / "02_run_workflow_inputs_annotated_cropped.png",
                "Figure 3. Manual workflow trigger inputs (environment, segment, location)",
            ),
        ],
    ),
    (
        "Workflow 3: .github/workflows/agent-capability-deploy.yml (USED for onboarding)",
        [
            (
                IMG / "05_trigger_workflow_page_cropped.jpg",
                "Figure 4. Trigger Foundry Setup workflow page",
            ),
        ],
    ),
    (
        "Step 8: Deployment Validation",
        [
            (
                IMG / "03_run_summary_graph_annotated_cropped.png",
                "Figure 5. Run summary graph with plan/apply path highlighted",
            ),
        ],
    ),
    (
        "STEP 1: VERIFY TERRAFORM SUCCESS",
        [
            (
                IMG / "06_run_summary_page_cropped.jpg",
                "Figure 6. Workflow run summary used for success verification",
            ),
            (
                IMG / "07_plan_job_page_cropped.jpg",
                "Figure 7. Plan job details page",
            ),
            (
                IMG / "08_apply_job_page_cropped.jpg",
                "Figure 8. Apply job details page",
            ),
        ],
    ),
]

missing = []
for target, items in placements:
    anchor = find_paragraph(doc, target)
    if not anchor:
        missing.append(f"Missing target paragraph: {target}")
        continue

    current_anchor = anchor
    for image_path, caption in items:
        if not image_path.exists():
            missing.append(f"Missing image: {image_path.name}")
            continue
        current_anchor = add_image_block(current_anchor, image_path, caption)

if missing:
    warn = doc.add_paragraph("Image embedding warnings:")
    warn.runs[0].bold = True
    for m in missing:
        doc.add_paragraph(m)

doc.save(str(OUTPUT_DOC))

print(f"Created: {OUTPUT_DOC}")
if missing:
    print("Warnings:")
    for m in missing:
        print(f"- {m}")
else:
    print("All target sections and images were found and embedded.")
