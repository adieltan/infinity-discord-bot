module.exports = (client) => {
    client.handleCommands = async (commandFolders, path) => {
        client.CommandArray = [];
        for (folder of commandFolders) {
            const commandFiles = fs.readdirSync(`${path}/${folder}`).filter(file => file.endsWith('.js'));
            for (const file of commandFiles) { 
                const command = require(`${path}/${folder}/${file}`);
                client.commands.set(command.data.name, command);
                client.CommandArray.push(command.data.toJson());
            }

        }
    };
};