const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('server')
		.setDescription('Display info about this server.'),
	async execute(interaction) {
		const e = new MessageEmbed()
			.setColor('AQUA')
			.setTitle(`${interaction.guild.name}`)
			.setDescription(`**ID**: ${interaction.guild.id}\n**Owner**: <@${interaction.guild.ownerId}>`)
			.addField('Members', `${interaction.guild.memberCount} members`)

		if (interaction.guild.vanityURLCode){e.setURL(`${interaction.guild.vanityURLCode}`)};
		if (interaction.guild.icon){e.setThumbnail(`${interaction.guild.iconURL()}`)};
		if (interaction.guild.banner){e.setImage(`${interaction.guild.bannerURL()}`)};
		
		return interaction.reply({embeds: [e]});
	},
};