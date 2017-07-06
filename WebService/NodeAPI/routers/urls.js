'use strict';
var apiRouter = require('../apps/api/controllers');

var routers = (server)=>{
	server.use('/api',apiRouter);
};

module.exports = routers;