###Add foundry account owner group to foundry resource
resource "azurerm_role_assignment" "foundry_account_owner" {
  for_each = local.resource_names
  scope                = azapi_resource.ai_foundry[each.key].id
  role_definition_name = "Foundry Account Owner"
  principal_id         = var.foundry_account_owner
  depends_on = [azapi_resource.ai_foundry]
}

###Add Foundry Account Reader group to foundry resource
resource "azurerm_role_assignment" "foundry_account_reader" {
  for_each = local.resource_names
  scope                = azapi_resource.ai_foundry[each.key].id
  role_definition_name = "Nestle Foundry Account Reader"
  principal_id         = var.foundry_account_reader
  depends_on = [azapi_resource.ai_foundry]
}

resource "azurerm_role_assignment" "acr_pull_permission" {
  for_each = local.resource_names
  scope                = data.azurerm_container_registry.platform_acr.id
  role_definition_name = "AcrPull"
  principal_id         = azapi_resource.ai_foundry[each.key].output.identity.principalId
  depends_on = [azapi_resource.ai_foundry]
}