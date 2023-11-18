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

class Course(db.Model):
    """
    Course Model
    """
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    code = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    assignments = db.relationship("Assignment", cascade = "delete")
    instructors = db.relationship("User", secondary = assoc_course_instructors, back_populates = "instructing")
    students = db.relationship("User", secondary = assoc_course_students, back_populates = "studying")
    def __init__(self, **kwargs):
        """
        Initialize a course object
        """

        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serialize a course object
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [assignment.simple_serialize() for assignment in self.assignments],
            "instructors": [instructor.simple_serialize() for instructor in self.instructors],
            "students": [student.simple_serialize() for student in self.students]
        }

    def simple_serialize(self):
        """
        Serialize a course object without its assignments, instructors, and students fields
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }
    
class Assignment(db.Model):
    """
    Assignment Model
    """
    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    due_date = db.Column(db.Integer, nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable = False)

    def __init__(self, **kwargs):
        """
        Initialize an assignment object
        """

        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date", "")
        self.course_id = kwargs.get("course_id")

    def serialize(self):
        """
        Serialize an assignment object
        """
        course = Course.query.filter_by(id = self.course_id).first()
        
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course": course.simple_serialize()
        }
    
    def simple_serialize(self):
        """
        Serialize an assignment object without course field
        """
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date
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
    