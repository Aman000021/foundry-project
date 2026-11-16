locals {
    # config_file_path = "${path.module}/../project_configs/${var.project_segment}/config.yaml"
    config = try(yamldecode(file(var.config_path)), {})
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
      it = "itp"
    }

    location = local.project_location[var.foundry_location]
    # segment = local.segment_acronyms[var.project_segment]

    resource_names = {
        for resource in local.config : resource.resource_index => {
            network_injection = resource.managed_subnet
            # segment = local.segment_acronyms[resource.resource_segment]
            # subnet = resource.resource_subnet
            # index = resource.resource_index
            # segment = prj.project_segment
            # location = prj.location
        }
    }

    # foundry_resource_name = "glbl-${var.environment_name}-${var.solution_name}${local.segment_acronyms[var.project_segment]}-${local.location_acronyms[local.location]}-cgs"
    # foundry_resource_pep = "glbl-${var.environment_name}-${var.solution_name}.hub-pep"
}