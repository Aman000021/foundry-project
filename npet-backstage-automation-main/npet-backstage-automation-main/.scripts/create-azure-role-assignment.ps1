param (
    [Parameter(Mandatory)][string]$umiPrincipalId,
    [Parameter(Mandatory)][string]$virtualNetworkName,
    [Parameter(Mandatory)][string]$virtualNetworkRg,
    [Parameter(Mandatory)][string]$delegatedSubnetName
)

$ErrorActionPreference = 'Stop'

$vnet = Get-AzVirtualNetwork -Name $virtualNetworkName -ResourceGroupName $virtualNetworkRg
$subnet = Get-AzVirtualNetworkSubnetConfig -Name $delegatedSubnetName -VirtualNetwork $vnet

Write-Host 'Determining if Role Assignment already exists.'
$found = Get-AzRoleAssignment -ObjectId $umiPrincipalId -RoleDefinitionName 'Nestle RBAC App Contributor' -Scope $subnet.Id

if (!$found) {
    Write-Host 'Role Assignment not found, creating Role Assignment.'
    New-AzRoleAssignment -ObjectId $umiPrincipalId -RoleDefinitionName 'Nestle RBAC App Contributor' -Scope $subnet.Id
}
else {
    Write-Host 'Role Assignment found. Exiting.'
}
