# provider "azurerm" {
#   use_oidc                        = true
#   resource_provider_registrations = "none"
#   features {
#     # Vaults at Nestle are soft-deleted and purge protected (for 90 days). These global configuration settings will
#     # make it possible to (soft) delete a Vault and later restore it when destroying and then re-applying the same Vault.
#     key_vault {
#       purge_soft_delete_on_destroy = false
#       recover_soft_deleted_key_vaults = true
#     }

#   }
# }

terraform {
  required_providers {
    azapi = {
      source  = "azure/azapi"
      version = "~> 2.11.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 3.0"
    }
  }
}