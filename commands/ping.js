const { SlashCommandBuilder } = require('@discordjs/builders');
const {MessageActionRow, MessageButton} = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('ping')
		.setDescription('Latency (delay time) of the bot.'),
	async execute(interaction) {
		const row = new MessageActionRow()
			.addComponents(
				new MessageButton()
				.setLabel("Ping")
				.setCustomId("ping")
				.setStyle("PRIMARY"),
			);
		await interaction.reply({content:`Ping: ${Math.round(interaction.client.ws.ping)} ms`, components: [row]});
		const filter = i => i.customId === 'ping' && i.user.id === interaction.user.id;

		const collector = interaction.channel.createMessageComponentCollector({ filter, time: 15000 });

		collector.on('collect', async i => {
			await i.update({ content: `Ping: ${Math.round(interaction.client.ws.ping)} ms`, components: [] });
		});

	},
};