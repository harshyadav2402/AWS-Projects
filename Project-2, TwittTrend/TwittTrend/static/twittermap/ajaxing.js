/**
 * Created by Parteek Khushdil on 20-10-2016.
 */
var searchKeyword;
var locations;
var markers=[];
function initMap() {
        var uluru = {lat: 20, lng: -30};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 3,
          center: uluru
        });
        var marker = new google.maps.Marker({
          position: uluru,
          map: map
        });
        var selectedword=getElementById("ddlSearchWords");
        searchKeyword=selectedword.options[selectedword.selectedIndex].value;
        console.log();
      }

/*$('#listform').on('submit', function(event){
    event.preventDefault();

    $.ajax({
        url : '/',
        type : 'POST',
        data : { Search : $('#ddlSearchWords').val() },

        success : function(json){
            var latit=json.lati;
            var longit=json.longi;

            if(searchKeyword=='Hillary'){
                var marker=new google.maps.Marker({
                    map:map,
                    position:json

                })
                markers.push(marker);

            }

        }
    });
});*/