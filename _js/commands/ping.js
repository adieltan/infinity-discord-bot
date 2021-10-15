const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('ping')
		.setDescription('Latency (delay time) of the bot.'),
	async execute(interaction) {
		return await interaction.reply(`Ping: ${Math.round(interaction.client.ws.ping)} ms`);
	},
};