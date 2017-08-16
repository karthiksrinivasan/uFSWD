// Viewport for Knockout Framework
var KO_View = function () {
    "use strict";
    // Map Center point surrounding Santa Clara
    self.map_point = new google.maps.LatLng(37.330005, -121.950237);
    self.neighbourhood_parks = ko.observableArray([]);
    self.filteredParks = ko.observableArray([]);
    self.searchString = ko.observable("");
    self.initialize = function () {
        $('.error_alert').hide();
        self.infowindow = new google.maps.InfoWindow();
        self.gMap = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: self.map_point
        });
        //Searching of nearby parks to a given location within a specified radius
        var request = {
            location: self.map_point,
            radius: 5000, // Radius of 5kms
            types: ["park"]
        };
        self.gService = new google.maps.places.PlacesService(self.gMap);
        //Searching of nearby parks to a given location within a specified radius
        gService.nearbySearch(request, function(results, status) {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                results.forEach(function(e) {
                    self.generateMarker(e);
                    self.neighbourhood_parks.push(e);
                    self.filteredParks.push(e);
                });
            } else {
                self.errorBox();
            }
        });
    };
    //Shows an error box on the website when Google APIs request fail
    self.errorBox = function() {
        $('.error_alert').show();
    };
    //Creates a Marker item for the Google Maps
    self.generateMarker = function(place) {
        var marker = new google.maps.Marker({
            map: self.gMap,
            position: place.geometry.location,
            place_id: place.place_id,
            icon: "https://maps.google.com/mapfiles/kml/shapes/parks_maps.png"
        });
        place.marker = marker;
        // Adding click event listener for the Marker
        google.maps.event.addListener(marker, "click", self.markerClick);
    };
    // Filtering the parks based on text input
    self.filterParks = function() {
        
        self.filteredParks([]);
        self.neighbourhood_parks().forEach(function(e) {
            if (e.name.toLowerCase().indexOf(self.searchString()) > -1) {
                self.filteredParks.push(e);
                e.marker.setVisible(true);
            } else {
                e.marker.setVisible(false);
            }
        });
    };
    //self.searchString.subscribe(filterParks);
    // Click event function for the list/maps marker
    self.markerClick = function(park) {
        // Differentiating between a click on the marker and on the list
        var currentMarker;
        if (park.marker === undefined) {
            currentMarker = this;
        } else {
            currentMarker = this.marker;
        }
        //Setting animation when clicked on the marker
        currentMarker.setAnimation(google.maps.Animation.BOUNCE);
        //Disabling animation after 1second
        setTimeout(function() {
            currentMarker.setAnimation(null);
        }, 1000);
        //Creating a request for Google Places to retrieve the place information
        var request = {
            placeId: this.place_id
        };
        self.gService.getDetails(request, function(place, status) {
            if (status == google.maps.places.PlacesServiceStatus.OK) {
                //Defining the Marker information window content
                var infowindow_content = "<div>";
                infowindow_content += "<strong><a href='" + place.website + "'>" + place.name + "</a></strong><br>";
                infowindow_content += "Address: " + place.formatted_address + "<br>";
                infowindow_content += "Google Ratings: " + place.rating;
                infowindow_content += "</div>";
                infowindow_content += "<div id='fs_" + place.place_id + "'></div>";
                self.infowindow.setContent(infowindow_content);
                self.infowindow.open(map, currentMarker);
                //Creating a request to Foursquare API
                var request = {
                    ll: "" + place.geometry.location.lat() + "," + place.geometry.location.lng(),
                    client_id: "YXA4XR3NW4WHU2HTWLSQVRWRH0NTXQN2I4ZXH3GZGTVM0BHD",
                    client_secret: "4LYKLG4OFBUVVY4FM144NGME5S33XOHB5V0Q4SNRSXZAWD2Y",
                    v: 20170810,
                    limit: 1
                };
                $.get("https://api.foursquare.com/v2/venues/search", request)
                    .done(function(data) {
                        data = data.response.venues[0];
                        //Adding Foursquare information to information window
                        infowindow_content += "<div>";
                        infowindow_content += "FourSquare CheckIns: " + data.stats.checkinsCount + "<br>";
                        infowindow_content += "FourSquare Users Count: " + data.stats.usersCount;
                        infowindow_content += "</div>";
                    })
                    .fail(function() {
                        //Adding an error statement if foursquare api fails
                        infowindow_content += "<div>";
                        infowindow_content += "Could not reach FourSquare!";
                        infowindow_content += "</div>";

                    })
                    .always(function() {
                        self.infowindow.setContent(infowindow_content);
                        self.infowindow.open(map, currentMarker);
                    });
            } else {
                errorBox();
            }
        });
    };
    //Calling initial function when website window loads
    google.maps.event.addDomListener(window, 'load', function() {
        self.initialize();
    });

};
//Setting up call back function after google apis is initialized
function gMapsCallback() {
    ko.applyBindings(new KO_View());
}
function gMapsError(){
	$('.error_alert').show();
}
//Ajax setup and sliding sidebar setup
$(document).ready(function() {
    $.ajaxSetup({
        timeout: 1000 // in milliseconds
    });
    $("[data-toggle=offcanvas]").click(function() {
        $(".row-offcanvas").toggleClass("active");
    });

});
