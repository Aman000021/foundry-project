# Operations segment setup

This is a scaffold for the `operations` segment in `dv/europe` only. Do not select it
for PP or Prod until matching segment configuration exists for those environments.
Before deploying:

- Confirm the operations resource group name in the segment tfvars files.
- Add operations-approved `foundry_account_reader` and `foundry_account_owner` group IDs to `agent-service.tfvars` and `foundry-resource.tfvars`.
- Add the `ops_foundry_index` variable to the `dv` GitHub Environment.
- Add Foundry resource indexes and their approved managed subnet names to `foundry_resource_configs/config.yaml` when resources are ready to deploy.
- Add project definitions to `project_configs/config.yaml` as projects are approved.
