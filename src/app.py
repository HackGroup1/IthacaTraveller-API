import json

from db import db
from flask import Flask
from flask import request
from db import Location
from db import Feature

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
@app.route("/api/locations/", methods=["POST"])
def add_location():
    """
    Enpoint for adding location
    """
    body = json.loads(request.data)
    long = body.get("longitude")
    lati = body.get("latitude")
    name = body.get("name")
    description = body.get("description")
    location = Location(
        longitude = long,
        latitude = lati,
        name = name,
        description = description
    )
    
    db.session.add(location)
    db.session.commit()
    
    return success_reponse(location.serialize(), 201)

    
@app.route("/api/features/", methods=["POST"])
def add_feature():
    """
    Enpoint for adding locations
    """
    body = json.loads(request.data)
    name = body.get("name")
    feature = Feature(name = name)

    db.session.add(feature)
    db.session.commit()

    return success_reponse(feature.serialize(), 201)

@app.route("/api/locations/<int:location_id>/features/", methods = ["POST"])
def add_feature_to_location(location_id):
    """
    Endpoint adding feature tag to the location
    Requires feature id
    """
    body = json.loads(request.data)
    feature_id = body.get("feature_id")
    if feature_id is None:
        return failure_response("missing parameter", 400)

    feature = Feature.query.filter_by(id=feature_id).first()
    if feature is None:
        return failure_response("feature not found")
    
    location = Location.query.filter_by(id=location_id).first()
    if location is None:
        return failure_response("location not found")

    location.features.append(feature)

    db.session.commit()

    location = Location.query.filter_by(id=location_id).first()

    return success_reponse(location.serialize(), 401)


@app.route("/api/features/<feature>/locations/")
def get_location_id_by_feature(feature):
    """
    Endpoint for getting location assoicated with feature by feature name
    """
    feature = Feature.query.filter_by(name=feature).first()
    if feature is None:
        return failure_response("feature not found", 404)
    
    locations = feature.serialize().get("locations")

    return success_reponse(locations)

@app.route("/api/locations/<int:location_id>/")
def get_location_by_id(location_id):
    """
    Endpoint for getting location details by its id
    """
    location = Location.query.filter_by(id=location_id).first()
    
    if location is None:
        return failure_response("location not found")
    
    return success_reponse(location.serialize())



@app.route("/api/locations/<int:location_id>/")
def get_posts(location_id):
    """
    Endpoint for getting posts under specific location by id
    Requires user id
    """

    location = Location.query.filter_by(id=location_id).first()

    if location is None:
        return failure_response("location not found", 404)

    body = json.loads(request.data)
    user_id = body.get("user_id")

    if user_id is None:
        return failure_response("missing parameter", 400)
    





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
