param(
    [Parameter(Mandatory = $True)]
    [string]$user,
    [Parameter(Mandatory = $True)]
    [string]$ticket,
    [string]$worknotes,
    [string]$uribase,
    [switch]$resolve
)

$ErrorActionPreference = 'Stop'

if (!$env:SERVICENOW_API_PASSWORD) {
    Write-Error 'environment variable SERVICENOW_API_PASSWORD must be set'
}

if ($uribase -contains 'service-now.com') {
    Write-Error 'URI base does seem to be ServiceNow.'
}

if ($ticket -match '([a-zA-Z]*)\d*') {
    $type = $matches[1]
}

if (-not $type) {
    Write-Error 'Could not parse ticket type'
    return
}

$table = @{'INC' = 'incident'; 'RITM' = 'sc_req_item'; 'SCTASK' = 'sc_task' }
$token = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes("$($user):$($env:SERVICENOW_API_PASSWORD)"))

# GetSysID
$uri = "$($uribase)/api/now/table/$($table[$type])?sysparm_query=number%3D$($ticket)&sysparm_limit=1"
try {
    $result = Invoke-WebRequest -Uri $uri -Headers @{'Authorization' = "BASIC $($token)"; 'Accept' = 'application/json' }
    $sysid = ($result.Content | ConvertFrom-Json).Result.sys_id
}
catch {
    Write-Error "Unable to invoke api call: $_"
}

$uri = "$($uribase)/api/now/table/$($table[$type])/$($sysid)"

if ($resolve) {
    if ($type -eq 'RITM') {
        $body = @{
            'comments' = "[code]$($worknotes)[/code]"
            'state'    = '6'
            'active'   = 'false'
        }
    }
    else {
        $body = @{
            'close_notes' = "[code]$($worknotes)[/code]"
            'state'       = '6'
            'active'      = 'false'
        }
    }
}
else {
    $body = @{
        'work_notes' = "[code]$($worknotes)[/code]"
    }
}

$body = $body | ConvertTo-Json

try {
    $result = Invoke-WebRequest -Uri $uri -Headers @{'Authorization' = "BASIC $($token)"; 'Accept' = 'application/json' } -Method 'PUT' -Body $body
    Write-Host "Updated $($ticket): $result"
}
catch {
    Write-Error "Unable to invoke api call: $_"
}
