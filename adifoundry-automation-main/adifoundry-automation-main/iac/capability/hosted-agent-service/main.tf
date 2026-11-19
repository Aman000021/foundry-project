module "hosted_agent_deployment" {
    source = "../../modules/hosted-agent-service"
    # tags_json_file = "tags.json"
    # config_path = "../../../environments/${var.environment_name}/${var.foundry_location}/${var.project_segment}/project_configs/config.yaml"
    environment_name = var.environment_name
    resource_group_name = var.resource_group_name
    solution_name = var.solution_name
    project_segment = var.project_segment
    foundry_location = var.foundry_location
    project_name = var.project_name
    agent_builder_group_id = var.agent_builder_group_id
    agent_consumer_group_id = var.agent_consumer_group_id
    agent_mgr_group_id = var.agent_mgr_group_id
    foundry_index = var.foundry_index
    acr_name = var.acr_name
    ais_name = var.ais_name
    platform_rg = var.platform_rg
    umi_object_id = var.umi_object_id
    tags = var.tags
    global_acrPush_group = var.global_acrPush_group
    global_acrPull_group = var.global_acrPull_group
    global_appInsights_publisher_group = var.global_appInsights_publisher_group
}
