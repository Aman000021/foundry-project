data azurerm_resource_group rg_name {
    name = var.resource_group_name
}

#data azurerm_storage_account existing {
#  name                = var.storage_account
#  resource_group_name = var.resource_group_name
#}

data "azapi_resource" "ai_foundry" {
  type = "Microsoft.CognitiveServices/accounts@2025-06-01"
  name = "glbl-${var.environment_name}-${var.solution_name}${var.foundry_index}-${local.location_acronyms[local.location]}-cgs"
  parent_id = data.azurerm_resource_group.rg_name.id
}

##Get ACR details
data "azurerm_container_registry" "platform_acr" {
  name = var.acr_name
  resource_group_name = var.platform_rg
}

# data "azuread_group" "project_manager" {
#   display_name     = var.prj_manager_group
#   security_enabled = true
# }

# data "azuread_group" "project_user" {
#   display_name     = var.prj_user_group
#   security_enabled = true
# }