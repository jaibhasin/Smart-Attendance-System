"""
A web-based smart attendance management system for educational institutions, built with Python and Flask.
"""
from myproject import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    # Format of user_id will be "role_actualid" e.g., "student_1"
    role, id = user_id.split('_')
    if role == 'student':
        return Student.query.get(int(id))
    elif role == 'parent':
        return Parent.query.get(int(id))
    elif role == 'professor':
        return Professor.query.get(int(id))
    return None

class Student(db.Model , UserMixin):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    contact = db.Column(db.String(50))
    branch = db.Column(db.String(50))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))

    def get_id(self):
        return f'student_{self.student_id}'

    def __init__(self , first_name , last_name , email , password , address , contact , branch):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.address = address
        self.contact = contact
        self.branch = branch

    def __repr__(self):
        return (f"{self.first_name} {self.last_name} : {self.branch} : {self.email}")

    def check_password(self, password):
        """Verify a student's password."""
        return check_password_hash(self.password_hash, password)


class Professor(db.Model , UserMixin):
    __tablename__ = 'professor'
    professor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    # name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50))

    def get_id(self):
        return f'professor_{self.professor_id}'
    
    def __init__(self , first_name , last_name , email , password , contact):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.contact = contact
    
    def __repr__(self):
        return (f"{self.first_name} {self.last_name} : {self.email}")

    def check_password(self, password):
        """Verify a professor's password."""
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    total_classes = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey('professor.professor_id'))

class Parent(db.Model , UserMixin):
    __tablename__ = 'parent'
    parent_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    # name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50))

    def check_password(self, password):
        """Verify a parent's password."""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return f'parent_{self.parent_id}'
    
    def __init__(self , first_name , last_name , email , password , contact):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.contact = contact

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50))

class ClassRoom(db.Model):
    __tablename__ = 'classroom'
    room_number = db.Column(db.String(20), primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.professor_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))

class Attendance(db.Model):
    __tablename__ = 'attendance'
    attendance_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    
    # Define relationships
    student = db.relationship('Student', backref=db.backref('attendances', lazy='dynamic'))
    course = db.relationship('Course', backref=db.backref('attendances', lazy='dynamic'))

# Relationship tables
student_parent = db.Table('student_parent',
    db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'), primary_key=True),
    db.Column('parent_id', db.Integer, db.ForeignKey('parent.parent_id'), primary_key=True)
)

professor_student = db.Table('professor_student',
    db.Column('professor_id', db.Integer, db.ForeignKey('professor.professor_id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
)

student_course = db.Table('student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.course_id'), primary_key=True)
)

marks = db.Table('marks',
    db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'), primary_key=True),
    db.Column('professor_id', db.Integer, db.ForeignKey('professor.professor_id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.course_id'), primary_key=True),
    db.Column('mark', db.Numeric(5, 2), nullable=False)
)

student_classroom = db.Table('student_classroom',
    db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'), primary_key=True),
    db.Column('room_number', db.String(20), db.ForeignKey('classroom.room_number'), primary_key=True)
)

professor_classroom = db.Table('professor_classroom',
    db.Column('professor_id', db.Integer, db.ForeignKey('professor.professor_id'), primary_key=True),
    db.Column('room_number', db.String(20), db.ForeignKey('classroom.room_number'), primary_key=True)
)

parent_attendance_view = db.Table('parent_attendance_view',
    db.Column('parent_id', db.Integer, db.ForeignKey('parent.parent_id'), primary_key=True),
    db.Column('attendance_id', db.Integer, db.ForeignKey('attendance.attendance_id'), primary_key=True)
)

professor_attendance_view = db.Table('professor_attendance_view',
    db.Column('professor_id', db.Integer, db.ForeignKey('professor.professor_id'), primary_key=True),
    db.Column('attendance_id', db.Integer, db.ForeignKey('attendance.attendance_id'), primary_key=True)
)

admin_attendance = db.Table('admin_attendance',
    db.Column('admin_id', db.Integer, db.ForeignKey('admin.admin_id'), primary_key=True),
    db.Column('attendance_id', db.Integer, db.ForeignKey('attendance.attendance_id'), primary_key=True)
)

