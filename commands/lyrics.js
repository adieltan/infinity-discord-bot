const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const fetch = require('node-fetch');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('lyrics')
		.setDescription('Display a song lyrics.')
		.addStringOption(option => option.setName('song_name').setDescription('The song you want to search for.').setRequired(true)),
	async execute(interaction) {
        await interaction.deferReply({ephemeral: true});
		let song_name = interaction.options.getString('song_name');
        let lyrics = await fetch(`https://api.darrennathanael.com/lyrics?song=${song_name}`).then((res) => res.json());
    
        // check if the response is 200
        try {
          if (lyrics.response !== 200) {
            lyrics = await fetch(`https://api.darrennathanael.com/lyrics-genius?song=${song_name}`).then((res) => res.json());
            if (lyrics.response !== 200) {
              let noLyrics = new MessageEmbed()
                .setColor(0x2F3136)
                .setDescription(
                  `❌ | No lyrics found for ${song_name}! Please try again.`
                );
              return interaction.editReply({ embeds: [noLyrics], ephemeral: true });
            } else {
              let embed = new MessageEmbed()
                .setColor(0x2F3136)
                .setTitle(`${lyrics.full_title}`)
                .setURL(lyrics.url)
                .setThumbnail(lyrics.thumbnail)
                .setDescription(lyrics.lyrics);
              return interaction.editReply({ embeds: [embed], ephemeral: false });
            }
          }
          // if the response is 200
          let embed = new MessageEmbed()
            .setColor(0x2F3136)
            .setTitle(`${lyrics.full_title}`)
            .setURL(lyrics.url)
            .setThumbnail(lyrics.thumbnail)
            .setDescription(lyrics.lyrics);
          return interaction.editReply({ embeds: [embed], ephemeral: false });
        } catch (err) {
          let noLyrics = new MessageEmbed()
            .setColor(0x2F3136)
            .setDescription(
              `❌ | No lyrics found for ${song_name}! Please try again.`
            );
          return interaction.editReply({ embeds: [noLyrics], ephemeral: true });
        }
	},
};