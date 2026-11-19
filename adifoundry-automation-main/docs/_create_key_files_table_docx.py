from docx import Document

out_path = r"c:\Users\XSPriyaGa\Downloads\npet-foundry-template\docs\Platform_Key_Deployment_Files_Table.docx"

doc = Document()
doc.add_heading("Key Deployment Files", level=1)

table = doc.add_table(rows=12, cols=2)
table.style = "Light Grid Accent 1"

table.rows[0].cells[0].text = "File / Directory"
table.rows[0].cells[1].text = "Purpose"
table.rows[1].cells[0].text = ".github/workflows/iac.yaml"
table.rows[1].cells[1].text = "Entry workflow to trigger infrastructure deployment flows."
table.rows[2].cells[0].text = ".github/workflows/platform-deploy.yml"
table.rows[2].cells[1].text = "Reusable workflow that deploys platform and hub infrastructure."
table.rows[3].cells[0].text = ".github/workflows/agent-capability-deploy.yml"
table.rows[3].cells[1].text = "Reusable workflow for agent capability infrastructure deployment."
table.rows[4].cells[0].text = "environments/<env>/platform.tfvars"
table.rows[4].cells[1].text = "Environment-level platform variables used during Terraform plan/apply."
table.rows[5].cells[0].text = "environments/<env>/<segment>/foundry-hub.tfvars"
table.rows[5].cells[1].text = "Segment-level hub variables for Foundry hub deployment."
table.rows[6].cells[0].text = "environments/<env>/<segment>/backend-config-hub.tfvars"
table.rows[6].cells[1].text = "Terraform backend state configuration for hub stack per env/segment."
table.rows[7].cells[0].text = "iac/platform-hub/"
table.rows[7].cells[1].text = "Terraform root stack for platform-hub resource deployment."
table.rows[8].cells[0].text = "iac/capability/foundry-hub/"
table.rows[8].cells[1].text = "Terraform root stack for foundry-hub capability resources."
table.rows[9].cells[0].text = "iac/modules/platform/"
table.rows[9].cells[1].text = "Shared Terraform module definitions for platform resources."
table.rows[10].cells[0].text = "iac/modules/foundry-hub/"
table.rows[10].cells[1].text = "Shared Terraform module definitions for foundry-hub resources."
table.rows[11].cells[0].text = "iac/foundry_hub_configs/<segment>/config.yaml"
table.rows[11].cells[1].text = "Segment onboarding/config metadata consumed by deployment flows."

doc.save(out_path)
print(out_path)
