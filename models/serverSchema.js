const mongoose = require("mongoose");

module.exports = mongoose.model("server", new mongoose.Schema({
    _id: { type: String },
    prefix: {type: String, default: '='},
    autoreact: {type: Object, default: {}},
    tags: {type: Array, default: []},
    premium: {type: Boolean},
    premiumDuration: {type: Number},
    logs: {type: Object, default: {}}

}));