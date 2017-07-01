var map_info, map_users;

       $('a[href="#mapa"]').click(function(e) {
            setTimeout(initialise, 500);
       });

       function initialise() {
            var myMap = document.getElementById('map-users');
            google.maps.event.trigger(myMap, 'resize');
       }

      function showError(error)
      {
            switch (error.code)
            {
                case error.PERMISSION_DENIED:
                    alert("El requerimiento negado por el usuario");
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
            // Create a Google coordinate object for where to center the map
            var latlng = new google.maps.LatLng( position.coords.latitude, position.coords.longitude );
            var infoOptions = {
              zoom:12,
              mapTypeId: google.maps.MapTypeId.ROADMAP,
              center: latlng,
              draggable: true
            };
            var myOptions = {
              zoom:10,
              mapTypeId: google.maps.MapTypeId.ROADMAP,
              center: latlng
            };
            map_info = new google.maps.Map(document.getElementById("map-info"), infoOptions);
            map_info.mapTypes.set('styled_map', styledMap);
            map_info.setMapTypeId('styled_map');
            map_users = new google.maps.Map(document.getElementById("map-users"), myOptions);
            map_users.mapTypes.set('styled_map', styledMap);
            map_users.setMapTypeId('styled_map');
            var marker = new google.maps.Marker({
                position: latlng,
                map: map_info,
                icon: 'http://m.schuepfen.ch/icons/helveticons/black/60/Pin-location.png'
            });
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