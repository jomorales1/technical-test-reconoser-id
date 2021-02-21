from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_security import hash_password
from src.api.models.users import UserSchema
from src.main import user_datastore, db


class Users(Resource):
    def post(self):
        data = request.get_json()
        user_schema = UserSchema()
        user = user_schema.load(data)
        if not (user.get('email') and user.get('password')):
            return make_response('', 400)
        if user_datastore.find_user(email=user.get('email')):
            return make_response('', 400)
        user_datastore.create_user(email=user.get('email'), password=hash_password(user.get('password')))
        db.session.commit()
        return make_response('User created', 201)


class Login(Resource):
    def post(self):
        data = request.get_json()
        user_schema = UserSchema()
        user = user_schema.load(data)
        if not (user.get('email') and user.get('password')):
            return make_response('', 400)
        user_fetched = user_datastore.find_user(email=user.get('email'))
        if not user_fetched:
            return make_response('', 400)
        return make_response(jsonify({'access_token': user_fetched.get_auth_token()}), 200)
