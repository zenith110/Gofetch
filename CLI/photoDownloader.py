import azureFunctions
import requests
# Handles downloading images
def pictureDownloader(self, photoURL, instagramURL, photoName, blobName, container, accountName):
    photoName = photoName.replace(" ", "-")

    # Begins to download the image
    requestsUrl = requests.get(photoURL)

    # Creates the file in memory
    file = open(photoName + ".jpg", "ab")

    # Writes the file from the request stream
    file.write(requestsUrl.content)

    # Closes to save memory/prevent leaks
    file.close()

    # Uploads to our azure container before we move it to local
    azureFunctions.azureUpload("", photoURL, instagramURL, photoName, blobName, container, photoName + ".jpg", accountName)

 