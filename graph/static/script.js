$(document).ready(function(){ 
	// switch interval
    $('#switchInterval').click(function() {

    })
    // user update preference
    $('#userUpdate').click(function() {
    	var temp = $('#userTemperature').val();
        var time = $('#userTime').val();
        console.log(temp + " "+ time);

        $.ajax({
            url: '/updateUser',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
	});
});

