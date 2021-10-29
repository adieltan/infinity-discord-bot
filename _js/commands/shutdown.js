const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('shutdown')
		.setDescription('Shutsdown the bot.'),
	async execute(interaction) {
		if (interaction.member.id in interaction.client.bot.owners()){
            interaction.reply("BYE")
            return interaction.client.destroy()}
		else{ return interaction.reply(`You aren't owner ${interaction.client.bot.owners()}`)
        }

	},
};