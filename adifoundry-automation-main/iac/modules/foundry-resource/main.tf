# Microsoft Foundry Resource
resource "azapi_resource" "ai_foundry" {
  for_each = local.resource_names
  type                      = "Microsoft.CognitiveServices/accounts@2026-05-01"
  name                      = "glbl-${var.environment_name}-${var.solution_name}${each.key}-${local.location_acronyms[local.location]}-cgs"
  parent_id                 = data.azurerm_resource_group.rg_name.id   
  location                  = local.project_location[var.foundry_location]
  schema_validation_enabled = false
 
  body = {
    kind = "AIServices"
    sku = {
      name = "S0"
    }
    identity = {
      type = "SystemAssigned"
    }
    properties = {
      disableLocalAuth       = false
      allowProjectManagement = true
      customSubDomainName    = "glbl-${var.environment_name}-${var.solution_name}${each.key}-${local.location_acronyms[local.location]}-cgs"
      publicNetworkAccess = "Disabled"
      networkInjections = [
        {
          scenario                   = "agent"
          subnetArmId                = data.azurerm_subnet.hosted_agent_subnet[each.key].id
          useMicrosoftManagedNetwork = false
        }
      ]
    }
  }
  response_export_values = ["identity.principalId"]
}

resource "time_sleep" "wait_for_foundry" {
  depends_on      = [azapi_resource.ai_foundry]
  create_duration = "60s"
}

#resource "azurerm_storage_container" "foundry" {
#  name                  = var.storage_container_name
#  storage_account_id    = data.azurerm_storage_account.existing.id
#  container_access_type = "private"
#}

resource "azurerm_private_endpoint" "ai_foundry_private_endpoint" {
  for_each = local.resource_names
  name                = "glbl-${var.environment_name}-${each.key}.hub-${local.location_acronyms[local.location]}-pep"
  # foundry_resource_pep = "glbl-${var.environment_name}-${var.solution_name}.hub-pep"
  depends_on = [time_sleep.wait_for_foundry]
  location            = data.azurerm_resource_group.rg_name.location
  resource_group_name = var.resource_group_name
  subnet_id           = data.azurerm_subnet.shared_subnet.id
  private_service_connection {
    name                           = replace("glbl-${var.environment_name}-${var.project_segment}${each.key}.hub-${local.location_acronyms[local.location]}-pep", "pep", "pec")
    private_connection_resource_id = azapi_resource.ai_foundry[each.key].id
    subresource_names              = ["account"]
    is_manual_connection           = false
  }
  # subnet_id: when a subnet for PEP is expanded (because there we no more available IPs in the old subnet),
  #            we do not want to re-deploy the PEP - it should stay in the old/original subnet. So ignore_changes
  # private_dns_zone_group: DNS settings are auto-applied by Azure policy. We want to ignore these changes so
  #                         that the TF re-deployment (apply-apply) does not fight the settings set by the Azure policy
  lifecycle {
    ignore_changes = [
      subnet_id,
      private_dns_zone_group
    ]
  }
}

