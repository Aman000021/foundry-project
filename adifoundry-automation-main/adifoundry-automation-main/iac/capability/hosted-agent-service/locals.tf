# locals {
#     config = yamldecode(file("project_configs/${var.project_segment}/config.yaml"))
#     prj_name = local.config.project_name
#     prj_segment = local.config.project_segment
#     location = local.config.location
# }