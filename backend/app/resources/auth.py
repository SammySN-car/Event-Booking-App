from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..models import db, User

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(email=data.get('email')).first():
            return {'message': 'Email already exists'}, 409
        
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            role=data.get('role', 'user')
        )
        
        # Additional fields can be mapped here dynamically
        for key in ['address', 'phone', 'resume_link', 'skills', 'bio']:
            if key in data and hasattr(user, key):
                setattr(user, key, data[key])

        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully', 'data': {'id': user.id}}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user or not check_password_hash(user.password_hash, data.get('password')):
            return {'message': 'Invalid credentials'}, 401
            
        token = create_access_token(identity=user.id, additional_claims={'role': user.role})
        return {
            'message': 'Login successful',
            'data': {
                'token': token,
                'user': {'id': user.id, 'role': user.role, 'name': user.name}
            }
        }, 200
