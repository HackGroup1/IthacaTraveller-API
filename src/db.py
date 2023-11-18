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
        Serialize a feature object
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
    longitude = db.Column(db.Double, nullable = False)
    latitude = db.Column(db.Double, nullable = False)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    feature = db.Column(db.String, nullable = False)
    posts = db.relationship("Post", cascade = "delete")
    features = db.relationship("Feature", secondary = assoc_features_locations, back_populates = "locations")

    def __init__(self, **kwargs):
        """
        Initialize a location object
        """

        self.longitude = kwargs.get("longitude", 0.0)
        self.latitude = kwargs.get("latitude", 0.0)
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.feature = kwargs.get("feature", "")

    def serialize(self):
        """
        Serialize a course object
        """
        return {
            "id": self.id,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "name": self.name,
            "description": self.description,
            "posts": [post.serialize() for post in self.posts],
            "features": [feature.simple_serialize() for feature in self.features]
        }

    def simple_serialize(self):
        """
        Serialize a course object without its assignments, instructors, and students fields
        """
        return {
            "id": self.id,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "name": self.name,
            "description": self.description
        }
    
class Post(db.Model):
    """
    Post Model
    """
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    comment = db.Column(db.String, nullable = False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    likes = db.relationship("User", secondary = assoc_posts_users_likes, back_populates = "users")

    def __init__(self, **kwargs):
        """
        Initialize a post object
        """

        self.comment = kwargs.get("comment", "")
        self.location_id = kwargs.get("name", "")
        self.user_id = kwargs.get("user_id", "")

    def serialize(self):
        """
        Serialize a course object
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [course.simple_serialize() for course in (self.instructing + self.studying)]
        }
    
    def simple_serialize(self):
        """
        Serialize a course object without courses field
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
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
    posts_liked = db.relationship("Post", secondary = assoc_posts_users_likes, back_populates = "likes")

    def __init__(self, **kwargs):
        """
        Initialize a user object
        """

        self.username = kwargs.get("username", "")
        self.password = kwargs.get("", "")

    def serialize(self):
        """
        Serialize a course object
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [course.simple_serialize() for course in (self.instructing + self.studying)]
        }
    
    def simple_serialize(self):
        """
        Serialize a course object without courses field
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }
    