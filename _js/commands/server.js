const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('server')
		.setDescription('Display info about this server.'),
	async execute(interaction) {
		return interaction.reply(`**${interaction.guild.name}** ${interaction.guild.id} ${interaction.guild.vanityURLCode}\nOwner: ${interaction.guild.ownerId}\nTotal members: ${interaction.guild.memberCount}`);
	},
};