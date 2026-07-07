from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db, User
from werkzeug.security import generate_password_hash

from .resources.auth import SignupResource, LoginResource
from .resources.event import EventListResource, EventResource, SeatListResource
from .resources.booking import BookingListResource, BookingResource
from .resources.summary import SummaryResource

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    api = Api(app)
    # Auth
    api.add_resource(SignupResource, '/api/signup')
    api.add_resource(LoginResource, '/api/login')

    # Events
    api.add_resource(EventListResource, '/api/events')
    api.add_resource(EventResource, '/api/events/<int:event_id>')
    api.add_resource(SeatListResource, '/api/events/<int:event_id>/seats')

    # Bookings
    api.add_resource(BookingListResource, '/api/bookings')
    api.add_resource(BookingResource, '/api/bookings/<int:booking_id>')

    # Summary
    api.add_resource(SummaryResource, '/api/summary')

    with app.app_context():
        db.create_all()

    return app
