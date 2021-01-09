console.log("Our script is running")
    function initMap() {
        console.log("Initialize Map")
        geocoder = new google.maps.Geocoder();
        geocoder.geocode({ 'address': "21816 Lanark St. Canoga Park, CA 91304" }, function (results, status) {
            if (status == 'OK') {
                const map = new google.maps.Map(document.getElementById("map"), {
                    zoom: 10,
                    center: results[0].geometry.location,
                });
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    zoom: 8
                });
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    }