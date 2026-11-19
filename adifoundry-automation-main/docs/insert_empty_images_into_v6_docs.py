from pathlib import Path
from tempfile import TemporaryDirectory

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
from PIL import Image, ImageDraw

ROOT = Path(r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template")

AGENT_IN = ROOT / "docs/Agent_Service_Deployment_Guide_Updated_v6_PLACEHOLDERS_ONLY.docx"
AGENT_OUT = ROOT / "docs/Agent_Service_Deployment_Guide_Updated_v8_EMPTY_IMAGES.docx"

PLATFORM_IN = ROOT / "docs/Platform_Resources_Deployment_Guide_Updated_v6_PLACEHOLDERS_ONLY.docx"
PLATFORM_OUT = ROOT / "docs/Platform_Resources_Deployment_Guide_Updated_v8_EMPTY_IMAGES.docx"


def make_empty_image(path: Path, width_cm: float, height_cm: float):
    px_per_cm = 37.8
    w = max(100, int(width_cm * px_per_cm))
    h = max(60, int(height_cm * px_per_cm))

    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle((1, 1, w - 2, h - 2), outline="#B8B8B8", width=3)
    # Light guide diagonals
    draw.line((8, 8, w - 8, h - 8), fill="#D6D6D6", width=2)
    draw.line((w - 8, 8, 8, h - 8), fill="#D6D6D6", width=2)

    img.save(path)


def apply_empty_images(doc_in: Path, doc_out: Path, size_map: dict):
    doc = Document(str(doc_in))
    inserted = 0

    with TemporaryDirectory() as td:
        td_path = Path(td)

        for para in doc.paragraphs:
            txt = para.text.strip()

            if txt.startswith("Screenshot Placeholder: [Insert Screenshot Here] - "):
                key = txt.replace("Screenshot Placeholder: [Insert Screenshot Here] - ", "").strip()
                width_cm, height_cm = size_map.get(key, (15.0, 8.0))

                img_file = td_path / f"empty_{inserted + 1}.png"
                make_empty_image(img_file, width_cm, height_cm)

                para.clear()
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = para.add_run()
                run.add_picture(str(img_file), width=Cm(width_cm), height=Cm(height_cm))
                inserted += 1

            if txt.startswith("Caption:"):
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if para.runs:
                    para.runs[0].font.size = Pt(10)
                    para.runs[0].italic = True
                para.paragraph_format.space_before = Pt(4)
                para.paragraph_format.space_after = Pt(10)

    doc.save(str(doc_out))
    return inserted


def main():
    agent_sizes = {
        "High-level agent onboarding infrastructure flow": (16.0, 8.0),
        "Agent infrastructure architecture (Service Now to Terraform apply)": (16.0, 9.0),
        "Repository tree with iac, environments, and workflow files": (15.0, 8.0),
        "Config.yaml entry with project_name, segment, index, manager and user IDs": (15.0, 4.0),
        "PR creation and approval details": (15.0, 6.0),
        "Workflow trigger input panel (choice, segment, location)": (15.0, 6.0),
        "Terraform plan job execution logs": (15.0, 6.0),
        "Environment approval gate": (15.0, 6.0),
        "Terraform apply job execution": (15.0, 6.0),
        "Validation in Foundry and Azure IAM": (15.0, 6.0),
    }

    platform_sizes = {
        "High-level platform infrastructure flow": (16.0, 8.0),
        "Platform deployment architecture (shared infra only)": (16.0, 9.0),
        "Repository tree with platform and foundry-hub deployment files": (15.0, 8.0),
        "Platform/foundry-hub config update section": (15.0, 4.0),
        "PR creation and approval for platform flow": (15.0, 6.0),
        "Workflow trigger input panel (platform choice)": (15.0, 6.0),
        "Plan execution for platform-hub and foundry-hub": (15.0, 6.0),
        "Environment approval gate": (15.0, 6.0),
        "Apply execution for platform and foundry-hub": (15.0, 6.0),
        "Validation in Azure for platform resources": (15.0, 6.0),
    }

    a = apply_empty_images(AGENT_IN, AGENT_OUT, agent_sizes)
    p = apply_empty_images(PLATFORM_IN, PLATFORM_OUT, platform_sizes)

    print(f"Agent empty images inserted: {a}")
    print(f"Platform empty images inserted: {p}")
    print(f"Created: {AGENT_OUT}")
    print(f"Created: {PLATFORM_OUT}")


if __name__ == "__main__":
    main()
