'use strict';
var express = require('express'),
	server = express(),
	bodyParser = require('body-parser').json(),
	port = process.env.PORT || 9000;

/*var server = http.createServer((req,res)=>{
	console.log("making petition to API");
	res.writeHead(200,{'content_type':'text/plain'});
	res.end('IspFinderProjectAPI');
});*/

server.listen(port,()=>{
	console.log("API server Ready on port "+port);
});

server.use(bodyParser);

server.get('/',(req,res)=>{
	res.send('IspFinderProjectAPI');
});

//var api = require('./apps/api/controllers');
//server.use('/api',api);

require('./routers/urls')(server);