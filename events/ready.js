const Discord = require("discord.js");
const { MessageEmbed } = require("discord.js");
const logger = require("../utils/logger");
module.exports = {
  name: "ready",
  once: true,
  async execute(client) {
    logger.custom('v'+Discord.version, 'grey', 'discord.js');
    logger.custom(process.version, 'grey', 'Node');
    logger.info(`${client.user.tag}`);
    const channel = client.channels.cache.get("813251835371454515");
    channel.send('`♾️`');
    const logs = client.channels.cache.get("874461656938340402")
    const thread = await logs.threads.fetch("931362898469601351", {archived:true});
    client.log_channel = thread
    if (thread.joinable) await thread.join();
    if (thread.unarchivable && !thread.sendable) await thread.setArchived(false);
    if (!thread.sendable) return logger.log(`Can't send in ${thread}`);
    const embedMsg = new MessageEmbed()
      .setColor("RANDOM")
      .setTitle("Infinity")
      .setFooter({text:`${client.user.tag}`, iconURL:client.user.avatarURL()})
      .addField(
        `<:javascript:882621813291642921> Node version:`,
        "`" + process.version + "`",
        true
      )
      .addField(
        `<:discord:898811517217144882> discord.js version:`,
        "`" + Discord.version + "`",
        true
      )
      .setThumbnail(client.user.avatarURL())
      .setTimestamp();
    client.log_channel.send({ embeds: [embedMsg] });
  },
};
