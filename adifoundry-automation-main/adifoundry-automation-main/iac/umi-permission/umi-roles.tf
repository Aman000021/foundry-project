# Access to foundry project
resource "azurerm_role_assignment" "foundry_project_agent_builder_umi" {
  scope                = data.azapi_resource.ai_foundry_project.id
  role_definition_name = "Nestle Foundry Project Agent Builder"
  principal_id         = var.umi_object_id
  # depends_on = [azapi_resource.ai_foundry_project]
}

resource "azurerm_role_assignment" "acr_push_permission_umi" {
  scope                = data.azurerm_container_registry.platform_acr.id
  role_definition_name = "AcrPush"
  principal_id         = var.umi_object_id
  # depends_on = [azapi_resource.ai_foundry_project]
}