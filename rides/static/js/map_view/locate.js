function initMap() {

  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer({
    suppressMarkers: true
  });
  const map_element = document.getElementById("map");
  const map = new google.maps.Map(map_element, {
      center: { lat: 20.5937, lng: 78.9629 },
      zoom: 4,
  });
  map_element.style.display = "none";
  directionsRenderer.setMap(map);  

  const pl = document.getElementById('pickup_loc');
  const dl = document.getElementById('drop_loc');
  const pick_src = document.getElementById("pickup_icon").src;
  const drop_src = document.getElementById("drop_icon").src;
  const ac_p = new google.maps.places.Autocomplete(pl);
  // ac_p.bindTo("bounds", map);
  ac_p.setFields([
    "address_components",
    "geometry",
    "icon",
    "name",
  ]);
  const marker_pickup = new google.maps.Marker({
    map,
    anchorPoint: new google.maps.Point(0,-29),
  });
  const marker_drop = new google.maps.Marker({
    map,
    anchorPoint: new google.maps.Point(0,-29),
  });
  // let loc;
  // let bounds;
  ac_p.addListener("place_changed", () => {
    marker_pickup.setVisible(false);
    const place = ac_p.getPlace();
    // bounds = new google.maps.LatLngBounds();
    // bounds.extend(place.latLng);
    // loc = place;
    map_element.style.display = "block";
    if(!place.geometry || !place.geometry.location){
      window.alert("No details available for input: '" + place.name + "'");
      return;
    }
    // debugger;
    console.log(pick_src);
    marker_pickup.setIcon(pick_src);
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);
    }
    // marker_pickup.setMap(map);
    marker_pickup.setPosition(place.geometry.location);
    marker_pickup.setVisible(true);
  });

  const ac_d = new google.maps.places.Autocomplete(dl);
  ac_d.setFields([
    "address_components",
    "geometry",
    "icon",
    "name",
  ]);

  ac_d.addListener("place_changed", () => {
    marker_drop.setVisible(false);
    const place = ac_d.getPlace();
    if(!place.geometry || !place.geometry.location){
      window.alert("No details available for input: '" + place.name + "'");
      return;
    }
    // bounds = new google.maps.LatLngBounds();
    marker_drop.setIcon(drop_src);
    // debugger;
    // const bounds = loc.getBounds();
    // bounds.extend(place.getBounds());
    calculateAndDisplayRoute(directionsService, directionsRenderer);
    marker_drop.setPosition(place.geometry.location);
    marker_drop.setVisible(true);
    // map.fitBounds(bounds);
    // bounds = new google.maps.LatLngBounds();
  });

};

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  directionsService.route(
    {
      origin: {
        query: document.getElementById("pickup_loc").value,
      },
      destination: {
        query: document.getElementById("drop_loc").value,
      },
      travelMode: google.maps.TravelMode.DRIVING,
    },
    (response, status) => {
      if (status === "OK") {
        directionsRenderer.setDirections(response);
      } else {
        window.alert("Directions request failed due to " + status);
      }
    }
  );
}


// function handleLocationError(browserHasGeolocation, pos) {
//   infoWindow.setPosition(pos);
//   infoWindow.setContent(
//     browserHasGeolocation
//       ? "Error: The Geolocation service failed."
//       : "Error: Your browser doesn't support geolocation."
//   );
//   infoWindow.open(map);
// }

// function show_map(){
//   const elem = document.getElementById("map");
//   const contianer = document.getElementById("map_container");

//   // elem.style.overflow = visible
// }