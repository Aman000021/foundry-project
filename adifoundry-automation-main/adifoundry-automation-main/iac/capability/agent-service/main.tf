module "agent_service_deployment" {
    source = "../../modules/agent-service"
    # tags_json_file = "tags.json"
    # config_path = "../../../environments/${var.environment_name}/${var.foundry_location}/${var.project_segment}/project_configs/config.yaml"
    environment_name = var.environment_name
    resource_group_name = var.resource_group_name
    solution_name = var.solution_name
    project_segment = var.project_segment
    foundry_location = var.foundry_location
    project_name = var.project_name
    agent_builder_group_id = var.agent_builder_group_id
    foundry_index = var.foundry_index
}
