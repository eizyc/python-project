import hashlib
import json
from app import app, db
from flask import request
from app.models import Student, Fee, Result, Course, Subject

# student 
@app.route('/add-student', methods=['GET'])
def add_user():
    if request.method == 'GET':
          name = request.args.get('name')
          email = request.args.get('email')
          gender = request.args.get('gender')
          date_of_birth = request.args.get('date_of_birth')
          address = request.args.get('address')
          status = request.args.get('status')
          roll_id = request.args.get('roll_id')
          phone_number = request.args.get('phone_number')
          password = hashlib.md5(request.args.get('password').encode('utf-8')).hexdigest()
          username = request.args.get('username')
          student = Student(name, email, gender, date_of_birth, address, roll_id, status, phone_number, password, username)
          db.session.add(student)
          db.session.commit()

          return "SUCCESS ADD STUDENT \n" + json.dumps({
              "name": student.student_name,
              "student_id": student.student_id,
              "password": student.password,
              "email": student.student_name,
              "username": student.username
          })


@app.route('/update-student', methods=['POST'])
def update_student():
     if request.method == 'POST':
          student_id = request.form.get('student_id')
          data = json.loads(request.form.get('data'))
          res = db.session.query(Student).filter_by(student_id=student_id).first()
          for col_name in data.keys():
            if col_name in Student.__dict__.keys():
              setattr(res, col_name, data[col_name])
          db.session.commit()
          return json.dumps(res.serialize)


# fee
@app.route('/fee-list', methods=['GET'])
def fee_list():
     data = None
     if request.method == 'GET':
          student_id = request.args.get('student_id')
          fee_id = request.args.get('fee_id')
          scolarship_status = request.args.get('scolarship_status')
          fees_status = request.args.get('fees_status')
          query = db.session.query(Fee)
          if fee_id: 
            query = query.filter_by(id=fee_id)
          if student_id:
            query = query.filter_by(student_id=student_id)
          if fees_status:
              query = query.filter_by(fees_status=fees_status)
          if scolarship_status:
              query = query.filter_by(scolarship_status=scolarship_status).all()
          res = query.all() 
          data = [i.serialize for i in res]
          return json.dumps(data)  

@app.route('/add-fee', methods=['POST'])
def add_fee():
      fees_status = request.form.get('fees_status')
      scolarship_status = request.form.get('scolarship_status')
      student_id = request.form.get('student_id')
      if fees_status and scolarship_status and student_id:
           fee = Fee(fees_status, scolarship_status, student_id)
           db.session.add(fee)
           db.session.commit()
           return json.dumps(fee.serialize)
      
@app.route('/update-fee', methods=['POST'])
def update_fee():
      data = None
      record_id = request.form.get('fee_id')
      fees_status = request.form.get('fees_status')
      scolarship_status = request.form.get('scolarship_status')
      if record_id == None:
        return None
      data = db.session.query(Fee).filter_by( id=record_id ).first()
      if fees_status: 
          data.fees_status = fees_status
      if scolarship_status:
          data.scolarship_status = scolarship_status
      db.session.commit()
      return json.dumps(data.serialize)     


@app.route('/delete-fee', methods=['POST'])
def delete_fee():
      fee_id = request.form.get('fee_id')
      if fee_id:
          data = db.session.query(Fee).filter_by( id=fee_id ).first()
          db.session.delete(data)
      db.session.commit()
      return json.dumps(data.serialize)


# course 
@app.route('/add-course', methods=['GET'])
def add_course():
    if request.method == 'GET':
          course_name = request.args.get('course_name')
          section = request.args.get('section') 
          course = Course(course_name, section)
          db.session.add(course)
          db.session.commit()
          return json.dumps(course.serialize)
    
@app.route('/course-list', methods=['GET'])
def course_list():
    if request.method == 'GET':
          res = db.session.query(Course).all()
          data = [i.serialize for i in res]
          return json.dumps(data)


@app.route('/course-students', methods=['GET'])
def course_students():
    if request.method == 'GET':
          course_id = request.args.get('course_id')
          res = db.session.query(Course).filter_by(id=course_id).first()
          result = db.session.query(Result).filter_by(course_id=course_id).join(Student).all()
          return json.dumps({
              "course-info":res.serialize,
              "students": [i.student.serialize for i in result]
          })
    

# record          
@app.route('/record-list', methods=['GET'])
def get_record():
    if request.method == 'GET':
        data = None
        course_id = request.args.get('course_id')
        student_id = request.args.get('student_id')
        subject_id = request.args.get('subject_id')
        record_id = request.args.get('record_id')
        query = db.session.query(Result)
        if student_id: 
            query = query.filter_by(student_id=student_id)
        if course_id:
            query = query.filter_by(course_id=course_id)
        if subject_id:
            query = query.filter_by(subject_id=subject_id)
        if record_id:
            query = query.filter_by(id=record_id)
        res = query.all()
        data = [ dict(i.serialize | {"course": i.course.serialize}) for i in res]
        return json.dumps(data)

@app.route('/add-record', methods=['POST'])
def add_record():
      course_id = request.form.get('course_id')
      student_id = request.form.get('student_id')
      subject_id = request.form.get('subject_id')
      marks = request.form.get('marks')
      if student_id and course_id: 
          result = Result(student_id, course_id, marks, subject_id)
          db.session.add(result)
          db.session.commit()
          return json.dumps({
              "result": result.serialize,
              "student": result.student.serialize
          })

@app.route('/update-record', methods=['POST'])
def update_record():
      data = None
      record_id = request.form.get('record_id')
      marks = request.form.get('marks')
      if record_id and marks: 
          data = db.session.query(Result).filter_by( id=record_id ).first()
          data.marks = marks
          db.session.commit()
          return json.dumps({
              "record": data.serialize,
              "student": data.student.serialize,
          })

@app.route('/delete-record', methods=['POST'])
def delete_record():
      data = None
      record_id = request.form.get('record_id')
      if record_id: 
          data = db.session.query(Result).filter_by( id=record_id ).first()
          db.session.delete(data)
      db.session.commit()
      return json.dumps(data.serialize)

# subject
@app.route('/add-subject', methods=['POST'])
def add_subject():
      subject_name = request.form.get('subject_name')
      subject_code = request.form.get('subject_code')
      if subject_name and subject_name: 
          subject = Subject(subject_name, subject_code)
          db.session.add(subject)
          db.session.commit()
          return json.dumps(subject.serialize)
      

@app.route('/subject-list', methods=['GET'])   
def get_subject():
    if request.method == 'GET':
        data = None
        subject_id = request.args.get('subject_id')
        subject_code = request.args.get('subject_code')
        subject_name = request.args.get('subject_name')
        query = db.session.query(Subject)
        if subject_id: 
            query = query.filter_by(id=subject_id)
        if subject_code:
            query = query.filter_by(subject_code=subject_code)
        if subject_name:
            query = query.filter_by(subject_name=subject_name)
        res = query.all()
        data = [i.serialize for i in res]
        return json.dumps(data)
    
@app.route('/update-subject', methods=['POST'])
def update_subject():
      data = None
      subject_id = request.form.get('subject_id')
      subject_code = request.form.get('subject_code')
      subject_name = request.form.get('subject_name')
      if subject_id: 
          data = db.session.query(Subject).filter_by( id=subject_id ).first()
      if data == None:
          return "None"
      if subject_code:
          data.subject_code = subject_code
      if subject_name:
          data.subject_name = subject_name
      db.session.commit()
      return json.dumps(data.serialize)

@app.route('/delete-subject', methods=['POST'])
def delete_subject():
      data = None
      subject_id = request.form.get('subject_id')
      if subject_id: 
          data = db.session.query(Subject).filter_by( id=subject_id ).first()
          db.session.delete(data)
      db.session.commit()
      return json.dumps(data.serialize)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")