provider "azurerm" {
  use_oidc                        = true
  resource_provider_registrations = "none"
  features {
    # Vaults at Nestle are soft-deleted and purge protected (for 90 days). These global configuration settings will
    # make it possible to (soft) delete a Vault and later restore it when destroying and then re-applying the same Vault.
    key_vault {
      purge_soft_delete_on_destroy = false
      recover_soft_deleted_key_vaults = true
    }

  }
}

provider "azapi" {
  # Advanced configuration for OIDC can go here if needed
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.5"
    }
    random = {
      version = "~> 3.6"
    }
    http = {
      version = "~> 3.4"
    }
    azapi = {
      source  = "azure/azapi"
      version = "~> 2.11.0"
    }
  }
}