terraform {
  backend "azurerm" {
    use_oidc = true
    # This backend requires three authentication parameters; we provide them via environment variables
    # (ARM_TENANT_ID, ARM_SUBSCRIPTION_ID, ARM_CLIENT_ID). Unless we are running interactively, in which
    # case authentication is handled by "az login"
    # The other required parameters (resource_group_name, storage_account_name, container_name) are fed 
    # via the command line, namely    terraform init -backend-config="environments/np/backend-config.tfvars"
    key                    = "backend.tfstate"
  }
}
