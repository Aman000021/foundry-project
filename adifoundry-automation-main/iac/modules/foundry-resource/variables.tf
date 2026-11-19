variable "environment_name" {
  type = string
}
variable "solution_name" {
  type = string
}
variable "resource_group_name" {
  type = string
}
#variable "storage_container_name" {
#  type = string
#}
#variable "storage_account" {
#  type = string
#}
variable "project_segment" {
  type = string
}
variable "config_path" {
  type = string
}
variable "foundry_location" {
  type = string
}
variable "vnet_name" {
  description = "VNet name"
  type = string
}
variable "shared_subnet_name" {
  description = "Subnet name"
  type = string
}
variable "vnet_resource_group_name" {
  type = string
}
# variable "hosted_agent_subnet_name" {
#   type = string
# }
variable "foundry_account_reader" {
  type = string
}
variable "foundry_account_owner" {
  type = string
}
variable "acr_name" {
  type = string
}
variable "platform_rg" {
  type = string
}
