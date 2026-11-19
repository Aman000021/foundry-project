from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import shutil
import os

doc = Document(r'c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated.docx')

# Dictionary mapping section titles to updated content
updates = {
    "1. Overview": [
        "This guide covers the Agent Service deployment pipeline triggered from a Service Now approved request.",
        "",
        "Flow: Service Now Request → Team Updates Config → PR Approved & Merged → Operator Triggers Pipeline → "
        "Terraform Plan & Apply → Azure Resources Created",
        "",
        "Outcome: Foundry projects, IAM role assignments, and Azure infrastructure deployed to target environment."
    ],
    "2. Architecture Diagram": [
        "Service Now Request Approved → Project Config Updated → GitHub Workflow Triggered → "
        "Terraform Plan (dv/pp/pr) → Manual Approval Gate → Terraform Apply → Azure Resources & Foundry Projects Created"
    ],
    "3. Repository Structure": [
        "Key deployment files:",
        "• iac/project_configs/marketing/config.yaml - Project definitions (updated after Service Now approval)",
        "• .github/workflows/iac.yaml - Main trigger workflow (Trigger Foundry Setup)",
        "• .github/workflows/agent-capability-deploy.yml - Reusable deployment workflow",
        "• environments/dv/marketing/agent-service.tfvars - Environment-specific variables",
        "• iac/capability/agent-service/ - Terraform modules for agent service deployment"
    ],
    "4. Configuration Update": [
        "1. Service Now request is approved with project details (name, segment, manager IDs, location)",
        "2. Team adds new entry to iac/project_configs/marketing/config.yaml with approved details",
        "3. Team creates Pull Request with config changes",
        "4. Reviewer approves PR",
        "5. Merge to main branch triggers workflow readiness",
        "",
        "Config entry example:",
        "- project_name: [approved_project_name]",
        "  project_segment: marketing",
        "  foundry_index: 'mkt001'",
        "  project_manager_group_id: [from_service_now]",
        "  project_manager_user_id: [from_service_now]"
    ],
    "5. Pull Request Process": [
        "1. Team creates PR against main branch with updated config.yaml",
        "2. PR reviewers verify:",
        "   - Service Now ticket reference is included",
        "   - Project details match approved request",
        "   - Manager IDs are correct",
        "3. Approval → Merge to main branch",
        "4. Merge automatically triggers GitHub Actions readiness",
        "5. Config is now available for pipeline consumption"
    ],
    "6. Terraform Plan": [
        "Trigger: Click 'Trigger Foundry Setup' workflow in GitHub Actions",
        "Inputs required:",
        "• Environment: Choose Dev (dv), Pre-Prod (pp), or Prod (pr)",
        "• Project Segment: Select 'marketing' (or applicable segment)",
        "• Location: Select 'europe' (or applicable region)",
        "",
        "Pipeline execution:",
        "1. iac.yaml dispatches to agent-capability-deploy.yml with selected inputs",
        "2. Workflow reads environment variables from environments/[env]/marketing/agent-service.tfvars",
        "3. Terraform initializes state backend from backend-config-project.tfvars",
        "4. Terraform plan executed against iac/capability/agent-service/",
        "5. Plan output saved as tfplan artifact (uploaded for apply stage)",
        "",
        "Validation: Review plan output for resource creation details, cost estimation, and IAM role assignments"
    ],
    "7. Terraform Apply": [
        "Prerequisites: terraform plan completed successfully AND manual approval provided",
        "Branch condition: Apply only runs if branch = 'updated-foundry-deployment'",
        "",
        "Approval gate:",
        "1. Plan completes → automatic pause at environment-approval gate",
        "2. Authorized reviewer approves in GitHub Environments UI",
        "3. Apply automatically triggered after approval",
        "",
        "Apply execution:",
        "1. Terraform downloads tfplan artifact from plan stage",
        "2. Applies configuration: terraform apply tfplan",
        "3. Creates Azure resources:",
        "   - Foundry Hub projects (one per config.yaml entry)",
        "   - Azure role assignments for project managers",
        "   - Project-level resource groups",
        "   - Key Vaults, storage accounts, private endpoints",
        "",
        "Outcome: All approved projects deployed to Azure with proper IAM and connectivity configured"
    ]
}

# Find sections and update them
section_found = {}
current_section = None

for i, para in enumerate(doc.paragraphs):
    for section_key in updates:
        if section_key in para.text:
            current_section = section_key
            section_found[section_key] = i
            break

# Update content after each section heading
for section_key, content_lines in updates.items():
    if section_key in section_found:
        heading_idx = section_found[section_key]
        # Find the next section heading or end of document
        next_section_idx = None
        for other_key in updates:
            if other_key != section_key and other_key in section_found:
                if section_found[other_key] > heading_idx:
                    if next_section_idx is None or section_found[other_key] < next_section_idx:
                        next_section_idx = section_found[other_key]
        
        if next_section_idx is None:
            next_section_idx = len(doc.paragraphs)
        
        # Remove old content paragraphs until next section (but keep heading)
        removal_count = 0
        for j in range(heading_idx + 1, next_section_idx):
            if j - removal_count < len(doc.paragraphs):
                p = doc.paragraphs[j - removal_count]
                # Stop if we hit another section heading
                if any(s in p.text for s in updates if s != section_key):
                    break
                # Remove paragraph if it's placeholder or old content
                if p.text.strip() and not p.text.strip().startswith(tuple([s for s in updates if s != section_key])):
                    p_elem = p._element
                    p_elem.getparent().remove(p_elem)
                    removal_count += 1
        
        # Insert new content after heading
        heading_para = doc.paragraphs[heading_idx]
        insert_after = heading_para._element
        
        for line in content_lines:
            if line == "":
                new_para = heading_para._element.addnext(doc.add_paragraph("")._element)
            else:
                # Determine if this is a bullet or regular text
                if line.startswith("•"):
                    new_para = doc.add_paragraph(line, style='List Bullet')._element
                else:
                    new_para = doc.add_paragraph(line)._element
                insert_after.addnext(new_para)
                insert_after = new_para

import shutil
import os
temp_path = r'c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_TEMP.docx'
final_path = r'c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated.docx'
doc.save(temp_path)
if os.path.exists(final_path):
    os.remove(final_path)
shutil.move(temp_path, final_path)
print("✓ Document updated with Service Now flow and exact pipeline details")
print("✓ Saved to: c:\\Users\\XSPriyaGa\\Downloads\\Agent_Service_Deployment_Guide_Updated.docx")
