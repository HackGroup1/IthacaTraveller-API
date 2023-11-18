import json

import db
from flask import Flask
from flask import request
from db import Location

DB = db.DatabaseDriver()

app = Flask(__name__)
db_filename = "IthacaTraveller.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

#generalize return
def success_reponse(body, code = 200):
    return json.dumps(body), code

def failure_response(message, code = 404):
    return json.dumps({"error": message}), code



@app.route("/")
def front_page():
    return "Hello!"


#routes here
@app.route("/api/add/", methods=["POST"])
def add_location():
    """
    Enpoint for adding location
    """
    body = json.loads(request.data)
    long = body.get("longitude")
    lati = body.get("latitude")
    name = body.get("name")
    description = body.get("description")
    features = body.get("features")
    #TODO init
    

@app.route("/api/location/<int:location_id>/")
def get_location_by_id(location_id):
    """
    Endpoint for getting location details by its id
    """
    location = Location.query.filter_by(id=location_id).first()



@app.route("/api/post/<int:location_id>/")
def get_post(location_id):
    """
    Endpoint for getting posts under specific location by id
    Requires user id
    """
    body = json.loads(request.data)
    user_id = body.get("user_id")
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
