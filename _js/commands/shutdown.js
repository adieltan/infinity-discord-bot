const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('shutdown')
		.setDescription('Shuts down the bot.'),
	async execute(interaction) {
		if (interaction.client.bot.owners().indexOf(`${interaction.member.id}`) >-1 ){
            interaction.defer()
            return interaction.client.destroy()}
		else{ return interaction.reply(`You aren't owner ${interaction.client.bot.owners()}\n${interaction.member.id}`)
        }

	},
};