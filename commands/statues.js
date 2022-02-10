const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, MessageButton, MessageActionRow } = require('discord.js');
const wait = require('util').promisify(setTimeout);

module.exports = {
	data: new SlashCommandBuilder()
		.setName('statues')
		.setDescription('Initialises a red light green light game.'),
	async execute(interaction) {
        await interaction.deferReply();
        const e = new MessageEmbed()
            .setColor(0x2F3136)
            .setTitle(`Statues Game Information`)
            .setDescription(`Statues (also known as Red Light, Green Light) is a popular children\'s game, often played in different countries.\nSource: [Wikipedia](https://en.wikipedia.org/wiki/Statues_(game))\nThe game is also seen in Netflix™ Drama: [Squid Game](https://g.co/kgs/WmEEUi) \nIn this game, you have to run as far as possible by pressing the Run button when it is green. Pressing it when it is red will get you instantly executed.\nThe button **might** change from red to green or from green to red every 5 seconds. Burple coloured button is "Yellow".`)
            .setImage(`https://cdn.mos.cms.futurecdn.net/WDBV52ZBsohECa3V9HeKyZ.jpg`)
        const row = new MessageActionRow()
			.addComponents(
				new MessageButton()
				.setLabel("Run")
				.setCustomId("run")
				.setStyle("SUCCESS")
                .setEmoji("🏃‍♂️"),
                new MessageButton()
                .setLabel("My Position")
                .setCustomId("position")
                .setStyle("SECONDARY")
                .setEmoji("<:Jade:940157556469420083>"),
			);
        await interaction.editReply({content: "The game will start in 3 minutes.", embeds: [e], components: [row]});
        await wait(10)
        const filter = i => i.customId === 'run';

		const collector = interaction.channel.createMessageComponentCollector({ filter, time: 15000 });

		collector.on('collect', async i => {
			await i.deferUpdate();
		});
	},
};