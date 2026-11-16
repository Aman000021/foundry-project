data azurerm_resource_group rg_name {
    name = var.resource_group_name
}

data "azurerm_client_config" "current" {
}