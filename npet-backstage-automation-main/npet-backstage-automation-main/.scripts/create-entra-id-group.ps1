param (
    [Parameter(Mandatory = $true)][string[]]$groupNames,
    [Parameter(Mandatory = $true)][string[]]$groupOwners,
    [switch]$dryRun = $false
)

Import-Module Microsoft.Entra -RequiredVersion 1.0.6
Import-Module Az.Accounts -RequiredVersion 4.1.0

$ErrorActionPreference = 'Stop'

function CreateGroup {
    param(
        [string]$name
    )

    $groupParams = @{
        DisplayName     = "$name"
        MailEnabled     = $false
        SecurityEnabled = $true
        MailNickName    = 'NotSet'
    }

    try {
        New-EntraGroup @groupParams
    }
    catch {
        Write-Error "Unable to create group: $($_.Exception.Message)"
    }
}

function AddGroupOwner {
    param(
        [string]$user,
        [string]$group
    )

    try {
        # $filteredGroup = Get-EntraGroup -Filter "DisplayName eq '$group'"
        $owner = Get-EntraUser -UserId $user

        az ad group owner add --group $group --owner-object-id $owner.Id

        # $groupOwner = Get-EntraGroup -GroupId $filteredGroup.Id | Get-EntraGroupOwner | Where-Object { $_.Id -eq $owner.Id }
        # if (!$groupOwner) {
        #     Add-EntraGroupOwner -GroupId $filteredGroup.Id -OwnerId $owner.Id
        # }
    }
    catch {
        Write-Error "Unable to add GroupOwner to group: $($_.Exception.Message)"
    }
}

function AddGroupMember {
    param(
        [string]$user,
        [string]$group
    )

    try {
        $filteredGroup = Get-EntraGroup -Filter "DisplayName eq '$group'"
        $member = Get-EntraUser -UserId $user

        $groupMember = Get-EntraGroup -GroupId $filteredGroup.Id | Get-EntraGroupMember | Where-Object { $_.Id -eq $member.Id }
        if (!$groupMember) {
            Add-EntraGroupMember -GroupId $filteredGroup.Id -MemberId $member.Id
        }
    }
    catch {
        Write-Error "Unable to add GroupMember to group: $($_.Exception.Message)"
    }
}

$token = (Get-AzAccessToken -ResourceUrl 'https://graph.microsoft.com' -AsSecureString).Token
Connect-Entra -AccessToken $token -NoWelcome

foreach ($group in $groupNames) {

    $found = Get-EntraGroup -Filter "DisplayName eq '$group'"
    if (!$found) {
        Write-Host "Creating Group: $group"
        CreateGroup -name $group
    }

    foreach ($owner in $groupOwners) {
        Write-Host "Adding User $owner as GroupOwner to $group"
        AddGroupOwner -user $owner -group $group
        AddGroupMember -user $owner -group $group
    }
}
