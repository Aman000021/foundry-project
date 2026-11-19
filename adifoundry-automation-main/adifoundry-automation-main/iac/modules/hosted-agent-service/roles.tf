# # Access to foundry project
resource "azurerm_role_assignment" "foundry_project_agent_builder" {
  scope                = azapi_resource.ai_foundry_project.id
  role_definition_name = "Nestle Foundry Project Agent Builder"
  principal_id         = var.agent_builder_group_id
  depends_on = [azapi_resource.ai_foundry_project]
}

# Access to foundry project
resource "azurerm_role_assignment" "foundry_project_agent_builder_umi" {
  scope                = azapi_resource.ai_foundry_project.id
  role_definition_name = "Nestle Foundry Project Agent Builder"
  principal_id         = var.umi_object_id
  depends_on = [azapi_resource.ai_foundry_project]
}

# resource "azurerm_role_assignment" "acr_pull_permission" {
#   scope                = data.azurerm_container_registry.platform_acr.id
#   role_definition_name = "AcrPull"
#   principal_id         = azapi_resource.ai_foundry_project.output.identity.principalId
#   depends_on = [azapi_resource.ai_foundry_project]
# }

# resource "azurerm_role_assignment" "acr_push_permission_umi" {
#   scope                = data.azurerm_container_registry.platform_acr.id
#   role_definition_name = "AcrPush"
#   principal_id         = var.umi_object_id
#   depends_on = [azapi_resource.ai_foundry_project]
# }

resource "azurerm_role_assignment" "foundry_user_permission" {
  scope                = azapi_resource.ai_foundry_project.id
  role_definition_name = "Foundry User"
  principal_id         = var.agent_mgr_group_id
  depends_on = [azapi_resource.ai_foundry_project]
}

# resource "azurerm_role_assignment" "metrics_publisher_permission" {
#   scope                = data.azurerm_application_insights.platform_ais.id
#   role_definition_name = "Monitoring Metrics Publisher"
#   principal_id         = var.agent_mgr_group_id
#   depends_on = [azapi_resource.ai_foundry_project]
# }

resource "azurerm_role_assignment" "agent_consumer_permission" {
  scope                = azapi_resource.ai_foundry_project.id
  role_definition_name = "Foundry Agent Consumer"
  principal_id         = var.agent_consumer_group_id
  depends_on = [azapi_resource.ai_foundry_project]
}

# resource "time_sleep" "wait_for_role_assignment" {
#   depends_on      = [azurerm_role_assignment.foundry_project_manager,azurerm_role_assignment.foundry_project_user]
#   create_duration = "120s"
# }

# Add Foundry Project MI to ACR Pull group
# resource "azuread_group_member" "project_acr_pull_permission" {
#   group_object_id  = var.global_acrPull_group
#   member_object_id = azapi_resource.ai_foundry_project.output.identity.principalId
#   depends_on = [azapi_resource.ai_foundry_project]
# }

# Add Foundry UMI to ACR Push group
# resource "azuread_group_member" "umi_acr_push_permission" {
#   group_object_id  = var.global_acrPush_group
#   member_object_id = var.umi_object_id
#   depends_on = [azapi_resource.ai_foundry_project]
# }

# Add Usecase Manager group to global metircs publicher group
# resource "azuread_group_member" "agent_mgr_metric_permission" {
#   group_object_id  = var.global_appInsights_publisher_group
#   member_object_id = var.agent_mgr_group_id
#   depends_on = [azapi_resource.ai_foundry_project]
# }

# Add Foundry UMI to Metrics publisher group
# resource "azuread_group_member" "umi_metric_permission" {
#   group_object_id  = var.global_appInsights_publisher_group
#   member_object_id = var.umi_object_id
#   depends_on = [azapi_resource.ai_foundry_project]
# }