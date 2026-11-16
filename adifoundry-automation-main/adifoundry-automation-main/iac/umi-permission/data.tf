data azurerm_resource_group rg_name {
    name = var.resource_group_name
}


data "azapi_resource" "ai_foundry" {
  type = "Microsoft.CognitiveServices/accounts@2025-06-01"
  name = var.foundry_resource_name
  parent_id = data.azurerm_resource_group.rg_name.id
}

data "azapi_resource" "ai_foundry_project" {
    type = "Microsoft.CognitiveServices/accounts/projects@2025-06-01"
    name = var.foundry_project_name
    parent_id = data.azapi_resource.ai_foundry.id
}

##Get ACR details
data "azurerm_container_registry" "platform_acr" {
  name = var.acr_name
  resource_group_name = var.platform_rg
}