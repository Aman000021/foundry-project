resource "azapi_resource" "ai_foundry_project" {
  type                      = "Microsoft.CognitiveServices/accounts/projects@2025-06-01"
  name                      = "glbl-${var.environment_name}-${var.project_name}-prj-${local.location_acronyms[local.location]}-cgs"
  parent_id                 = data.azapi_resource.ai_foundry.id
  location                  = local.location
  schema_validation_enabled = false
 
  body = {
    sku = {
      name = "S0"
    }
    identity = {
      type = "SystemAssigned"
    }
    properties = {
      description = "AI development project"
    }
  }

  tags = {
    foundry_project = local.app_name
  }

  response_export_values = ["properties.endpoints"]
}

