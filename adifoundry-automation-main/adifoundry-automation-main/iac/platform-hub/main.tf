module "platform_deployment" {
    source = "../modules/platform"
    resource_group_name = var.platform_rg
    log_analytics_name = var.log_analytics_name
    shared_subnet_name = var.shared_subnet_name
    app_insights_name = var.ais_name
    key_name = var.key_name
    key_pep = var.key_pep
    acr_name = var.acr_name
    acr_pep = var.acr_pep
    environment_name = var.environment_name
    global_acrPush_group = var.global_acrPush_group
    global_acrPull_group = var.global_acrPull_group
    global_appInsights_publisher_group = var.global_appInsights_publisher_group
    sustain_aad_group = var.sustain_aad_group
}