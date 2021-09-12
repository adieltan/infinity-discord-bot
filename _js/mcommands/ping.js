module.exports = {
    data : {name:'ping', description:'Latency (delay time) of the bot.'},
    async execute(message) {
        return await message.reply(`${Math.round(message.client.ws.ping)} ms`)
    }
}