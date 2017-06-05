function showAllWayPoints(){
//   var x = 5;
//   var y = 6;
//   var z = 6+5;
//
// console.log(z);

var locations = [
     ['Bondi Beach', -33.890542, 151.274856, 4],
     ['Coogee Beach', -33.923036, 151.259052, 5],
     ['Cronulla Beach', -34.028249, 151.157507, 3],
     ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
     ['Maroubra Beach', -33.950198, 151.259302, 1]
   ];

// define the location from the dictionary
var waypointByID = {};
   {% for waypoint in waypoints %}
   waypointByID[{{waypoint.id}}] = {
       name: "{{waypoint.name}}",
       lat: {{waypoint.geometry.y}},
       lng: {{waypoint.geometry.x}}
   };
   console.log(waypointByID[waypoint.id]['name'])

   {% endfor %}

   var map = new google.maps.Map(document.getElementById('map'), {
     zoom: 10,
     center: new google.maps.LatLng(-33.92, 151.25),
     mapTypeId: google.maps.MapTypeId.ROADMAP
   });

   var key,value,waypoint;
   var marker;


  //  {% for key, value in waypointByID.items() %}
  //  waypoint = waypointByID[key];
   //
  //   marker = new google.maps.Marker({
  //    position: new google.maps.LatLng(waypoint.lat, waypoint.lng),
  //    map: map
   //
  //  {% endfor %}

   $('.waypoint').each(function () {
            this = $(this);
           var waypoint = waypointByID[this];
           var center = new google.maps.LatLng(waypoint.lat, waypoint.lng);
           if (marker) marker.setMap();
           marker = new google.maps.Marker({map: map, position: center});
           map.panTo(center);

   });

   var infowindow = new google.maps.InfoWindow();

  //  var marker, i;
   //
  //  for (i = 0; i < locations.length; i++) {
  //    marker = new google.maps.Marker({
  //      position: new google.maps.LatLng(locations[i][1], locations[i][2]),
  //      map: map
   //
  //    });


     google.maps.event.addListener(marker, 'mouseover', (function(marker, i) {
       return function() {
         infowindow.setContent(locations[i][0]);
         infowindow.open(map, marker);
       }
     })(marker, i));
   }

}


document.getElementById('btn').onclick = function() {
  showAllWayPoints()

};

<script type="text/javascript" src="{% static "js/all.js" %}"></script>
