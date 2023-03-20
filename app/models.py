from app import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'STUDENTS'
    student_id = db.Column(db.Integer, primary_key = True)
    student_name = db.Column(db.String(255))
    student_email = db.Column(db.String(255), unique=True)
    gender = db.Column(db.String(255))
    date_of_birth = db.Column(db.String(255))
    address = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    updation_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    roll_id = db.Column(db.Integer, unique=True)
    status = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    password = db.Column(db.String(255))
    username = db.Column(db.String(255))
    results = db.relationship('Result', backref='student', lazy=True)

    def __init__(self, name, email, gender, date_of_birth, address, roll_id, status, phone_number, password, username):
        self.student_name = name
        self.student_email = email
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.address = address
        self.roll_id = roll_id
        self.status = status
        self.phone_number = phone_number
        self.password = password
        self.username = username
    
    @property
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    


class Fee(db.Model):
    __tablename__ = 'FEES'
    id = db.Column(db.Integer, primary_key = True)
    fees_status = db.Column(db.String(255))
    scolarship_status = db.Column(db.String(255))
    student_id = db.Column(db.Integer, db.ForeignKey('STUDENTS.student_id'))

    def __init__(self, fees_status, scolarship_status, student_id):
        self.fees_status = fees_status
        self.scolarship_status = scolarship_status
        self.student_id = student_id
    
    @property
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    

class Course(db.Model):
    __tablename__ = 'COURSES'
    id = db.Column(db.Integer, primary_key = True)
    course_name = db.Column(db.String(255))
    section = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    updation_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    results = db.relationship('Result', backref='course', lazy=True)

    def __init__(self, course_name, section):
        self.course_name = course_name
        self.section = section

    @property
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Subject(db.Model):
    __tablename__ = 'SUBJECTS'
    id = db.Column(db.Integer, primary_key = True)
    subject_name = db.Column(db.String(255))
    subject_code = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    updation_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    results = db.relationship('Result', backref='subject', lazy=False)

    def __init__(self, subject_name, subject_code):
        self.subject_name = subject_name
        self.subject_code = subject_code

    @property
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class SubjectCombination(db.Model):
    __tablename__ = 'SUBJECT_COMBINATION'
    id = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.Integer, db.ForeignKey('COURSES.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('SUBJECTS.id'))
    status = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    updation_date = db.Column(db.DateTime, default=datetime.utcnow ,onupdate=datetime.utcnow)

    @property
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Result(db.Model):
    __tablename__ = 'RESULT'
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('STUDENTS.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('COURSES.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('SUBJECTS.id'))
    marks = db.Column(db.Integer)
    posting_date = db.Column(db.DateTime, default=datetime.utcnow)
    updation_date = db.Column(db.DateTime, default=datetime.utcnow ,onupdate=datetime.utcnow)

    def __init__(self, student_id, course_id, marks ,subject_id):
        self.course_id = course_id
        self.student_id = student_id
        self.marks = marks
        self.subject_id = subject_id
    
    @property
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}