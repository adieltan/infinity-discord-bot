const Discord = require("discord.js");
const guildSchema = require("./Schema/server.js");
const memberSchema = require("./Schema/Member.js");
const logger = require('../utils/logger');

//Create/find Guilds Database
module.exports.fetchGuild = async function(key){

    let guildDB = await guildSchema.findOne({ _id: key });

    if(guildDB){
        return guildDB;
    }else{
        guildDB = new guildSchema({
            _id: key,
            prefix: '=',
            autoresponse: {},
            autoreact: {}
        })
        await guildDB.save().catch(err => logger.error(err));
        return guildDB;
    }
};

//Create/find Members Database
module.exports.fetchMember = async function(userID){

    let memberDB = await memberSchema.findOne({ id: userID});
    if(memberDB){
        return memberDB;
    }else{
        memberDB = new memberSchema({
            _id: userID,
            weight: 0,
            height: 0,
            bd: 0,
            country: '',
            // bl: false,
            // blreason: '',
            manager: false
        })
        await memberDB.save().catch(err => console.log(err));
        return memberDB;
    };
};