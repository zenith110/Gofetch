#!flask/bin/python
from flask import Flask, render_template, request, redirect
import os, random
import glob
import re
import json
import psycopg2
# Initalizes the flask application
app = Flask(__name__)


# Renders the home page
@app.route("/")
def index():
    return render_template("index.html")
    
# Route that posts all dogs available
@app.route("/dogs/", methods =["POST"])
def grabAllDogs():
    return "Breeds:\n\tCorgi\n\tShiba Inu\n\tCavailer\n\tChow Chow\n\tDachshund\n\tDoberman Pinschers\n\tGerman Sheperd\n\tGolden Retriever\n\tRottweiler\n\tShar Pei\n\tTibetan Mastiff\n\tAmerican Bulldog\n\tAmerican Pitbull\n\tBorder Collie\n\tShih tzu\n\tBloodhound\n\tLabador Retriever\n\tWest Highland Terrier\n\tYorkshire Terrier"

@app.route("/cats/", methods =["POST"])
def grabAllCats():
    return "Breeds:\n\tAmerican Bobtail"
   
@app.route("/hamsters/", methods =["POST"])
def grabAllHamsters():
    return "Breeds:\n\tWinter White"
# Grab arguments from curl request
@app.route("/apidocs/")
def apiDocs():
    return render_template("docs.html")
@app.route("/breeds/", methods =["POST"])
def sendNameApi():
    animalName = request.args.get("breed")
    animalName = animalName.lower()
    animalName = animalName.replace(" ", "_")
    
    with open("settings/dblogin.json", "r") as loop:
        data = json.load(loop)
        
    #Establish a connection using the dblogin.json
    connection = psycopg2.connect(user = data["Login"]["Username"],
                                  password = data["Login"]["Password"],
                                  host = data["Login"]["Host"],
                                  port = data["Login"]["Port"],
                                  database = data["Login"]["Database"])

    cur = connection.cursor()
    # Checks to see if the name exist in the record, then grabs a random row from that column limiting it to one.
    try:
      sourceUrl = cur.execute("SELECT * FROM " + data["Login"]["Table"] + " WHERE sourceurl LIKE '%" + animalName + "%' ORDER BY RANDOM() LIMIT 1")
    except:
        return "Unfortunately, we do not have data available on " + animalName + " at this time. \nLook again soon however, or email the admin!"
    
    # Fetches us all the rows so we can grab data from each
    records = cur.fetchall()
    for row in records:
        fileName = row[0]
        instagramUrl = row[1]
        instagramPageUrl = row[2]
        fileName = row[3]
        sourceUrl = row[4]
        
    # Creates a dictionary
    data = {}

    # Creates a primary catagory
    data[animalName.lower()] = []

    # Create a default JSON structure
    data[animalName.lower()].append(
    {
        "breed": animalName.lower(),
        "filename": fileName,
        "instagramURL": instagramPageUrl,
        "sourceURL": instagramUrl,
        "imageURL": sourceUrl
    })
    
    
    breedReturn = json.dumps(data, indent = 2)
    
    return breedReturn

# Our post request that redirects and renames the url for the breed
@app.route("/breed", methods =["POST"])
def sendName():
    # Grabs input from user and removes spaces and replaces with _
    animalName = request.form["animal"]
    animalName = animalName.lower()
    animalName = animalName.replace(" ", "-")

    # If passed in empty space, question user
    if animalName == "":
        return render_template("index.html", message = ("Please enter required field"))

    # Return redirect to breed page
    return redirect("/breed/"+ animalName)
# Add breed name to the url, and does our image fetching
@app.route("/breed/<string:animalName>/", methods =["GET"])
def getApiBreed(animalName):
    
    with open("settings/dblogin.json", "r") as loop:
        data = json.load(loop)
        
    #Establish a connection using the dblogin.json
    connection = psycopg2.connect(user = data["Login"]["Username"],
                                  password = data["Login"]["Password"],
                                  host = data["Login"]["Host"],
                                  port = data["Login"]["Port"],
                                  database = data["Login"]["Database"])

    cur = connection.cursor()
    
    # Checks to see if the name exist in the record, then grabs a random row from that column limiting it to one.
    try:
        cur.execute("SELECT * FROM " + data["Login"]["Table"] + " WHERE sourceurl LIKE '%" + animalName + "%' ORDER BY RANDOM() LIMIT 1")
        records = cur.fetchall()
        for row in records:
            fileName = row[0]
            breedName = row[1]
            instagramUrl = row[2]
            instagramPageUrl = row[3]
            sourceUrl = row[4]
        
        finalName = animalName.replace("-", " ")
        # Returns a new page with the image
        return render_template("successpage.html", imageurl = sourceUrl, name = finalName, pageurl = instagramUrl, pageName = animalName)
    except:
        return render_template("500.html", name = animalName, imageurl = "https://breeds.blob.core.windows.net/websitefiles/404image.png")

if __name__ == '__main__':
    app.run(host='0.0.0.0')

