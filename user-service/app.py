from flask import Flask, session
from flask_cors import CORS
from flask_restful import Api
from flask_jwt import JWT
from flask import request
# from security import authenticate, identity
from resources.user import UserRegister, User, getUserDetailsByName
from models.user import search_by_username, authentication
from create_tables import createdb

app = Flask(__name__)

app.secret_key =  'jose'

CORS(app)

api = Api(app)

@app.route('/')
def index():
    if 'userid' in session:
        return 'Logged in as {}'.format(userid)
    return 'You are not logged in.'


@app.route('/login', methods=['POST'])
def login():
    if request.is_json is None:
        return {'message': 'Send data in form of json'}, 400
    data = request.get_json()
    print(data)
    if data['username'] is None or data['password'] is None:
        return {'message':'Please provide the valid imformation to authenticate'}, 401
    return authentication(data['username'], data['password'])


@app.route('/userdetails', methods=['POST'])
def getUserDetails():
    if request.is_json is None:
        return {'message': 'send data in form of json'}, 400
    data = request.get_json()
    return getUserDetailsByName(data['username'])


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)



api.add_resource(User,'/user')
api.add_resource(UserRegister,'/register')

if __name__ == "__main__":
    createdb()
    app.run(port = 5003, host='0.0.0.0', debug = True)
