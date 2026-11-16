output "project_endpoints" {
  value = try(
    azapi_resource.ai_foundry_project.output.properties.endpoints["AI Foundry API"],
    null
  )
}