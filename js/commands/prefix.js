const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('prefix')
		.setDescription('Shows the prefix for the server.'),
	async execute(interaction) {
		return await interaction.reply(`Default prefix is =`);
	},
};