from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
import uuid
from ..models import db, Booking, Seat, Event

def is_organizer():
    claims = get_jwt()
    return claims.get('role') == 'organizer'

class BookingListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        # If user, return their bookings. If organizer, they usually want to see bookings for their events, 
        # but let's make a separate endpoint or just handle user's bookings here.
        if is_organizer():
            # For organizers, return all bookings for their events
            events = Event.query.filter_by(organizer_id=user_id).all()
            event_ids = [e.id for e in events]
            bookings = Booking.query.filter(Booking.event_id.in_(event_ids)).all()
        else:
            # For users
            bookings = Booking.query.filter_by(user_id=user_id).all()
            
        result = []
        for b in bookings:
            result.append({
                'id': b.id,
                'ticket_id': b.ticket_id,
                'event_name': b.event.name,
                'date': b.event.date.isoformat(),
                'seat': f"{b.seat.row}{b.seat.number}",
                'status': b.status,
                'user_name': b.user.name if is_organizer() else None
            })
        return {'message': 'Bookings retrieved', 'data': result}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        
        event_id = data.get('event_id')
        seat_id = data.get('seat_id')

        if not event_id or not seat_id:
            return {'message': 'event_id and seat_id required'}, 400

        seat = Seat.query.get(seat_id)
        if not seat or seat.event_id != int(event_id):
            return {'message': 'Invalid seat'}, 400
            
        if seat.status == 'booked':
            return {'message': 'Seat is already booked'}, 409

        ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"

        booking = Booking(
            user_id=user_id,
            event_id=event_id,
            seat_id=seat_id,
            ticket_id=ticket_id,
            status='confirmed'
        )
        
        seat.status = 'booked'
        
        db.session.add(booking)
        db.session.commit()
        
        return {
            'message': 'Ticket booked successfully', 
            'data': {'ticket_id': ticket_id, 'seat': f"{seat.row}{seat.number}"}
        }, 201


class BookingResource(Resource):
    @jwt_required()
    def delete(self, booking_id):
        # Cancellation
        user_id = get_jwt_identity()
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return {'message': 'Booking not found'}, 404

        # Allow user to cancel their own, or organizer to cancel
        if not is_organizer() and booking.user_id != user_id:
            return {'message': 'Unauthorized'}, 403
            
        if is_organizer() and booking.event.organizer_id != user_id:
            return {'message': 'Unauthorized'}, 403

        if booking.status == 'cancelled':
            return {'message': 'Already cancelled'}, 409

        booking.status = 'cancelled'
        
        # Free up the seat
        seat = Seat.query.get(booking.seat_id)
        if seat:
            seat.status = 'available'

        db.session.commit()
        return {'message': 'Booking cancelled successfully'}, 200
