module.exports = {
	name: 'messageCreate',
	async execute(message) {
		function getPrefix(guildid) {
			return `=`;
		}

		if (message.guild) prefix = getPrefix(message.guild.id)
		if (!message.author.id === 701009836938231849) return;
	
		let args = message.content.slice(prefix.length).split(' ');
		if (!message.content.startsWith(prefix) && message.guild) return;
		const command = message.client.mcommands.get(args[0].toLowerCase())
		if (!command) return;

		try {
			message = await command.execute(message);
			message.react(`${message.client.emoji.javascript}`)
			.catch(console.error);
		} catch (error) {
			console.error(error);
			await message.reply({content:'There was an error while executing this command!'})
		}
		if (message.content === '玩不起'){
			message.reply({
				content: '挖槽 挖槽 你搞偷袭 你玩不起 你没有实力啊你 你都不敢跟我正面儿对抗 你玩儿个屁'
			})
		};
		if (message.content ==='testing'){
			let leaderboard =  await amari.getGuildLeaderboard(`${message.guild.id}`)
			message.reply({content:`${JSON.stringify(leaderboard.data,null,2)}`})}
		}
};