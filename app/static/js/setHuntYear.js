$(document).ready(function() {
    $('#huntYearDropdown').on('change', function() {
        var selectedYear = $(this).val();
        
        $.ajax({
            url: '/api/set_hunt_year',  // Flask route that handles setting the hunt year
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ huntYear: selectedYear }),
            success: function(response) {
                console.log('Hunt year set successfully');
                location.reload();
            },
            error: function(error) {
                console.error('Error setting hunt year', error);
            }
        });
    });
});