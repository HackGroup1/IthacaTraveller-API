import json

import db
from flask import Flask
from flask import request
from db import Spot

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
@app.route("/api/add", methods=["POST"])
def add_spot():
    body = json.loads(request.data)
    long = body.get("longitude")
    lati = body.get("latitude")
    name = body.get("name")
    description = body.get("description")
    features = body.get("features")
    #TODO init
    

@app.route("/api/spot/<int:spot_id>")
def get_spot_by_id(spot_id):
    spot = Spot.query.filter_by(id=spot_id).first()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
