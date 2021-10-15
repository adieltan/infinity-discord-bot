const {SlashCommandBuilder} = require('@discordjs/builders')

module.exports = {
    data: new SlashCommandBuilder()
    .setName('restart')
    .setDescription('Restarts the bot'),
    async execute(interaction){
        return await interaction.reply(`Restarting...`);
    },
}