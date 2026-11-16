from datetime import date
from pathlib import Path
from typing import Iterable

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches, Pt


def safe_import_matplotlib():
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
        return plt, FancyArrowPatch, FancyBboxPatch
    except Exception:
        return None, None, None


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DIAGRAMS = DOCS / "diagrams"
CODE_SHOTS = DIAGRAMS / "code_shots"
SHOTS = DOCS / "screenshots" / "actions" / "cropped"
IMAGES = ROOT / "images"

PLATFORM_DOCX = DOCS / "Platform_Resources_Deployment_Guide_FULL.docx"
FOUNDRY_DOCX = DOCS / "Foundry_Project_Deployment_Guide_FULL.docx"

PLATFORM_FLOW_PNG = DIAGRAMS / "platform_deployment_flow.png"
PLATFORM_ARCH_PNG = DIAGRAMS / "platform_deployment_architecture.png"
FOUNDRY_FLOW_PNG = DIAGRAMS / "foundry_project_deployment_flow.png"
FOUNDRY_ARCH_PNG = DIAGRAMS / "foundry_project_deployment_architecture.png"

PLATFORM_DRAWIO = DIAGRAMS / "platform_resources_deployment_architecture.drawio"
FOUNDRY_DRAWIO = DIAGRAMS / "foundry_project_deployment_architecture.drawio"

PLATFORM_DEPLOY_YAML = ROOT / ".github" / "workflows" / "platform-deploy.yml"
AGENT_DEPLOY_YAML = ROOT / ".github" / "workflows" / "agent-capability-deploy.yml"
TRIGGER_YAML = ROOT / ".github" / "workflows" / "iac.yaml"
PLATFORM_MAIN_TF = ROOT / "iac" / "modules" / "platform" / "main.tf"
FOUNDRY_HUB_MAIN_TF = ROOT / "iac" / "modules" / "foundry-hub" / "main.tf"
AGENT_SERVICE_MAIN_TF = ROOT / "iac" / "modules" / "agent-service" / "main.tf"
AGENT_SERVICE_ROLES_TF = ROOT / "iac" / "modules" / "agent-service" / "roles.tf"
HUB_CONFIG_YAML = ROOT / "iac" / "foundry_hub_configs" / "marketing" / "config.yaml"
PROJECT_CONFIG_YAML = ROOT / "iac" / "project_configs" / "marketing" / "config.yaml"


def ensure_dirs() -> None:
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    CODE_SHOTS.mkdir(parents=True, exist_ok=True)


def _read_lines(path: Path, start: int, end: int) -> str:
    if not path.exists():
        return f"# Missing file: {path}"

    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    start_idx = max(1, start) - 1
    end_idx = min(len(lines), end)
    selected = lines[start_idx:end_idx]
    numbered = [f"{idx + start_idx + 1:>4} | {line}" for idx, line in enumerate(selected)]
    return "\n".join(numbered)


def render_code_snapshot(output_path: Path, title: str, content: str) -> None:
    plt, _, _ = safe_import_matplotlib()
    if plt is None:
        return

    lines = content.splitlines()
    max_lines = 38
    lines = lines[:max_lines]

    fig_h = max(3.8, min(9.2, 1.5 + len(lines) * 0.18))
    fig, ax = plt.subplots(figsize=(14, fig_h))
    ax.axis("off")
    ax.set_facecolor("#0f172a")
    fig.patch.set_facecolor("#0f172a")

    ax.text(0.01, 0.98, title, color="#93c5fd", fontsize=12, fontweight="bold", va="top", ha="left", transform=ax.transAxes)
    ax.text(0.01, 0.93, "Deployment-relevant code snapshot", color="#cbd5e1", fontsize=9, va="top", ha="left", transform=ax.transAxes)

    code_text = "\n".join(lines) if lines else "# No content"
    ax.text(
        0.01,
        0.89,
        code_text,
        color="#e2e8f0",
        fontsize=8.7,
        family="monospace",
        va="top",
        ha="left",
        transform=ax.transAxes,
    )

    plt.tight_layout(pad=0.6)
    fig.savefig(output_path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)


def generate_code_screenshots() -> None:
    shots: Iterable[tuple[Path, str, Path, int, int]] = [
        (CODE_SHOTS / "01_trigger_workflow_yaml.png", "Trigger Workflow (.github/workflows/iac.yaml)", TRIGGER_YAML, 1, 120),
        (CODE_SHOTS / "02_platform_pipeline_yaml.png", "Platform Pipeline (.github/workflows/platform-deploy.yml)", PLATFORM_DEPLOY_YAML, 1, 180),
        (CODE_SHOTS / "03_agent_pipeline_yaml.png", "Agent Pipeline (.github/workflows/agent-capability-deploy.yml)", AGENT_DEPLOY_YAML, 1, 170),
        (CODE_SHOTS / "04_platform_module_main_tf.png", "Platform Module (iac/modules/platform/main.tf)", PLATFORM_MAIN_TF, 1, 120),
        (CODE_SHOTS / "05_foundry_hub_module_main_tf.png", "Foundry Hub Module (iac/modules/foundry-hub/main.tf)", FOUNDRY_HUB_MAIN_TF, 1, 180),
        (CODE_SHOTS / "06_hub_config_yaml.png", "Hub Config (iac/foundry_hub_configs/marketing/config.yaml)", HUB_CONFIG_YAML, 1, 120),
        (CODE_SHOTS / "07_agent_module_main_tf.png", "Agent Service Module (iac/modules/agent-service/main.tf)", AGENT_SERVICE_MAIN_TF, 1, 140),
        (CODE_SHOTS / "08_agent_roles_tf.png", "Agent Service Roles (iac/modules/agent-service/roles.tf)", AGENT_SERVICE_ROLES_TF, 1, 140),
        (CODE_SHOTS / "09_project_config_yaml.png", "Project Config (iac/project_configs/marketing/config.yaml)", PROJECT_CONFIG_YAML, 1, 180),
    ]

    for output_path, title, source_path, start, end in shots:
        content = _read_lines(source_path, start, end)
        render_code_snapshot(output_path, title, content)


def draw_boxes_with_arrows(output_path: Path, title: str, nodes: list[dict], edges: list[tuple[int, int]]) -> None:
    plt, FancyArrowPatch, FancyBboxPatch = safe_import_matplotlib()
    if plt is None:
        return

    fig, ax = plt.subplots(figsize=(14, 4.8))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 5)
    ax.axis("off")

    ax.text(0.2, 4.75, title, fontsize=14, fontweight="bold")

    for idx, node in enumerate(nodes):
        x, y, w, h = node["x"], node["y"], node["w"], node["h"]
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.4,
            edgecolor="#1f4e79",
            facecolor=node.get("fill", "#e8f1fb"),
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, node["label"], ha="center", va="center", fontsize=10)

    for src, dst in edges:
        s = nodes[src]
        d = nodes[dst]
        start = (s["x"] + s["w"], s["y"] + s["h"] / 2)
        end = (d["x"], d["y"] + d["h"] / 2)
        arrow = FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=16, linewidth=1.6, color="#1f4e79")
        ax.add_patch(arrow)

    plt.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def draw_architecture(output_path: Path, title: str, groups: list[dict], links: list[tuple[tuple[float, float], tuple[float, float]]]) -> None:
    plt, FancyArrowPatch, FancyBboxPatch = safe_import_matplotlib()
    if plt is None:
        return

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")

    ax.text(0.2, 9.5, title, fontsize=14, fontweight="bold")

    for group in groups:
        gx, gy, gw, gh = group["x"], group["y"], group["w"], group["h"]
        frame = FancyBboxPatch(
            (gx, gy), gw, gh,
            boxstyle="round,pad=0.03,rounding_size=0.08",
            linewidth=1.6,
            edgecolor="#2f5597",
            facecolor=group.get("fill", "#f5f8ff"),
        )
        ax.add_patch(frame)
        ax.text(gx + 0.2, gy + gh - 0.35, group["title"], fontsize=10, fontweight="bold", ha="left")

        for node in group.get("nodes", []):
            nx, ny, nw, nh = node
            item = FancyBboxPatch(
                (nx, ny), nw, nh,
                boxstyle="round,pad=0.02,rounding_size=0.05",
                linewidth=1.0,
                edgecolor="#4f81bd",
                facecolor="#ffffff",
            )
            ax.add_patch(item)

    for group in groups:
        for label in group.get("labels", []):
            ax.text(label[0], label[1], label[2], fontsize=9, ha="center", va="center")

    for start, end in links:
        arrow = FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=14, linewidth=1.4, color="#1f4e79")
        ax.add_patch(arrow)

    plt.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def drawio_xml(title: str, nodes: list[dict], edges: list[tuple[int, int]]) -> str:
    cells = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>'
    ]

    for i, n in enumerate(nodes, start=2):
        cells.append(
            f'<mxCell id="{i}" value="{n["label"]}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e8f1fb;strokeColor=#1f4e79;" '
            f'vertex="1" parent="1"><mxGeometry x="{n["x"] * 60}" y="{(5 - n["y"] - n["h"]) * 60}" width="{n["w"] * 60}" height="{n["h"] * 60}" as="geometry"/></mxCell>'
        )

    edge_id = 100
    for src, dst in edges:
        s_id = src + 2
        d_id = dst + 2
        cells.append(
            f'<mxCell id="{edge_id}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;" '
            f'edge="1" parent="1" source="{s_id}" target="{d_id}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        edge_id += 1

    cell_block = "".join(cells)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<mxfile host="app.diagrams.net" modified="2026-06-23T00:00:00.000Z" agent="Copilot" version="24.7.17">'
        f'<diagram id="diagram-1" name="{title}">'
        f'<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="900" math="0" shadow="0"><root>{cell_block}</root></mxGraphModel>'
        '</diagram></mxfile>'
    )


def write_drawio(path: Path, title: str, nodes: list[dict], edges: list[tuple[int, int]]) -> None:
    path.write_text(drawio_xml(title, nodes, edges), encoding="utf-8")


def add_title(doc: Document, title: str, subtitle: str) -> None:
    p = doc.add_paragraph()
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(22)
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    p2 = doc.add_paragraph()
    r2 = p2.add_run(subtitle)
    r2.font.size = Pt(13)
    p2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    p3 = doc.add_paragraph()
    p3.add_run(f"Prepared on: {date.today().isoformat()}\\nRepository: npet-foundry-template")
    p3.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


def h1(doc: Document, text: str) -> None:
    doc.add_heading(text, level=1)


def h2(doc: Document, text: str) -> None:
    doc.add_heading(text, level=2)


def h3(doc: Document, text: str) -> None:
    doc.add_heading(text, level=3)


def bullet(doc: Document, text: str) -> None:
    doc.add_paragraph(text, style="List Bullet")


def num(doc: Document, text: str) -> None:
    doc.add_paragraph(text, style="List Number")


def code_block(doc: Document, text: str) -> None:
    for line in text.splitlines():
        p = doc.add_paragraph()
        run = p.add_run(line)
        run.font.name = "Consolas"
        run.font.size = Pt(9)


def add_image(doc: Document, path: Path, caption: str, width: float = 6.2) -> None:
    if path.exists():
        doc.add_picture(str(path), width=Inches(width))
        cp = doc.add_paragraph(caption)
        cp.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


def add_table(doc: Document, headers: list[str], rows: list[list[str]]) -> None:
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = value


def toc(doc: Document, section_name: str) -> None:
    h1(doc, "1. Table of Contents")
    toc_lines = [
        "1. Table of Contents",
        "2. Overview of Deployment",
        "2.1 Purpose",
        "2.2 Visual Deployment Flow",
        "3. Deployment Architecture",
        "4. Repository Structure and Deployment Files",
        "5. Configuration Updates",
        "6. Pull Request Process",
        "7. Deployment Process",
        "8. Validation Steps",
        "9. Responsibilities Matrix",
        "10. Troubleshooting Guide",
        "11. Summary",
    ]
    for line in toc_lines:
        bullet(doc, line)


def common_screenshots(doc: Document) -> None:
    add_image(doc, SHOTS / "01_actions_overview_annotated_cropped.png", "GitHub Actions overview")
    add_image(doc, SHOTS / "02_run_workflow_inputs_annotated_cropped.png", "Run workflow input screen")
    add_image(doc, SHOTS / "03_run_summary_graph_annotated_cropped.png", "Pipeline run graph")
    add_image(doc, SHOTS / "04_actions_overview_current_cropped.jpg", "Current Actions page")
    add_image(doc, SHOTS / "05_trigger_workflow_page_cropped.jpg", "Workflow trigger page")
    add_image(doc, SHOTS / "06_run_summary_page_cropped.jpg", "Run summary page")
    add_image(doc, SHOTS / "07_plan_job_page_cropped.jpg", "Terraform plan job details")
    add_image(doc, SHOTS / "08_apply_job_page_cropped.jpg", "Terraform apply job details")


def platform_doc() -> None:
    doc = Document()
    add_title(doc, "Platform Resources Deployment Guide", "Self-Contained Deployment Guide for New Teams")
    toc(doc, "platform")

    h1(doc, "2. Overview of Deployment")
    h2(doc, "2.1 Purpose")
    bullet(doc, "What is deployed: Platform observability resources and Foundry hub resources.")
    bullet(doc, "Why required: Shared foundation is required before any project onboarding.")
    bullet(doc, "Key components: GitHub Actions, Terraform, platform-hub stack, foundry-hub stack, Azure resource groups.")
    bullet(doc, "Expected outcome: Shared monitoring/security foundation plus Foundry hub resources and private endpoints.")

    h2(doc, "2.2 Visual Deployment Flow")
    add_image(doc, PLATFORM_FLOW_PNG, "Platform deployment flow diagram", width=6.4)
    bullet(doc, "This guide intentionally includes only deployment-path components from the full solution architecture.")
    add_image(doc, SHOTS / "03_run_summary_graph_annotated_cropped.png", "Deployment sequence in run graph")

    h1(doc, "3. Deployment Architecture")
    add_image(doc, PLATFORM_ARCH_PNG, "Platform deployment architecture diagram", width=6.4)
    bullet(doc, f"Editable draw.io source: {PLATFORM_DRAWIO.relative_to(ROOT)}")
    bullet(doc, "Resource Groups involved: glbl-ts-adifoundryhub-adi-euwe-rgp and glbl-ts-adiagtsvmkt-adi-euwe-rgp.")
    bullet(doc, "Resources created: Log Analytics Workspace, Log Analytics Solution, Application Insights, Key Vault module resources, Foundry hub resources, private endpoints, storage container.")
    bullet(doc, "Terraform flow: platform-hub plan/apply -> foundry-hub plan/apply.")
    bullet(doc, "Dependencies: foundry-hub deployment follows platform-hub plan; apply stages are branch-gated.")

    h1(doc, "4. Repository Structure and Deployment Files")
    code_block(doc, """
.github/workflows/
  iac.yaml
  platform-deploy.yml
environments/dv/
  backend-config-platform.tfvars
  platform.tfvars
environments/dv/marketing/
  backend-config-hub.tfvars
  foundry-hub.tfvars
iac/platform-hub/
  backend.tf, provider.tf, variables.tf, main.tf, outputs.tf
iac/capability/foundry-hub/
  backend.tf, provider.tf, variables.tf, main.tf, outputs.tf
iac/modules/platform/
  data.tf, main.tf, variables.tf
iac/modules/foundry-hub/
  data.tf, locals.tf, main.tf, variables.tf
iac/foundry_hub_configs/marketing/config.yaml
""".strip())

    add_table(
        doc,
        ["File", "Purpose", "When Modified", "Owner Responsibility"],
        [
            [".github/workflows/iac.yaml", "Entry trigger workflow", "When adding env/segment options", "Platform Team"],
            [".github/workflows/platform-deploy.yml", "Platform and hub plan/apply pipeline", "When pipeline logic changes", "Platform Team"],
            ["environments/*/platform.tfvars", "Platform runtime parameters", "When target infra names change", "Platform Team"],
            ["environments/*/*/foundry-hub.tfvars", "Foundry hub runtime parameters", "When hub deployment parameters change", "Platform Team"],
            ["iac/foundry_hub_configs/*/config.yaml", "Hub index to subnet mapping", "When new hub/subnet mappings are required", "Platform Team"],
            ["iac/modules/foundry-hub/*.tf", "Hub resource definitions", "When architecture evolves", "Platform Team"],
        ],
    )
    h2(doc, "4.1 Deployment File Screenshots (IAC and Pipeline)")
    add_image(doc, CODE_SHOTS / "01_trigger_workflow_yaml.png", "Screenshot: trigger workflow YAML")
    add_image(doc, CODE_SHOTS / "02_platform_pipeline_yaml.png", "Screenshot: platform deployment pipeline YAML")
    add_image(doc, CODE_SHOTS / "04_platform_module_main_tf.png", "Screenshot: platform module Terraform")
    add_image(doc, CODE_SHOTS / "05_foundry_hub_module_main_tf.png", "Screenshot: foundry-hub module Terraform")

    h1(doc, "5. Configuration Updates")
    h2(doc, "5.1 Files to Update Before Deployment")
    bullet(doc, "Mandatory: environments/<env>/platform.tfvars")
    bullet(doc, "Mandatory: environments/<env>/<segment>/foundry-hub.tfvars")
    bullet(doc, "Mandatory: iac/foundry_hub_configs/<segment>/config.yaml")
    bullet(doc, "Optional: workflow options in .github/workflows/iac.yaml")

    h2(doc, "5.2 Mandatory and Optional Parameters")
    add_table(
        doc,
        ["Parameter", "File", "Type", "Mandatory", "Description"],
        [
            ["environment_name", "platform.tfvars/foundry-hub.tfvars", "string", "Yes", "Target environment (dv/pp/pr)"],
            ["resource_group_name", "platform.tfvars/foundry-hub.tfvars", "string", "Yes", "Target Azure resource group"],
            ["solution_name", "foundry-hub.tfvars", "string", "Yes", "Solution prefix used in naming"],
            ["vnet_name", "foundry-hub.tfvars", "string", "Yes", "VNet used for private endpoint subnet lookup"],
            ["resource_index", "config.yaml", "string", "Yes", "Hub instance key (for_each key)"],
            ["resource_subnet", "config.yaml", "string", "Yes", "Subnet name for private endpoint"],
        ],
    )

    h2(doc, "5.3 Sample Configuration")
    code_block(
        doc,
        """
# iac/foundry_hub_configs/marketing/config.yaml
- resource_index: "mkt001"
  resource_subnet: "emna-np-g.2-adi-euwe-001-snt"

- resource_index: "mkt002"
  resource_subnet: "emna-np-g.3-adi-euwe-001-snt"
""".strip(),
    )
    bullet(doc, "Validation checks: resource_index must be unique; subnet must exist in target VNet resource group.")
    add_image(doc, CODE_SHOTS / "06_hub_config_yaml.png", "Screenshot: hub configuration YAML")
    common_screenshots(doc)

    h1(doc, "6. Pull Request Process")
    h2(doc, "6.1 PR Creation")
    num(doc, "Create branch from main (example: feature/platform-hub-update).")
    num(doc, "Commit config and Terraform changes with clear commit messages.")
    num(doc, "Raise PR to main and fill change summary, impact, and rollback notes.")

    h2(doc, "6.2 Review Process")
    bullet(doc, "Reviewers verify tfvars/config consistency and naming conventions.")
    bullet(doc, "CODEOWNERS approval is required where branch protection is enabled.")
    bullet(doc, "Validation checks: no secrets in code, correct environment/segment targeting, no unintended delete actions in plan.")

    h2(doc, "6.3 Merge Process")
    bullet(doc, "Merge only after required approvals and resolved comments.")
    bullet(doc, "Preferred merge criterion: clean plan output and no blocking checks.")

    add_image(doc, IMAGES / "settings-button.png", "Repository settings navigation (branch protection/governance)")
    add_image(doc, IMAGES / "repo_visibility.png", "Repository visibility and governance context")

    h1(doc, "7. Deployment Process")
    h2(doc, "7.1 Terraform Plan")
    num(doc, "Trigger workflow: Trigger Foundry Setup.")
    num(doc, "Choose Deploy Dev Platform or Deploy Prod Platform.")
    num(doc, "Pipeline runs platform-hub-plan then foundry-hub-plan.")
    bullet(doc, "Expected output: tfplan artifact for each stack and no blocking errors.")

    h2(doc, "7.2 Terraform Apply")
    num(doc, "Ensure branch is updated-foundry-deployment for apply path.")
    num(doc, "Provide manual approval in <env>-approval environment when prompted.")
    num(doc, "Apply jobs consume tfplan artifacts and execute terraform apply tfplan.")

    h2(doc, "7.3 Full Deployment Sequence")
    for step in [
        "Configuration updates",
        "PR creation",
        "PR review",
        "Merge",
        "Terraform plan",
        "Terraform apply",
        "Resource validation",
    ]:
        num(doc, step)

    h1(doc, "8. Validation Steps")
    h2(doc, "8.1 Resource Validation")
    bullet(doc, "Validate in Azure Portal under target resource groups.")
    bullet(doc, "Expected: Log Analytics Workspace, Application Insights, Key Vault resources, Foundry hub resources, private endpoints.")

    h2(doc, "8.2 Role Assignment Validation")
    bullet(doc, "Platform guide scope: validate pipeline identity has required permissions and resource deployment succeeded.")
    bullet(doc, "Portal path: Resource Group -> Access control (IAM) -> Role assignments.")

    h2(doc, "8.3 Deployment Success Validation")
    bullet(doc, "GitHub validation: all plan/apply jobs green.")
    bullet(doc, "Azure validation: resources in Succeeded state; private endpoint approved/connected.")

    add_image(doc, IMAGES / "github-environments.png", "GitHub environments used for approval and secrets")
    add_image(doc, IMAGES / "github-environments2.png", "Environment-level deployment controls")
    add_image(doc, IMAGES / "github-environments3.png", "Environment permission and secret configuration")

    h1(doc, "9. Responsibilities Matrix")
    add_table(
        doc,
        ["Activity", "Platform Team", "Use Case Team", "RACI"],
        [
            ["Maintain platform Terraform modules", "Yes", "No", "Platform Team: A/R; Use Case Team: I"],
            ["Update platform/hub tfvars and config", "Yes", "Input only", "Platform Team: A/R; Use Case Team: C"],
            ["Trigger platform deployment", "Yes", "No", "Platform Team: R; Use Case Team: I"],
            ["Validate shared infra", "Yes", "No", "Platform Team: A/R"],
            ["Support post-deployment incidents", "Yes", "Report", "Platform Team: A/R; Use Case Team: C"],
        ],
    )

    h1(doc, "10. Troubleshooting Guide")
    add_table(
        doc,
        ["Issue", "Symptoms", "Root Cause", "Resolution"],
        [
            ["Permission issue", "Azure login or apply fails", "Missing role on subscription/resource group", "Grant required RBAC to federated identity and rerun"],
            ["Terraform init backend failure", "State backend not found", "Wrong backend-config values", "Validate storage account/container/resource group names"],
            ["Subnet lookup failure", "Plan fails at azurerm_subnet data source", "Invalid resource_subnet in config.yaml", "Correct subnet name and VNet RG values"],
            ["Branch-gated apply not triggered", "Only plan jobs run", "branch != updated-foundry-deployment", "Use expected branch or update workflow condition"],
            ["Private endpoint provisioning issue", "PEP in failed or pending state", "Network policy or subnet constraints", "Validate subnet policy/delegation and retry"],
        ],
    )

    h1(doc, "11. Summary")
    bullet(doc, "Platform deployment is the prerequisite shared foundation and should run before onboarding projects.")
    bullet(doc, "Deployment boundaries are clearly separated between platform-hub and foundry-hub stacks.")
    bullet(doc, "Key success checks: green plan/apply jobs, healthy Azure resources, validated network/private endpoints.")
    bullet(doc, "Use this document as the authoritative runbook for platform and hub deployment changes.")

    doc.save(str(PLATFORM_DOCX))


def foundry_doc() -> None:
    doc = Document()
    add_title(doc, "Foundry Project Deployment Guide", "Self-Contained Deployment Guide for New Teams")
    toc(doc, "foundry")

    h1(doc, "2. Overview of Deployment")
    h2(doc, "2.1 Purpose")
    bullet(doc, "What is deployed: Foundry projects under existing Foundry hub resources.")
    bullet(doc, "Why required: enables use-case teams to use isolated Foundry project workspaces with correct access.")
    bullet(doc, "Key components: GitHub Actions, Terraform agent-service stack, project config YAML, role assignments.")
    bullet(doc, "Expected outcome: Foundry projects created/updated and project roles assigned to AD principals.")

    h2(doc, "2.2 Visual Deployment Flow")
    add_image(doc, FOUNDRY_FLOW_PNG, "Foundry project deployment flow diagram", width=6.4)
    bullet(doc, "This guide intentionally includes only deployment-path components from the full solution architecture.")
    add_image(doc, SHOTS / "03_run_summary_graph_annotated_cropped.png", "Deployment sequence in run graph")

    h1(doc, "3. Deployment Architecture")
    add_image(doc, FOUNDRY_ARCH_PNG, "Foundry project deployment architecture diagram", width=6.4)
    bullet(doc, f"Editable draw.io source: {FOUNDRY_DRAWIO.relative_to(ROOT)}")
    bullet(doc, "Resource Group involved: glbl-ts-adiagtsvmkt-adi-euwe-rgp.")
    bullet(doc, "Resources created: Foundry project resources and project-level role assignments.")
    bullet(doc, "Dependencies: Foundry hub resources must already exist and be discoverable by index.")

    h1(doc, "4. Repository Structure and Deployment Files")
    code_block(doc, """
.github/workflows/
  iac.yaml
  agent-capability-deploy.yml
environments/dv/marketing/
  backend-config-project.tfvars
  agent-service.tfvars
iac/capability/agent-service/
  backend.tf, provider.tf, variables.tf, main.tf, outputs.tf
iac/modules/agent-service/
  data.tf, locals.tf, main.tf, roles.tf, variables.tf
iac/project_configs/marketing/config.yaml
""".strip())

    add_table(
        doc,
        ["File", "Purpose", "When Modified", "Owner Responsibility"],
        [
            [".github/workflows/agent-capability-deploy.yml", "Plan/apply workflow for Foundry projects", "When pipeline logic changes", "Platform Team"],
            ["environments/*/*/agent-service.tfvars", "Runtime variables for project stack", "When resource naming/target changes", "Use Case Team with Platform Review"],
            ["environments/*/*/backend-config-project.tfvars", "Remote state backend config", "When state storage setup changes", "Platform Team"],
            ["iac/project_configs/*/config.yaml", "Project list and role principal mapping", "For each onboarding/update", "Use Case Team"],
            ["iac/modules/agent-service/main.tf", "Project resource definition", "When architecture evolves", "Platform Team"],
            ["iac/modules/agent-service/roles.tf", "Project role assignment resources", "When access model changes", "Platform Team"],
        ],
    )
    h2(doc, "4.1 Deployment File Screenshots (IAC and Pipeline)")
    add_image(doc, CODE_SHOTS / "01_trigger_workflow_yaml.png", "Screenshot: trigger workflow YAML")
    add_image(doc, CODE_SHOTS / "03_agent_pipeline_yaml.png", "Screenshot: agent deployment pipeline YAML")
    add_image(doc, CODE_SHOTS / "07_agent_module_main_tf.png", "Screenshot: agent-service module Terraform")
    add_image(doc, CODE_SHOTS / "08_agent_roles_tf.png", "Screenshot: role assignment Terraform")

    h1(doc, "5. Configuration Updates")
    h2(doc, "5.1 Files to Update Before Deployment")
    bullet(doc, "Mandatory: environments/<env>/<segment>/agent-service.tfvars")
    bullet(doc, "Mandatory: iac/project_configs/<segment>/config.yaml")
    bullet(doc, "Mandatory: workflow dispatch inputs (segment, location)")
    bullet(doc, "Optional: additional project records in config.yaml")

    h2(doc, "5.2 Mandatory and Optional Parameters")
    add_table(
        doc,
        ["Parameter", "File", "Type", "Mandatory", "Description"],
        [
            ["project_name", "config.yaml", "string", "Yes", "Foundry project name suffix"],
            ["project_segment", "config.yaml", "string", "Yes", "Segment key (e.g., marketing)"],
            ["foundry_index", "config.yaml", "string", "Yes", "Hub lookup key used to map project parent account"],
            ["project_manager_group_id", "config.yaml", "string", "Yes", "AAD principal for Foundry Project Manager role"],
            ["project_manager_user_id", "config.yaml", "string", "Yes", "AAD principal for Foundry User role"],
            ["foundry_location", "workflow input", "string", "Yes", "Location mapping key (e.g., europe)"],
        ],
    )

    h2(doc, "5.3 Sample Configuration")
    code_block(
        doc,
        """
# iac/project_configs/marketing/config.yaml
- project_name: redeploy01
  project_segment: marketing
  foundry_index: "mkt001"
  project_manager_group_id: 0bce9cc6-5820-447d-a8c5-6e7cccf7523a
  project_manager_user_id: 6022217d-ac60-4915-a8b9-e663dfa87487
""".strip(),
    )
    bullet(doc, "Validation checks: foundry_index must map to existing hub; principal IDs must be valid AAD object IDs.")
    add_image(doc, CODE_SHOTS / "09_project_config_yaml.png", "Screenshot: project configuration YAML")
    common_screenshots(doc)

    h1(doc, "6. Pull Request Process")
    h2(doc, "6.1 PR Creation")
    num(doc, "Create branch from main (example: feature/foundry-project-onboarding).")
    num(doc, "Commit config.yaml and tfvars updates.")
    num(doc, "Raise PR with change impact and validation checklist.")

    h2(doc, "6.2 Review Process")
    bullet(doc, "Validate project naming, foundry_index mapping, and role principal IDs.")
    bullet(doc, "Confirm no unrelated Terraform changes in PR.")
    bullet(doc, "Ensure required approvers/CODEOWNERS sign off.")

    h2(doc, "6.3 Merge Process")
    bullet(doc, "Merge only after successful review and approved checks.")
    bullet(doc, "Use branch policy-compliant merge strategy.")

    add_image(doc, IMAGES / "settings-button.png", "Repository settings navigation")
    add_image(doc, IMAGES / "repo_visibility.png", "Repository governance context")

    h1(doc, "7. Deployment Process")
    h2(doc, "7.1 Terraform Plan")
    num(doc, "Run Trigger Foundry Setup -> Deploy Dev Agent Service or Deploy Prod Agent Service.")
    num(doc, "Workflow executes plan job in iac/capability/agent-service.")
    num(doc, "Plan uses backend-config-project.tfvars and agent-service.tfvars.")
    bullet(doc, "Expected output: tfplan artifact and no critical errors.")

    h2(doc, "7.2 Terraform Apply")
    num(doc, "If branch condition matches, approval stage appears.")
    num(doc, "Approve deployment in <env>-approval environment.")
    num(doc, "Apply job downloads tfplan and runs terraform apply tfplan.")

    h2(doc, "7.3 Full Deployment Sequence")
    for step in [
        "Configuration updates",
        "PR creation",
        "PR review",
        "Merge",
        "Terraform plan",
        "Terraform apply",
        "Resource validation",
    ]:
        num(doc, step)

    h1(doc, "8. Validation Steps")
    h2(doc, "8.1 Resource Validation")
    bullet(doc, "Azure Portal -> target resource group -> verify Foundry projects exist and show healthy state.")
    bullet(doc, "Validate project naming pattern: glbl-<env>-<project_name>-prj-cgs.")

    h2(doc, "8.2 Role Assignment Validation")
    bullet(doc, "Portal path: Foundry project -> Access Control (IAM) -> Role assignments.")
    bullet(doc, "Expected roles: Foundry Project Manager and Foundry User assigned to configured principal IDs.")

    h2(doc, "8.3 Deployment Success Validation")
    bullet(doc, "Pipeline validation: plan/apply jobs green.")
    bullet(doc, "Azure validation: project resource and IAM bindings present.")
    bullet(doc, "Foundry validation: project visible and accessible for assigned users.")

    add_image(doc, IMAGES / "github-environments.png", "GitHub environments for deployment approvals")
    add_image(doc, IMAGES / "github-environments2.png", "Environment security and approvals")
    add_image(doc, IMAGES / "github-environments3.png", "Environment-level secret and permission controls")

    h1(doc, "9. Responsibilities Matrix")
    add_table(
        doc,
        ["Activity", "Platform Team", "Use Case Team", "RACI"],
        [
            ["Maintain core Terraform modules", "Yes", "No", "Platform Team: A/R; Use Case Team: I"],
            ["Update project config.yaml", "Review", "Yes", "Use Case Team: R; Platform Team: A/C"],
            ["Raise PR and respond to review", "Review", "Yes", "Use Case Team: R; Platform Team: C"],
            ["Trigger project deployment", "Support", "Yes", "Use Case Team: R; Platform Team: C"],
            ["Validate project access", "Support", "Yes", "Use Case Team: R; Platform Team: C"],
        ],
    )

    h1(doc, "10. Troubleshooting Guide")
    add_table(
        doc,
        ["Issue", "Symptoms", "Root Cause", "Resolution"],
        [
            ["Hub mapping failure", "Project creation fails at parent lookup", "Invalid foundry_index", "Correct foundry_index and verify hub exists"],
            ["Role assignment failure", "Apply fails on azurerm_role_assignment", "Invalid or unauthorized principal ID", "Validate AAD object IDs and permissions"],
            ["Plan succeeds but apply not visible", "No apply job", "Branch gate condition not met", "Use expected branch or adjust workflow condition"],
            ["Terraform state lock/backend issue", "Init/apply backend errors", "Incorrect backend tfvars", "Fix storage account/container/RG values"],
            ["Permission denied in workflow", "azure/login or apply fails", "Federated identity lacks RBAC", "Assign required role on subscription/resource group"],
        ],
    )

    h1(doc, "11. Summary")
    bullet(doc, "Foundry project deployment uses existing hub resources and creates project plus role assignments only.")
    bullet(doc, "Critical config quality checks are foundry_index mapping and principal IDs for IAM roles.")
    bullet(doc, "Key success checks: green plan/apply jobs, project visible in Azure/Foundry, roles correctly assigned.")
    bullet(doc, "Use this document as the end-to-end runbook for onboarding project deployments.")

    doc.save(str(FOUNDRY_DOCX))


def generate_diagrams() -> None:
    platform_nodes = [
        {"label": "Git Repository", "x": 0.6, "y": 2.1, "w": 2.2, "h": 0.95},
        {"label": "Trigger Foundry Setup\n(iac.yaml)", "x": 3.3, "y": 2.1, "w": 2.5, "h": 0.95},
        {"label": "platform-deploy.yml", "x": 6.3, "y": 2.1, "w": 2.3, "h": 0.95},
        {"label": "Terraform\nplatform-hub + foundry-hub", "x": 9.1, "y": 2.1, "w": 3.2, "h": 0.95},
        {"label": "Azure Shared Resources\n+ Foundry Hubs + PEP", "x": 12.8, "y": 2.1, "w": 2.0, "h": 0.95},
    ]
    platform_edges = [(0, 1), (1, 2), (2, 3), (3, 4)]

    foundry_nodes = [
        {"label": "Git Repository", "x": 0.6, "y": 2.1, "w": 2.2, "h": 0.95},
        {"label": "Trigger Foundry Setup\n(iac.yaml)", "x": 3.3, "y": 2.1, "w": 2.5, "h": 0.95},
        {"label": "agent-capability-deploy.yml", "x": 6.3, "y": 2.1, "w": 2.8, "h": 0.95},
        {"label": "Terraform\nagent-service", "x": 9.6, "y": 2.1, "w": 2.4, "h": 0.95},
        {"label": "Azure Foundry Projects\n+ Role Assignments", "x": 12.5, "y": 2.1, "w": 2.3, "h": 0.95},
    ]
    foundry_edges = [(0, 1), (1, 2), (2, 3), (3, 4)]

    draw_boxes_with_arrows(PLATFORM_FLOW_PNG, "Platform Resource Deployment Flow", platform_nodes, platform_edges)
    draw_boxes_with_arrows(FOUNDRY_FLOW_PNG, "Foundry Project Deployment Flow", foundry_nodes, foundry_edges)

    platform_groups = [
        {
            "title": "GitHub",
            "x": 0.5, "y": 6.0, "w": 5.4, "h": 3.1,
            "nodes": [(1.0, 7.5, 2.0, 0.8), (3.3, 7.5, 2.0, 0.8), (1.0, 6.4, 4.3, 0.8)],
            "labels": [(2.0, 7.9, "Repository"), (4.3, 7.9, "platform-deploy.yml"), (3.0, 6.8, "Trigger Foundry Setup + Approvals")],
        },
        {
            "title": "RG: glbl-ts-adifoundryhub-adi-euwe-rgp",
            "x": 6.4, "y": 5.2, "w": 5.8, "h": 4.0,
            "nodes": [(7.0, 8.0, 2.0, 0.8), (9.3, 8.0, 2.4, 0.8), (7.0, 6.9, 2.0, 0.8), (9.3, 6.9, 2.4, 0.8)],
            "labels": [(8.0, 8.4, "Log Analytics"), (10.5, 8.4, "Application Insights"), (8.0, 7.3, "Key Vault"), (10.5, 7.3, "Platform State Backend")],
        },
        {
            "title": "RG: glbl-ts-adiagtsvmkt-adi-euwe-rgp",
            "x": 6.4, "y": 0.8, "w": 8.4, "h": 3.8,
            "nodes": [(7.0, 3.4, 2.6, 0.8), (10.0, 3.4, 2.6, 0.8), (13.0, 3.4, 1.4, 0.8), (7.0, 2.2, 7.4, 0.8)],
            "labels": [(8.3, 3.8, "Foundry Hub mkt001"), (11.3, 3.8, "Foundry Hub mkt002/mkt003"), (13.7, 3.8, "PEP"), (10.7, 2.6, "VNet/Subnet Mapping from config.yaml")],
        },
    ]
    platform_links = [
        ((5.4, 7.0), (6.4, 7.0)),
        ((5.4, 6.6), (6.4, 3.3)),
    ]

    foundry_groups = [
        {
            "title": "GitHub",
            "x": 0.5, "y": 6.0, "w": 5.4, "h": 3.1,
            "nodes": [(1.0, 7.5, 2.0, 0.8), (3.3, 7.5, 2.0, 0.8), (1.0, 6.4, 4.3, 0.8)],
            "labels": [(2.0, 7.9, "Repository"), (4.3, 7.9, "agent-capability-deploy.yml"), (3.0, 6.8, "Trigger Foundry Setup + Approvals")],
        },
        {
            "title": "RG: glbl-ts-adiagtsvmkt-adi-euwe-rgp",
            "x": 6.4, "y": 1.0, "w": 8.8, "h": 8.2,
            "nodes": [
                (7.0, 8.2, 2.8, 0.8),
                (10.2, 8.2, 2.8, 0.8),
                (7.0, 6.9, 6.0, 0.8),
                (7.0, 5.6, 6.0, 0.8),
                (7.0, 4.3, 6.0, 0.8),
                (7.0, 3.0, 6.0, 0.8),
            ],
            "labels": [
                (8.4, 8.6, "Existing Foundry Hub(s)"),
                (11.6, 8.6, "State Backend (tfstateproject)"),
                (10.0, 7.3, "Foundry Project: glbl-<env>-<project>-prj-cgs"),
                (10.0, 6.0, "Role: Foundry Project Manager"),
                (10.0, 4.7, "Role: Foundry User"),
                (10.0, 3.4, "Principal IDs from config.yaml"),
            ],
        },
    ]
    foundry_links = [
        ((5.4, 6.9), (6.4, 7.2)),
    ]

    draw_architecture(PLATFORM_ARCH_PNG, "Platform Deployment Architecture", platform_groups, platform_links)
    draw_architecture(FOUNDRY_ARCH_PNG, "Foundry Project Deployment Architecture", foundry_groups, foundry_links)

    write_drawio(PLATFORM_DRAWIO, "Platform Deployment Architecture", platform_nodes, platform_edges)
    write_drawio(FOUNDRY_DRAWIO, "Foundry Project Deployment Architecture", foundry_nodes, foundry_edges)


def main() -> None:
    ensure_dirs()
    generate_code_screenshots()
    generate_diagrams()
    platform_doc()
    foundry_doc()
    print("Generated full split guides:")
    print(PLATFORM_DOCX)
    print(FOUNDRY_DOCX)
    print("Generated draw.io sources:")
    print(PLATFORM_DRAWIO)
    print(FOUNDRY_DRAWIO)


if __name__ == "__main__":
    main()
