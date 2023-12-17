document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: [ 'interaction', 'dayGrid' ],
        defaultView: 'dayGridMonth',
        height: 500,
        firstDay: 1,
        displayEventTime: true,
        events: function(fetchInfo, successCallback, failureCallback) {
            $.ajax({
                url: '/api/event/get_all_events', // Flask route to fetch events
                type: 'GET',
                dataType: 'json',
                success: function(data) {
                    var events = [];
                    data.forEach(function(event) {
                        var startDateTime = event.datetime.start_date + 'T' + event.datetime.start_time
                        var endDateTime = event.datetime.end_date + 'T' + event.datetime.end_date
                        events.push({
                            title: event.title,
                            start: startDateTime,
                            end: endDateTime,
                            color: event.metadata.color
                        });
                    });
                    successCallback(events);
                },
                error: function() {
                    failureCallback();
                }
            });
        },
    });

    calendar.render();
});