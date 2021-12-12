const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
require('dotenv').config()
const fs = require('fs');
const logger = require('./utils/logger')

const commands = [];
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

// Place your client and guild ids here
const clientId = '882811387427037184';
const guildId = '709711335436451901';

for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	commands.push(command.data.toJSON());
}

const rest = new REST({ version: '9' }).setToken(process.env.DISCORD_TOKEN);

(async () => {
	try {
		logger.log('Started refreshing application (/) commands.');

		await rest.put(
			// Routes.applicationCommands(clientId),
			Routes.applicationGuildCommands(clientId, guildId),
			{ body: commands },
		);

		logger.log('Successfully reloaded application (/) commands.');
	} catch (error) {
		logger.stacktrace(error);
	}
})();