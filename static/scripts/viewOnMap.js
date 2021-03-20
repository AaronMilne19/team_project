function initMap(center) {
    const map = new google.maps.Map(document.getElementById("citymap"), {
      zoom: 12,
      center: center,
    });
    return map;
}

function addMarker(map, lat, lng, name, id){
    var body_format = "<strong>" + name + "</strong>";

    var infowindow = new google.maps.InfoWindow({
        content: body_format,
    });

	var marker = new google.maps.Marker({
        position: {lat: lat, lng: lng},
        map: map,
        title: name,
        locId: id,
        infowindow: infowindow,
    });
    
    marker.addListener("click", () => {
        closeAllInfowindows();
        infowindow.open(map, marker);
    });
    
    return marker;
}

function viewOnMap(id)
{
    let wantedMarker = markers.find(marker => marker.locId == id);
    
    if (wantedMarker != undefined) {
        map.panTo(wantedMarker.position);
        map.setZoom(16);
        closeAllInfowindows();
        wantedMarker.infowindow.open(map, wantedMarker);
    }
}

function closeAllInfowindows(){
    for (marker of markers){
        marker.infowindow.close();
    }
}