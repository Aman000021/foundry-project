# # Access to foundry project
resource "azurerm_role_assignment" "foundry_project_agent_builder" {
  scope                = azapi_resource.ai_foundry_project.id
  role_definition_name = "Nestle Foundry Project Agent Builder"
  principal_id         = var.agent_builder_group_id
  depends_on = [azapi_resource.ai_foundry_project]
}

# resource "time_sleep" "wait_for_role_assignment" {
#   depends_on      = [azurerm_role_assignment.foundry_project_manager,azurerm_role_assignment.foundry_project_user]
#   create_duration = "120s"
# }