
import json
import db
def JSONData(self, animalName, imageURL, instagramURL, photoName, cdnLink, azimage):

# Creates a unique ID for filename
    # photoName = photoName.replace(" ", "_")
    # # Uncomment if you wish to create a json file.
    # # fileName = photoName

    # # Creates a dictionary
    # data = {}

    # # Creates a primary catagory
    # data[animalName.lower()] = []

    # # Create a default JSON structure
    # data[animalName.lower()].append(
    # {
    #     "breed": animalName.lower(),
    #     "filename": fileName,
    #     "instagramURL": instagramURL,
    #     "sourceURL": imageURL,
    #     "imageURL": cdnLink
    # })
    # print(cdnLink)
    # # Opens up the JSON file
    # file = open(fileName + ".json", "w")

    # # Dumps the data to the file
    # json.dump(data, file, indent = 1)
    # file.close()

    db.connectToDB(self, animalName, imageURL, instagramURL, photoName, cdnLink, azimage)