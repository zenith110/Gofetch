# GoFetch

REST API intended to deliver to the user animal images scraped from instagram.
The images are scrapped using a program created in PySide2 using selenium, azure functionality, and beautifulsoup

Endpoint for currently available dog breeds can be found at http://gofetch.pictures/dogs/
Dogs:

    Corgi
    Shiba Inu
    Cavailer
    Chow Chow
    Dachshund
    Doberman Pinschers
    German Shepard
    Golden Retriver
    Rottweiler
    Shar Pei
    Tibetan Mastiff
    American Bulldog
    American Pitbull
    Siberian Husky
    Yorkshire Terrier
    

Endpoint for currently available cat breeds can be found at http://gofetch.pictures/cats/
Cats:
    
    American Bobtail
    Maine Coon
    
Endpoint for currently available hamster breeds can be found at http://gofetch.pictures/hamsters/    
Hamsters:

    Winter White
    Campbell

This list will constantly be updated and is not final, message admin@gofetch.pictures for breeds to add to this list.

The images are stored in an azure storage, using containers to hold the image.
Using postgreSQL, we are able to fetch the images and query random results each time.

CURL requests are the primary format to grab the data from api, and must be approached in this format:

    - curl -x POST www.gofetch.pictures/breeds/?breed=

Query must remove spaces otherwise will not fetch correctly, eliminate spaces if using a discord bot or fetching service.
