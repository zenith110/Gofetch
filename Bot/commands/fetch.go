package commands
import(
	"strings"
	"net/http"
	"github.com/bwmarrin/discordgo"
	"io/ioutil"
	"regexp"
	"time"
	
)
func jsonParser(textMatch string, text string) string {
	removeData := strings.Replace(textMatch, text, "", -1)
	removeData = strings.Replace(removeData, `"`, "", -1)
	removeData = removeData[7:]
	removeData = strings.Replace(removeData, ",", "", -1)
	return removeData
}

func Fetchrun(s *discordgo.Session, m *discordgo.MessageCreate)int{
			client := &http.Client{}
			// Grabs the name from the user who inputted it
			secondaryArgs := m.Content[6:]
			// Lowercases it for ease of use into the database
			secondaryArgstest := strings.ToLower(secondaryArgs)
			// Removes all spaces in the name
			test := strings.Replace(secondaryArgstest, " ", "", -1)
			
			fetchurl := "http://gofetch.pictures:5000/breeds/?breed=" + test

			// Sends a post request to the url above
			req, err := http.NewRequest("POST", fetchurl, nil)
			// Will always be NIL, ignore
			if err == nil{
			}
			// Recieves the data so we can parse the body
			resp, error := client.Do(req)
			if error == nil{

			}
			// Puts the body text into the bodyText variable
			bodyText, err := ioutil.ReadAll(resp.Body)

			// Returns an error whenever we get something that's not in the database
			if len(bodyText) < 300{
				s.ChannelMessageSend(m.ChannelID, "It seems the breed you have inputted does not exist. Please look at our list at what breeds are currently being offered.")
				return 0
			}
			// Parses the text for instagram link
			instagramURLCheck := regexp.MustCompile(`.*"instagramURL": .*`)
			instaURLMatch := instagramURLCheck.FindStringSubmatch(string(bodyText))
			instagramURL := jsonParser(instaURLMatch[0], "instagramURL")
			// Parses the text for image url
			imageURLCheck := regexp.MustCompile(`.*"imageURL": .*`)
			imageURLMatch := imageURLCheck.FindStringSubmatch(string(bodyText))
			imageURL := jsonParser(imageURLMatch[0], "imageURL")
			
			embed := &discordgo.MessageEmbed{
				Color: 0x00ff00, // Green
				Fields: []*discordgo.MessageEmbedField{
					&discordgo.MessageEmbedField{
						Name:   "Image provided by http://gofetch.pictures",
						Value:  "Instagram page credits: " + instagramURL,
						Inline: true,
					},
				},

				Image: &discordgo.MessageEmbedImage{
					URL: imageURL,
				},

				Timestamp: time.Now().Format(time.RFC3339), // Discord wants ISO8601; RFC3339 is an extension of ISO8601 and should be completely compatible.
			}
			// Sends message
			s.ChannelMessageSendEmbed(m.ChannelID, embed)
		return 0	
}

