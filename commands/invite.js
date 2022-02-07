const { SlashCommandBuilder } = require('@discordjs/builders');
const {Permissions} = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('invite')
		.setDescription('Invite Link for the bot.'),
	async execute(interaction) {
        const link = interaction.client.generateInvite({
            scopes: ['applications.commands', 'bot'],
          });
        const admin = interaction.client.generateInvite({
            permissions: [
              Permissions.FLAGS.ADMINISTRATOR,
            ],
            scopes: ['applications.commands', 'bot'],
          });
		return await interaction.reply({content:`**Bot Invite Links**\n<:Jade:940157556469420083> [Invite](${link})\n<:Cyan:940157545165754388> [Admin](${admin})`, ephemeral: true});

	},
};