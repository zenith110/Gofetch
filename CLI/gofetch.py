# cli.py
import click
import requests 
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
from random import randint
import os, time, uuid
import shutil
import azureFunctions
import psycopg2
import json
import pandas as pd
import pyfiglet

# Loads our json from azure blob storage
dbLogin = ""
content = requests.get(dbLogin)
data = json.loads(content.content)

#Loads the ascii art
result = pyfiglet.figlet_format("Gofetch CLI", font = "doom") 
print(result) 

# Creates the command group
@click.group()
def main():
    pass

# Creates the post command for breed data
@main.command()
@click.argument("breed_name")
def breed(breed_name):
    params = (
        ('breed', breed_name),
    )
    response = requests.post('http://gofetch.pictures:5000/breeds/', params=params).json()
    print(response.content)

# Pings all the dogs using a curl request
@main.command()
def dogs():
    "Grabs the dog list from the website"
    response = requests.post('http://gofetch.pictures:5000/dogs/')
    text  = response.content.decode("utf-8") 
    text  = text.replace("Breeds:", "")
    text  = text.replace("\t", "")
    print(text)

@main.command()
def cats():
    "Grabs the cat list from the website"
    response = requests.post('http://gofetch.pictures:5000/cats/')
    text  = response.content.decode("utf-8") 
    text  = text.replace("Breeds:", "")
    text  = text.replace("\t", "")
    print(text)

@main.command()
def hamsters():
    "Grabs the hamster list from the website"
    response = requests.post('http://gofetch.pictures:5000/hamsters/')
    text  = response.content.decode("utf-8") 
    text  = text.replace("Breeds:", "")
    text  = text.replace("\t", "")
    print(text)

@main.command()
def birds():
    "Grabs the bird list from the website"
    response = requests.post('http://gofetch.pictures:5000/birds/')
    text  = response.content.decode("utf-8") 
    text  = text.replace("Breeds:", "")
    text  = text.replace("\t", "")
    print(text)

# Lets us delete all mentions of the container files in the db
@main.command()
@click.argument("container_name")
def delete(container_name): 
    "Deletes all instances of container name from the PostgreSQL db"
    #Establish a connection using the dblogin.json
    connection = psycopg2.connect(user = data["Login"]["Username"],
                                  password = data["Login"]["Password"],
                                  host = data["Login"]["Host"],
                                  port = data["Login"]["Port"],
                                  database = data["Login"]["Database"])

    cur = connection.cursor()
    print("Now deleting " + container_name)
    cur.execute("DELETE FROM " + data["Login"]["Table"] + " WHERE sourceurl LIKE '%" + container_name + "%'")
    nameQuery = pd.read_sql("SELECT * FROM " + data["Login"]["Table"] + " WHERE sourceurl LIKE '%" + container_name.lower() + "%'", connection)
    print(nameQuery)
    #Close the database
    connection.close()
@main.command()
def secret():
    "My magnum opus"
    print("pls gib job, email contact@abrahannevarez.dev")

@main.command()
@click.argument('breed_name', nargs=-1)
@click.argument('link_url', nargs=1)
def linkscrape(breed_name, link_url):
    "When you cannot click a random instagram page, use this command"
    chrome_driver = os.environ.get("SCRAPE")
    animalText = str(breed_name)
    animalText = animalText.replace(",", "")
    animalText = animalText.replace("(", " ")
    animalText = animalText.replace(")", " ")
    animalText = animalText.replace("'", " ")
    animalText = animalText.replace("'", " ")
    animalText = animalText.replace(" ", "")
    animalText = animalText.replace("-", "")
    options =  webdriver.ChromeOptions() 
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)
    

    # Begin the web driver by starting on google
    driver.get(link_url)

    windowAddress = driver.current_url
    result = requests.get(windowAddress)
    src = result.content
    
    # Instantate beautifulsoup object
    data = BeautifulSoup(src, 'lxml')
        
    # Grabs us all the images on the current page that is currently shown
    picClick = driver.find_elements_by_class_name("_bz0w")

    # Stores all the pics into a list, letting selenium to decide which to pick
    l = picClick[randint(0, len(picClick)-1)]
    try:
        l.click()
    except:
        driver.close()
            
    # Fetches the picture URL
    windowPicture = driver.current_url

    resultPic = requests.get(windowPicture)
    srcPic = resultPic.content
    imageData = BeautifulSoup(srcPic, 'lxml')
    imageURL = imageData.find('meta', property="og:image")

    photoName = animalText.lower() + "_" + str(randint(0, 100000))

    animalText = animalText.lower()
    animalText = animalText.replace(" ", "")
    azureFunctions.azureUploaderFirst("", str(imageURL["content"]), windowPicture, photoName, animalText)
    driver.close()
@main.command()
@click.argument('breed_name', nargs=-1)
@click.argument('breed_type', nargs=1)
# Scrapes given the breed type
def scrape(breed_name, breed_type):
    "Scrapes the breed following the catagory"
    chrome_driver = os.environ.get("SCRAPE")
    animalText = str(breed_name)
    animalText = animalText.replace(",", "")
    animalText = animalText.replace("(", " ")
    animalText = animalText.replace(")", " ")
    animalText = animalText.replace("'", " ")
    animalText = animalText.replace("'", " ")
    animalText = animalText.replace(" ", "")
    animalText = animalText.replace("-", "")
    options =  webdriver.ChromeOptions() 
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)


    # Begin the web driver by starting on google
    driver.get("https://google.com")

    # Searches for animal that is specified by user
    search = driver.find_element_by_name('q')

    # Adds a instagram to filter out the results
    search.send_keys(animalText + " " + str(breed_type) + " instagram")
    search.send_keys(Keys.RETURN)

    # Clicks on the first instagram link that is found
    animalLink = driver.find_element_by_css_selector("h3")
    animalLink.click()

    # Grabs the URL of the instagram page
    windowAddress = driver.current_url
    result = requests.get(windowAddress)
    src = result.content
    
    # Instantate beautifulsoup object
    data = BeautifulSoup(src, 'lxml')

    # Grabs us all the images on the current page that is currently shown
    picClick = driver.find_elements_by_class_name("_bz0w")

    # Stores all the pics into a list, letting selenium to decide which to pick
    l = picClick[randint(0, len(picClick)-1)]
    try:
        l.click()
    except:
        driver.close()
            
    # Fetches the picture URL
    windowPicture = driver.current_url

    resultPic = requests.get(windowPicture)
    srcPic = resultPic.content
    imageData = BeautifulSoup(srcPic, 'lxml')
    imageURL = imageData.find('meta', property="og:image")

    photoName = animalText.lower() + "_" + str(randint(0, 100000))

    animalName = animalText.lower()
    animalName = animalName.replace(" ", "")
    azureFunctions.azureUploaderFirst("", str(imageURL["content"]), windowPicture, photoName, animalName)
    driver.close()

if __name__ == "__main__":
    main()


