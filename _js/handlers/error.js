const logger = require('../utils/logger')
const nodeMajorVersion = parseInt(process.versions.node.split('.')[0, 10]); // Get the Node version

if (nodeMajorVersion < 10) { //This bot only works with a version 10 of Node.js/higher. So, stop running if this is the case 
    logger.warn(`Version ${nodeMajorVersion} is an unsupported Node.JS version. Please install and use Node.JS 10 or newer.`);
    process.exit(1);
}

const { accessSync } = require('fs')
const path = require('path')

try {
    accessSync(path.join(__dirname, '..', 'node_modules')); //Check if node_modules folder exists
} catch (err) {
    logger.warn('Please install all dependencies before starting the bot, the node_modules directory was not found.');
    process.exit(1);
}

//* Error Handler
process.on('uncaughtExeption', err => {
    logger.error(err)
    process.exit(1)
})

try {
    const packageJson = require('../package.json');
    const modules = Object.keys(packageJson.dependencies);
    //These are names of all the modules
    modules.forEach(mod => {
        accessSync(path.join(__dirname, '..', node_modules, mod))
    })
}
//For each of these modules, check if they exist in the node_modules folder.
catch (err) {
    logger.warn('It appears that you have a missing package, do npm install.');
    process.exit(1)
}

logger.info('You have all the required modules installed!') //Let the user know they're good to go!