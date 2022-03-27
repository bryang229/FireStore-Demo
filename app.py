import json

from flask import Flask, jsonify, request, make_response, abort
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import cross_origin, CORS
import cv2

app = Flask(__name__)

@app.route('/api/camera')
def func():
    #blah blah
    return {}



class User(object):
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        #we want the email to be constant
        self.EMAIL = email

    @staticmethod
    def from_dict(source):
       return User(source.username,source.password,source.email)

    def to_dict(self):
        return {   u'Username' : self.username,
                   u'Password' : self.password,
                   u'Email':     self.EMAIL
           }

    def __repr__(self):
        return (
            f'User(\
                   name={self.username}, \
                   password={self.password}, \
                   EMAIl={self.EMAIL}\
               )'
        )


bryan = User(u'bryang229',u'Password324',u'bryang229.com')



CORS(app, resources=r'/api/*')

cred = credentials.Certificate("ai-database-test-firebase-adminsdk-iwodd-c4bc79e522.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def hello_world():
    return "Hello"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found L'}), 404)

@app.route('/api/check_user', methods=["POST"])
def get_user():
    input_json = request.get_json(force=True)
    print(input_json)
    user = User(input_json['Username'],input_json['Password'],input_json['Email'])
    user_ref = db.collection(u'Users').document(user.username).get().to_dict()
    if user_ref['Email'] == user.email and user_ref['Password'] == user.password:
        return {
            "Status": "Success",
            "User"  : user_ref
        }
    else:
        return {
            "Status": "Failed",
            "User"  : user.to_dict()
        }




@app.route('/api/send_data', methods=['POST'])
def send_to_database():
    print("Json:", request.is_json)
    print("Json formatting", request.get_json())
    print("Headers:",request.headers,"type:", type(request.headers))
    input_json = request.get_json(force=True)
    print(input_json,type(input_json))
    if not request.is_json or "Username" not in input_json:
        print('working')
        print(request.headers, type(request.headers), request.headers )
        return jsonify({"Error":"Invalid Request L^2"})
    print(input_json,type(input_json))
    user = User(input_json['Username'], input_json['Password'], input_json['Email'])
    print('////////////////////')
    print(user.to_dict())
    user_ref = db.collection(u'Users')
    user_ref.document(user.username).set(user.to_dict())
    return user.to_dict()




    # Postman Method
    # input_json = request.get_data()
    # print(input_json, type(input_json))
    #
    # input_json = input_json.decode('utf8')
    # print(input_json, type(input_json))
    # input_json = json.loads(input_json)
    # print(input_json, type(input_json))

    # if not request.headers or "Username" not in input_json:
    #     print('working')
    #     print(request.headers, type(request.headers), request.headers )
    #     return jsonify({"Error":"Invalid Request"})
    #
    #
    # print('////////////////////')
    # print(input_json,type(input_json))
    # user = User(input_json['Username'], input_json['Password'], input_json['Email'])
    # print('////////////////////')
    # print(user.to_dict())
    # user_ref = db.collection(u'Users')
    # user_ref.document(user.username).set(user.to_dict())
    # return user.to_dict()

if __name__ == '__main__':
    app.run()
