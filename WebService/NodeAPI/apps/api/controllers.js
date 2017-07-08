'use strict';
var express = require('express'),
	router = express.Router(),
	request = require("request"),
	Collaborator = require('./models').Collaborator,
	Provider = require('./models').Provider;

var http = require('http');

// middleware that is specific to this router
router.use(function timeLog(req, res, next) {
  console.log('Time: ', Date.now());
  next();
});

router.get('/collaborators',(req,res)=>{
		res.send('API GET collaborator');
	});

router.get('/providers',(req,res)=>{
		res.send('API GET provider');
	});

router.get('/collaborators/:collaborator',(req,res)=>{
		var collaborator = req.params.collaborator;
		res.send('API GET collaborator '+collaborator);
	});

router.get('/providers/:provider',(req,res)=>{
		var provider = req.params.provider;
		if(provider.length){
			request('http://ip-api.com/json/'+provider, function(error, response, body) {
  				var jsonObject = JSON.parse(body);
  				res.json({'data':jsonObject});
			});
		}
	});

router.post('/collaborators',(req,res)=>{
		var email = req.body.email;
		var username = req.body.username;
		var fk_provider = req.body.fk_provider;
		var lat = req.body.lat;
		var lon = req.body.lon;

		var collaborator = new Collaborator({
			email : email,
			username : username,
			fk_provider : fk_provider,
			lat : lat,
			lon : lon
		});
		collaborator.save((error)=>{
			if(error){
				res.json({'message':'Error al guardar datos '+error});
			}else{
				res.json({'message':'Datos compartidos exitosamente'});
			}
		});
	});


module.exports = router;