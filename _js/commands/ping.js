const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('ping')
		.setDescription('Latency (delay time) of the bot.'),
	async execute(interaction) {
		return await interaction.reply(`Ping: ${Math.round(interaction.client.ws.ping)} ms`);
	},
};

/*const { cpuUsage } = require('process');

const startUsage = cpuUsage();
// { user: 38579, system: 6986 }

// spin the CPU for 500 milliseconds
const now = Date.now();
while (Date.now() - now < 500);

console.log(cpuUsage(startUsage));
// { user: 514883, system: 11226 } */