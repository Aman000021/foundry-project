$myemail = "Brandon.Adams@nestle.com"
$whotoadd = "Marcio.AleixoVieira@it.nestle.com"

$whotoid = $(az ad user show --id $whotoadd | ConvertFrom-Json).id

$groups = $(az ad user get-member-groups --id $myemail | ConvertFrom-Json -depth 10 |  select displayName, id | where { $_.displayName -like "*contributors*" })

$groups | ForEach-Object {
    $owner = $(az ad group owner list --group $_.displayName | ConvertFrom-Json | select mail | where { $_.mail -eq $myemail })

    if ($owner -ne $null) {

        try {
            az ad group owner add --group $_.displayName --owner-object-id $whotoid
            az ad group member add --group $_.displayName --member-id $whotoid
        }
        catch {
            Write-Host "An error occurred while adding the owner and member to group $_.displayName: $_"
        }
    }
}
