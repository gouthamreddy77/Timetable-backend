from ttg import db, login_manager
from flask_login import UserMixin
from sqlalchemy import inspect

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(20),nullable=False)
    username=db.Column(db.String(20),unique=True,nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

# productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)

class Department(db.Model):
    # __table_args__ = {'extend_existing': True}
    dept_id = db.Column(db.Integer,primary_key=True)
    dept_name = db.Column(db.String(10),unique=True,nullable=False)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Room(db.Model):
    # __table_args__ = {'extend_existing': True}
    room_id = db.Column(db.Integer,primary_key=True)
    room_no = db.Column(db.Integer,unique=True,nullable=False)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Batch(db.Model):
    # __table_args__ = {'extend_existing': True}
    batch_id = db.Column(db.Integer,primary_key=True)
    year = db.Column(db.Integer,nullable=False)
    dept_name = db.Column(db.String(10), db.ForeignKey('department.dept_name'), nullable=False)
    section = db.Column(db.Integer,nullable=False)
    non_empty_slots = db.Column(db.Integer,nullable=True)
    room_no = db.Column(db.Integer,db.ForeignKey('room.room_no'),nullable=False)
    def __repr__(self):
        return str(self.year)+" "+str(self.dept_name)+" "+str(self.section) # IV CSE 2
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


class Professor(db.Model):
    # __table_args__ = {'extend_existing': True}
    professor_id = db.Column(db.String(20),primary_key=True)
    professor_name = db.Column(db.String(50),unique=True,nullable=False)
    # prof_courses = db.Column(db.String(100),unique=True,nullable=False)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Course(db.Model):
    # __table_args__ = {'extend_existing': True}
    course_id = db.Column(db.String(20),primary_key=True)
    course_name = db.Column(db.String(50),unique=True,nullable=False)
    course_short_form = db.Column(db.String(10),unique=True,nullable=False)
    course_type = db.Column(db.String(10),nullable=False)
    duration = db.Column(db.Integer,nullable=True)
    frequency = db.Column(db.Integer,nullable=True)
    preferred_rooms =db.Column(db.Integer, db.ForeignKey('room.room_no'), nullable=False)
    def __repr__(self):
        return str(self.course_short_form)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Lectures(db.Model):
    # __table_args__ = {'extend_existing': True}
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.batch_id'), nullable=False,primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False,primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.professor_id'), nullable=False,primary_key=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Labs(db.Model):
    # __table_args__ = {'extend_existing': True}
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.batch_id'), nullable=False,primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False,primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.professor_id'), nullable=False,primary_key=True)
    can_be_paired = db.Column(db.Integer,nullable=False)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Electives(db.Model):
    # __table_args__ = {'extend_existing': True}
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False,primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.professor_id'), nullable=False,primary_key=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


# TODO: Create [Room & Branch] Class According to USE CASE

class Data:

    def __new__(cls, *args, **kwargs):
        temp = object.__new__(cls)
        return temp

    def __init__(self):
        self.batch = None
        self.course = None
        self.faculty = None
        self.slots = None
        self.room = []
        self.batch_check = None
        self.faculty_check = None
        self.room_check = None
        self.duration = None
        self.frequency = None
        self.can_change_time = None
        self.can_change_day = None
        self.is_pseudo = False
        self.is_compound = False
        self.is_lab = False
        self.is_jnr = None

    def create_lecture_data(self, batch, course, faculty):
        self.batch = batch
        self.course = course
        self.faculty = faculty

        # Initiation
        self.room = list(batch)[0].room_no
        self.duration = list(course)[0].duration
        self.frequency = list(course)[0].frequency
        self.batch_check = True
        self.room_check = False
        self.faculty_check = True
        self.can_change_day = True
        self.can_change_time = True
        self.is_jnr = True if((list(batch)[0].year) == 1) else False

        # Misc
        for b in batch:
            b.non_empty_slots += self.duration * self.frequency

        return self

    def create_lab_data(self, batch, course, faculty, duration, frequency):
        self.batch = batch
        self.course = course
        self.faculty = faculty

        # Initiation
        # self.room = []
        # for _ in course:
        #     self.room.append(list(_.preferred_rooms))
        self.duration = duration
        self.frequency = frequency
        self.batch_check = True
        self.room_check = True
        self.faculty_check = True
        self.can_change_day = True
        self.can_change_time = True
        self.is_lab = True
        self.is_jnr = True if((list(batch)[0].year) == 1) else False

        # Misc
        for b in batch:
            b.non_empty_slots += self.duration * self.frequency

        return self

    def create_compound_data(self, batch, course):
        self.batch = batch
        self.course = course

        # Initiation
        self.duration = list(course)[0].duration
        self.frequency = list(course)[0].frequency
        self.batch_check = True
        self.room_check = False
        self.faculty_check = False
        self.can_change_day = True
        self.can_change_time = True
        self.is_compound = True
        self.is_jnr = True if((list(batch)[0].year) == 1) else False

        # Misc
        for b in batch:
            b.non_empty_slots += self.duration * self.frequency

        return self

    def create_pseudo_data(self, batch, duration, frequency):
        self.batch = batch

        # Initiation
        self.duration = duration
        self.frequency = frequency
        self.room = list(batch)[0].room_no
        self.batch_check = True
        self.room_check = False
        self.faculty_check = False
        self.can_change_day = True
        self.can_change_time = False
        self.is_pseudo = True
        self.is_jnr = True if((list(batch)[0].year) == 1) else False

        return self
