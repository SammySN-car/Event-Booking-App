from backend.utils.db import db

class Users(db.Model):
    __tablename__='USERS'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    full_name=db.Column(db.String,nullable=False)
    email_id=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    phone=db.Column(db.String)
    role=db.Column(db.String,db.CheckConstraint("role in ('organizer','user')"),nullable=False,default='user')

    events=db.relationship('Event',backref='organizer',cascade='all,delete')
    bookings=db.relationship('Booking',backref='user',cascade='all,delete')

class Event(db.Model):
    __tablename__='EVENT'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    organizer_id=db.Column(db.Integer,db.ForeignKey('USERS.id',ondelete='CASCADE'),nullable=False)
    name=db.Column(db.String,nullable=False)
    venue=db.Column(db.String,nullable=False)
    date=db.Column(db.String,nullable=False)
    start_time=db.Column(db.String,nullable=False)
    end_time=db.Column(db.String,nullable=False)
    price=db.Column(db.Integer,nullable=False,default=0)
    total_seats=db.Column(db.Integer,nullable=False)

    seats=db.relationship('Seat',backref='event',cascade='all,delete')
    bookings=db.relationship('Booking',backref='event',cascade='all,delete')

class Seat(db.Model):
    __tablename__='SEAT'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    event_id=db.Column(db.Integer,db.ForeignKey('EVENT.id',ondelete='CASCADE'),nullable=False)
    row=db.Column(db.String,nullable=False)
    number=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String,db.CheckConstraint("status in ('A','B')"),nullable=False,default='A')

    bookings=db.relationship('Booking',backref='seat',cascade='all,delete')

class Booking(db.Model):
    __tablename__='BOOKING'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('USERS.id',ondelete='CASCADE'),nullable=False)
    event_id=db.Column(db.Integer,db.ForeignKey('EVENT.id',ondelete='CASCADE'),nullable=False)
    seat_id=db.Column(db.Integer,db.ForeignKey('SEAT.id',ondelete='CASCADE'),nullable=False)
    ticket_id=db.Column(db.String,unique=True,nullable=False)
    booking_timestamp=db.Column(db.String,nullable=False)
    status=db.Column(db.String,db.CheckConstraint("status in ('confirmed','cancelled')"),nullable=False,default='confirmed')
