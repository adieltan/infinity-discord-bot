const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('choose')
		.setDescription('Chooses an item between 2 or more choices.')
        .addStringOption((option) => option.setName("1st").setDescription("1st choice to choose from.").setRequired(true))
        .addStringOption((option) => option.setName("2nd").setDescription("2nd choice to choose from.").setRequired(true))
        .addStringOption((option) => option.setName("3rd").setDescription("3rd choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("4th").setDescription("4th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("5th").setDescription("5th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("6th").setDescription("6th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("7th").setDescription("7th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("8th").setDescription("8th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("9th").setDescription("9th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("10th").setDescription("10th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("11th").setDescription("11th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("12th").setDescription("12th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("13th").setDescription("13th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("14th").setDescription("14th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("15th").setDescription("15th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("16th").setDescription("16th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("17th").setDescription("17th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("18th").setDescription("18th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("19th").setDescription("19th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("20th").setDescription("20th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("21th").setDescription("21th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("22th").setDescription("22th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("23th").setDescription("23th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("24th").setDescription("24th choice to choose from.").setRequired(false))
        .addStringOption((option) => option.setName("25th").setDescription("25th choice to choose from.").setRequired(false)),
	async execute(interaction) {
        const options = interaction.options.data.map(x => x.value);
        let item = options[Math.floor(Math.random()*options.length)];

		return await interaction.reply({content:`The chosen item is: ${item}`});
	},
};
