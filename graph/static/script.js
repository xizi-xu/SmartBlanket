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
    	var temp = $('#userTemperature').val();
        var time = $('#userTime').val();
        if ($('#saveSetting').is(":checked")) {
        	console.log("user wants to save current config");
        }
        console.log("set " + temp + "F at "+ time);
	});
});

