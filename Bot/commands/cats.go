package commands

import (
	"io/ioutil"
	"log"
	"net/http"
	"strings"
	"time"
	"github.com/bwmarrin/discordgo"
)

func Catrun(s *discordgo.Session, m *discordgo.MessageCreate) {
	client := &http.Client{}
	req, err := http.NewRequest("POST", "http://gofetch.pictures:5000/cats/", nil)
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
	catBreed := strings.Replace(string(bodyText), "Breeds:", "", -1)
	catBreeds := strings.Replace(catBreed, "\t", "", -1)
	embed := &discordgo.MessageEmbed{
		Author: &discordgo.MessageEmbedAuthor{},
		Color:  0x00ff00, // Green
		Fields: []*discordgo.MessageEmbedField{
			&discordgo.MessageEmbedField{
				Name:   "Cat breeds",
				Value:  catBreeds,
				Inline: true,
			},
		},
		Timestamp: time.Now().Format(time.RFC3339), // Discord wants ISO8601; RFC3339 is an extension of ISO8601 and should be completely compatible.
	}
	s.ChannelMessageSendEmbed(m.ChannelID, embed)
}
