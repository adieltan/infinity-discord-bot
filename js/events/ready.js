const logger = require('../utils/logger');
Discord = require("discord.js");
module.exports = {
	name: 'ready',
	once: true,
	execute(client) {
		logger.info(`${client.user.tag}\nNode version: ${process.version}\nDiscord.js version: ${Discord.version}`);
		client.user.setPresence({ activities: [{ name: `${client.guilds.cache.reduce((acc, guild) => acc + guild.memberCount, 0)} users in ${client.guilds.cache.size} guilds.` , type:'WATCHING'}], status: 'idle' });
		const channel = client.channels.cache.get('813251835371454515');
		channel.send(`∞ ${client.emoji.javascript}`);
	},
};