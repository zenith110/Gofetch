# Gofetch
## Website
### Info:
* Created in Flask and Python
* Uses Microsoft Azure for pictures alongside with content delivery network(CDN) to deliver fast images using edge servers nearby
* Uses PostgreSQL as the database to allow versatility in services(ie, use all data in multiple platforms)

### Running the site:
- Navigate to website directory and run python app.py or python3 app.py if you have python2. It should launch a flask local host.
- Configure the database config(dblogin.json) and azure login(settings.json) with your own credentials.
 
## CLI
 ### Info:
* Command Line Interface web scraper for the site gofetch.pictures.
* Uses Microsoft's Azure for cloud, and PostgreSQL for database.
* Uses Pyfiglet for the art and Click for the backbone of the command system.
* Uses Selenium and Chromewebdriver to web scrape Instagram images.

### How to use:
1) Create info and dblogin json files and load them in(either locally or on the cloud).
2) Run gofetch.py.
3) Use the commands however you wish.

## Gofetch bot
### Info:
  * Created in Go and uses DiscordGO
  * Uses post requests to gofetch to do the functions such as: listing all dog, cats, hamsters, and birds as well as fetching the breed specified by the discord user.
### How to use
1) Install go, and discordgo.
2) Modify the config file with your custom discord bot token and hit go run.
