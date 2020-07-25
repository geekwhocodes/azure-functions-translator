#!/bin/pwsh

$AZURE_STORAGE_ACCOUNT = "<<>>"
$resource_group = "<<>>"
$functionAppName = "<<>>"
$shareName = "models"
$directoryName = "models"
$shareId = "gwc$(Get-Random -Count 1)"
$mountPath = "/models" # DO not change

#Write-Progress "Get Storage account key" "Inprogress"
$AZURE_STORAGE_KEY = $(az storage account keys list -g $resource_group -n $AZURE_STORAGE_ACCOUNT --query '[0].value' -o tsv)
#Write-Progress "Get Storage account key" "Complete"

#Write-Progress "Create file share $shareName" "Inprogress"
az storage share create --account-name $AZURE_STORAGE_ACCOUNT `
  --account-key $AZURE_STORAGE_KEY `
  --name $shareName `
  --quota 50
#Write-Progress "Create file share $shareName" "Complete"

# #Write-Progress "Create directory $shareName" "Inprogress"
# az storage directory create --account-name $AZURE_STORAGE_ACCOUNT `
#   --account-key $AZURE_STORAGE_KEY `
#   --share-name $shareName `
#   --name $directoryName
# #Write-Progress "Create directory $shareName" "Complete"

#Write-Progress "Mount share to web app" "Inprogress"
az webapp config storage-account add `
  --resource-group $resource_group `
  --name $functionAppName `
  --custom-id $shareId `
  --storage-type "AzureFiles" `
  --share-name $shareName `
  --account-name $AZURE_STORAGE_ACCOUNT `
  --mount-path $mountPath `
  --access-key $AZURE_STORAGE_KEY
#Write-Progress "Mount share to web app" "Complete"


# This command upload files from directory to file share
# az storage file upload-batch --account-key $AZURE_STORAGE_KEY `
#   --account-name $AZURE_STORAGE_ACCOUNT --destination $directoryName `
#   --source ./models
