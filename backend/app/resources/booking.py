from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from backend.utils.db import db
from backend.models.models import Booking,Seat,Event,Users
from backend.utils.jwt_utils import organizer_required
import datetime
import uuid

class BookTicket(Resource):
    @jwt_required()
    def post(self, lot_id):
        user_id=get_jwt_identity()
        data=request.get_json()
        event_id=data.get('event_id')
        seat_id=data.get('seat_id')

        if not all([event_id,seat_id]):
            return {'message':'require all details'},400

        event=Event.query.get(event_id)
        if not event:
            return {'message':'event not found'},404

        try:
            current_dt = datetime.datetime.now()
            event_start_dt = datetime.datetime.strptime(f"{event.date} {event.start_time}", "%Y-%m-%d %H:%M")
            event_end_dt = datetime.datetime.strptime(f"{event.date} {event.end_time}", "%Y-%m-%d %H:%M")
            
            if current_dt >= event_end_dt:
                return {'message': 'Event ended'}, 400
            if current_dt >= event_start_dt:
                return {'message': 'Event already started. Tickets cannot be booked.'}, 400
        except ValueError:
            pass

        seat=Seat.query.get(seat_id)
        if not seat:
            return {'message':'seat not found'},404
        if seat.status=='B':
            return {'message':'seat already booked'},409

        ticket_id='TKT-'+uuid.uuid4().hex[:8].upper()
        booking_timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        booking=Booking(
            user_id=int(user_id),
            event_id=event_id,
            seat_id=seat_id,
            ticket_id=ticket_id,
            booking_timestamp=booking_timestamp
        )
        seat.status='B'
        db.session.add(booking)
        db.session.commit()

        return {'message':'ticket booked successfully','ticket_id':ticket_id},201

class CancelBooking(Resource):
    @jwt_required()
    def put(self,reservation_id):
        booking=Booking.query.get(reservation_id)
        if not booking:
            return {'message':'booking not found'},404
        if booking.status=='cancelled':
            return {'message':'already cancelled'},409

        booking.status='cancelled'
        seat=Seat.query.get(booking.seat_id)
        seat.status='A'
        db.session.commit()

        return {'message':'booking cancelled successfully'},200

class ViewBookings(Resource):
    @jwt_required()
    def get(self):
        user_id=get_jwt_identity()
        user=Users.query.get(int(user_id))

        if user.role=='organizer':
            events=Event.query.filter_by(organizer_id=int(user_id)).all()
            event_ids=[e.id for e in events]
            bookings=Booking.query.filter(Booking.event_id.in_(event_ids)).all()
        else:
            bookings=Booking.query.filter_by(user_id=int(user_id)).all()

        all_bookings=[]
        for b in bookings:
            event=Event.query.get(b.event_id)
            seat=Seat.query.get(b.seat_id)
            all_bookings.append({
                'id':b.id,'ticket_id':b.ticket_id,'event_name':event.name if event else 'Unknown',
                'venue':event.venue if event else '','date':event.date if event else '',
                'seat':seat.row+str(seat.number) if seat else '','status':b.status,
                'booking_timestamp':b.booking_timestamp,'user_id':b.user_id
            })

        return {'message':'here are the details','all_bookings':all_bookings},200
