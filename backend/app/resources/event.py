from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from backend.utils.db import db
from backend.models.models import Event,Seat,Booking
from backend.utils.jwt_utils import organizer_required
from sqlalchemy import text

class AddEvent(Resource):
    @jwt_required()
    @organizer_required
    def post(self):
        data=request.get_json()
        name=data.get('name')
        venue=data.get('venue')
        date=data.get('date')
        start_time=data.get('start_time')
        end_time=data.get('end_time')
        price=data.get('price')
        total_seats=data.get('total_seats')

        if not all([name,venue,date,start_time,end_time,total_seats]):
            return {'message':'require all details'},400

        if start_time >= end_time:
            return {'message': 'Start time must be before end time'}, 400

        organizer_id=get_jwt_identity()
        event=Event(
            organizer_id=int(organizer_id),
            name=name,
            venue=venue,
            date=date,
            start_time=start_time,
            end_time=end_time,
            price=price or 0,
            total_seats=total_seats
        )
        db.session.add(event)
        db.session.flush()

        rows='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        seats_per_row=10
        count=0
        for r in rows:
            for n in range(1,seats_per_row+1):
                if count>=total_seats:
                    break
                seat=Seat(event_id=event.id,row=r,number=n)
                db.session.add(seat)
                count+=1
            if count>=total_seats:
                break

        db.session.commit()
        return {'message':'event added successfully'},201

class EditEvent(Resource):
    @jwt_required()
    @organizer_required
    def put(self,event_id):
        data=request.get_json()
        name=data.get('name')
        venue=data.get('venue')
        date=data.get('date')
        start_time=data.get('start_time')
        end_time=data.get('end_time')
        price=data.get('price')
        total_seats=data.get('total_seats')

        if not all([name,venue,date,start_time,end_time,total_seats]):
            return {'message':'require all details'},400

        if start_time >= end_time:
            return {'message': 'Start time must be before end time'}, 400

        event=Event.query.get(event_id)
        if not event:
            return {'message':'event not found'},404

        old_total=event.total_seats
        event.name=name
        event.venue=venue
        event.date=date
        event.start_time=start_time
        event.end_time=end_time
        event.price=price or 0
        event.total_seats=total_seats

        if total_seats>old_total:
            rows='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            existing=Seat.query.filter_by(event_id=event_id).count()
            count=existing
            for r in rows:
                for n in range(1,11):
                    if count>=total_seats:
                        break
                    exists=Seat.query.filter_by(event_id=event_id,row=r,number=n).first()
                    if not exists:
                        seat=Seat(event_id=event_id,row=r,number=n)
                        db.session.add(seat)
                        count+=1
                if count>=total_seats:
                    break
        elif total_seats<old_total:
            available=Seat.query.filter_by(event_id=event_id,status='A').count()
            to_remove=old_total-total_seats
            if to_remove<=available:
                seats_to_del=Seat.query.filter_by(event_id=event_id,status='A').limit(to_remove).all()
                for s in seats_to_del:
                    db.session.delete(s)
            else:
                return {'message':'Free up seats first to reduce'},409

        db.session.commit()
        return {'message':'event updated successfully'},200

    @jwt_required()
    @organizer_required
    def get(self,event_id):
        event=Event.query.get(event_id)
        if not event:
            return {'message':'event not found'},404
        event_details={'id':event.id,'name':event.name,'venue':event.venue,'date':event.date,'start_time':event.start_time,'end_time':event.end_time,'price':event.price,'total_seats':event.total_seats}
        return {'message':'here are the details','event_details':event_details},200

class DeleteEvent(Resource):
    @jwt_required()
    @organizer_required
    def delete(self,event_id):
        count=Booking.query.filter_by(event_id=event_id,status='confirmed').count()
        if count>0:
            return {'message':'Cannot delete because event has confirmed bookings'},409
        obj=Event.query.filter_by(id=event_id).first()
        if not obj:
            return {'message':'event not found'},404
        db.session.delete(obj)
        db.session.commit()
        return {'message':'event deleted successfully'},200

class ViewEvents(Resource):
    @jwt_required()
    def get(self):
        sql=text("""
            SELECT e.*,
                (SELECT COUNT(*) FROM SEAT s WHERE s.event_id=e.id AND s.status='A') AS available,
                (SELECT COUNT(*) FROM SEAT s WHERE s.event_id=e.id AND s.status='B') AS booked
            FROM EVENT e
        """)
        result=db.session.execute(sql)
        events=[dict(row._mapping) for row in result]
        full_events=[]
        for event in events:
            spo=Seat.query.filter_by(event_id=event['id']).all()
            seats=[{'id':s.id,'row':s.row,'number':s.number,'status':s.status} for s in spo]
            ev=dict(event)
            ev['seats']=seats
            full_events.append(ev)
        return {'message':'here are the details','all_events':full_events},200
