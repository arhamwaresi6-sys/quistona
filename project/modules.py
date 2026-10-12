from .extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
class User(db.Model,UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(50) , nullable = False)
    email = db.Column(db.String(50) , nullable = False, unique = True)
    created_at = db.Column(db.Date,default =lambda: datetime.now().date())
    password_hash = db.Column(db.Text , nullable = False)
    role = db.Column(
        db.Enum("user", "admin", "root", name="user_roles"),
        default="user",
        nullable=False
    )
    @property
    def password(self):
        return "nice try!"
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    semesters = db.relationship(
        "Semester",
        backref="batch",
        cascade="all, delete-orphan"
    )

    @property
    def semester_count(self):
        return db.session.execute(
            db.select(db.func.count(Semester.id))
            .where(Semester.batch_id == self.id)
        ).scalar_one()



class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey("batch.id", ondelete="CASCADE"),
        nullable=False
    )

    courses = db.relationship(
        "Course",
        backref="semester",
        cascade="all, delete-orphan"
    )

    @property
    def course_count(self):
        return db.session.execute(
            db.select(db.func.count(Course.id))
            .where(Course.semester_id == self.id)
        ).scalar_one()



class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    semester_id = db.Column(
        db.Integer,
        db.ForeignKey("semester.id", ondelete="CASCADE"),
        nullable=False
    )

    images = db.relationship(
        "Image",
        backref="course",
        cascade="all, delete-orphan"
    )

    @property
    def question_count(self):
        return db.session.execute(
            db.select(db.func.count(Image.id))
            .where(Image.course_id == self.id)
        ).scalar_one()


class Image(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    url = db.Column(db.Text , nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(
    db.Integer,
    db.ForeignKey("course.id", ondelete="CASCADE"),
    nullable=False
)
    user = db.relationship("User", backref="images")
    type = db.Column(
            db.Enum("quiz", "final", name="q_type"),
            default="final",
            nullable=False
        )
    course_type = db.Column(
            db.Enum("regular", "supli"),
            default="regular",
            nullable=False
        )
    created_at = db.Column(db.Date,default =lambda: datetime.now().date())
    @property
    def pretty_date(self):
        return self.created_at.strftime("%d %B,%Y").lower()
    
