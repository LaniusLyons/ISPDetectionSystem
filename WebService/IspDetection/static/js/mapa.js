var map_info, map_users;

		  function shareContributionLink(lat,lon){
				if(lat != null && lon != null && ispIP != "" && ispName != ""){
					latitude = lat;
					longitude = lon;
					shareLink = "/login/facebook/?coords="+lat + "," + lon + "&ispIP="+ispIP + "&ispName=" + ispName;
				}
		  }


	   $('a[href="#mapa"]').click(function(e) {
	        var pos;
            var markerIsp;
            var info;

            $.ajax({
                    type: "GET",
                    url: "/getIsp/",
                    dataType: "json",
                    contentType:"text/plain",
                    success: function (data, status) {
                        for(var index in data.isp)
                        {
                            pos = {
                                lat:data.isp[index].latitud,
                                lng:data.isp[index].longitud
                            };

                            markerIsp = new google.maps.Marker({
                                position: pos,
                                map: map_users,
                                draggable: false,
                                icon: url_marker
                            });

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

	   function initialise() {
			var myMap = document.getElementById('map-users');
			google.maps.event.trigger(myMap, 'resize');
	   }

	   function handleEvent(event) {
    		var lat = event.latLng.lat();
    		var lon = event.latLng.lng();
    		if(lat != null && lon != null){
    			latitude = lat;
				longitude = lon;
    		}
		}

	   function showMap(is_permite_ubicacion , position )
	   {
		   var latlng = is_permite_ubicacion ? new google.maps.LatLng( position.coords.latitude, position.coords.longitude ) : {lat: -2.1709978999999997, lng: -79.9223592};
		   var infoOptions = {
			  zoom:14,
			  disableDefaultUI: true,
			  mapTypeControl: false,
			  center: latlng,
			  animation: google.maps.Animation.DROP,
			  streetViewControl: false
			};
			var myOptions = {
			  zoom:14,
			  disableDefaultUI: true,
			  mapTypeControl: false,
			  streetViewControl: false,
			  center: latlng
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
				var marker = new google.maps.Marker({
					position: latlng,
					map: map_info,
					draggable: true,
					icon: url_marker
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
					alert("Informacion de localizacion no disponible");
					break;
				case error.TIMEOUT:
					alert("Tiempo de espera expirado");
					break;
				case error.UNKNOWN_ERROR:
					alert("ERROR DESCONOCIDO");
					break;
			}
	  }

	  function showPosition(position)
	  {
		  showMap(true , position);
	  }

	  function initMap()
	  {
			if (navigator.geolocation)
			{
			   navigator.geolocation.getCurrentPosition(showPosition,showError);
			} else
			{
			   // Browser doesn't support Geolocation
			   console.log("Browser doesn't support Geolocation");
			}
	  }

	  google.maps.event.addDomListener(window, 'load', initMap);