from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from backend.utils.db import db
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Mail config (unused/stubs)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# JWT config
app.config['JWT_SECRET_KEY'] = 'this-is-my-secret-key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
jwt = JWTManager(app)

# Database config
db_path = os.path.join(os.path.dirname(__file__), 'data', 'event.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)  # ensure the folder exists
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db.init_app(app)

from backend.models.models import Users, Event, Seat, Booking

with app.app_context():
    db.create_all()
    print("✅ DB created")
    if not Users.query.filter_by(role='organizer').first():
        password_val = 'organizer'
        adm = Users(
            full_name='ORGANIZER',
            email_id="ORGANIZER@gmail.com",
            password=generate_password_hash(password_val),
            phone='0000000000',
            role='organizer'
        )
        db.session.add(adm)
        db.session.commit()
        print("✅ Organizer superuser created")

# Resources
from backend.app.resources.auth import Register, Login
from backend.app.resources.event import AddEvent, EditEvent, DeleteEvent, ViewEvents
from backend.app.resources.booking import BookTicket, CancelBooking, ViewBookings
from backend.app.resources.summary import OrganizerSummary, UserSummary, CSVExport, CSVDownload

api = Api(app)

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(AddEvent, '/admin/add_lot')  # Match user's frontend habit of "/admin/add_lot"
api.add_resource(EditEvent, '/admin/edit_lot/<int:event_id>')
api.add_resource(DeleteEvent, '/admin/delete_lot/<int:event_id>')
api.add_resource(ViewEvents, '/admin/home')
api.add_resource(BookTicket, '/user/book/<int:lot_id>') # lot_id is event_id in this project
api.add_resource(CancelBooking, '/user/release/<int:reservation_id>') # reservation_id is booking_id
api.add_resource(ViewBookings, '/user/home')
api.add_resource(OrganizerSummary, '/admin/summary')
api.add_resource(UserSummary, '/user/summary')
api.add_resource(CSVExport, '/user/export_csv')
api.add_resource(CSVDownload, '/user/export_csv/<string:file_name>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
