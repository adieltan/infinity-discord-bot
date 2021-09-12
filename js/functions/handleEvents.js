module.exports = (client) => {
    client.handleEvents = async (eventfiles, path) => {
        for (const file of eventfiles) {
            const event = require(`${path}/${file}`)
            if (event.once) {
                client.once(event.name, (...args) => event.execute(...args, client));
            } else {
                client.on(event.name, (...args) => event.execute(...args, client));
            }
        }
    }
}