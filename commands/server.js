const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('server')
		.setDescription('Display info about this server.')
		.addStringOption(option => option.setName('server_id').setDescription('The server id if applicable.')),
	async execute(interaction) {
		let server = interaction.options.getString('server_id');
		try {server = interaction.client.guilds.cache.get(server)} catch(error) {};
		if (!server) {server=interaction.guild}
		const e = new MessageEmbed()
			.setColor('AQUA')
			.setTitle(`${server.name}`)
			.setDescription(`**ID**: ${server.id}\n**Owner**: <@${server.ownerId}>`)
			.addField('Members', `${server.memberCount} members`)

		if (server.vanityURLCode){e.setURL(`${server.vanityURLCode}`)};
		if (server.icon){e.setThumbnail(`${server.iconURL()}`)};
		if (server.banner){e.setImage(`${server.bannerURL()}`)};
		
		return interaction.reply({embeds: [e]});
	},
};