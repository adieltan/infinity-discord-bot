const Discord = require("discord.js");

function noPerms(message, perm) {
    let embed = new Discord.RichEmbed()
        .setAuthor(message.author.username)
        .setTitle("NO PERMS")
        .setColor(config.red)
        .addField("Insufficient permission:", perm);
    message.channel.send(embed).then(m => m.delete(4000));
}

function equalPerms(message, user, perms) {
    let embed = new Discord.RichEmbed()
        .setAuthor(message.author.username)
        .setColor(config.red)
        .setTitle("Error")
        .addField(`${user.user.username} has perms`, perms);
    message.channel.send(embed).then(m => m.delete(4000));  
}

function botuser(message, command) {
    let embed = new Discord.RichEmbed()
        .setTitle("Error")
        .setDescription(`You cannot ${command} a bot!`)
        .setColor(config.red);
    message.channel.send(embed).then(m => m.delete(4000));
} 

function cantfindUser(channel) {
    let embed = new Discord.RichEmbed()
        .setTitle("Error")
        .setDescription("That user was not found!")
        .setColor(config.red);
    channel.send(embed).then(m => m.delete(3000));
}

function noRole(channel) {
    let embed = new Discord.RichEmbed()
        .setTitle("Error")
        .setDescription("That role was not found!")
        .setColor(config.red);
    channel.send(embed).then(m => m.delete(3000));
}

function lack(channel, perm) {
    let embed = new Discord.RichEmbed()
        .setTitle("I DONT HAVE ENOUGH PERMS")
        .setColor(config.red)
        .addField("I do not have the permission", perm);
    channel.send(embed).then(m => m.delete(3000));
}

function notBanned(channel, id) {
    let embed = new Discord.RichEmbed()
        .setTitle("Error")
        .setDescription(`User with the ID ${id} isn't banned.`)
        .setColor(config.red);
    channel.send(embed).then(m => m.delete(3000));
}

module.exports = {
    noPerms,
    equalPerms,
    botuser,
    cantfindUser,
    noRole,
    lack,
    notBanned
}