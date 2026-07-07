from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import datetime
from ..models import db, Event, Seat

def is_organizer():
    claims = get_jwt()
    return claims.get('role') == 'organizer'

class EventListResource(Resource):
    @jwt_required()
    def get(self):
        # Users see all events, organizers see only theirs if we want, but let's just return all for browsing
        # Filter can be applied via query params if needed
        events = Event.query.all()
        result = []
        for e in events:
            result.append({
                'id': e.id,
                'organizer_id': e.organizer_id,
                'name': e.name,
                'venue': e.venue,
                'date': e.date.isoformat(),
                'time': e.time.isoformat(),
                'price': e.price,
                'total_seats': e.total_seats
            })
        return {'message': 'Events retrieved', 'data': result}, 200

    @jwt_required()
    def post(self):
        if not is_organizer():
            return {'message': 'Organizer access required'}, 403
            
        data = request.get_json()
        organizer_id = get_jwt_identity()

        # Parse date and time
        try:
            event_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
            event_time = datetime.strptime(data.get('time'), '%H:%M').time()
        except (ValueError, TypeError):
            return {'message': 'Invalid date/time format. Use YYYY-MM-DD and HH:MM'}, 400

        total_seats = int(data.get('total_seats', 0))

        event = Event(
            organizer_id=organizer_id,
            name=data.get('name'),
            venue=data.get('venue'),
            date=event_date,
            time=event_time,
            price=float(data.get('price', 0.0)),
            total_seats=total_seats
        )
        db.session.add(event)
        db.session.commit() # commit to get event.id

        # Generate seat grid (e.g., A1, A2, B1...)
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        seats_per_row = total_seats // len(rows)
        if seats_per_row == 0:
            seats_per_row = total_seats
            rows = ['A']

        seat_objects = []
        seat_count = 0
        for r in rows:
            for n in range(1, seats_per_row + 1):
                if seat_count >= total_seats:
                    break
                seat_objects.append(Seat(event_id=event.id, row=r, number=n))
                seat_count += 1
            if seat_count >= total_seats:
                break
                
        db.session.bulk_save_objects(seat_objects)
        db.session.commit()

        return {'message': 'Event created successfully', 'data': {'id': event.id}}, 201

class EventResource(Resource):
    @jwt_required()
    def get(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404
            
        return {
            'message': 'Event retrieved',
            'data': {
                'id': event.id,
                'name': event.name,
                'venue': event.venue,
                'date': event.date.isoformat(),
                'time': event.time.isoformat(),
                'price': event.price,
                'total_seats': event.total_seats
            }
        }, 200

    @jwt_required()
    def delete(self, event_id):
        if not is_organizer():
            return {'message': 'Organizer access required'}, 403
            
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 404
            
        if event.organizer_id != get_jwt_identity():
            return {'message': 'Unauthorized to delete this event'}, 403

        db.session.delete(event)
        db.session.commit()
        return {'message': 'Event deleted successfully'}, 200

class SeatListResource(Resource):
    @jwt_required()
    def get(self, event_id):
        seats = Seat.query.filter_by(event_id=event_id).all()
        result = [{'id': s.id, 'row': s.row, 'number': s.number, 'status': s.status} for s in seats]
        return {'message': 'Seats retrieved', 'data': result}, 200
