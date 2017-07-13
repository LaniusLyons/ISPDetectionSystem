'use strict';
var mongoose = require('../../config/mongoose'),
	collaboratorSchema = require('./schemas').collaboratorSchema,
	providerSchema = require('./schemas').providerSchema;

var models = {

	Collaborator : mongoose.model('collaborators',collaboratorSchema),
	Provider : mongoose.model('providers',providerSchema)
};

module.exports = models;