from flask import Blueprint, jsonify
from app.events.models import EventType, EventDay, Event

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/event/get_all_events')
def api_get_events():
    events = Event.query.join(EventType).join(EventDay).all()
    print(events)
    events_data = []
    for event in events:
        for day in event.event_days:
            events_data.append({
                "id": event.id,
                "title": event.event_type.name,
                "start": day.date.isoformat(),
                "end": day.date.isoformat()
            })
    return jsonify(events_data)