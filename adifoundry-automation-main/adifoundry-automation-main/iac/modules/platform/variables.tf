variable "resource_group_name" {
    type = string
    description = "Name of the Resource Group"  
}
variable "environment_name" {
    type = string
    description = "Environment to be deployed"  
}
variable "shared_subnet_name" {
  type = string
  description = "Shared subnet details for PEP"
}
variable "key_name" {
  type = string
  description = "Key vault name"
}
variable "key_pep" {
  type = string
  description = "Name of the KV PEP"
}
variable "log_analytics_name" {
  type = string
  description = "Name of the Log analytics"
}
variable "app_insights_name" {
  type = string
}
variable "acr_name" {
  type = string
  description = "Name of container registry"
}
variable "acr_pep" {
  type = string
  description = "Name of container registry private endpoint"
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
variable "sustain_aad_group" {
  type = string
}