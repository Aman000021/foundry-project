locals {
    # config_file_path = "${path.module}/../project_configs/${var.project_segment}/config.yaml"
    # config = try(yamldecode(file(var.config_path)), {})
    # prj_name = local.config.project_name
    # prj_segment = local.config.project_segment
    # location = local.config.location
    location_acronyms = {
      westeurope    = "euwe"
    }
    project_location = {
        europe = "westeurope"
    }

    segment_acronyms = {
      marketing   = "mkt"
      finance = "fin"
      operations = "ops"
      dev01 = "dev01"
      dev02 = "dev02"
    }
    # tags = try(jsondecode(file(var.tags_json_file)), {})

    # name_format = replace(var.project_name, "/[^a-zA-Z0-9]/", "")
    # prj_name = substr(local.name_format, 0, 18)

    location = local.project_location[var.foundry_location]

    app_name = replace(var.project_name, " ", "")

    # project_names = {
    #     for prj in local.config : prj.project_name => {
    #         segment = local.segment_acronyms[prj.project_segment]
    #         builder_group_id = prj.agent_builder_group_id
    #         tags = prj.tags
    #         # segment = prj.project_segment
    #         # location = prj.location
    #     }
    # }

    # project_name = "glbl-${var.environment_name}-${local.prj_name}-prj-cgs"

    # foundry_resource_name = "glbl-${var.environment_name}-${var.solution_name}${local.segment_acronyms[var.project_segment]}-${local.location_acronyms[local.location]}-cgs"
}