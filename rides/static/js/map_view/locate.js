function initMap() {

    // const directionsService = new google.maps.DirectionService();
    const directionsRenderer = new google.maps.DirectionsRenderer({suppressMarkers: true});

    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 20.5937, lng: 78.9629 },
        zoom: 4,
    });
    directionsRenderer.setMap(map);

    const pl = document.getElementById('pickup_loc')
    
    const dl = document.getElementById('drop_loc')
    
    const ac_p = new google.maps.places.Autocomplete(pl);
    ac_p.bindTo("bounds", map);
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
    let loc;
    ac_p.addListener("place_changed", () => {
      marker_pickup.setVisible(false)
      const place = ac_p.getPlace();
      loc = place;
      if(!place.geometry || !place.geometry.location){
        window.alert("No details available for input: '" + place.name + "'");
        return;
      }
      marker_pickup.setIcon('../images/map_view/sour_m.jpg')
    
      if (place.geometry.viewport) {
        map.fitBounds(place.geometry.viewport);
      } else {
        map.setCenter(place.geometry.location);
        map.setZoom(17);
      }
    });
    ac_p.addListener("place_changed", () => {

      marker_pickup.setVisible(false)
      const place = ac_p.getPlace();
      if(!place.geometry || !place.geometry.location){
        window.alert("No details available for input: '" + place.name + "'");
        return;
      }
      marker_pickup.setIcon('../images/map_view/sour_m.jpg')
    
      if (place.geometry.viewport) {
        map.fitBounds(place.geometry.viewport);
      } else {
        map.setCenter(place.geometry.location);
        map.setZoom(17);
      }
    });
    const ac_d = new google.maps.places.Autocomplete(dl);
    ac_d.setFields([
      "address_components",
      "geometry",
      "icon",
      "name",
    ]);

    ac_d.addListener("place_changed", () => {
      
      marker_drop.setVisible(false)
      const place = ac_d.getPlace();
      if(!place.geometry || !place.geometry.location){
        window.alert("No details available for input: '" + place.name + "'");
        return;
      }
      marker_drop.setIcon('../images/map_view/dest_m1.png')
      const bounds = loc.getBounds();
      
      bounds.extend(place.getBounds())

      map.fitBounds(bounds)
    });

};