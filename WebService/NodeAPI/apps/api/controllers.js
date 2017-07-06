'use strict';
var express = require('express'),
	router = express.Router();

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
		res.send('API GET provider '+provider);
	});

router.post('/collaborators',(req,res)=>{
			res.send('API POST collaborator');
		});

module.exports = router;