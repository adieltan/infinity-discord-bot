const mongoose = require("mongoose");

const profileSchema = new mongoose.Schema({
    _id: {type: String, require: true, unique: true},
    weight: { type: Number},
    height: { type: Number},
    bd: { type: Number},
    country: { type: String},
    bio: {type: String},
    bl: {type: Boolean},
    blreason: {type: String},
    manager: {type: Boolean},
    premium: {type: Boolean/Number},
});

const model = mongoose.model("profile", profileSchema);
module.exports = model;