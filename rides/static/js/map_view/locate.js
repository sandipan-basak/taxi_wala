function initMap() {

    let map;
    const directionsService = new google.maps.DirectionService();
    const directionsRenderer = new google.maps.DirectionsRenderer({suppressMarkers: true});

    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 20.5937, lng: 78.9629 },
        zoom: 4,
    });

    const pl = document.getElementById('pickup_loc')
    const dl = document.getElementById('drop_loc')

    const ac_p = new google.maps.places.Autocomplete(pl);
    const marker_p = new google.maps.Marker({
        map,
        anchorPoint: new google.maps.Point(0, -29),
    
      });

    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8,
      });

    ac_p.addListener("place_changed")
};

function destination() {

}