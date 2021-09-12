const mongoose = require("mongoose");

module.exports = mongoose.model("profile", new mongoose.Schema({
    _id: { type: String },
    weight: { type: Number, default: 0},
    height: { type: Number, default: 0},
    bd: { type: Number, default: 0},
    country: { type: String, default: ''},
    bl: {type: Boolean, default: false},
    blreason: {type: String, default: ''},
    manager: {type: Boolean, default: false}
}));