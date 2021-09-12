const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('profile')
		.setDescription('Display info about the user.')
		.addUserOption(option => option.setName('user').setDescription('The user\'s profile to show')),
	async execute(interaction) {
		var user = interaction.options.getUser('user');
		if (!user) {var user = interaction.user}
		const embed = new MessageEmbed()
			.setAuthor(user.username, user.displayAvatarURL({dynamic:true}))
			.setThumbnail(user.displayAvatarURL({dynamic:true}))
		return interaction.reply({embeds:[embed]});
	},
};