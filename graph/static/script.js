$(document).ready(function(){ 
	// switch graphs
	var is_graph_15_shown = true;
	$('#graph1').hide();
    $('#switchInterval').click(function() {
	    if (is_graph_15_shown == true) {
        	$('#graph15').hide();
        	$('#graph1').show();
        	is_graph_15_shown = false;
        } else {
        	$('#graph15').show();
        	$('#graph1').hide();
        	is_graph_15_shown = true;
        }
    })
    
    // user update preference
    $('#userUpdate').click(function() {
    	var temp1 = $('#userTemperature1').val();
        var temp2 = $('#userTemperature2').val();
        var temp3 = $('#userTemperature3').val();
        var temp4 = $('#userTemperature4').val();
        var setTime = $('#userTime').val();
        if ($('#saveSetting').is(":checked")) {
            alert("Your preference is saved!")
        }
        var result = {
            time: setTime,
            prefs: [temp1, temp2, temp3, temp4]
        }
        console.log(result);
	});
});

