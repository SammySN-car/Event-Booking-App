from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func
from ..models import db, Event, Booking

def is_organizer():
    claims = get_jwt()
    return claims.get('role') == 'organizer'

class SummaryResource(Resource):
    @jwt_required()
    def get(self):
        if not is_organizer():
            return {'message': 'Organizer access required'}, 403

        organizer_id = get_jwt_identity()
        events = Event.query.filter_by(organizer_id=organizer_id).all()
        
        summary = []
        for e in events:
            # Calculate revenue for confirmed bookings
            confirmed_count = Booking.query.filter_by(event_id=e.id, status='confirmed').count()
            revenue = confirmed_count * e.price
            occupancy = (confirmed_count / e.total_seats * 100) if e.total_seats > 0 else 0
            
            summary.append({
                'event_name': e.name,
                'confirmed_bookings': confirmed_count,
                'revenue': revenue,
                'occupancy_percent': round(occupancy, 2)
            })

        return {'message': 'Summary retrieved', 'data': summary}, 200
