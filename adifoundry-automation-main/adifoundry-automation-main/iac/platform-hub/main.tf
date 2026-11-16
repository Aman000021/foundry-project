module "platform_deployment" {
    source = "../modules/platform"
    resource_group_name = var.resource_group_name
    log_analytics_name = var.log_analytics_name
    shared_subnet_name = var.shared_subnet_name
    key_name = var.key_name
    key_pep = var.key_pep
    acr_name = var.acr_name
    acr_pep = var.acr_pep
    environment_name = var.environment_name
}