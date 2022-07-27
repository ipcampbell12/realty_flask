
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from house import House, Houses

app = Flask(__name__)
app.secret_key = 'Ian'
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(House, '/house/<string:name>')
api.add_resource(Houses, '/houses')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(port=5006, debug=True)
