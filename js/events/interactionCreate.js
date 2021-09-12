module.exports = {
	name: 'interactionCreate',
	async execute(interaction) {
		if (!interaction.isCommand()) return;

		const command = interaction.client.commands.get(interaction.commandName);

		if (!command) return;

		try {
			reply = await command.execute(interaction);
		} catch (error) {
			console.error(error);
			await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
		}
		const channel = interaction.client.channels.cache.get('874461656938340402');
		channel.send(`${interaction.user.tag} in <#${interaction.channel.id}> triggered an interaction.`);
	},
};