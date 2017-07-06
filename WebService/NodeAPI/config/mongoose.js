'use strict';
var mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/ispfinderprojectDB');

module.exports = mongoose;