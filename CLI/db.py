import psycopg2
import json
import pandas as pd
import os
import requests
# Loads our json from azure blob storage
loginJsonFile = ""
content = requests.get(loginJsonFile)
data = json.loads(content.content)
def connectToDB(self, name, imageURL, instagramURL, fileName, sourceURL, azimage):
            
        
        #Establish a connection using the dblogin.json
        connection = psycopg2.connect(user = data["Login"]["Username"],
                                  password = data["Login"]["Password"],
                                  host = data["Login"]["Host"],
                                  port = data["Login"]["Port"],
                                  database = data["Login"]["Database"])

        cur = connection.cursor()

        # Inserts the data into each column
        cur.execute('INSERT INTO ' + data["Login"]["Table"] + '(breed, image, instagram, filename, sourceurl, azvalue) VALUES (%s, %s, %s, %s, %s, %s)', (name.lower(), imageURL, instagramURL, fileName, sourceURL, azimage))
        #cur.execute("DELETE FROM " + data["Login"]["Table"] + " WHERE sourceurl LIKE '%" + name + "%'")
        #print("Now deleting " + name)
        #Push the data onto the database
        connection.commit()
        nameQuery = pd.read_sql("SELECT * FROM " + data["Login"]["Table"] + " WHERE sourceurl LIKE '%" + name.lower() + "%'", connection)
        
        print(nameQuery)
        #Close the database
        connection.close()
        
        # Removes the file once we're done using it
        os.remove(fileName + ".jpg")