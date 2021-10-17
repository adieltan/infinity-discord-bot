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
                    .setLabel('Home')
                    .setURL(`https://tynxen.netlify.app`),

                    new MessageButton()
                    .setStyle('LINK')
                    .setLabel('Privacy')
                    .setURL('https://tynxen.netlify.app/privacy'),

                    new MessageButton()
                    .setStyle('LINK')
                    .setLabel('Terms')
                    .setURL('https://tynxen.netlify.app/terms'),

                    new MessageButton()
                    .setStyle('LINK')
                    .setLabel('Bot')
                    .setURL('https://tynxen.netlify.app/bot'),
    
                    new MessageButton()
                    .setStyle('LINK')
                    .setLabel('Team')
                    .setURL('https://tynxen.netlify.app/team'),

          );
          return interaction.reply({content:'Tynxen',components:[row]})
     }
}