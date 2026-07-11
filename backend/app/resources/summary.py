from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from backend.utils.db import db
from backend.models.models import Event,Booking,Users
from backend.utils.jwt_utils import organizer_required
from sqlalchemy import text

class OrganizerSummary(Resource):
    @jwt_required()
    @organizer_required
    def get(self):
        organizer_id=get_jwt_identity()

        revenue_sql=text("""
            SELECT e.name,e.price,
                (SELECT COUNT(*) FROM BOOKING b WHERE b.event_id=e.id AND b.status='confirmed') as confirmed_bookings,
                e.price*(SELECT COUNT(*) FROM BOOKING b WHERE b.event_id=e.id AND b.status='confirmed') as revenue
            FROM EVENT e WHERE e.organizer_id=:oid
        """)
        revenue_result=db.session.execute(revenue_sql,{'oid':int(organizer_id)})
        revenue_data=[dict(row._mapping) for row in revenue_result]

        occupancy_sql=text("""
            SELECT e.name,e.total_seats,
                (SELECT COUNT(*) FROM SEAT s WHERE s.event_id=e.id AND s.status='B') as booked
            FROM EVENT e WHERE e.organizer_id=:oid
        """)
        occupancy_result=db.session.execute(occupancy_sql,{'oid':int(organizer_id)})
        occupancy_data=[dict(row._mapping) for row in occupancy_result]

        return {'message':'here are the reports','revenue_data':revenue_data,'occupancy_data':occupancy_data},200

class UserSummary(Resource):
    @jwt_required()
    def get(self):
        user_id=get_jwt_identity()
        bookings=Booking.query.filter_by(user_id=int(user_id)).all()
        total_bookings=len(bookings)
        confirmed=len([b for b in bookings if b.status=='confirmed'])
        cancelled=len([b for b in bookings if b.status=='cancelled'])

        return {'message':'here are the reports','total_bookings':total_bookings,'confirmed':confirmed,'cancelled':cancelled},200

class CSVExport(Resource):
    @jwt_required()
    def get(self):
        import os
        user_id = get_jwt_identity()
        file_name = f"user_{user_id}_export.csv"
        
        try:
            from backend.celery_tasks import export_csv
            task = export_csv.delay(user_id)
            task_id = task.id
        except Exception:
            task_id = "dummy_task_id"
            
        return {'message': 'CSV export task started', 'task_id': task_id, 'file_name': file_name}, 202

class CSVDownload(Resource):
    @jwt_required()
    def get(self, file_name):
        import os
        from flask import send_file
        user_id = get_jwt_identity()
        expected_file = f"user_{user_id}_export.csv"

        if file_name != expected_file:
            return {"message": "You are not authenticated for this file"}, 403
        
        exports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'exports'))
        file_path = os.path.join(exports_dir, expected_file)

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return {"message": "Either file has not been completed yet or you have not exported the file"}, 404

