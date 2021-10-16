const {SlashCommandBuilder} = require('@discordjs/builders')
const permissions = [
    {
        id: ['701009836938231849','718328210030592031'],
        type: 'USER',
        permission: true,
    },
];

module.exports = {
    data: new SlashCommandBuilder()
    .setName('restart')
    .setDescription('Restarts the bot'),
    async execute(interaction){
        await command.permissions.set({ permissions });
        return await interaction.reply(`Restarting...`);
        
    },
}