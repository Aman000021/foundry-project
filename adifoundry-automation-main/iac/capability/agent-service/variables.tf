variable "resource_group_name" {
    type = string
    description = "Name of the Resource Group"  
}
variable "environment_name" {
    type = string
    description = "Environment to be deployed"  
}
variable "solution_name" {
  type = string
}
variable "project_segment" {
  type = string
}
variable "shared_subnet_name" {
  type = string
}
variable "foundry_location" {
  type = string
}
variable "project_name" {
  type = string
}
variable "agent_builder_group_id" {
  type = string
}
variable "account_reader_group_id" {
  type = string
}
variable "foundry_index" {
  type = string
}

