function initMap(center) {
    return new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: center,
    });
}

function addMarker(map, lat, lng, name, id){
    // 26/3/2021 TODO for Ben: readjust zoom of the map component based on the contained markers
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
    
    document.getElementById('map-container').scrollIntoView();
}

function closeAllInfowindows(){
    for (marker of markers){
        marker.infowindow.close();
    }
}