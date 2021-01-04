function initMap() {
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer({suppressMarkers: true});
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 20.5937, lng: 78.9629 },
    zoom: 4,
  });
  directionsRenderer.setMap(map);
  const pickup = document.getElementById("pickup");
  const ac_p = new google.maps.places.Autocomplete(pickup);
  ac_p.bindTo("bounds", map);
  ac_p.setFields([
    "address_components",
    "geometry",
    "icon",
    "name",
  ]);
  const infowindow_p = new google.maps.InfoWindow();
  const infowindowContent_p = document.getElementById("info-content-p");
  infowindow_p.setContent(infowindowContent_p);

  const marker_p = new google.maps.Marker({
    map,
    anchorPoint: new google.maps.Point(0, -29),

  });

  const drop_1 = document.getElementById("drop-1");
  // debugger;
  const ac_d_1 = new google.maps.places.Autocomplete(drop_1);
  ac_d_1.bindTo("bounds", map);

  ac_d_1.setFields([
    "address_components",
    "geometry",
    "icon",
    "name",
  ]);

  const infowindow_d_1 = new google.maps.InfoWindow();
  const infowindowContent_d_1 = document.getElementById("info-content-d-1");
  infowindow_d_1.setContent(infowindowContent_d_1);

  const m_d_1 = new google.maps.Marker({
    map: map,
    anchorPoint: new google.maps.Point(0, -29),
    icon: "https://maps.google.com/mapfiles/marker_green.png",
    // draggable: true,
    // animation: google.maps.Animation.DROP,
  });
  
  ac_p.addListener("place_changed", () => {
    infowindow_p.close();
    marker_p.setVisible(false);
    const place = ac_p.getPlace();

    if (!place.geometry) {
      window.alert(
        "No details available for input: '" + place.name + "'"
      );
      return;
    }

    marker_p.setPosition(place.geometry.location);
    map.setCenter(place.geometry.location);
    map.setZoom(10);
    marker_p.setVisible(true);
    let address = "";

    if (place.address_components) {
      address = [
        (place.address_components[0] &&
          place.address_components[0].short_name) ||
          "",
        (place.address_components[1] &&
          place.address_components[1].short_name) ||
          "",
        (place.address_components[2] &&
          place.address_components[2].short_name) ||
          "",
      ].join(" ");
    }
    infowindowContent_p.children["place-icon"].src = place.icon;
    infowindowContent_p.children["place-name"].textContent = place.name;
    infowindowContent_p.children["place-address"].textContent = address;
    infowindow_p.open(map, marker_p);
    map.setCenter()
  });
 
  ac_d_1.addListener("place_changed", () => {
    infowindow_d_1.close();
    m_d_1.setVisible(false);

    const place_d_1 = ac_d_1.getPlace();
    
    if (!place_d_1.geometry) {
      window.alert(
        "No details available for input: '" + place_d_1.name + "'"
      );
      return;
    }

    m_d_1.setPosition(place_d_1.geometry.location);
    m_d_1.setVisible(true);
    map.setCenter(place_d_1.geometry.location);
    map.setZoom(9);
    let address = "";

    if (place_d_1.address_components) {
      address = [
        (place_d_1.address_components[0] &&
          place_d_1.address_components[0].short_name) ||
          "",
        (place_d_1.address_components[1] &&
          place_d_1.address_components[1].short_name) ||
          "",
        (place_d_1.address_components[2] &&
          place_d_1.address_components[2].short_name) ||
          "",
      ].join(" ");
    }
    infowindowContent_d_1.children["place-icon-d-1"].src = place_d_1.icon;
    infowindowContent_d_1.children["place-name-d-1"].textContent = place_d_1.name;
    infowindowContent_d_1.children["place-address-d-1"].textContent = address;
    infowindow_d_1.open(map, m_d_1);
  });
  const onChangeHandler = function () {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
  };
  if(ac_p && ac_d_1){
    document.getElementById("pickup").addEventListener("change", onChangeHandler);
    document.getElementById("drop-1").addEventListener("change", onChangeHandler);
  }
}



function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  const request = {
    origin: {
      query: document.getElementById("pickup").value,
    },
    destination: {
      query: document.getElementById("drop-1").value,
    },
    travelMode: google.maps.TravelMode.DRIVING,
  }
  directionsService.route(request, (response, status) => {
      if (status === "OK") {
        directionsRenderer.setDirections(response);
      } else {
        window.alert("Directions request failed due to " + status);
      }
    }
  );
}