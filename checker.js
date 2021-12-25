const logger = require('./utils/logger')
const nodeMajorVersion = parseInt(process.versions.node.split('.')[0, 10]); // Get the Node version

if (nodeMajorVersion < 10) { //This bot only works with a version 10 of Node.js/higher. So, stop running if this is the case 
    logger.custom(`Version ${nodeMajorVersion} is an unsupported Node.JS version. Please install and use Node.JS 10 or newer.`, 'yellow', 'Check:Failed');
    process.exit(1);
}

const { accessSync } = require('fs')
const path = require('path')

try {
    accessSync(path.join(__dirname, './.', 'node_modules')); //Check if node_modules folder exists
} catch (err) {
    logger.custom('Please install all dependencies before starting the bot, the node_modules directory was not found.', 'yellow', 'Check:Failed');
    process.exit(1);
}


try {
    const packageJson = require('./package.json');
    const modules = Object.keys(packageJson.dependencies);
    //These are names of all the modules
    modules.forEach(mod => {
        accessSync(path.join(__dirname, './', 'node_modules', mod))
    })
}
//For each of these modules, check if they exist in the node_modules folder.
catch (err) {
    logger.custom('It appears that you have a missing package, do npm install.', 'yellow', 'Check:Failed');
    process.exit(1)
}
logger.custom('You have all the required modules installed!', 'green', 'Check') //Let the user know they're good to go!