from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'Ian'
api = Api(app)


houses = []


class House(Resource):
    pass


class Houses(Resource):
    pass


api.add_resource(UserRegister, '/register')
api.add_resource(House, '/house/<string:name')
api.add_resource(Houses, '/houses')
