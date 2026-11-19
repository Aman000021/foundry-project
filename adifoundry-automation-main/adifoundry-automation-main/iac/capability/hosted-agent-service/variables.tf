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
variable "agent_consumer_group_id" {
  type = string
}
variable "agent_mgr_group_id" {
  type = string
}
variable "foundry_index" {
  type = string
}
variable "acr_name" {
  type = string
}
variable "ais_name" {
  type = string
}
variable "platform_rg" {
  type = string
}
variable "umi_object_id" {
  type = string
}
variable "tags" {
  type = string
}
variable "global_acrPush_group" {
  type = string
}
variable "global_acrPull_group" {
  type = string
}
variable "global_appInsights_publisher_group" {
  type = string
}
