from flask import Blueprint, jsonify, session, request
from app import db
from app.models.events import EventType, EventDay, Event
from app.models.users import UsersTags, User
from app.models.hunting import StandAssignment, Stand

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/set_hunt_year', methods=['POST'])
def set_hunt_year():
    data = request.get_json()
    hunt_year = data['huntYear']
    session['hunt_year'] = hunt_year
    return jsonify({'success': f'HuntYear is set to {hunt_year}'})

@api.route('/event/get_all_events')
def api_get_events():
    events = Event.query.join(EventType).join(EventDay).all()
    events_data = []
    for event in events:
        for day in event.event_days:
            event_data = {
                "id": event.id,
                "title": event.event_type.name,
                "start": day.date.isoformat(),
                "end": day.date.isoformat()
            }
            if event.is_cancelled:
                event_data["color"] = "red"  # or any color to indicate cancellation
            else:
                if event.event_type.name.lower() == 'älgjakt':
                    event_data["color"] = "blue"
                elif event.event_type.name.lower() == 'årsmöte':
                    event_data["color"] = "green"

            events_data.append(event_data)
            
    return jsonify(events_data)


@api.route('/user/<int:user_id>/<string:action>/<int:tag_id>', methods=['POST'])
def api_handle_user_tag(user_id, action, tag_id):
    try:
        if action == 'add':
            handle_tag = UsersTags(user_id=user_id, tag_id=tag_id)
            db.session.add(handle_tag)
        elif action == 'delete':
            handle_tag = UsersTags.query.filter_by(user_id=user_id, tag_id=tag_id).first()
            if handle_tag:
                db.session.delete(handle_tag)
            else: 
                return jsonify({"error": "Tag not found"}), 404   
        else:
            return jsonify({"error": "Invalid action"}), 400  
        db.session.commit()
        return jsonify({"success": True}), 200
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "An error occured"}), 500
    

@api.route('/hunting/<int:hunt_year_id>/<int:user_id>/assign_stand/<int:stand_number>', methods=['POST'])
def api_assign_stand(hunt_year_id, user_id, stand_number):
    try:
        user = User.query.get(user_id).first()
        if not user:
            raise ValueError("User not found")
        
        stands = Stand.query.filter_by(number=stand_number).all()

        for stand in stands:
            assignment = StandAssignment(user_id=user.id, stand_id=stand.id, hunt_year_id=hunt_year_id)
            db.session.add(assignment)

        db.session.commit()
        return jsonify({"success": True}), 200
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "An error occured"}), 500

# @api.route('/user/', methods=['POST'])
# @api.route('/user/assign_team', methods=['POST'])
# @api.route('/user/assign_team', methods=['POST'])
# @api.route('/user/assign_team', methods=['POST'])