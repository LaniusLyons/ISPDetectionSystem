var map_info, map_users;
      function shareContributionLink(latitude,longitude){
        var link = "#";
        if(latitude && longitude){
          link = "/login/facebook/?coords="+latitude + "," + longitude;
        }
        $(".share-class").attr("href", link);
      }

       $('a[href="#mapa"]').click(function(e) {
            setTimeout(initialise, 500);
       });

       function initialise() {
            var myMap = document.getElementById('map-users');
            google.maps.event.trigger(myMap, 'resize');
       }

       function showMap(is_permite_ubicacion , position )
       {
           var latlng = is_permite_ubicacion ? new google.maps.LatLng( position.coords.latitude, position.coords.longitude ) : {lat: -2.16667, lng: -79.9};
           var infoOptions = {
              zoom:14,
              mapTypeId: google.maps.MapTypeId.ROADMAP,
              center: latlng,
              animation: google.maps.Animation.DROP,
              streetViewControl: false
            };
            var myOptions = {
              zoom:10,
              mapTypeId: google.maps.MapTypeId.ROADMAP,
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
            }else{

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