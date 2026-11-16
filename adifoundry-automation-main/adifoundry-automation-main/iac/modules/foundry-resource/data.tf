data azurerm_resource_group rg_name {
    name = var.resource_group_name
}

#data azurerm_storage_account existing {
#  name                = var.storage_account
#  resource_group_name = var.resource_group_name
#}

data "azurerm_subscription" "current" {
}

data "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  resource_group_name = var.vnet_resource_group_name
}

# Read Subnet
data "azurerm_subnet" "shared_subnet" {
  # for_each = { for subnet in local.config : subnet.resource_index => subnet }
  name                 = var.shared_subnet_name
  virtual_network_name = data.azurerm_virtual_network.vnet.name
  resource_group_name  = var.vnet_resource_group_name
}

#Read Hosted Agent Subnet
data "azurerm_subnet" "hosted_agent_subnet" {
  for_each = local.resource_names
  name                 = each.value.network_injection
  virtual_network_name = data.azurerm_virtual_network.vnet.name
  resource_group_name  = var.vnet_resource_group_name
}

data "azurerm_container_registry" "platform_acr" {
  name = var.acr_name
  resource_group_name = var.platform_rg
}