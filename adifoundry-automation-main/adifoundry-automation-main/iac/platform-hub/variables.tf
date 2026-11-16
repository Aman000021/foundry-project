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
variable "storage_account" {
  type = string
}
variable "acr_name" {
  type = string
}
variable "acr_pep" {
  type = string
}