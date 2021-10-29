const mongoose = require("mongoose");

module.exports = mongoose.model("server", new mongoose.Schema({
    _id: { type: String },
    prefix: {type: String, default: '='},
    autoresponse: {type: Object, default: {}},
    autoreact: {type: Object, default: {}}
}));