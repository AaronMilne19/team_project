function initMap(center) {
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: center,
    });
    return map;
}

function addMarker(map, lat, lng, name){
    var body_format = "<strong>" + name + "</strong>";

    var infowindow = new google.maps.InfoWindow({
        content: body_format,
    });

	var marker = new google.maps.Marker({
        position: {lat: lat, lng: lng},
        map: map,
        title: name,
    });
    
    marker.addListener("click", () => {
        infowindow.open(map, marker);
    });
}