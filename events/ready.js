const Discord = require("discord.js");
const { MessageEmbed } = require("discord.js");
module.exports = {
  name: "ready",
  once: true,
  execute(client) {
    console.log(
      `${client.user.tag}\nNode version: ${process.version}\nDiscord.js version: ${Discord.version}`
    );
    client.user.setPresence({
      activities: [
        {
          name: `with Infinity`,
          type: "PLAYING",
        },
      ],
      status: "dnd",
    });
    const channel = client.channels.cache.get("813251835371454515");
    client.log_channel = client.channels.cache.get('874461656938340402')
    channel.send(`∞`);
    const embedMsg = new MessageEmbed()
      .setColor("RANDOM")
      .setTitle("Infinity")
      .setFooter(
        `${client.user.tag}`,
        client.user.avatarURL()
      )
      .addField(`<:javascript:882621813291642921> Node version:`,
        "`" + process.version + "`",
        true
      )
      .addField(`<:discord:898811517217144882> discord.js version:`,
        "`" + Discord.version + "`",
        true
      )
      .setThumbnail(client.user.avatarURL())
      .setTimestamp();
    client.log_channel.send({ embeds: [embedMsg] });
  },
};
