from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Create new document
doc = Document()

# Add title
title = doc.add_heading('Agent Service Deployment Guide (Stakeholder Ready)', 0)

# 1. Overview
doc.add_heading('1. Overview', 1)
doc.add_paragraph('This guide covers the Agent Service deployment pipeline triggered from a Service Now approved request.')
doc.add_paragraph('')
doc.add_paragraph('Flow: Service Now Request → Team Updates Config → PR Approved & Merged → Operator Triggers Pipeline → Terraform Plan & Apply → Azure Resources Created')
doc.add_paragraph('')
doc.add_paragraph('Outcome: Foundry projects, IAM role assignments, and Azure infrastructure deployed to target environment.')
doc.add_paragraph('[Insert Screenshot Here] - High-level deployment flow diagram')

# 2. Architecture Diagram
doc.add_heading('2. Architecture Diagram', 1)
doc.add_paragraph('Service Now Request Approved → Project Config Updated → GitHub Workflow Triggered → Terraform Plan (dv/pp/pr) → Manual Approval Gate → Terraform Apply → Azure Resources & Foundry Projects Created')
doc.add_paragraph('[Insert Screenshot Here] - Deployment architecture from Service Now to Azure')

# 3. Repository Structure
doc.add_heading('3. Repository Structure', 1)
doc.add_paragraph('Key deployment files:')
doc.add_paragraph('iac/project_configs/marketing/config.yaml - Project definitions (updated after Service Now approval)', style='List Bullet')
doc.add_paragraph('.github/workflows/iac.yaml - Main trigger workflow (Trigger Foundry Setup)', style='List Bullet')
doc.add_paragraph('.github/workflows/agent-capability-deploy.yml - Reusable deployment workflow', style='List Bullet')
doc.add_paragraph('environments/dv/marketing/agent-service.tfvars - Environment-specific variables', style='List Bullet')
doc.add_paragraph('iac/capability/agent-service/ - Terraform modules for agent service deployment', style='List Bullet')
doc.add_paragraph('[Insert Screenshot Here] - Repository structure')

# 4. Configuration Update
doc.add_heading('4. Configuration Update', 1)
doc.add_paragraph('1. Service Now request is approved with project details (name, segment, manager IDs, location)')
doc.add_paragraph('2. Team adds new entry to iac/project_configs/marketing/config.yaml with approved details')
doc.add_paragraph('3. Team creates Pull Request with config changes')
doc.add_paragraph('4. Reviewer approves PR')
doc.add_paragraph('5. Merge to main branch triggers workflow readiness')
doc.add_paragraph('')
doc.add_paragraph('Config entry example:')
code_para = doc.add_paragraph('- project_name: [approved_project_name]')
code_para = doc.add_paragraph('  project_segment: marketing')
code_para = doc.add_paragraph('  foundry_index: \'mkt001\'')
code_para = doc.add_paragraph('  project_manager_group_id: [from_service_now]')
code_para = doc.add_paragraph('  project_manager_user_id: [from_service_now]')
doc.add_paragraph('[Insert Screenshot Here] - Config file update')

# 5. Pull Request Process
doc.add_heading('5. Pull Request Process', 1)
doc.add_paragraph('1. Team creates PR against main branch with updated config.yaml')
doc.add_paragraph('2. PR reviewers verify:')
doc.add_paragraph('Service Now ticket reference is included', style='List Bullet 2')
doc.add_paragraph('Project details match approved request', style='List Bullet 2')
doc.add_paragraph('Manager IDs are correct', style='List Bullet 2')
doc.add_paragraph('3. Approval → Merge to main branch')
doc.add_paragraph('4. Merge automatically triggers GitHub Actions readiness')
doc.add_paragraph('5. Config is now available for pipeline consumption')
doc.add_paragraph('[Insert Screenshot Here] - GitHub PR approval and merge')

# 6. Terraform Plan
doc.add_heading('6. Terraform Plan', 1)
doc.add_paragraph('Trigger: Click \'Trigger Foundry Setup\' workflow in GitHub Actions')
doc.add_paragraph('')
doc.add_paragraph('Inputs required:')
doc.add_paragraph('Environment: Choose Dev (dv), Pre-Prod (pp), or Prod (pr)', style='List Bullet')
doc.add_paragraph('Project Segment: Select \'marketing\' (or applicable segment)', style='List Bullet')
doc.add_paragraph('Location: Select \'europe\' (or applicable region)', style='List Bullet')
doc.add_paragraph('')
doc.add_paragraph('Pipeline execution:')
doc.add_paragraph('iac.yaml dispatches to agent-capability-deploy.yml with selected inputs')
doc.add_paragraph('Workflow reads environment variables from environments/[env]/marketing/agent-service.tfvars')
doc.add_paragraph('Terraform initializes state backend from backend-config-project.tfvars')
doc.add_paragraph('Terraform plan executed against iac/capability/agent-service/')
doc.add_paragraph('Plan output saved as tfplan artifact (uploaded for apply stage)')
doc.add_paragraph('')
doc.add_paragraph('Validation: Review plan output for resource creation details, cost estimation, and IAM role assignments')
doc.add_paragraph('[Insert Screenshot Here] - GitHub Actions workflow dispatch')
doc.add_paragraph('[Insert Screenshot Here] - Terraform plan output')

# 7. Terraform Apply
doc.add_heading('7. Terraform Apply', 1)
doc.add_paragraph('Prerequisites: terraform plan completed successfully AND manual approval provided')
doc.add_paragraph('Branch condition: Apply only runs if branch = \'updated-foundry-deployment\'')
doc.add_paragraph('')
doc.add_paragraph('Approval gate:')
doc.add_paragraph('1. Plan completes → automatic pause at environment-approval gate')
doc.add_paragraph('2. Authorized reviewer approves in GitHub Environments UI')
doc.add_paragraph('3. Apply automatically triggered after approval')
doc.add_paragraph('')
doc.add_paragraph('Apply execution:')
doc.add_paragraph('Terraform downloads tfplan artifact from plan stage')
doc.add_paragraph('Applies configuration: terraform apply tfplan')
doc.add_paragraph('Creates Azure resources:', style='List Bullet')
doc.add_paragraph('Foundry Hub projects (one per config.yaml entry)', style='List Bullet 2')
doc.add_paragraph('Azure role assignments for project managers', style='List Bullet 2')
doc.add_paragraph('Project-level resource groups', style='List Bullet 2')
doc.add_paragraph('Key Vaults, storage accounts, private endpoints', style='List Bullet 2')
doc.add_paragraph('')
doc.add_paragraph('Outcome: All approved projects deployed to Azure with proper IAM and connectivity configured')
doc.add_paragraph('[Insert Screenshot Here] - Manual approval gate in GitHub Environments')
doc.add_paragraph('[Insert Screenshot Here] - Terraform apply job execution')
doc.add_paragraph('[Insert Screenshot Here] - Azure resource creation confirmation')

# Save
output_path = r'c:\Users\XSPriyaGa\Downloads\Agent_Service_Deployment_Guide_Updated_v2.docx'
doc.save(output_path)
print(f"✓ Updated document created: {output_path}")
print(f"✓ Please close any open instances and rename/replace the original file")

