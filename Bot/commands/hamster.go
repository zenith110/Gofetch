package commands
import (
	"strings"
	"net/http"
	"log"
	"github.com/bwmarrin/discordgo"
	"io/ioutil"
	"time"
)
func Hamsterun(s *discordgo.Session, m *discordgo.MessageCreate){
	client := &http.Client{}
			req, err := http.NewRequest("POST", "http://gofetch.pictures:5000/hamsters/", nil)
			if err != nil {
				log.Fatal(err)
			}
			resp, err := client.Do(req)
			if err != nil {
				log.Fatal(err)
			}
			bodyText, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				log.Fatal(err)
			}
			hamsterBreed := strings.Replace(string(bodyText), "Breeds:", "", -1)
			hamsterBreeds := strings.Replace(hamsterBreed, "\t", "", -1)
			embed := &discordgo.MessageEmbed{
				Author:      &discordgo.MessageEmbedAuthor{},
				Color:       0x00ff00, // Green
				Description: "Email admin@gofetch.pictures if you wish to submit a request for a new breed",
				Fields: []*discordgo.MessageEmbedField{
					&discordgo.MessageEmbedField{
						Name:   "Hamster breeds",
						Value:  hamsterBreeds,
						Inline: true,
					},
				},
				Timestamp: time.Now().Format(time.RFC3339), // Discord wants ISO8601; RFC3339 is an extension of ISO8601 and should be completely compatible.
			}
			s.ChannelMessageSendEmbed(m.ChannelID, embed)
}