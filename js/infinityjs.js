require('dotenv').config();
const fs = require('fs');
const { Client, Collection, Intents } = require('discord.js');
const {AmariBot} = require('amaribot.js')
const emoji = require('./emoji.js');
const logger = require('./utils/logger.js');
const MongoClient = require('mongodb').MongoClient;

const mongoose = require('mongoose');

main().catch(err => console.log(err));

async function main() {
  await mongoose.connect(process.env.mongo);
}

const client = new Client({ 
	intents: [
		Intents.FLAGS.GUILDS, 
		Intents.FLAGS.GUILD_MEMBERS,
		Intents.FLAGS.GUILD_BANS,
		Intents.FLAGS.GUILD_EMOJIS_AND_STICKERS,
		Intents.FLAGS.GUILD_WEBHOOKS,
		Intents.FLAGS.GUILD_INVITES,
		Intents.FLAGS.GUILD_VOICE_STATES,
		Intents.FLAGS.GUILD_PRESENCES,
		Intents.FLAGS.GUILD_MESSAGES,
		Intents.FLAGS.GUILD_MESSAGE_REACTIONS,
		Intents.FLAGS.DIRECT_MESSAGES,
		Intents.FLAGS.DIRECT_MESSAGE_REACTIONS,
	], allowedMentions: { parse: ['users', 'roles'] } });
client.commands = new Collection();
client.emoji = emoji;
client.mcommands = new Collection();

const amari = new AmariBot(process.env.amari, {token:process.env.amari})

//commands
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	// Set a new item in the Collection
	// With the key as the command name and the value as the exported module
	client.commands.set(command.data.name, command);
}
//functions
const functions = fs.readdirSync('./functions').filter(file => file.endsWith('.js'));
for (file of functions) {
	require(`./functions/${file}`)(client);
}
//events
const eventFiles = fs.readdirSync('./events').filter(file => file.endsWith('.js'));
for (const file of eventFiles) {
	const event = require(`./events/${file}`);
	if (event.once) {
		client.once(event.name, (...args) => event.execute(...args));
	} else {
		client.on(event.name, (...args) => event.execute(...args));
	}
}

const mcommandFiles = fs.readdirSync('./mcommands').filter(file => file.endsWith('.js'));
for (const file of mcommandFiles) {
	const mcommand = require(`./mcommands/${file}`);
	client.mcommands.set(mcommand.data.name, mcommand);
}

client.login(process.env.DISCORD_TOKEN);