const { SlashCommandBuilder, time } = require('@discordjs/builders');
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
			.setColor(0x2F3136)
			.setAuthor({name: user.username, avatar: user.displayAvatarURL()})
			.setThumbnail(user.displayAvatarURL())
			.setFooter({text: `${user.id}`})
			.setTimestamp(user.createdAt)
			.addField("Registered", `${time(user.createdAt, "F")}\n${time(user.createdAt, "R")}`)
			.addField("Joined", `${time(user.joinedAt, "F")}\n${time(user.joinedAt, "R")}`);
			if (user.banner){embed.setImage(user.bannerURL())};
		try {
			const UserAmariLevel = await interaction.client.amari.getUserLevel(interaction.guild.id, interaction.user.id);
			embed.addField("Amari Level", value=`EXP: **${UserAmariLevel.exp}** (Level ${UserAmariLevel.level})\nWeekly EXP: **${UserAmariLevel.weeklyExp}**`);
		} catch (error) {
			error => error;
		};
		return interaction.reply({embeds:[embed]});
	},
};