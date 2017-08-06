var map_info, map_users, markers;

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
						$('#isp-markers ul').append("<li class='collection-item dismissable'><i></i><span>Todos</span></li>");
						for(let marker in data.leyenda)
						{
							let j = marker.replace(/ /g, '');
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
			  center: latlng,
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
			   console.log("Browser doesn't support Geolocation");
			}
	  }

	  google.maps.event.addDomListener(window, 'load', initMap);