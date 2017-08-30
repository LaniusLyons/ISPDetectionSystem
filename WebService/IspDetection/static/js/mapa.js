var map_info, map_users, markers;
var navigators = {
  "Chrome": 50,
  "Firefox": 35,
  "MSIE": 9,
  "Opera": 10.6,
  "Safari": 5
};

		  function shareContributionLink(lat,lon){
				if(lat != null && lon != null && ispIP != "" && ispName != ""){
					latitude = lat;
					longitude = lon;
					shareLink = "/posting/?coords="+lat + "," + lon + "&ispIP="+ispIP + "&ispName=" + ispName;
				}
		  }

	   $('a[href="#consultar"]').click(function(){
			$('#isp-markers ul').empty();
			if(markers !== undefined){
				for(let isp_name in markers ){
					ShowAndHideMarkers(isp_name);
				}
				markers = [];
			}
	   });

	   $('a[href="#mapa"]').click(function(e) {
			var pos;
			var markerIsp;
			if( $('#isp-markers ul').children().length > 0 ) return;
			$.ajax({
					type: "GET",
					url: "/getIsp/",
					dataType: "json",
					contentType:"text/plain",
					success: function (data, status) {
						markers = [];
						$('#isp-markers ul').append("<li class='collection-item dismissable active'><i></i><span>Todos</span></li>");
						for(let marker in data.leyenda)
						{
							let j = marker.replace(/ /g, '').replace(/[&\/\\#,+()$~%\.'":*?<>{}]/g,'');
							markers[marker] = new Array();
							$('#isp-markers ul').append("<li class='collection-item dismissable'><i id='"+j+"'></i><span>"+marker+"</span></li>");

							let styles = {
							  cursor : "pointer"
							};
							$("#isp-markers ul li").css(styles);
							$("#isp-markers ul li i#" + j).css("content","url("+data.leyenda[marker]+")");
						}

						for(let index in data.isp)
						{
							pos = {
								lat:data.isp[index].latitud,
								lng:data.isp[index].longitud
							};
							markerIsp = new google.maps.Marker({
								position: pos,
								map: map_users,
								draggable: false,
								icon: data.leyenda[data.isp[index].isp]
							});
							markers[data.isp[index].isp].push(markerIsp);
							(function(marker, ispName) {
								// add click event
								google.maps.event.addListener(marker, 'click', function() {
									infowindow = new google.maps.InfoWindow({
										content: ispName
									});
									infowindow.open(map_users, marker);
								});
							})(markerIsp, data.isp[index].isp);
						}
					},
					error:function () {
						console.log('Error');
					}
				});
			setTimeout(initialise, 500);
	   });

	   function ShowAndHideMarkers(isp_name , mapa = null)
	   {//si mapa es null entonces hace un hide, else hace un show

			let array_isp = markers[isp_name];
			if(array_isp)
			{
				$.each(array_isp , function (k,v) {
					v.setMap(mapa);
				});
			}else
				console.log("no se encontro el index "+isp_name+" en markers");
	   }

	   $(document).on("touchstart click" , "#isp-markers ul li" , function () {
			$('ul li').removeClass("active");
			$(this).addClass("active");
			let isp_name_selected = $(this).children('span')[0].innerHTML;
			if(isp_name_selected === "Todos")
			{
				$("#isp-markers ul li").each(function (index,element) {
					let isp_name = $(element)[0].innerText;
					if(isp_name !== "Todos")
						ShowAndHideMarkers(isp_name,map_users);
				});
			}else
			{
				$("#isp-markers ul li").each(function (index,element) {
					let isp_name = $(element)[0].innerText;
					if(isp_name !== "Todos"){
						if(isp_name_selected === isp_name)
							ShowAndHideMarkers(isp_name_selected,map_users);
						else
							ShowAndHideMarkers(isp_name);
					}
				});
			}
	   });

	   function initialise() {
			let myMap = document.getElementById('map-users');
			google.maps.event.trigger(myMap, 'resize');
	   }

	   function handleEvent(event) {
			let lat = event.latLng.lat();
			let lon = event.latLng.lng();
			if(lat != null && lon != null){
				latitude = lat;
				longitude = lon;
			}
		}

	   function showMap(is_permite_ubicacion , position )
	   {
		   let latlng = is_permite_ubicacion ? new google.maps.LatLng( position.coords.latitude, position.coords.longitude ) : {lat: -2.172712, lng: -80.018234};
		   let infoOptions = {
			  zoom:14,
			  disableDefaultUI: false,
			  mapTypeControl: false,
			  center: latlng,
			  streetViewControl: false
		   };
		   let myOptions = {
			  zoom:12,
			  disableDefaultUI: false,
			  mapTypeControl: false,
			  center: {lat: -2.037534, lng: -80.082092},
			   streetViewControl: false
			};
			map_info = new google.maps.Map(document.getElementById("map-info"), infoOptions);
			map_info.mapTypes.set('styled_map', styledMap);
			map_info.setMapTypeId('styled_map');
			map_users = new google.maps.Map(document.getElementById("map-users"), myOptions);
			map_users.mapTypes.set('styled_map', styledMap);
			map_users.setMapTypeId('styled_map');
			if(is_permite_ubicacion)
			{
				shareContributionLink(position.coords.latitude,position.coords.longitude);
				showToast(showToastMessage);
				let marker = new google.maps.Marker({
					position: latlng,
					map: map_info,
					draggable: true,
					icon: "static/img/location.png"
					});
				marker.addListener('drag', handleEvent);
				marker.addListener('dragend', handleEvent);

			}else{
				console.log("no ha aceptado la ubicacion");
			}
	   }

	   function showToast(toastMessage) {
		   if(toastMessage)
		   {
			   var $toastContent = $('<span>Hemos localizado tu ubicación <br> Asegurate moviendo el marcador al lugar exacto donde te encuentras</span>');
			   Materialize.toast($toastContent, 5000, 'rounded');
		   }
	   }
	  function showError(error)
	  {
			switch (error.code)
			{
				case error.PERMISSION_DENIED:
					//alert("El requerimiento negado por el usuario");
					$('#modal1').modal('open');
					showMap(false);
					$('#compartir-facebook').css("display","none");
					break;
				case error.POSITION_UNAVAILABLE:
					swal('Error','Se recomienda utilziar el navegador de Google Chrome','info');
					//alert("Informacion de localizacion no disponible");
					break;
				case error.TIMEOUT:
					swal('','iempo de espera expirado','info');
					//alert("Tiempo de espera expirado");
					break;
				case error.UNKNOWN_ERROR:
					swal('','Error desconocido, contacte con el administrador','info');
					//alert("ERROR DESCONOCIDO");
					break;
			}
	  }

	  function showPosition(position)
	  {
		  showMap(true , position);
	  }

	  function loadJSON(file, callback) {
			var xobj = new XMLHttpRequest();
			xobj.overrideMimeType("application/json");
			xobj.open('GET', file, true); // Replace 'my_data' with the path to your file
			xobj.onreadystatechange = function () {
				  if (xobj.readyState == 4 && xobj.status == "200") {
					// Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
					callback(xobj.responseText);
				  }
			};
			xobj.send(null);
	  }

	  function detectarBrowser(){
			let nAgt = navigator.userAgent;
			let browserName  = navigator.appName;
			let fullVersion  = ''+parseFloat(navigator.appVersion);
			let majorVersion = parseInt(navigator.appVersion,10);
			let nameOffset,verOffset,ix;

			// In Opera 15+, the true version is after "OPR/"
			if ((verOffset=nAgt.indexOf("OPR/"))!=-1) {
			 browserName = "Opera";
			 fullVersion = nAgt.substring(verOffset+4);
			}
			// In older Opera, the true version is after "Opera" or after "Version"
			else if ((verOffset=nAgt.indexOf("Opera"))!=-1) {
			 browserName = "Opera";
			 fullVersion = nAgt.substring(verOffset+6);
			 if ((verOffset=nAgt.indexOf("Version"))!=-1)
			   fullVersion = nAgt.substring(verOffset+8);
			}
			// In MSIE, the true version is after "MSIE" in userAgent
			else if ((verOffset=nAgt.indexOf("MSIE"))!=-1) {
			 browserName = "Microsoft Internet Explorer";
			 fullVersion = nAgt.substring(verOffset+5);
			}
			// In Chrome, the true version is after "Chrome"
			else if ((verOffset=nAgt.indexOf("Chrome"))!=-1) {
			 browserName = "Chrome";
			 fullVersion = nAgt.substring(verOffset+7);
			}
			// In Safari, the true version is after "Safari" or after "Version"
			else if ((verOffset=nAgt.indexOf("Safari"))!=-1) {
			 browserName = "Safari";
			 fullVersion = nAgt.substring(verOffset+7);
			 if ((verOffset=nAgt.indexOf("Version"))!=-1)
			   fullVersion = nAgt.substring(verOffset+8);
			}
			// In Firefox, the true version is after "Firefox"
			else if ((verOffset=nAgt.indexOf("Firefox"))!=-1) {
			 browserName = "Firefox";
			 fullVersion = nAgt.substring(verOffset+8);
			}
			// In most other browsers, "name/version" is at the end of userAgent
			else if ( (nameOffset=nAgt.lastIndexOf(' ')+1) <
					  (verOffset=nAgt.lastIndexOf('/')) )
			{
			 browserName = nAgt.substring(nameOffset,verOffset);
			 fullVersion = nAgt.substring(verOffset+1);
			 if (browserName.toLowerCase()==browserName.toUpperCase()) {
			  browserName = navigator.appName;
			 }
			}
			// trim the fullVersion string at semicolon/space if present
			if ((ix=fullVersion.indexOf(";"))!=-1)
			   fullVersion=fullVersion.substring(0,ix);
			if ((ix=fullVersion.indexOf(" "))!=-1)
			   fullVersion=fullVersion.substring(0,ix);

			majorVersion = parseInt(''+fullVersion,10);
			if (isNaN(majorVersion)) {
			 fullVersion  = ''+parseFloat(navigator.appVersion);
			 majorVersion = parseInt(navigator.appVersion,10);
			}
			let version = Number(navigators[browserName]);
			if( fullVersion < version )
			{
				swal('Error','Actualiza el navegador a una version nueva...','info');
			}
	  }

	  function initMap()
	  {
			detectarBrowser();
			if (navigator.geolocation)
			{
			   navigator.geolocation.getCurrentPosition(showPosition,showError);
			} else
			{
			   console.log("Browser doesn't support Geolocation");
			}
	  }

	  google.maps.event.addDomListener(window, 'load', initMap);