from pathlib import Path
from PIL import Image
from docx import Document
from docx.shared import Inches, Pt

base = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs")
src = base / "screenshots" / "actions"
cropped_dir = src / "cropped"
cropped_dir.mkdir(parents=True, exist_ok=True)

# Crop rules: keep only the upper, relevant part; remove overly long tails/log lengths.
max_heights = {
    "01_actions_overview_annotated.png": 1700,
    "02_run_workflow_inputs_annotated.png": 2300,
    "03_run_summary_graph_annotated.png": 2200,
    "04_actions_overview_current.jpg": 1700,
    "05_trigger_workflow_page.jpg": 2300,
    "06_run_summary_page.jpg": 2200,
    "07_plan_job_page.jpg": 1200,
    "08_apply_job_page.jpg": 1200,
}

captions = {
    "01_actions_overview_annotated.png": "Actions Overview (workflow list and latest Trigger Foundry Setup run)",
    "02_run_workflow_inputs_annotated.png": "Run Workflow Inputs (choice, segment, location)",
    "03_run_summary_graph_annotated.png": "Run Summary Graph (successful plan and apply path)",
    "04_actions_overview_current.jpg": "Current Actions Overview page",
    "05_trigger_workflow_page.jpg": "Trigger Foundry Setup workflow page",
    "06_run_summary_page.jpg": "Run summary details and execution graph",
    "07_plan_job_page.jpg": "Plan job page",
    "08_apply_job_page.jpg": "Apply job page",
}

cropped_files = []
for name, max_h in max_heights.items():
    in_path = src / name
    if not in_path.exists():
        continue

    with Image.open(in_path) as im:
        w, h = im.size
        new_h = min(h, max_h)
        cropped = im.crop((0, 0, w, new_h))

        out_name = f"{Path(name).stem}_cropped{Path(name).suffix}"
        out_path = cropped_dir / out_name
        cropped.save(out_path, quality=92)
        cropped_files.append((out_path, captions.get(name, name)))

input_doc = base / "Foundry_Onboarding_Deployment_Guide_CORRECTED.docx"
output_doc = base / "Foundry_Onboarding_Deployment_Guide_CORRECTED_WITH_SCREENSHOTS.docx"

doc = Document(str(input_doc))

doc.add_page_break()
h = doc.add_heading("13. Workflow Screenshot Evidence", level=1)
for run in h.runs:
    run.bold = True

intro = doc.add_paragraph(
    "The following screenshots were captured from existing GitHub Actions pages. "
    "Long log/page tails were cropped to keep only relevant evidence."
)
intro.paragraph_format.space_after = Pt(10)

for img_path, caption in cropped_files:
    cap = doc.add_paragraph(caption)
    cap.runs[0].bold = True
    cap.paragraph_format.space_after = Pt(6)

    doc.add_picture(str(img_path), width=Inches(6.2))
    p = doc.paragraphs[-1]
    p.paragraph_format.space_after = Pt(12)

# Save as new version to preserve original.
doc.save(str(output_doc))

print(f"Created: {output_doc}")
print(f"Cropped images: {cropped_dir}")
for p, _ in cropped_files:
    print(p.name)
