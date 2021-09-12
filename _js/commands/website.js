const {SlashCommandBuilder} = require('@discordjs/builders');
const { MessageActionRow, MessageButton, MessageEmbed } = require('discord.js');

module.exports = {
     data: new SlashCommandBuilder()
     .setName('website')
     .setDescription('Responds with the current Tynxen website url'),
     async execute(interaction){
          const row = new MessageActionRow()
          .addComponents(
               new MessageButton()
                    .setStyle('LINK')
                    .setLabel('Website')
                    .setURL(`https://tynxen.netlify.app`),
          );
          return interaction.reply({content:`https://tynxen.netlify.app`,components:[row]})
     }
}