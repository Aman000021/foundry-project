from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_figure_guide(doc, fig_num, title, source, nav_steps, capture, highlight, crop, width_px, height_px, blur_notes, caption):
    doc.add_heading(f"Figure {fig_num}: {title}", 2)
    
    doc.add_paragraph(f"Source: {source}", style="List Bullet")
    
    if nav_steps:
        doc.add_paragraph("Navigation Steps:", style="List Bullet")
        for step in nav_steps:
            doc.add_paragraph(step, style="List Number 2")
    
    doc.add_paragraph(f"Capture: {capture}", style="List Bullet")
    
    if highlight:
        doc.add_paragraph(f"Highlight: {highlight}", style="List Bullet")
    
    doc.add_paragraph(f"Crop Area: {crop}", style="List Bullet")
    
    doc.add_paragraph(f"Recommended Size: {width_px}px × {height_px}px", style="List Bullet")
    
    if blur_notes:
        doc.add_paragraph(f"Blur/Redact: {blur_notes}", style="List Bullet")
    
    doc.add_paragraph(f"Caption: {caption}", style="List Bullet")
    
    doc.add_paragraph("[Insert Screenshot Here]")
    doc.add_paragraph("")


def main():
    doc = Document()
    doc.add_heading("Platform Deployment Guide - Screenshot Collection Reference", 0)
    doc.add_paragraph("This guide helps Manikandan and stakeholders capture the correct screenshots for each figure placeholder in the Platform Deployment Guide.")
    doc.add_paragraph("")

    # Figure 1
    doc.add_heading("FIGURE 1 – High-Level Platform Deployment Flow", 1)
    doc.add_paragraph("Type: Draw.io Architecture Diagram (NOT a screenshot)")
    doc.add_paragraph("Tool: Draw.io or similar diagram tool")
    doc.add_paragraph("")
    doc.add_paragraph("Diagram Flow Steps:")
    doc.add_paragraph("ServiceNow Request Approved", style="List Bullet")
    doc.add_paragraph("Platform Configuration Updated", style="List Bullet")
    doc.add_paragraph("Pull Request Created", style="List Bullet")
    doc.add_paragraph("Pull Request Reviewed & Approved", style="List Bullet")
    doc.add_paragraph("Merge to Main Branch", style="List Bullet")
    doc.add_paragraph("Operator Triggers Platform Deployment Pipeline", style="List Bullet")
    doc.add_paragraph("Terraform Plan", style="List Bullet")
    doc.add_paragraph("Terraform Apply", style="List Bullet")
    doc.add_paragraph("Platform Resources Provisioned", style="List Bullet")
    doc.add_paragraph("Platform Foundation Ready for Foundry Onboarding", style="List Bullet")
    doc.add_paragraph("")
    doc.add_paragraph("Design Style: Flowchart with boxes and arrows, left-to-right or top-to-bottom flow")
    doc.add_paragraph("Color Scheme: Use platform-neutral colors (blue/gray)")
    doc.add_paragraph("Recommended Size: 1600px × 900px")
    doc.add_paragraph("Caption: Figure 1 - High-Level Platform Deployment Flow")
    doc.add_paragraph("")

    # Figure 2
    doc.add_heading("FIGURE 2 – Platform Deployment Architecture", 1)
    doc.add_paragraph("Type: Draw.io Layered Architecture Diagram (NOT a screenshot)")
    doc.add_paragraph("Tool: Draw.io or similar diagram tool")
    doc.add_paragraph("")
    doc.add_paragraph("Diagram Layers:")
    
    doc.add_paragraph("Platform Layer (Bottom):", style="List Bullet")
    doc.add_paragraph("Azure AI Foundry Hub", style="List Bullet 2")
    doc.add_paragraph("Azure Key Vault", style="List Bullet 2")
    doc.add_paragraph("Key Vault Private Endpoint", style="List Bullet 2")
    doc.add_paragraph("Log Analytics Workspace", style="List Bullet 2")
    doc.add_paragraph("Application Insights", style="List Bullet 2")
    doc.add_paragraph("Storage Container", style="List Bullet 2")
    doc.add_paragraph("Private Endpoints", style="List Bullet 2")
    
    doc.add_paragraph("Foundry Layer (Middle):", style="List Bullet")
    doc.add_paragraph("Foundry Projects", style="List Bullet 2")
    doc.add_paragraph("Foundry Role Assignments", style="List Bullet 2")
    
    doc.add_paragraph("Use Case Layer (Top):", style="List Bullet")
    doc.add_paragraph("Future Use Case Resources", style="List Bullet 2")
    
    doc.add_paragraph("Show relationship: Platform Layer → Foundry Layer → Use Case Layer (vertical flow)")
    doc.add_paragraph("Recommended Size: 1600px × 1000px")
    doc.add_paragraph("Caption: Figure 2 - Platform Deployment Architecture")
    doc.add_paragraph("")

    # Figure 3
    add_figure_guide(
        doc,
        3,
        "Platform Repository Structure",
        "GitHub Repository",
        [
            "Open GitHub repository in browser",
            "Navigate to root directory",
            "Expand folders: .github/workflows, iac/platform-hub, environments/dv/"
        ],
        "Repository tree showing folder structure, workflow files, and platform deployment directories",
        "Highlight: platform-deploy.yml, platform-destroy.yml, iac/platform-hub, environments/dv folder",
        "Left navigation tree only (exclude file contents, exclude right-side details)",
        1400,
        900,
        "None (public repository)",
        "Figure 3 - Platform Repository Structure"
    )

    # Figure 4
    add_figure_guide(
        doc,
        4,
        "Platform Configuration Files",
        "VS Code",
        [
            "Open VS Code with repository",
            "Open file: environments/dv/platform.tfvars",
            "Show: environment_name, resource_group_name, shared_subnet_name, storage_account, key_name"
        ],
        "Code editor showing platform.tfvars configuration with key variables visible",
        "Highlight: variable names and their example values (e.g., environment_name = 'dv')",
        "Code editor only (exclude sidebar, exclude terminal)",
        1400,
        700,
        "Blur actual resource names if they contain sensitive identifiers",
        "Figure 4 - Platform Configuration Files"
    )

    # Figure 5
    add_figure_guide(
        doc,
        5,
        "Platform Deployment Pull Request",
        "GitHub Pull Request",
        [
            "Open GitHub repository",
            "Go to Pull Requests tab",
            "Find a platform deployment PR (e.g., 'Update platform deployment config')",
            "Open PR detail page"
        ],
        "PR title, description, changed files list, reviewers section, approval status",
        "Highlight: Reviewer names, approval status (green checkmark), ServiceNow reference if visible",
        "PR header and approval area only (exclude code diff details)",
        1400,
        800,
        "Blur reviewer email addresses if visible; blur any internal ticket numbers",
        "Figure 5 - Platform Deployment Pull Request"
    )

    # Figure 7
    add_figure_guide(
        doc,
        7,
        "Platform Workflow Trigger Inputs",
        "GitHub Actions",
        [
            "Open GitHub repository",
            "Go to Actions tab",
            "Click workflow: 'Trigger Foundry Setup'",
            "Click 'Run workflow' button",
            "Screenshot the 'Run workflow' popup/modal"
        ],
        "Input fields: Environment (dv/pp/pr), Segment, Location",
        "Highlight: Input field values and labels",
        "Run Workflow popup/modal only (exclude surrounding page)",
        1200,
        700,
        "None",
        "Figure 7 - Platform Workflow Trigger Inputs"
    )

    # Figure 8
    add_figure_guide(
        doc,
        8,
        "Terraform Plan Execution",
        "GitHub Actions Run Log",
        [
            "From Actions tab, select a recent platform deployment run",
            "Click 'plan' job (or 'platform-hub-plan' job)",
            "Scroll to see: terraform init, terraform plan, plan completion"
        ],
        "Plan job logs showing: terraform init step, terraform plan step, successful plan completion message",
        "Highlight: Plan summary line (e.g., 'Plan: X to add, Y to change, Z to destroy')",
        "Plan execution logs only (exclude other jobs, exclude workflow tabs)",
        1600,
        900,
        "Blur any actual resource names or values that appear in logs",
        "Figure 8 - Terraform Plan Execution"
    )

    # Figure 9
    add_figure_guide(
        doc,
        9,
        "Deployment Approval Gate",
        "GitHub Environment Approval",
        [
            "From Actions tab, select a run that is waiting for approval",
            "Look for 'Waiting for approval' status",
            "Screenshot shows the approval card/panel"
        ],
        "Approval waiting status, Approve button, Deploy context info",
        "Highlight: Approve action button",
        "Approval card/panel only (exclude job list, exclude other UI elements)",
        1200,
        700,
        "Blur environment name if sensitive",
        "Figure 9 - Deployment Approval Gate"
    )

    # Figure 10
    add_figure_guide(
        doc,
        10,
        "Terraform Apply Execution",
        "GitHub Actions Run Log",
        [
            "From Actions tab, select an apply run",
            "Click 'apply' job (or 'foundry-hub-deployment' or 'platform-hub-apply' job)",
            "Scroll to see: terraform init, terraform apply, successful apply completion"
        ],
        "Apply job logs showing: terraform init, terraform apply, apply completion message with resource summary",
        "Highlight: Apply summary line (e.g., 'Apply complete! Resources: X added, Y changed, Z destroyed')",
        "Apply execution logs only (exclude other jobs, exclude workflow tabs)",
        1600,
        900,
        "Blur any actual resource names in output",
        "Figure 10 - Terraform Apply Execution"
    )

    # Figure 11
    add_figure_guide(
        doc,
        11,
        "Platform Resource Validation",
        "Azure Portal",
        [
            "Log into Azure Portal",
            "Search for 'Resource Groups'",
            "Find platform resource group (e.g., 'glbl-dv-adifoundryhub-adi-euwe-rgp')",
            "Click resource group",
            "View Resources list"
        ],
        "Resource group showing provisioned resources: Azure AI Foundry Hub, Key Vault, Application Insights, Log Analytics Workspace, Private Endpoints, Storage accounts",
        "Highlight: Newly created resources with checkmarks or 'Succeeded' status",
        "Resource list view only (exclude breadcrumb, exclude resource details panel on right)",
        1600,
        900,
        "Blur Subscription ID if visible; blur any sensitive resource names; blur Tenant ID if visible",
        "Figure 11 - Platform Resource Validation"
    )

    # Additional recommendations
    doc.add_heading("Additional Screenshot Recommendations", 1)
    doc.add_paragraph("Consider adding optional supplementary screenshots:", style="List Bullet")
    doc.add_paragraph("GitHub Merge Confirmation: Screenshot of 'Merge' button clicked and PR status showing 'Merged'", style="List Bullet 2")
    doc.add_paragraph("Terraform Error Handling (optional): Example of plan/apply failure and error messages (useful for troubleshooting section)", style="List Bullet 2")
    doc.add_paragraph("Azure Private Endpoint Details (optional): Detailed view of private endpoint configuration", style="List Bullet 2")
    doc.add_paragraph("")

    # Best practices
    doc.add_heading("Screenshot Capture Best Practices", 1)
    doc.add_paragraph("Use landscape (16:9) orientation for all screenshots", style="List Bullet")
    doc.add_paragraph("Zoom browser to 100% or 110% for readability", style="List Bullet")
    doc.add_paragraph("Hide browser bookmarks/favorites bar before capturing", style="List Bullet")
    doc.add_paragraph("Close/minimize unnecessary tabs and notifications", style="List Bullet")
    doc.add_paragraph("Use a clean environment (no personal notifications, no unrelated windows)", style="List Bullet")
    doc.add_paragraph("For sensitive data, use blur tools or redact before including in documentation", style="List Bullet")
    doc.add_paragraph("Crop to show only relevant content (no extra whitespace)", style="List Bullet")
    doc.add_paragraph("Use rectangular crop tool, not full-screen captures", style="List Bullet")

    out = r"c:\Users\XSPriyaGa\Downloads\Platform_Deployment_Guide_SCREENSHOT_COLLECTION_GUIDE.docx"
    doc.save(out)
    print(f"Created: {out}")


if __name__ == "__main__":
    main()
