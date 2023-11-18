from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

assoc_course_instructors = db.Table(
    "association_course_instructors",
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("instructor_id", db.Integer, db.ForeignKey("user.id"))
)

assoc_course_students = db.Table(
    "association_course_students",
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("student_id", db.Integer, db.ForeignKey("user.id"))
)

class Spot(db.Model):
    """
    Spot Model
    """
    __tablename__ = "spot"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    longitude = db.Column(db.Double, nullable = False)
    latitude = db.Column(db.Double, nullable = False)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    # image_name = db.Column(db.String, nullable = False)
    feature = db.Column(db.String, nullable = False)
    posts = db.relationship("Post", cascade = "delete")

    def __init__(self, **kwargs):
        """
        Initialize a spot object
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
            "posts": [post.serialize() for post in self.posts]
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
            "description": self.description,
        }
    
class Post(db.Model):
    """
    Post Model
    """
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    comment = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    likes = db.relationship("Course", secondary = assoc_course_students, back_populates = "students")

    def __init__(self, **kwargs):
        """
        Initialize a post object
        """

        self.netid = kwargs.get("netid", "")
        self.name = kwargs.get("name", "")

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
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    instructing = db.relationship("Course", secondary = assoc_course_instructors, back_populates = "instructors")
    studying = db.relationship("Course", secondary = assoc_course_students, back_populates = "students")

    def __init__(self, **kwargs):
        """
        Initialize a user object
        """

        self.netid = kwargs.get("netid", "")
        self.name = kwargs.get("name", "")

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
    