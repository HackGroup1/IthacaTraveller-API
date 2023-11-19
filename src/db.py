from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

assoc_features_locations = db.Table(
    "association_features_locations",
    db.Column("feature_id", db.Integer, db.ForeignKey("feature.id")),
    db.Column("location_id", db.Integer, db.ForeignKey("location.id"))
)

assoc_posts_users_likes = db.Table(
    "association_posts_users_likes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"))
)

class Feature(db.Model):
    """
    Feature Model
    """

    __tablename__ = "feature"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    locations = db.relationship("Location", secondary = assoc_features_locations, back_populates = "features")

    def __init__(self, **kwargs):
        """
        Initialize a feature object
        """

        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serialize a feature object
        """
        return {
            "id": self.id,
            "name": self.name,
            "locations": [location.id for location in self.locations]
        }
    
    def simple_serialize(self):
        """
        Serialize a feature object without its corresponding locations
        """
        return {
            "id": self.id,
            "name": self.name
        }


class Location(db.Model):
    """
    Location Model
    """
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    longitude = db.Column(db.String, nullable = False)
    latitude = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    posts = db.relationship("Post", cascade = "delete")
    features = db.relationship("Feature", secondary = assoc_features_locations, back_populates = "locations")

    def __init__(self, **kwargs):
        """
        Initialize a location object
        """

        self.longitude = kwargs.get("longitude", "0.0")
        self.latitude = kwargs.get("latitude", "0.0")
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")

    def serialize(self):
        """
        Serialize a location object
        """
        return {
            "id": self.id,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "name": self.name,
            "description": self.description,
            "posts": [post.simple_serialize() for post in self.posts],
            "features": [feature.simple_serialize() for feature in self.features]
        }

    def simple_serialize(self):
        """
        Serialize a location object without its posts
        """
        return {
            "id": self.id,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "name": self.name,
            "description": self.description,
            "features": [feature.simple_serialize() for feature in self.features]
        }
    
class Post(db.Model):
    """
    Post Model
    """
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    timestamp = db.Column(db.TIMESTAMP, nullable = False)
    comment = db.Column(db.String, nullable = False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    liked_users = db.relationship("User", secondary = assoc_posts_users_likes, back_populates = "posts_liked")

    def __init__(self, **kwargs):
        """
        Initialize a post object
        """

        self.timestamp = kwargs.get("timestamp", null)
        self.comment = kwargs.get("comment", "")
        self.location_id = kwargs.get("location_id", "")
        self.user_id = kwargs.get("user_id", "")

    def serialize(self):
        """
        Serialize a post object
        """
        return {
            "id": self.id,
            "comment": self.comment,
            "location_id": self.location_id,
            "user_id": self.user_id,
            "liked_users": [user.simple_serialize() for user in self.liked_users]
        }
    
    def simple_serialize(self):
        """
        Serialize a post object without liked_users field
        """
        return {
            "id": self.id,
            "comment": self.comment,
            "location_id": self.location_id,
            "user_id": self.user_id
        }
    
    def checked_serialize(self, uid):
        """
        Serialize a post object, containing whether it is editable for the user #uid
        """
        return {
            "id": self.id,
            "comment": self.comment,
            "location_id": self.location_id,
            "user_id": self.user_id,
            "liked_users": [user.simple_serialize() for user in self.liked_users],
            "is_editable": uid == self.user_id
        }

class User(db.Model):
    """
    User Model
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    posts = db.relationship("Post", cascade = "delete")
    posts_liked = db.relationship("Post", secondary = assoc_posts_users_likes, back_populates = "liked_users")

    def __init__(self, **kwargs):
        """
        Initialize a user object
        """

        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password", "")

    def serialize(self):
        """
        Serialize a user object
        """
        return {
            "id": self.id,
            "username": self.name,
            "posts": [post.serialize() for post in self.posts],
            "post_liked": [post.serialize() for post in self.posts_liked]
        }
    
    
    def simple_serialize(self):
        """
        Serialize a user object without posts field
        """
        return {
            "id": self.id,
            "username": self.name
        }
    