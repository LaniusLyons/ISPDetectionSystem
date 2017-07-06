'use strict';
var express = require('express'),
	server = express(),
	port = process.env.PORT || 9000;

/*var server = http.createServer((req,res)=>{
	console.log("making petition to API");
	res.writeHead(200,{'content_type':'text/plain'});
	res.end('IspFinderProjectAPI');
});*/

server.get('/',(req,res)=>{
	res.send('IspFinderProjectAPI');
});

server.listen(port,()=>{
	console.log("API server Ready on port "+port);
});

//var api = require('./apps/api/controllers');
//server.use('/api',api);

require('./routers/urls')(server);