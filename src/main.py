"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person, Queue
from twilio.rest import Client

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

queue = Queue()

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/next')
def sitemap():
    removed_person = queue.dequeue()
    account_sid = 'AC74597789a998d190319007e4bd2a36ad'
    auth_token = '8102a60f2115a7a6cbf6ef740357a58c'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                    body='Hi there!',
                    from_='+12053154250',to= removed_person["phone"]
                )

    return generate_sitemap(app)

@app.route('/new', methods=['POST'])
def addNewPerson():

    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'phone' not in body:
        raise APIException('You need to specify the phone number', status_code=400)
    if body["phone"][-1] != "+1" and len(body["phone"]) != 12:
        raise APIException('Phone number should have 11 numbers and start with +1', status_code=400)
    queue.enqueue(body)
    return "ok", 200

@app.route('/sms/:phone')
def handle_person(item, phone):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'AC74597789a998d190319007e4bd2a36ad'
    auth_token = '8102a60f2115a7a6cbf6ef740357a58c'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                    body='Hi there!',
                    from_='+12053154250',to= item["phone"]
                )

@app.route('/all')
def getAllPeople():
    return jsonify(queue.get_queue())












if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
