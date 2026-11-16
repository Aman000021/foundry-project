[OutputType([String])]
Param
(
    [Parameter(Position = 1)]
    [string]$Issue_Create_Repo,

    [Parameter(Position = 2)]
    [string]$Apm_Id,

    [Parameter(Position = 3)]
    [string]$AAD_Object_Id,

    [Parameter(Position = 4)]
    [string]$Id_Type, # ="Enterprise application (service principal or managed identity)" , #  "App registration (application)"

    [Parameter(Position = 5)]
    [string]$Delegated_Permission_List,

    [Parameter(Position = 6)]
    [string]$Application_Permission_List,

    [Parameter(Position = 7)]
    [string]$Pat,

    [Parameter(ValueFromRemainingArguments = $True)]
    [Object[]]$AdditionalArgs
)

$token = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes("BogusUser:$Pat"))
Write-Host 'Adding API permission by creating a new issue'
Write-Host " $AD_Resource_Type, $AAD_Object_Id, $aad_delegatedpermissions  "
$ISSUE_TITLE = '[UpdatePermissions] NPET Update AAD Permissions'
$uri = "https://api.github.com/repos/nestle-it/$Issue_Create_Repo/issues"

<#
if([string]::IsNullOrEmpty($Delegated_Permission_List) -and [string]::IsNullOrEmpty($Application_Permission_List) )
{
    if ($Id_Type -eq "App registration (application)") {
        $Delegated_Permission_List = 'offline_access,profile,user.read'
        $Application_Permission_List = $null
    }
    elseif($Id_Type -eq "Enterprise application (service principal or managed identity)")
    {
        $Delegated_Permission_List = $null
        $Application_Permission_List = 'Application.Read.All,GroupMember.Read.All,User.Read.All'
    }
}
#>

$delegated_value = @{'Application.Read.All' = ' '
    'email'                                 = ' '
    'GroupMember.Read.All'                  = ' '
    'offline_access'                        = ' '
    'openid'                                = ' '
    'profile'                               = ' '
    'user.read'                             = ' '
    'User.Read.All'                         = ' '
    'User.ReadBasic.All'                    = ' '
}

$application_value = @{'Application.Read.All' = ' '
    'GroupMember.Read.All'                    = ' '
    'User.Read.All'                           = ' '
}

if (![string]::IsNullOrEmpty($Delegated_Permission_List)) {
    $delegated_permission_list_arr = ($Delegated_Permission_List -split ',').Trim()
    foreach ($item in $delegated_permission_list_arr) {
        $delegated_value.$($item) = 'X'
    }
}

if (![string]::IsNullOrEmpty($Application_Permission_List)) {
    $Application_Permission_List_arr = ($Application_Permission_List -split ',').Trim()
    foreach ($item in $Application_Permission_List_arr) {
        $application_value.$($item) = 'X'
    }
}

$ISSUE_BODY = @"
### APM ID

$Apm_Id

### Workload Identity Type

$Id_Type

### Object ID

$AAD_Object_Id

### Delegated Permissions

- [{0}] Application.Read.All
- [{1}] email
- [{2}] GroupMember.Read.All
- [{3}] offline_access
- [{4}] openid
- [{5}] profile
- [{6}] user.read
- [{7}] User.Read.All
- [{8}] User.ReadBasic.All

### Application Permissions

- [{9}] Application.Read.All
- [{10}] GroupMember.Read.All
- [{11}] User.Read.All

"@ -f "$($delegated_value.'Application.Read.All')", "$($delegated_value.'email')", "$($delegated_value.'GroupMember.Read.All')",
"$($delegated_value.'offline_access')", "$($delegated_value.'openid')", "$($delegated_value.'profile')", "$($delegated_value.'user.read')",
"$($delegated_value.'User.Read.All')", "$($delegated_value.'User.ReadBasic.All')", "$($application_value.'Application.Read.All')",
"$($application_value.'GroupMember.Read.All')", "$($application_value.'User.Read.All')"

$body = @{
    title    = "$ISSUE_TITLE"
    body     = "$ISSUE_BODY"
    template = 'Update Graph API Permissions'
} | ConvertTo-Json

$Result = Invoke-WebRequest -Headers @{'Authorization' = "BASIC $token" } -Uri $uri -Method 'POST' -ContentType 'application/json' -Body $body -UseBasicParsing
$req = $Result.Content | ConvertFrom-Json
$fet_issue_number = $req.number
Write-Output "fet_issue_number=$( $fet_issue_number )" >> $env:GITHUB_OUTPUT
$fet_url = $req.html_url

Write-Host "Issue Number: $fet_issue_number"
Write-Host "Issue URL: $fet_url"
