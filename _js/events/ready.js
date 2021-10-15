const logger = require("../utils/logger");
Discord = require("discord.js");
const bot = require("../utils/botData");
const { MessageEmbed } = require("discord.js");
module.exports = {
  name: "ready",
  once: true,
  execute(client) {
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
    logger.info(
      `${client.user.tag}\nNode version: ${process.version}\nDiscord.js version: ${Discord.version}\nPlatform: ${os}\nPID: ${pid}`
    );
    client.user.setPresence({
      activities: [
        {
          name: `${client.guilds.cache.reduce(
            (acc, guild) => acc + guild.memberCount,
            0
          )} users in ${client.guilds.cache.size} guilds.`,
          type: "WATCHING",
        },
      ],
      status: "idle",
    });
    const channel = client.channels.cache.get("813251835371454515");
    channel.send(`∞ ${client.emoji.javascript}`);
    const user = client.users.cache.get("718328210030592031");
    const embedMsg = new MessageEmbed()
      .setColor("RANDOM")
      .setTitle("InfinityJS Startup Information")
      .setFooter(
        `${client.user.tag}`,
        "https://tynxen.netlify.app/img/infinity_3.png"
      )
.addField( client.emoji.javascript + " `Node version:`",  '`' + process.version + '`' , true)
.addField(client.emoji.discord+"`Discord version:`", '`' + Discord.version + '`' , true)
.addField(':desktop:'+ "`Platform:`", '`' + os + '`' , true)
.addField(':placard:'+ "`PID:`", '`' + process.pid + '`' , true)
.setTimestamp()
    user.send({ embeds: [embedMsg] });
  },
};
