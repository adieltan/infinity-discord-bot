const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('profile')
		.setDescription('Display info about the user.')
		.addUserOption(option => option.setName('user').setDescription('The user\'s profile to show')),
	async execute(interaction) {
		let user = interaction.options.getUser('user');
		try {user = interaction.guild.member.fetch(user)} catch(error) {};
		if (!user) {user = interaction.user}
		const embed = new MessageEmbed()
			.setTitle('User Info')
			.setDescription(`<@${user.id}> ${user.tag}`)
			.setColor(user.hexAccentColor)
			.setAuthor(user.username, user.displayAvatarURL())
			.setThumbnail(user.displayAvatarURL())
			.setFooter(`${user.id}`)
			.setTimestamp(user.createdAt);
			if (user.banner){embed.setImage(user.bannerURL())};
		return interaction.reply({embeds:[embed]});
	},
};