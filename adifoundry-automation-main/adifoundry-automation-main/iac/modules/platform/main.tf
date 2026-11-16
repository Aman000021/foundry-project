#Log Analytics Configuration
resource "azurerm_log_analytics_workspace" "logs_workspace" {
  name                = var.log_analytics_name
  resource_group_name = var.resource_group_name
  location            = data.azurerm_resource_group.rg_name.location
  sku                 = "PerGB2018"
  retention_in_days   = 365
}
resource "azurerm_log_analytics_solution" "logs_solution" {
  solution_name         = "ApplicationInsights"
  location              = data.azurerm_resource_group.rg_name.location
  resource_group_name   = var.resource_group_name
  workspace_resource_id = azurerm_log_analytics_workspace.logs_workspace.id
  workspace_name        = azurerm_log_analytics_workspace.logs_workspace.name
  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/ApplicationInsights"
  }
}
resource "azurerm_application_insights" "app_insights" {
  name                   = replace(var.log_analytics_name, "log", "ais")
  location               = data.azurerm_resource_group.rg_name.location
  resource_group_name    = var.resource_group_name
  workspace_id           = azurerm_log_analytics_workspace.logs_workspace.id
  application_type       = "web"
  internet_query_enabled = "false"

  lifecycle {
    ignore_changes = [ tags ]
  }
}

#Key Vault Configuration with Private Endpoint
module "key_vault" {
  source                = "git::https://github.com/nestle-it/terraform-azure-key.git?ref=v2.2.0"
  tenant_id             = data.azurerm_client_config.current.tenant_id #AD tenant ID which will be used for authenticating to the key vault
  key_vault_name        = var.key_name
  resource_group_name   = var.resource_group_name
  private_endpoint_name = var.key_pep
  shared_subnet_name    = var.shared_subnet_name
}

module "terraform-azure-acr" {
  source                = "git::https://github.com/nestle-it/terraform-azure-acr.git?ref=v2.3.0"
  resource_group_name   = var.resource_group_name
  acr_name              = var.acr_name
  private_endpoint_name = var.acr_pep
  shared_subnet_name    = var.shared_subnet_name
  trust_policy_enabled = false
}