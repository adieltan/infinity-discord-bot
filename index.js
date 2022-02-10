const chalk = require("chalk");
console.clear(); //clear the console before start logging
console.log(chalk.bold("		          	  ♾️  Infinity")); //Infinity logo for fun

require("dotenv").config();

const fs = require("fs");
const { Client, Collection, Intents } = require("discord.js");
const logger = require("./utils/logger");
require("./checker");
// require("./deploy");
const mongoose = require("mongoose");
const { AmariBot } = require("amaribot.js")

mongoose
  .connect(process.env.mongo_server)
  .then(logger.custom("Connected!", "green", "MongoDB"));


//Check for any package updates
const updateNotifier = require("update-notifier");
const pkg = require("./package.json");

updateNotifier({ pkg }).notify();

const client = new Client({
  intents: [
    Intents.FLAGS.GUILDS,
    Intents.FLAGS.GUILD_MEMBERS,
    Intents.FLAGS.GUILD_BANS,
    Intents.FLAGS.GUILD_EMOJIS_AND_STICKERS,
    // Intents.FLAGS.GUILD_INTEGRATIONS,
    Intents.FLAGS.GUILD_WEBHOOKS,
    Intents.FLAGS.GUILD_INVITES,
    Intents.FLAGS.GUILD_VOICE_STATES,
    // Intents.FLAGS.GUILD_PRESENCES,
    Intents.FLAGS.GUILD_MESSAGES,
    Intents.FLAGS.GUILD_MESSAGE_REACTIONS,
    // Intents.FLAGS.GUILD_MESSAGE_TYPING,
    Intents.FLAGS.DIRECT_MESSAGES,
    Intents.FLAGS.DIRECT_MESSAGE_REACTIONS,
    // Intents.FLAGS.DIRECT_MESSAGE_TYPING,
  ],
  allowedMentions: { parse: ["users"] },
  presence: {status: "online", activities: [{name: "With Infinity", type: "PLAYING"}]},
  ws: { properties: { $browser: "Discord iOS" }}

});

client.owner = [
  "701009836938231849",
  "703135131459911740",
  "708233854640455740",
];
client.commands = new Collection();
client.amari = new AmariBot(process.env.amari);
client.snipes = {
  snipes: new Collection(),
  esnipes: new Collection(),
}
client.db = {
  status: {}
}
//commands
const commandFiles = fs
  .readdirSync("./commands")
  .filter((file) => file.endsWith(".js"));
for (const file of commandFiles) {
  const command = require(`./commands/${file}`);
  // Set a new item in the Collection
  // With the key as the command name and the value as the exported module
  client.commands.set(command.data.name, command);
}
//events
const eventFiles = fs
  .readdirSync("./events")
  .filter((file) => file.endsWith(".js"));
for (const file of eventFiles) {
  const event = require(`./events/${file}`);
  if (event.once) {
    client.once(event.name, (...args) => event.execute(...args));
  } else {
    client.on(event.name, (...args) => event.execute(...args));
  }
}

process.on('uncaughtException', (err) => {
  console.log(err)
})

process.on('unhandledRejection', (err) => {
  console.log(err)
})
client.on('error', (error) => {
  console.log(error)
})
client.login(process.env.dc_beta);
