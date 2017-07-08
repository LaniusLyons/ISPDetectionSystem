'use strict';
var mongoose = require('../../config/mongoose'),
	Schema = mongoose.Schema;

var schemas = {

	collaboratorSchema : new Schema({
		email : {type : String},
		username : {type : String},
		fk_provider : {type : String},
		lat : {type : Number},
		lon : {type : Number},
		timestamps : { type: Date, default: Date.now }
	}),
	providerSchema : new Schema({
		name : {type : String},
		organizattion : {type : String},
		IP : {type : String},
		lat : {type : Number},
		lon : {type : Number},
		city : {type : String},
		country : {type : String}
	})
};

module.exports = schemas;