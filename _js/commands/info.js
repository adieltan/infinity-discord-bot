const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageActionRow, MessageButton, MessageEmbed } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('startup')
        .setDescription('InfinityJS Startup Info'),
    async execute(interaction) {
        const row = new MessageActionRow()
        const emoji = require('../emoji')
        const { platform, pid } = require("process");
    let os;
    if (platform == "win32") {
      os = "Windows";
    }
    if (platform == "aix") {
      os = "AIX";
    }
    if (platform == "darwin") {
      os = "Darwin";
    }
    if (platform == "freebsd") {
      os = "FreeBSD";
    }
    if (platform == "linux") {
      os = "Linux";
    }
    if (platform == "openbsd") {
      os = "OpenBSD";
    }
    if (platform == "sunos") {
      os = "SunOS";
    }
        const embed = new MessageEmbed()
        .setColor("RANDOM")
      .setTitle("InfinityJS Startup Information")
      .setFooter(
        `Infinity#5345`,
        "https://tynxen.netlify.app/img/infinity_3.png"
      )
.addField( emoji.javascript + " `Node version:`",  '`' + process.version + '`' , true)
.addField(emoji.discord +"`Discord version:`", '`' + Discord.version + '`' , true)
.addField(':desktop:'+ "`Platform:`", '`' + os + '`' , true)
.addField(':placard:'+ "`PID:`", '`' + process.pid + '`' , true)
.addField(emoji.server + '`Hosted on:`',  '`' + process.env.HOST + '`', true)
.setTimestamp()

        return interaction.reply({embeds: [embed]});
    },
};