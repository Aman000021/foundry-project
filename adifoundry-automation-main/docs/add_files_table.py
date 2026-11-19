from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def shade_cell(cell, fill_color):
    """Add background color to table cell"""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), fill_color)
    cell._element.get_or_add_tcPr().append(shading_elm)

# Open the document
doc = Document(r'c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_v2.docx')

# Find and update section 3 (Repository Structure)
repo_section_idx = None
for i, para in enumerate(doc.paragraphs):
    if "3. Repository Structure" in para.text:
        repo_section_idx = i
        break

if repo_section_idx is not None:
    # Find the next section heading or end
    next_section_idx = None
    for i in range(repo_section_idx + 1, len(doc.paragraphs)):
        if any(f"{j}." in doc.paragraphs[i].text for j in range(1, 10)):
            if doc.paragraphs[i].style.name.startswith('Heading'):
                next_section_idx = i
                break
    
    if next_section_idx is None:
        next_section_idx = len(doc.paragraphs)
    
    # Remove old content between section heading and next section
    removal_indices = []
    for i in range(repo_section_idx + 1, next_section_idx):
        para = doc.paragraphs[i]
        if para.text.strip() and not any(f"{j}." in para.text for j in range(1, 10)):
            removal_indices.append(i)
    
    # Remove in reverse order to maintain indices
    for idx in reversed(removal_indices):
        p = doc.paragraphs[idx]._element
        p.getparent().remove(p)
    
    # Insert table after the heading
    heading_para = doc.paragraphs[repo_section_idx]
    
    # Create table: 2 columns, 6 rows (header + 5 files)
    table = doc.add_table(rows=6, cols=2)
    table.style = 'Light Grid Accent 1'
    
    # Set column widths
    for row in table.rows:
        row.cells[0].width = Inches(2.5)
        row.cells[1].width = Inches(4.0)
    
    # Header row
    header_cells = table.rows[0].cells
    shade_cell(header_cells[0], '5B8DEF')
    shade_cell(header_cells[1], '5B8DEF')
    
    for cell in header_cells:
        for paragraph in cell.paragraphs:
            paragraph.clear()
    
    header_text = ['File / Directory', 'Purpose']
    for idx, text in enumerate(header_text):
        para = header_cells[idx].paragraphs[0]
        para.text = text
        para.runs[0].font.bold = True
        para.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Data rows
    data = [
        ('iac/project_configs/marketing/config.yaml', 'Project definitions (updated after Service Now approval)'),
        ('.github/workflows/iac.yaml', 'Main trigger workflow (Trigger Foundry Setup)'),
        ('.github/workflows/agent-capability-deploy.yml', 'Reusable deployment workflow'),
        ('environments/dv/marketing/agent-service.tfvars', 'Environment-specific variables'),
        ('iac/capability/agent-service/', 'Terraform modules for agent service deployment'),
    ]
    
    for row_idx, (file_path, purpose) in enumerate(data, start=1):
        cells = table.rows[row_idx].cells
        
        # File/Directory cell
        para = cells[0].paragraphs[0]
        para.text = file_path
        para.runs[0].font.size = Pt(10)
        para.runs[0].font.bold = True
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        # Purpose cell
        para = cells[1].paragraphs[0]
        para.text = purpose
        para.runs[0].font.size = Pt(10)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        # Alternate row colors
        if row_idx % 2 == 0:
            for cell in cells:
                shade_cell(cell, 'F7FBFF')
    
    # Add screenshot placeholder after table
    doc.add_paragraph('[Insert Screenshot Here] - Repository structure overview')

# Save
output_path = r'c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_v3.docx'
doc.save(output_path)
print(f"✓ Document updated with deployment files table")
print(f"✓ Saved to: {output_path}")
