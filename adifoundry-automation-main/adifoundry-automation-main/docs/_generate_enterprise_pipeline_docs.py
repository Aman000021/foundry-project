from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DIAGRAMS = DOCS / "diagrams"
SNAPSHOTS = DIAGRAMS / "iac_snapshots"
ACTION_SHOTS = DOCS / "screenshots" / "actions" / "cropped"
IMAGES = ROOT / "images"

AGENT_DOC = DOCS / "Agent_Service_Pipelines_Documentation_ENTERPRISE.docx"
PLATFORM_DOC = DOCS / "Platform_Resources_Pipelines_Documentation_ENTERPRISE.docx"

FONT = ImageFont.load_default()


def ensure_dirs() -> None:
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)


def draw_round_rect(draw, xy, fill, outline, width=2, radius=16):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_flow_diagram(path: Path, title: str, boxes: list[str]) -> None:
    w, h = 1800, 620
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)

    draw.text((40, 25), title, fill="#102a43", font=FONT)
    x = 80
    y = 250
    bw = 290
    bh = 110
    gap = 55

    for i, label in enumerate(boxes):
        draw_round_rect(draw, (x, y, x + bw, y + bh), fill="#eaf2ff", outline="#2b6cb0", width=3)
        draw.multiline_text((x + 18, y + 28), label, fill="#102a43", font=FONT, spacing=4)
        if i < len(boxes) - 1:
            ax1 = x + bw
            ay = y + bh // 2
            ax2 = x + bw + gap - 10
            draw.line((ax1, ay, ax2, ay), fill="#2b6cb0", width=4)
            draw.polygon([(ax2, ay), (ax2 - 16, ay - 8), (ax2 - 16, ay + 8)], fill="#2b6cb0")
        x += bw + gap

    img.save(path)


def draw_arch_diagram(path: Path, title: str, sections: list[tuple[str, tuple[int, int, int, int], list[tuple[str, tuple[int, int, int, int]]]]], connectors: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
    w, h = 1900, 1050
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)

    draw.text((40, 20), title, fill="#102a43", font=FONT)

    for sec_name, rect, items in sections:
        rx, ry, rw, rh = rect
        rbox = (rx, ry, rx + rw, ry + rh)
        draw_round_rect(draw, rbox, fill="#f7fbff", outline="#5b8def", width=3)
        draw.text((rx + 12, ry + 10), sec_name, fill="#1f3c88", font=FONT)
        for item_name, irect in items:
            ix, iy, iw, ih = irect
            ibox = (ix, iy, ix + iw, iy + ih)
            draw_round_rect(draw, ibox, fill="#ffffff", outline="#8aa5d6", width=2, radius=12)
            draw.multiline_text((ix + 10, iy + 14), item_name, fill="#102a43", font=FONT, spacing=4)

    for start, end in connectors:
        draw.line((start[0], start[1], end[0], end[1]), fill="#2b6cb0", width=3)
        draw.polygon([(end[0], end[1]), (end[0] - 12, end[1] - 6), (end[0] - 12, end[1] + 6)], fill="#2b6cb0")

    img.save(path)


def code_snapshot(src: Path, out: Path, title: str, start: int, end: int) -> None:
    lines = []
    if src.exists():
        content = src.read_text(encoding="utf-8", errors="ignore").splitlines()
        start_idx = max(1, start) - 1
        end_idx = min(len(content), end)
        for i in range(start_idx, end_idx):
            lines.append(f"{i + 1:>4} | {content[i]}")
    else:
        lines = [f"Missing file: {src}"]

    max_lines = 40
    lines = lines[:max_lines]

    w, h = 1800, max(420, 140 + len(lines) * 22)
    img = Image.new("RGB", (w, h), "#0b1220")
    draw = ImageDraw.Draw(img)
    draw.text((20, 14), title, fill="#8ab4ff", font=FONT)
    draw.text((20, 40), str(src.relative_to(ROOT)), fill="#cbd5e1", font=FONT)

    y = 72
    for line in lines:
        draw.text((20, y), line, fill="#e2e8f0", font=FONT)
        y += 20

    img.save(out)


def p(doc: Document, text: str) -> None:
    para = doc.add_paragraph(text)
    para.paragraph_format.space_after = Pt(8)


def h1(doc: Document, text: str) -> None:
    doc.add_heading(text, level=1)


def h2(doc: Document, text: str) -> None:
    doc.add_heading(text, level=2)


def add_title(doc: Document, title: str, subtitle: str) -> None:
    para = doc.add_paragraph()
    run = para.add_run(title)
    run.bold = True
    run.font.size = Pt(24)
    para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    para2 = doc.add_paragraph()
    run2 = para2.add_run(subtitle)
    run2.font.size = Pt(13)
    para2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    meta = doc.add_paragraph()
    meta.add_run(f"Prepared on: {date.today().isoformat()}\nRepository: npet-foundry-template")
    meta.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


def add_img(doc: Document, path: Path, caption: str, width=6.4):
    if path.exists():
        doc.add_picture(str(path), width=Inches(width))
        c = doc.add_paragraph(caption)
        c.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


def add_table(doc: Document, headers: list[str], rows: list[list[str]]):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        t.rows[0].cells[i].text = h
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = v


def generate_assets() -> dict:
    ensure_dirs()

    platform_flow = DIAGRAMS / "platform_pipeline_flow_enterprise.png"
    agent_flow = DIAGRAMS / "agent_pipeline_flow_enterprise.png"
    platform_arch = DIAGRAMS / "platform_architecture_deployment_only_enterprise.png"
    agent_arch = DIAGRAMS / "agent_architecture_deployment_only_enterprise.png"

    draw_flow_diagram(
        platform_flow,
        "Platform Resources Pipeline Flow (Deployment Path Only)",
        [
            "ServiceNow/\nBackstage Request",
            "Git Repo +\nPR Approval",
            "Trigger Foundry Setup\n(Platform Option)",
            "Terraform Plan/Apply\n(platform-hub, foundry-hub)",
            "Azure Shared Platform +\nFoundry Hub Resources",
        ],
    )

    draw_flow_diagram(
        agent_flow,
        "Agent Service Pipeline Flow (Deployment Path Only)",
        [
            "ServiceNow/\nBackstage Request",
            "Git Repo +\nPR Approval",
            "Trigger Foundry Setup\n(Agent Service Option)",
            "Terraform Plan/Apply\n(agent-service)",
            "Azure Foundry Projects +\nRole Assignments",
        ],
    )

    platform_sections = [
        (
            "CI/CD Control Layer",
            (40, 90, 900, 280),
            [
                ("GitHub Repo", (70, 160, 180, 90)),
                ("iac.yaml", (280, 160, 170, 90)),
                ("platform-deploy.yml", (480, 160, 220, 90)),
                ("Approval Gate", (730, 160, 180, 90)),
            ],
        ),
        (
            "Terraform Execution Layer",
            (40, 410, 900, 290),
            [
                ("iac/platform-hub", (70, 500, 200, 90)),
                ("iac/capability/foundry-hub", (300, 500, 260, 90)),
                ("Hub Config YAML", (590, 500, 170, 90)),
                ("State Backends", (790, 500, 130, 90)),
            ],
        ),
        (
            "Azure Deployment Layer",
            (980, 90, 870, 610),
            [
                ("RG: glbl-ts-adifoundryhub-adi-euwe-rgp\nLog Analytics\nApp Insights\nKey Vault", (1010, 170, 360, 220)),
                ("RG: glbl-ts-adiagtsvmkt-adi-euwe-rgp\nFoundry Hub Accounts\nPrivate Endpoints\nStorage Container", (1400, 170, 420, 220)),
                ("VNet/Subnet Lookup\nfrom tfvars + config.yaml", (1190, 450, 430, 130)),
            ],
        ),
    ]

    platform_connectors = [
        ((910, 205), (980, 205)),
        ((910, 545), (980, 545)),
        ((700, 205), (700, 500)),
    ]

    draw_arch_diagram(platform_arch, "Platform Deployment Architecture (Terraform-focused components only)", platform_sections, platform_connectors)

    agent_sections = [
        (
            "CI/CD Control Layer",
            (40, 90, 900, 280),
            [
                ("GitHub Repo", (70, 160, 180, 90)),
                ("iac.yaml", (280, 160, 170, 90)),
                ("agent-capability-deploy.yml", (480, 160, 280, 90)),
                ("Approval Gate", (790, 160, 130, 90)),
            ],
        ),
        (
            "Terraform Execution Layer",
            (40, 410, 900, 290),
            [
                ("iac/capability/agent-service", (70, 500, 250, 90)),
                ("iac/modules/agent-service", (350, 500, 240, 90)),
                ("project_configs/<segment>/config.yaml", (620, 500, 280, 90)),
            ],
        ),
        (
            "Azure Deployment Layer",
            (980, 90, 870, 610),
            [
                ("Existing Foundry Hub (Parent)", (1030, 180, 340, 110)),
                ("Foundry Projects\n(accounts/projects)", (1410, 180, 380, 110)),
                ("Role Assignments\nFoundry Project Manager\nFoundry User", (1220, 340, 420, 160)),
                ("AAD Principal IDs\nfrom project config", (1040, 530, 320, 120)),
            ],
        ),
    ]

    agent_connectors = [
        ((910, 205), (980, 205)),
        ((910, 545), (980, 545)),
        ((730, 205), (730, 500)),
        ((1370, 235), (1410, 235)),
    ]

    draw_arch_diagram(agent_arch, "Agent Service Deployment Architecture (Terraform-focused components only)", agent_sections, agent_connectors)

    snapshots = {
        "trigger": SNAPSHOTS / "01_trigger_workflow_yaml.png",
        "platform_pipeline": SNAPSHOTS / "02_platform_pipeline_yaml.png",
        "agent_pipeline": SNAPSHOTS / "03_agent_pipeline_yaml.png",
        "platform_module": SNAPSHOTS / "04_platform_module_main_tf.png",
        "hub_module": SNAPSHOTS / "05_foundry_hub_module_main_tf.png",
        "agent_module": SNAPSHOTS / "06_agent_service_main_tf.png",
        "roles": SNAPSHOTS / "07_agent_service_roles_tf.png",
        "hub_config": SNAPSHOTS / "08_hub_config_yaml.png",
        "project_config": SNAPSHOTS / "09_project_config_yaml.png",
    }

    code_snapshot(ROOT / ".github" / "workflows" / "iac.yaml", snapshots["trigger"], "Trigger workflow", 1, 130)
    code_snapshot(ROOT / ".github" / "workflows" / "platform-deploy.yml", snapshots["platform_pipeline"], "Platform pipeline", 1, 190)
    code_snapshot(ROOT / ".github" / "workflows" / "agent-capability-deploy.yml", snapshots["agent_pipeline"], "Agent service pipeline", 1, 180)
    code_snapshot(ROOT / "iac" / "modules" / "platform" / "main.tf", snapshots["platform_module"], "Platform module", 1, 130)
    code_snapshot(ROOT / "iac" / "modules" / "foundry-hub" / "main.tf", snapshots["hub_module"], "Foundry hub module", 1, 220)
    code_snapshot(ROOT / "iac" / "modules" / "agent-service" / "main.tf", snapshots["agent_module"], "Agent service module", 1, 220)
    code_snapshot(ROOT / "iac" / "modules" / "agent-service" / "roles.tf", snapshots["roles"], "Role assignments", 1, 180)
    code_snapshot(ROOT / "iac" / "foundry_hub_configs" / "marketing" / "config.yaml", snapshots["hub_config"], "Foundry hub config", 1, 120)
    code_snapshot(ROOT / "iac" / "project_configs" / "marketing" / "config.yaml", snapshots["project_config"], "Project config", 1, 180)

    return {
        "platform_flow": platform_flow,
        "agent_flow": agent_flow,
        "platform_arch": platform_arch,
        "agent_arch": agent_arch,
        "shots": snapshots,
    }


def platform_doc(assets: dict) -> None:
    doc = Document()
    add_title(doc, "Platform Resources Pipelines Documentation", "Enterprise Deployment Runbook")

    h1(doc, "Executive Summary")
    p(doc, "This document explains how the platform resources pipeline is operated in an enterprise onboarding model for Microsoft Foundry. It focuses only on deployment-relevant architecture, showing how request-driven changes move from repository updates into Terraform execution and finally into Azure infrastructure. The intent is to make operations clear for teams that may not be deeply familiar with Terraform internals.")
    p(doc, "The platform pipeline owns shared infrastructure concerns. It provisions observability and foundational platform assets, then creates or updates Foundry hub resources and private connectivity. These shared services are prerequisites for onboarding individual Foundry projects.")

    h1(doc, "Table of Contents")
    p(doc, "1. Executive Summary\n2. Deployment Story and Flow\n3. Repository Structure and File Responsibilities\n4. Architecture (Terraform-focused)\n5. Configuration and Environment Management\n6. Pull Request and Governance Process\n7. Pipeline Stages (Plan and Apply)\n8. Azure Validation and Resource Mapping\n9. Risks, Constraints, and Troubleshooting\n10. Final Operational Checklist")

    h1(doc, "Deployment Story and Flow")
    p(doc, "The platform pipeline begins with a controlled repository change. A team updates environment or hub mapping configuration, opens a pull request, and completes mandatory reviews. After merge, an operator manually triggers the Foundry setup workflow and selects the platform path. The workflow then calls the platform reusable pipeline, where Terraform plan is generated for both platform-hub and foundry-hub stacks. Once approval gates are cleared, apply runs and infrastructure is reconciled in Azure.")
    add_img(doc, assets["platform_flow"], "Platform flow from request to deployed Azure resources")
    add_img(doc, ACTION_SHOTS / "02_run_workflow_inputs_annotated_cropped.png", "Workflow trigger inputs used for platform deployment")

    h1(doc, "Repository Structure and File Responsibilities")
    p(doc, "The platform deployment logic is distributed across workflow files, environment tfvars, capability entry stacks, and reusable modules. The table below explains the practical ownership model used by most enterprise teams.")
    add_table(doc, ["File/Folder", "Purpose", "When Updated", "Typical Owner"], [
        [".github/workflows/iac.yaml", "Manual entry workflow with deployment choice", "When trigger options change", "Platform Team"],
        [".github/workflows/platform-deploy.yml", "Reusable platform/hub plan-apply pipeline", "When stage logic or approvals change", "Platform Team"],
        ["environments/<env>/platform.tfvars", "Platform resource settings", "When environment values change", "Platform Team"],
        ["environments/<env>/<segment>/foundry-hub.tfvars", "Hub deployment values", "When segment hub values change", "Platform Team"],
        ["iac/platform-hub/main.tf", "Entry stack for shared platform resources", "When stack wiring changes", "Platform Team"],
        ["iac/capability/foundry-hub/main.tf", "Entry stack for Foundry hub resources", "When stack wiring changes", "Platform Team"],
        ["iac/modules/platform/*", "Terraform resources for observability and key services", "When architecture evolves", "Platform Team"],
        ["iac/modules/foundry-hub/*", "Terraform resources for hub and private endpoints", "When architecture evolves", "Platform Team"],
        ["iac/foundry_hub_configs/<segment>/config.yaml", "Segment-to-subnet and index mapping", "When segment topology changes", "Platform Team"],
    ])
    add_img(doc, assets["shots"]["trigger"], "Workflow file snapshot: top-level trigger")
    add_img(doc, assets["shots"]["platform_pipeline"], "Workflow file snapshot: platform reusable pipeline")

    h1(doc, "Architecture (Terraform-focused)")
    p(doc, "The architecture below removes non-deployment components from the larger solution view and keeps only Terraform-relevant control and provisioning paths. The left side represents CI/CD and Terraform execution boundaries, while the right side represents Azure resource groups and deployed assets.")
    add_img(doc, assets["platform_arch"], "Platform deployment architecture (deployment components only)")
    p(doc, "This architecture aligns with enterprise operations where shared platform infrastructure is owned centrally, and onboarding teams consume the resulting hub capability as a managed dependency.")

    h1(doc, "Configuration and Environment Management")
    p(doc, "Configuration is layered. The workflow provides environment, segment, and location context. Environment tfvars provide resource-group and naming values. Segment-specific hub config defines resource indexes and subnet mapping. During plan and apply, these layers merge into a single runtime state.")
    add_table(doc, ["Parameter", "Source", "Mandatory", "Notes"], [
        ["environment", "workflow input", "Yes", "Determines environments/<env> path"],
        ["segment", "workflow input", "Yes", "Determines segment tfvars and YAML path"],
        ["location", "workflow input", "Yes", "Mapped in locals to Azure location code"],
        ["resource_group_name", "platform/foundry tfvars", "Yes", "Target Azure RG"],
        ["solution_name", "foundry-hub.tfvars", "Yes", "Hub naming prefix"],
        ["resource_index/resource_subnet", "config.yaml", "Yes", "for_each key and subnet lookup"],
    ])
    add_img(doc, assets["shots"]["hub_config"], "IAC snapshot: hub configuration YAML")
    add_img(doc, assets["shots"]["platform_module"], "IAC snapshot: platform module resources")
    add_img(doc, assets["shots"]["hub_module"], "IAC snapshot: foundry-hub module resources")

    h1(doc, "Pull Request and Governance Process")
    p(doc, "In a production onboarding process, infrastructure changes should not move directly from local edits to deployment. The controlled path is branch creation, pull request, reviewer validation, and merge approval. Reviewers should verify naming consistency, scope safety, and expected Terraform impact before merge.")
    add_img(doc, IMAGES / "settings-button.png", "Repository settings area used for branch protection and governance")
    add_img(doc, IMAGES / "repo_visibility.png", "Repository governance visibility context")

    h1(doc, "Pipeline Stages (Plan and Apply)")
    p(doc, "The platform pipeline runs in two major stack phases. First, platform-hub plan runs. Then foundry-hub plan runs. Apply phases are branch-gated and approval-gated in this repository configuration. This protects shared infrastructure from accidental execution.")
    add_table(doc, ["Stage", "What Happens", "Output"], [
        ["Trigger", "Manual workflow_dispatch run", "Run context created"],
        ["Init", "Terraform backend initialization", "State backend connected"],
        ["Plan", "Execution plan created per stack", "tfplan artifacts uploaded"],
        ["Approval", "Environment approval (when configured)", "Apply unlocked"],
        ["Apply", "Approved tfplan applied", "Azure resources created/updated"],
    ])
    add_img(doc, ACTION_SHOTS / "07_plan_job_page_cropped.jpg", "Plan job screen")
    add_img(doc, ACTION_SHOTS / "08_apply_job_page_cropped.jpg", "Apply job screen")

    h1(doc, "Azure Validation and Resource Mapping")
    p(doc, "After deployment, validation should be done from both GitHub and Azure perspectives. In Azure, verify each expected resource in the target resource groups. In GitHub, confirm plan and apply outcomes for both stacks.")
    add_table(doc, ["Terraform Area", "Azure Portal Expectation", "Validation Path"], [
        ["platform module", "Log Analytics + App Insights + Key Vault assets", "Resource Group -> Resources"],
        ["foundry-hub module", "Foundry hub accounts and private endpoints", "Resource Group -> Resources"],
        ["backend config", "State blobs present in storage container", "Storage Account -> Containers"],
    ])
    add_img(doc, IMAGES / "github-environments.png", "GitHub environments used for deployment variables/secrets")
    add_img(doc, IMAGES / "github-environments2.png", "Environment policies and approvals")

    h1(doc, "Risks, Constraints, and Troubleshooting")
    p(doc, "The primary risk in shared infrastructure pipelines is unintended change blast radius. High-impact field changes can force replacement behavior. Branch gating and approval checks reduce this risk but do not remove the need for careful plan review.")
    add_table(doc, ["Issue", "Typical Symptom", "Likely Cause", "Resolution"], [
        ["Backend init failure", "Terraform init cannot reach state", "Wrong backend tfvars values", "Verify storage account, RG, container names"],
        ["Subnet data lookup failure", "Plan fails in foundry-hub", "resource_subnet mismatch", "Correct subnet in segment config YAML"],
        ["Apply skipped", "Only plan stages visible", "Branch gate condition unmet", "Run from expected branch or update condition"],
        ["Unexpected replacement risk", "Plan shows destroy/create", "Naming/index field changes", "Review impact and schedule controlled rollout"],
    ])

    h1(doc, "Final Operational Checklist")
    p(doc, "Before closing a platform deployment cycle, capture run evidence, confirm Azure state, and communicate readiness to onboarding teams. The practical handover artifacts are run URL, commit SHA, environment/segment values, and validation outcome.")

    doc.save(str(PLATFORM_DOC))


def agent_doc(assets: dict) -> None:
    doc = Document()
    add_title(doc, "Agent Service Pipelines Documentation", "Enterprise Deployment Runbook")

    h1(doc, "Executive Summary")
    p(doc, "This document explains the onboarding pipeline that creates Foundry projects and configures project-level access. It is intentionally focused on deployment operations and avoids deep Terraform internals so onboarding teams can execute safely with minimal DevOps background.")
    p(doc, "The agent service pipeline assumes shared platform and Foundry hub infrastructure already exists. It maps onboarding configuration to project creation, then applies role assignments for team access.")

    h1(doc, "Table of Contents")
    p(doc, "1. Executive Summary\n2. Deployment Story and Flow\n3. Repository Structure and File Responsibilities\n4. Architecture (Terraform-focused)\n5. Configuration and Environment Management\n6. Pull Request and Governance Process\n7. Pipeline Stages (Plan and Apply)\n8. Azure Validation and Resource Mapping\n9. Risks, Constraints, and Troubleshooting\n10. Final Operational Checklist")

    h1(doc, "Deployment Story and Flow")
    p(doc, "Onboarding starts with a request and approved configuration update. The team updates project config entries, raises a PR, and merges after review. The operator runs Trigger Foundry Setup with the agent service option. Terraform plan runs first, then apply (if approval and branch conditions are satisfied), creating Foundry projects and applying IAM roles.")
    add_img(doc, assets["agent_flow"], "Agent service flow from request to Foundry project readiness")
    add_img(doc, ACTION_SHOTS / "02_run_workflow_inputs_annotated_cropped.png", "Workflow trigger inputs used for agent deployment")

    h1(doc, "Repository Structure and File Responsibilities")
    p(doc, "Agent service onboarding uses a focused set of files. The workflow file controls stage execution, capability stack files define module entry points, and project config YAML provides onboarding records including role principals.")
    add_table(doc, ["File/Folder", "Purpose", "When Updated", "Typical Owner"], [
        [".github/workflows/iac.yaml", "Manual trigger and deployment choice", "When options change", "Platform Team"],
        [".github/workflows/agent-capability-deploy.yml", "Agent reusable pipeline", "When stage logic changes", "Platform Team"],
        ["environments/<env>/<segment>/agent-service.tfvars", "Runtime values", "When env values change", "Use Case Team + Platform Review"],
        ["environments/<env>/<segment>/backend-config-project.tfvars", "State backend settings", "When state topology changes", "Platform Team"],
        ["iac/capability/agent-service/main.tf", "Capability entry stack", "When stack wiring changes", "Platform Team"],
        ["iac/modules/agent-service/main.tf", "Foundry project resource creation", "When architecture evolves", "Platform Team"],
        ["iac/modules/agent-service/roles.tf", "Role assignment creation", "When access model evolves", "Platform Team"],
        ["iac/project_configs/<segment>/config.yaml", "Onboarding project records", "Per onboarding change", "Use Case Team"],
    ])
    add_img(doc, assets["shots"]["trigger"], "Workflow file snapshot: trigger")
    add_img(doc, assets["shots"]["agent_pipeline"], "Workflow file snapshot: agent reusable pipeline")

    h1(doc, "Architecture (Terraform-focused)")
    p(doc, "This architecture isolates deployment-relevant components from the broader platform diagram. It shows CI/CD control flow, Terraform execution boundaries, existing hub dependency, project creation, and role assignment path.")
    add_img(doc, assets["agent_arch"], "Agent service deployment architecture (deployment components only)")

    h1(doc, "Configuration and Environment Management")
    p(doc, "Project onboarding is configuration-driven. Each project entry carries project name, segment, hub index mapping, and principal IDs for role assignment. Pipeline inputs provide environment, segment, and location context. Terraform reads and combines these values at runtime.")
    add_table(doc, ["Parameter", "Source", "Mandatory", "Notes"], [
        ["project_name", "project config YAML", "Yes", "Target Foundry project naming"],
        ["project_segment", "project config YAML", "Yes", "Segment key"],
        ["foundry_index", "project config YAML", "Yes", "Maps project to existing hub"],
        ["project_manager_group_id", "project config YAML", "Yes", "Principal for Foundry Project Manager"],
        ["project_manager_user_id", "project config YAML", "Yes", "Principal for Foundry User"],
        ["environment/segment/location", "workflow input", "Yes", "Routing and variable context"],
    ])
    add_img(doc, assets["shots"]["project_config"], "IAC snapshot: project configuration YAML")
    add_img(doc, assets["shots"]["agent_module"], "IAC snapshot: Foundry project creation module")
    add_img(doc, assets["shots"]["roles"], "IAC snapshot: role assignment module")

    h1(doc, "Pull Request and Governance Process")
    p(doc, "For onboarding safety, teams should treat project config updates as controlled infrastructure changes. The expected process is branch -> PR -> review -> merge. Review should validate hub index mapping and principal IDs before merge.")
    add_img(doc, IMAGES / "settings-button.png", "Repository settings for governance controls")
    add_img(doc, IMAGES / "repo_visibility.png", "Repository governance context")

    h1(doc, "Pipeline Stages (Plan and Apply)")
    p(doc, "The agent pipeline executes init and plan in the plan job, uploads tfplan, and later consumes the same plan artifact in apply. This is a predictable and auditable execution pattern for enterprise deployments.")
    add_table(doc, ["Stage", "What Happens", "Output"], [
        ["Trigger", "Manual run with agent choice", "Run context created"],
        ["Init", "Project state backend initialized", "Backend connected"],
        ["Plan", "Project + role delta computed", "tfplan artifact"],
        ["Approval", "Environment approval if gated", "Apply unlocked"],
        ["Apply", "Planned changes applied", "Projects and roles deployed"],
    ])
    add_img(doc, ACTION_SHOTS / "07_plan_job_page_cropped.jpg", "Plan job details")
    add_img(doc, ACTION_SHOTS / "08_apply_job_page_cropped.jpg", "Apply job details")

    h1(doc, "Azure Validation and Resource Mapping")
    p(doc, "Validation should confirm both resource existence and access correctness. Foundry project resources must be visible in Azure, and IAM role assignments must point to expected principal IDs.")
    add_table(doc, ["Terraform Area", "Azure Portal Expectation", "Validation Path"], [
        ["agent-service main", "Foundry projects created under expected hub", "Resource Group -> Foundry resources"],
        ["agent-service roles", "Project Manager and User assignments", "Project -> Access Control (IAM)"],
        ["project config mapping", "Principal IDs match assigned identities", "IAM list + AAD object lookup"],
    ])
    add_img(doc, IMAGES / "github-environments.png", "GitHub environments for deployment variables/secrets")
    add_img(doc, IMAGES / "github-environments3.png", "Environment permissions and controls")

    h1(doc, "Risks, Constraints, and Troubleshooting")
    p(doc, "The most common onboarding risk is configuration quality. A wrong foundry_index fails parent lookup, and wrong principal IDs fail role assignment or grant access to unintended identities. Plan review is the strongest prevention control.")
    add_table(doc, ["Issue", "Typical Symptom", "Likely Cause", "Resolution"], [
        ["Parent hub lookup failure", "Project creation fails", "Invalid foundry_index", "Correct index and rerun"],
        ["Role assignment failure", "Apply fails in roles.tf", "Invalid principal ID or permissions", "Validate IDs and RBAC"],
        ["Apply not running", "Only plan visible", "Branch gate unmet", "Use expected branch or update condition"],
        ["Unexpected project replacement", "Plan shows destroy/create", "High-impact name/index changes", "Review impact and sequence rollout"],
    ])

    h1(doc, "Final Operational Checklist")
    p(doc, "Before closing onboarding, verify project visibility, role mappings, and user access. Capture operational evidence including run URL, commit SHA, environment, segment, location, and validation outcomes.")

    doc.save(str(AGENT_DOC))


def main() -> None:
    assets = generate_assets()
    platform_doc(assets)
    agent_doc(assets)
    print("Generated:")
    print(PLATFORM_DOC)
    print(AGENT_DOC)


if __name__ == "__main__":
    main()
