output "project_endpoints" {
  value = try(
    azapi_resource.ai_foundry_project.output.properties.endpoints["AI Foundry API"],
    null
  )
}

output "ai_foundry_project_principal_id" {
  value = azapi_resource.ai_foundry_project.output.identity.principalId
}