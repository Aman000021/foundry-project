from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(width_cm, height_cm, title):
    """Create a placeholder image with proper sizing"""
    width_px = int(width_cm * 37.8)  # cm to pixels
    height_px = int(height_cm * 37.8)
    
    img = Image.new('RGB', (width_px, height_px), color='#F5F5F5')
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, width_px-1, height_px-1], outline='#CCCCCC', width=2)
    
    # Draw diagonal lines
    draw.line([0, 0, width_px, height_px], fill='#E0E0E0', width=1)
    draw.line([width_px, 0, 0, height_px], fill='#E0E0E0', width=1)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    text = f"[Screenshot Placeholder]\n{title}"
    draw.text((50, height_px//2 - 20), text, fill='#999999', font=font)
    
    return img

def add_screenshot_section(doc, figure_num, title, width_cm=15, height_cm=8, caption=""):
    """Add a screenshot section with proper formatting"""
    # Create placeholder image
    img = create_placeholder_image(width_cm, height_cm, title)
    img_path = f"/tmp/placeholder_{figure_num}.png"
    img.save(img_path)
    
    # Add centered paragraph with image
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.add_picture(img_path, width=Cm(width_cm))
    
    # Add caption
    caption_para = doc.add_paragraph()
    caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_run = caption_para.add_run(caption)
    caption_run.font.size = Pt(10)
    caption_run.font.italic = True
    caption_run.font.color.rgb = RGBColor(64, 64, 64)
    
    # Add spacing
    caption_para.paragraph_format.space_before = Pt(6)
    caption_para.paragraph_format.space_after = Pt(12)
    
    # Cleanup
    if os.path.exists(img_path):
        os.remove(img_path)

# Open document
doc = Document(r'c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_v2.docx')

# Find all sections and replace placeholders
sections_to_update = {
    "1. Overview": {
        "placeholder": "[Insert Screenshot Here] - High-level deployment flow diagram",
        "figure": 1,
        "title": "Deployment Flow",
        "width": 16,
        "height": 8,
        "caption": "Figure 1 - High-Level Agent Service Deployment Flow"
    },
    "2. Architecture Diagram": {
        "placeholder": "[Insert Screenshot Here] - Deployment architecture from Service Now to Azure",
        "figure": 2,
        "title": "Deployment Architecture",
        "width": 16,
        "height": 9,
        "caption": "Figure 2 - Agent Service Deployment Architecture"
    },
    "3. Repository Structure": {
        "placeholder": "[Insert Screenshot Here] - Repository structure",
        "figure": 3,
        "title": "Repository Tree",
        "width": 15,
        "height": 8,
        "caption": "Figure 3 - Deployment Repository Structure"
    },
    "4. Configuration Update": {
        "placeholder": "[Insert Screenshot Here] - Config file update",
        "figure": 4,
        "title": "Config Entry",
        "width": 15,
        "height": 4,
        "caption": "Figure 4 - Sample Project Configuration Entry"
    },
    "5. Pull Request Process": {
        "placeholders": [
            {"text": "[Insert Screenshot Here] - GitHub PR approval and merge", "figure": 5, "title": "PR Creation", "width": 15, "height": 6, "caption": "Figure 5 - Pull Request Creation"},
            {"text": "[Insert Screenshot Here] - GitHub PR approval", "figure": 6, "title": "PR Approval", "width": 15, "height": 6, "caption": "Figure 6 - Pull Request Approval and Merge"}
        ]
    },
    "6. Terraform Plan": {
        "placeholders": [
            {"text": "[Insert Screenshot Here] - GitHub Actions workflow dispatch", "figure": 7, "title": "Workflow Inputs", "width": 15, "height": 6, "caption": "Figure 7 - Workflow Trigger Inputs"},
            {"text": "[Insert Screenshot Here] - Terraform plan output", "figure": 8, "title": "Plan Output", "width": 15, "height": 6, "caption": "Figure 8 - Terraform Plan Execution"}
        ]
    },
    "7. Terraform Apply": {
        "placeholders": [
            {"text": "[Insert Screenshot Here] - Manual approval gate in GitHub Environments", "figure": 9, "title": "Approval Gate", "width": 15, "height": 6, "caption": "Figure 9 - Deployment Approval Gate"},
            {"text": "[Insert Screenshot Here] - Terraform apply job execution", "figure": 10, "title": "Apply Execution", "width": 15, "height": 6, "caption": "Figure 10 - Terraform Apply Execution"},
            {"text": "[Insert Screenshot Here] - Azure resource creation confirmation", "figure": 11, "title": "Azure Resources", "width": 15, "height": 6, "caption": "Figure 11 - Azure Resources Created"}
        ]
    }
}

# Process document
paragraphs_to_remove = []
for i, para in enumerate(doc.paragraphs):
    text = para.text
    
    # Find matching sections
    for section_key, section_data in sections_to_update.items():
        if section_key in text and section_data.get("placeholder"):
            # Find and replace single placeholder
            for j in range(i+1, min(i+20, len(doc.paragraphs))):
                if section_data["placeholder"] in doc.paragraphs[j].text:
                    # Mark for replacement
                    para_to_replace = doc.paragraphs[j]
                    para_elem = para_to_replace._element
                    parent = para_elem.getparent()
                    
                    # Insert screenshot before removing
                    img = create_placeholder_image(section_data["width"], section_data["height"], section_data["title"])
                    img_path = f"c:\\temp\\placeholder_{section_data['figure']}.png"
                    os.makedirs("c:\\temp", exist_ok=True)
                    img.save(img_path)
                    
                    # Create new paragraph with image
                    new_para = doc.add_paragraph()
                    new_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = new_para.add_run()
                    run.add_picture(img_path, width=Cm(section_data["width"]))
                    
                    # Add caption
                    cap_para = doc.add_paragraph(section_data["caption"])
                    cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    cap_para.runs[0].font.size = Pt(10)
                    cap_para.runs[0].font.italic = True
                    cap_para.runs[0].font.color.rgb = RGBColor(64, 64, 64)
                    cap_para.paragraph_format.space_before = Pt(6)
                    cap_para.paragraph_format.space_after = Pt(12)
                    
                    # Remove placeholder
                    parent.remove(para_elem)
                    break
        
        # Handle multiple placeholders per section
        if section_key in text and section_data.get("placeholders"):
            for placeholder_info in section_data["placeholders"]:
                for j in range(i+1, min(i+50, len(doc.paragraphs))):
                    if placeholder_info["text"] in doc.paragraphs[j].text:
                        para_elem = doc.paragraphs[j]._element
                        parent = para_elem.getparent()
                        
                        # Create image
                        img = create_placeholder_image(placeholder_info["width"], placeholder_info["height"], placeholder_info["title"])
                        img_path = f"c:\\temp\\placeholder_{placeholder_info['figure']}.png"
                        os.makedirs("c:\\temp", exist_ok=True)
                        img.save(img_path)
                        
                        # Create new paragraph with image
                        new_para = doc.add_paragraph()
                        new_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        run = new_para.add_run()
                        run.add_picture(img_path, width=Cm(placeholder_info["width"]))
                        
                        # Add caption
                        cap_para = doc.add_paragraph(placeholder_info["caption"])
                        cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        cap_para.runs[0].font.size = Pt(10)
                        cap_para.runs[0].font.italic = True
                        cap_para.runs[0].font.color.rgb = RGBColor(64, 64, 64)
                        cap_para.paragraph_format.space_before = Pt(6)
                        cap_para.paragraph_format.space_after = Pt(12)
                        
                        # Remove placeholder
                        parent.remove(para_elem)
                        break

# Save
output_path = r'c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_With_Screenshots.docx'
doc.save(output_path)
print(f"✓ Document updated with screenshot sections")
print(f"✓ All placeholders replaced with formatted screenshot areas")
print(f"✓ Captions and proper sizing applied")
print(f"✓ Saved to: {output_path}")
