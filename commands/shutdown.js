const { SlashCommandBuilder } = require("@discordjs/builders");
var owners = [
  "701009836938231849",
  "703135131459911740",
  "708233854640455740",
  "718328210030592031",
];

module.exports = {
  data: new SlashCommandBuilder()
    .setName("shutdown")
    .setDescription("Shuts down the bot."),
  async execute(interaction) {
    if (owners.indexOf(`${interaction.member.id}`) > -1) {
      await interaction.reply(`Success.`);
      return process.kill(1);
    } else {
      return interaction.reply(
        `You aren't owner\nList of Owners: ${owners}`
      );
    }
  },
};
