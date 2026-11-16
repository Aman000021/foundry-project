# Example testing group - Replace with actual group ID and name as needed

param(
    [Parameter(Mandatory = $true)]
    [string]$GroupId,
    [Parameter(Mandatory = $true)]
    [string]$EnterpriseAppObjectId,
    [Parameter(Mandatory = $false)]
    [string]$AppRoleId = "27d9891d-2c17-4f45-a262-781a0e55c80a"
)

Import-Module Microsoft.Graph.Applications
## This script assumes there is already a valid Azure session established.
$AccessToken = (Get-AzAccessToken -ResourceUrl "https://graph.microsoft.com" -AsSecureString -WarningAction SilentlyContinue).Token
# Connect to Microsoft Graph using the correct access token
Connect-MGGraph -AccessToken $AccessToken -NoWelcome

Write-Host "ADDING GROUP: $GroupId TO EA"

$params = @{
    principalId = $GroupId
    resourceId  = $EnterpriseAppObjectId
    appRoleId   = $AppRoleId
}

try {
    New-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $EnterpriseAppObjectId -BodyParameter $params -ErrorAction Stop
    Write-Host "Group added to EA"
    Write-Output $true
}
catch {
    $errorMessage = $_.Exception.Message
    Write-Host $errorMessage
    if ($errorMessage -like "*Permission being assigned already exists on the object*") {
        Write-Host "Assignment already exists. Ignoring."
        Write-Output $true
    }
    else {
        Write-Host "Could not add group to EA"
        throw
    }
}
