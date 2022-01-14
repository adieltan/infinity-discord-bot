const Discord = require("discord.js");
const { MessageEmbed } = require("discord.js");
const logger = require("../utils/logger");
module.exports = {
  name: "messageCreate",
  async execute(message) {
        
    // Get our input arguments
    const args = message.content.split(" ").slice(1);

    // The actual eval command
    if (message.content.startsWith(`eval`)) {

        // If the message author's ID does not equal
        // our ownerID, get outta there!
        if (message.author.id !== "701009836938231849")
        return;

        // In case something fails, we to catch errors
        // in a try/catch block
        try {
        // Evaluate (execute) our input
        const evaled = eval(args.join(" "));

        // Reply in the channel with our result
        message.channel.send(`\`\`\`js\n${evaled}\n\`\`\``);
        } catch (err) {
        // Reply in the channel with our error
        message.channel.send(`\`ERROR\` \`\`\`xl\n${err}\n\`\`\``);
        }

        // End of our command
    }
  },
};
