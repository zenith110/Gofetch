from azure.storage.blob import BlobServiceClient, ContainerClient, ContentSettings, generate_container_sas, ContainerSasPermissions, generate_blob_sas, BlobSasPermissions
import photoDownloader, jsonCreator
import json
import os
from datetime import datetime, timedelta
import requests
# Loads our json file from azure container
loginJsonFile = ""
# # Handles uploading our JSON files for us, can be used if necessary
# # def jsonUpload(self, jsonFile, containerClient, blobServiceClient):
# #     # Create a blob client using the local file name as the name for the blob
# #     blobClient = blobServiceClient.get_blob_client(container=containerClient, blob=jsonFile)

# #     print("\nUploading to Azure Storage as blob:\n\t" + str(jsonFile))

# #     # Upload the created file
# #     with open(jsonFile, "rb") as data:
# #         blobClient.upload_blob(data)

# Creates our container for the blob
def createContainer(self, photoURL, instagramURL, photoName, blobName, container, blobCreator):
    print("Now making " + container)
    containerClient = blobCreator.create_container(container)

    photoDownloader.pictureDownloader(self, photoURL, instagramURL, photoName, blobName, container, blobCreator)

# using generate_container_sas
def getImgUrlWithContainerSasToken(blobName, containerName):
    content = requests.get(loginJsonFile)
    data = json.loads(content.content)
    accountName = data["Login"]["Account"]
    accountKey = data["Login"]["Key"]
    containerSasToken = generate_container_sas(
        account_name=accountName,
        container_name=containerName,
        account_key=accountKey,
        permission= ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_container_sas_token = f"https://{accountName}.blob.core.windows.net/{containerName}/{blobName}?{containerSasToken}"

    return blob_url_with_container_sas_token
    
# using generate_blob_sas
def getImgUrlWithBlobSasToken(blobName, containerName):
    content = requests.get(loginJsonFile)
    data = json.loads(content.content)
    accountName = data["Login"]["Account"]
    accountKey = data["Login"]["Key"]

    blobSasToken = generate_blob_sas(
        account_name=accountName,
        container_name=containerName,
        blob_name=blobName,
        account_key=accountKey,
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_blob_sas_token = f"https://{accountName}.blob.core.windows.net/{containerName}/{blobName}?{blobSasToken}"
    return blob_url_with_blob_sas_token

# Uploads after the container has been created
def azureUpload(self, photoURL, instagramURL, photoName, blobName, containerClient, image, blobCreator):
    # Create a blob client using the local file name as the name for the blob
    blobClient = blobCreator.get_blob_client(container=containerClient, blob=image)
    # Upload the created file
    with open(image, "rb") as data:
        blobClient.upload_blob(data, content_settings = ContentSettings(content_type='jpg'))
    
    content = requests.get(loginJsonFile)
    data = json.loads(content.content)
    # Replace the site with cdn endpoint
    cdnLink = data["Login"]["cdnURL"] + blobName + "/" + image 
    azureImageUrl = getImgUrlWithBlobSasToken(blobName, containerClient)

    # Go make the json with the new data, and slide in the cdn
    jsonCreator.JSONData(self, blobName, photoURL, instagramURL, photoName, cdnLink, azureImageUrl)  

# # Handles uploading to storage account the first time
def azureUploaderFirst(self, photoURL, instagramURL, photoName, blobName):
    content = requests.get(loginJsonFile)
    data = json.loads(content.content)
    accountName = data["Login"]["Account"]
    accountKey = data["Login"]["Key"]

    # Makes our connection string to make it easier to upload
    connectStr = data["Login"]["connectionString"]

    # Assigns the name of the container to the blobName
    container = blobName
    # Creates a storage client to check if the storage is created or not
    storage = ContainerClient.from_connection_string(connectStr, container)

    # Creates a blob service so we can create our first storage container, and upload our blobs to our storage account.
    blobCreator = BlobServiceClient.from_connection_string(connectStr)
    
    try:
        createContainer("", photoURL, instagramURL, photoName, blobName, container, blobCreator)
    except:
        if(storage.get_container_properties()):
            photoDownloader.pictureDownloader(self, photoURL, instagramURL, photoName, blobName, container, blobCreator) 
            
    