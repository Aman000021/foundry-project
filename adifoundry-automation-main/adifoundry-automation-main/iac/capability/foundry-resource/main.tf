module "foundry-hub-deployment" {
    source = "../../modules/foundry-resource"
    config_path = "../../../environments/${var.environment_name}/${var.foundry_location}/${var.project_segment}/foundry_resource_configs/config.yaml"
    environment_name = var.environment_name
    resource_group_name = var.resource_group_name
    solution_name = var.solution_name
#    storage_container_name = var.storage_container_name
#    storage_account = var.storage_account 
    project_segment = var.project_segment
    # project_name = var.project_name
    foundry_location = var.foundry_location
    vnet_name = var.vnet_name
    shared_subnet_name = var.shared_subnet_name
    vnet_resource_group_name = var.vnet_resource_group_name
    # hosted_agent_subnet_name = var.hosted_agent_subnet_name
    foundry_account_reader = var.foundry_account_reader
    foundry_account_owner = var.foundry_account_owner
    acr_name = var.acr_name
    platform_rg = var.platform_rg
}
