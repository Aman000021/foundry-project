param(
    [Parameter(Mandatory = $true)]
    [string]$GroupName
)

Import-Module Microsoft.Entra -RequiredVersion 1.0.6
Import-Module Az.Accounts -RequiredVersion 4.1.0

$ErrorActionPreference = 'Stop'

$token = (Get-AzAccessToken -ResourceUrl 'https://graph.microsoft.com' -AsSecureString).Token
Connect-Entra -AccessToken $token -NoWelcome

try {
    $group = Get-EntraGroup -Filter "DisplayName eq '$GroupName'"
    
    if ($group) {
        Write-Host "Found group: $($group.DisplayName)"
        Write-Host "Group ID: $($group.Id)"
        Write-Output $group.Id
    }
    else {
        Write-Error "Group not found: $GroupName"
        exit 1
    }
}
catch {
    Write-Error "Error retrieving group: $($_.Exception.Message)"
    exit 1
}