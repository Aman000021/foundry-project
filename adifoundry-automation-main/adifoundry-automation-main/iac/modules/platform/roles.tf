# Assign ACR Push permissin to Group
resource "azurerm_role_assignment" "platform_acr_push_permission" {
  scope                = module.terraform-azure-acr.container_id
  role_definition_name = "AcrPush"
  principal_id         = var.global_acrPush_group
  depends_on = [module.terraform-azure-acr]
}

# Assign ACR Pull permission to Group
resource "azurerm_role_assignment" "platform_acr_pull_permission" {
  scope                = module.terraform-azure-acr.container_id
  role_definition_name = "AcrPull"
  principal_id         = var.global_acrPull_group
  depends_on = [module.terraform-azure-acr]
}

# Assign Metrics Publisher role to App Insights group
resource "azurerm_role_assignment" "metrics_publisher_permission" {
  scope                = azurerm_application_insights.app_insights.id
  role_definition_name = "Monitoring Metrics Publisher"
  principal_id         = var.global_appInsights_publisher_group
  depends_on = [azurerm_application_insights.app_insights]
}

# Assign Log Analytics role to Sustain Team group
resource "azurerm_role_assignment" "ais_log_analytics_reader_permission" {
  scope                = azurerm_application_insights.app_insights.id
  role_definition_name = "Log Analytics Reader"
  principal_id         = var.sustain_aad_group
  depends_on = [azurerm_application_insights.app_insights]
}

# Assign Log Analytics role to Sustain Team group
resource "azurerm_role_assignment" "law_log_analytics_reader_permission" {
  scope                = azurerm_log_analytics_workspace.logs_workspace.id
  role_definition_name = "Log Analytics Reader"
  principal_id         = var.sustain_aad_group
  depends_on = [azurerm_log_analytics_workspace.logs_workspace]
}

# # Add sustain team group in gloabl AcrPush group
# resource "azuread_group_member" "sustain_acr_push_permission" {
#   group_object_id  = var.global_acrPush_group
#   member_object_id = var.sustain_aad_group
# }

