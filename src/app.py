import json
import os
from datetime import datetime

from db import db, Location, Feature, Post, User
from flask import Flask, request, send_file
from hashlib import pbkdf2_hmac
from dotenv import load_dotenv

from image import image_route


app = Flask(__name__)
db_filename = "IthacaTraveller.db"

load_dotenv()
salting = os.environ.get("PASSWORD_SALT")
iterations = int(os.environ.get("NUMBER_OF_ITERATIONS"))
image_route(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

#### HELPER METHODS ####
def hash_password(password):
    secret_password = pbkdf2_hmac('sha384', password.encode(), salting.encode(), iterations)
    return secret_password


#### GENERALIZE RETURN ####
def success_response(body, code = 200):
    return json.dumps(body), code

def failure_response(message, code = 404):
    return json.dumps({"error": message}), code



@app.route("/")
def front_page():
    return "Hello!"


#### ROUTES ####

#--------- Feature Routes ------------

@app.route("/api/features/")
def get_all_features():
    """
    Endpoint for getting all the features
    """

    features = [feature.serialize() for feature in Feature.query.all()]
    return success_response({"features": features})
    

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

    return success_response(feature.serialize(), 201)

@app.route("/api/features/<int:feature_id>/", methods = ["DELETE"])
def delete_feature_by_id(feature_id):
    """
    Endpoint for deleting a feature by its id
    """

    feature = Feature.query.filter_by(id=feature_id).first()

    if feature is None:
        return failure_response("feature not found", 404)

    db.session.delete(feature)
    db.session.commit()
    return success_response(feature.serialize())


#--------- Location Routes ------------

@app.route("/api/locations/")
def get_all_locations():
    """
    Endpoint for getting all the locations
    """

    locations = [location.simple_serialize() for location in Location.query.all()]
    return success_response({"locations": locations})


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
    
    return success_response(location.serialize(), 201)


@app.route("/api/locations/<int:location_id>/")
def get_location_by_id(location_id):
    """
    Endpoint for getting location details by its id
    """

    location = Location.query.filter_by(id=location_id).first()
    
    if location is None:
        return failure_response("location not found")
    
    return success_response(location.serialize())


@app.route("/api/locations/<int:location_id>/features/<int:feature_id>/", methods = ["POST"])
def add_feature_to_location(location_id, feature_id):
    """
    Endpoint adding feature tag to the location
    Requires feature id
    """

    feature = Feature.query.filter_by(id=feature_id).first()
    if feature is None:
        return failure_response("feature not found")
    
    location = Location.query.filter_by(id=location_id).first()
    if location is None:
        return failure_response("location not found")

    if feature in location.features:
        return failure_response("location already has this feature", 400)

    location.features.append(feature)

    db.session.commit()

    location = Location.query.filter_by(id=location_id).first()

    return success_response(location.simple_serialize(), 401)


@app.route("/api/features/<feature>/locations/")
def get_locations_id_by_feature(feature):
    """
    Endpoint for getting locations id assoicated with feature by feature name
    """

    feature = Feature.query.filter_by(name=feature).first()
    if feature is None:
        return failure_response("feature not found", 404)
    
    locations = feature.serialize().get("locations")
    res = {"id":locations}
    return success_response([res])


@app.route("/api/locations/<int:location_id>/", methods = ["DELETE"])
def delete_location_by_id(location_id):
    """
    Endpoint for deleting a location by its id
    """

    location = Location.query.filter_by(id=location_id).first()

    if location is None:
        return failure_response("location not found", 404)

    db.session.delete(location)
    db.session.commit()
    return success_response(location.serialize())


#--------- Posts Routes ------------

@app.route("/api/posts/")
def get_all_posts():
    """
    Endpoint for getting all posts
    """

    posts = [post.serialize() for post in Post.query.all()]
    return success_response({"posts": posts})


@app.route("/api/posts/", methods=["POST"])
def add_post():
    """
    Enpoint for adding post
    """

    body = json.loads(request.data)
    comment = body.get("comment")
    location_id = body.get("location_id")
    user_id = body.get("user_id")

    if comment is None or location_id is None or user_id is None:
        return failure_response("missing parameter", 400)

    location = Location.query.filter_by(id=location_id).first()

    if location is None:
        return failure_response("location not found", 404)

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("user not found", 404)

    post = Post(
        timestamp = datetime.now(),
        comment = comment,
        location_id = location_id,
        user_id = user_id
    )
    
    db.session.add(post)
    db.session.commit()
    
    return success_response(post.serialize(), 201)


@app.route("/api/locations/<int:location_id>/posts/")
def get_posts_by_location(location_id):
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

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("user not found", 404)
    
    posts = [post.checked_serialize(user_id) for post in location.post]

    return success_response(posts)


@app.route("/api/posts/<int:post_id>/", methods = ["DELETE"])
def delete_post_by_id(post_id):
    """
    Endpoint for deleting a post by its id
    """

    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        return failure_response("post not found", 404)

    db.session.delete(post)
    db.session.commit()
    return success_response(post.serialize())


#--------- Users Routes ------------
@app.route("/api/users/")
def get_all_users():
    """
    Endpoint for getting all users
    """

    users = [user.serialize() for user in User.query.all()]
    return success_response({"users": users})


@app.route("/api/users/", methods = ["POST"])
def add_user():
    """
    Endpoint for adding users
    """
    
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")

    if username is None or password is None:
        return failure_response("missing parameter", 400)

    hashed_password = hash_password(password)

    user = User.query.filter_by(username = username).first()

    if user is not None:
        return failure_response("user already exist", 400)

    user = User(username = username,
                password = hashed_password
                )
    
    db.session.add(user)
    db.session.commit()

    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>")
def get_uesr_by_id(user_id):
    """
    Endpoint for getting user by id
    """
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return failure_response("user not found")
    
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/", methods = ["DELETE"])
def delete_user_by_id(user_id):
    """
    Endpoint for deleting an user by its id
    """

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("user not found", 404)

    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())


@app.route("/api/users/verify")
def verify_user():
    """
    Endpoint for verifying whether password is correct
    """
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")

    if username is None or password is None:
        return failure_response("missing parameter", 400)

    user = User.query.filter_by(username = username).first()

    if user is None:
        return failure_response("user not found", 404)
    
    hashed_password = hash_password(password)
    
    #check with frontend for return message format
    

    if user.password == hashed_password:
        res = {"verify":True}
        return success_response(res)
    else:
        res = {"verify":False}
        return success_response(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
