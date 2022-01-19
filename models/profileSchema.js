const mongoose = require("mongoose");

const profileSchema = new mongoose.Schema({
    _id: {type: String, require: true, unique: true},
    weight: { type: Number},
    height: { type: Number},
    bd: { type: Number},
    country: { type: String},
    bio: {type: String},
    manager: {type: Boolean},
    /* Premium */
    premium: {type: Boolean},
    premiumDuration: {type: Number},
    /* Currency */
    bal: {type: Number, default: 0}
});

const model = mongoose.model("profile", profileSchema);
module.exports = model;