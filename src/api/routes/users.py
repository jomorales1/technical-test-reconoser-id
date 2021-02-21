from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_security import hash_password, verify_password
from src.api.models.users import UserSchema
from src.main import user_datastore, db


class Users(Resource):
    def post(self):
        """
        Creates a new user
        ---
        tags:
            - users
        description: Given user's email and password creates a new instance in the database.
        parameters:
            - in: body
              name: email
              required: true
              type: string
              description: User's email.
              example: test@me.com
            - in: body
              name: password
              required: true
              type: string
              description: User's password.
              example: some_strong_password
        responses:
            201:
                description: User created
            400:
                description: Invalid input data
        """
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
        """
        Returns user's authentication token
        ---
        tags:
            - users
        description: Given user's email and password checks if user is registered so as to retrieve acess token
        parameters:
            - in: body
              name: email
              required: true
              type: string
              description: User's email.
              example: test@me.com
            - in: body
              name: password
              required: true
              type: string
              description: User's password.
              example: some_strong_password
        responses:
            200:
                description: User was found in the database and their token was returned
            400:
                description: Either user was not found or password was incorrect
        """
        data = request.get_json()
        user_schema = UserSchema()
        user = user_schema.load(data)
        if not (user.get('email') and user.get('password')):
            return make_response('', 400)
        user_fetched = user_datastore.find_user(email=user.get('email'))
        if not user_fetched:
            return make_response('', 400)
        if not verify_password(user.get('password'), user_fetched.password):
            return make_response('', 400)
        return make_response(jsonify({'access_token': user_fetched.get_auth_token()}), 200)
