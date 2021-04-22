function initMap() {
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer({
    // suppressMarkers: true
  });
  const pick_src = document.getElementById("pickup_icon").src;
  const drop_src = document.getElementById("drop_icon").src;
  const partner_pos = document.getElementById("partner_pos").src;
  const curr_lat = parseFloat(document.getElementById("lat").value);
  const curr_lng = parseFloat(document.getElementById("lng").value);
  const c_pos = { lat: curr_lat, lng: curr_lng };
  const available = document.getElementById("available").value;
  const map = new google.maps.Map(document.getElementById("map"), {
    center: c_pos,
    zoom: 14,
  });
  directionsRenderer.setMap(map);  
  const mk = new google.maps.Marker({
    map,
    icon: partner_pos,
    position: c_pos,
    anchorPoint: new google.maps.Point(0,-29),
  });
  if (available == "True"){
    const s_pos = {lat: parseFloat(document.getElementById("s_lat").value),
                   lng: parseFloat(document.getElementById("s_lng").value)};
    const d_pos = {lat: parseFloat(document.getElementById("d_lat").value),
                   lng: parseFloat(document.getElementById("d_lng").value)}
    if (document.getElementById("started").value == "True"){
      showDistance(directionsRenderer, directionsService, s_pos, d_pos);
    }
    else{
      // new google.maps.Marker({
      //   map,
      //   icon: drop_src,
      //   postition: s_pos,
      //   anchorPoint: new google.maps.Point(0,-29),
      // });
      console.log(d_pos);
      showDistance(directionsRenderer, directionsService, c_pos, s_pos);
    }
    
  }

};
function showDistance(directionsRenderer, directionsService, sr, ds){
  directionsRenderer.setMap(map);
  directionsService.route(
    {
      origin: sr,
      destination: ds,
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
  
