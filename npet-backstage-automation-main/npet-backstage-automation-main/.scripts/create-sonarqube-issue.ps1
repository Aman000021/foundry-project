param (
    [Parameter(Mandatory)][string]$Organization,
    [Parameter(Mandatory)][string]$Repository,
    [Parameter(Mandatory)][string]$Admins,
    [Parameter(Mandatory)][string]$RITM,
    [string]$SQRepository = 'nestle-it/azdo-automation'
)

'Creating SonarQube issue'

$title = "[CreateSonarQube] NPET template repository SonarQube - $RITM"

$ISSUE_BODY = @"
### >>Location<<

GitHub

### >>Project<<

$Repository

### >>Repository<<

$Organization/$Repository

### >>SonarQube<<

$Repository

### >>Admins<<

$Admins
"@

$response = gh issue create `
    --title $title `
    --body $ISSUE_BODY `
    --repo $SQRepository

$response


Write-Output "issue_detail=$($response)" >> $Env:GITHUB_ENV
Write-Output "issue_detail1=$($response)" >> $Env:GITHUB_ENV
