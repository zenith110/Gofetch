package commands
import(
	"strings"
	"net/http"
	"log"
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

func Fetchrun(s *discordgo.Session, m *discordgo.MessageCreate){
	client := &http.Client{}
			secondaryArgs := m.Content[6:]
			secondaryArgstest := strings.ToLower(secondaryArgs)
			test := strings.Replace(secondaryArgstest, " ", "", -1)

			fetchurl := "http://gofetch.pictures:5000/breeds/?breed=" + test

			req, err := http.NewRequest("POST", fetchurl, nil)

			if err != nil {
				log.Fatal(err)
			}

			//log.Print(req)
			resp, err := client.Do(req)
			if err != nil {
				log.Fatal(err)
			}
			bodyText, err := ioutil.ReadAll(resp.Body)
			//log.Print(string(bodyText))
			if err != nil {
				log.Fatal(err)
			}

			instagramURLCheck := regexp.MustCompile(`.*"instagramURL": .*`)
			instaURLMatch := instagramURLCheck.FindStringSubmatch(string(bodyText))
			instagramURL := jsonParser(instaURLMatch[0], "instagramURL")

			imageURLCheck := regexp.MustCompile(`.*"imageURL": .*`)
			imageURLMatch := imageURLCheck.FindStringSubmatch(string(bodyText))
			imageURL := jsonParser(imageURLMatch[0], "imageURL")
			print(imageURL)
			//print(imageURLMatch[0])
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
			s.ChannelMessageSendEmbed(m.ChannelID, embed)
}

