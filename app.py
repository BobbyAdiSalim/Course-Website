from flask import (
    Flask, 
    render_template, 
    request, 
    url_for,
    session,
    abort,
    flash,
    redirect
    )

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///assignment3.db'
app.config["SECRET_KEY"] = "HJSCYIGA1982UYCH2C78E2BCGWGVXFTGbYDXGUBAJGDWUYGVDXGvjgsjVGGHJDWI"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    name = db.Column(db.String(250), nullable = False)
    date_created = db.Column(db.Date, default = datetime.utcnow)
    grades = db.relationship("Grades", backref = 'student', lazy = True)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = True)
    name = db.Column(db.String(250), nullable = False)
    desc = db.Column(db.Text)
    weight = db.Column(db.Integer, nullable = False)
    due_date = db.Column(db.Date)
    grades = db.relationship("Grades", backref = 'test', lazy = True)

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable = False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable = False)
    grade = db.Column(db.Float, nullable = False)
    remarks = db.relationship("RemarkRequest", backref ='grade', lazy = True)

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    name = db.Column(db.String(250), nullable = False)
    date_created = db.Column(db.Date)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable = False)
    text = db.Column(db.Text)
    date_created = db.Column(db.Date, default = datetime.utcnow)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    feedback1 = db.Column(db.Text)
    feedback2 = db.Column(db.Text)
    feedback3 = db.Column(db.Text)
    feedback4 = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable = False)
    date_created = db.Column(db.Date, default = datetime.utcnow)

class RemarkRequest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'),nullable =False)
    desc = db.Column(db.Text)
    solved = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.Date, default = datetime.utcnow)

def isInstructor(identity):
    if "auth" in identity and identity["auth"] == 'Instructor':
        return True
    return False

def isStudent(identity):
    if "auth" in identity and identity["auth"] == 'Student':
        return True
    return False

@app.route("/")
def home():
    return render_template("index.html", home = True)

@app.route("/labs")
def labs():
    if not isInstructor(session) and not isStudent(session):
        return redirect('/')
    return render_template("labs.html", labs = True)

@app.route("/news")
def news():
    if not isInstructor(session) and not isStudent(session):
        return redirect('/')
    lst_news = Announcement.query.order_by(Announcement.id.desc()).all()
    return render_template("news.html", news = True, lst_news = lst_news)
    

@app.route('/news/add', methods =["GET", "POST"])
def news_add():
    if not isInstructor(session):
        return redirect('/')
    
    if request.method == "GET":
        return render_template("news_add.html", news = True)
    
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
    
        news = Announcement(title = title, text = text)
        db.session.add(news)
        db.session.commit()

        flash("Announcement " + title + " is live now!", "Success")
        return redirect("/news")

@app.route("/calendar")
def calendar():
    if not isInstructor(session) and not isStudent(session):
        return redirect('/')
    return render_template("calendar.html", calendar = True)

@app.route("/lectures")
def lectures():
    if not isInstructor(session) and not isStudent(session):
        return redirect('/')
    return render_template("lectures.html", lectures = True)

@app.route("/assignments")
def assignments():
    if not isInstructor(session) and not isStudent(session):
        return redirect('/')
    return render_template("assignments.html", assignments = True)

@app.route("/tests")
def tests():
    if not isInstructor(session) and not isStudent(session):
        return redirect('/')
    return render_template("tests.html", tests = True)

@app.route("/team")
def team():
    if not isInstructor(session) and not isStudent(session):
        return redirect('/')
    return render_template("team.html", team = True)

@app.route("/resources")
def resources():
    if not isStudent(session) and not isInstructor(session):
        return redirect('/')
    return render_template("resources.html", resources = True)

@app.route("/feedback", methods = ["GET", "POST"])
def feedback():

    if not isStudent(session) and not isInstructor(session):
        return redirect('/')
    
    if request.method == "GET":
        if isStudent(session):
            instructors = Instructor.query.all()
            return render_template("feedback.html", feedback = True, instructors = instructors)

        if isInstructor(session):
            
            lst_feedbacks = db.paginate(Feedback.query.order_by(Feedback.id.desc()).filter(Feedback.instructor_id == session["instructor_id"]))
            lst_pagination = lst_feedbacks.iter_pages()
            return render_template("feedback_view.html", feedback = True, lst_feedbacks = lst_feedbacks, lst_pagination = lst_pagination)

    if request.method == "POST":
        instructor_id = request.form["instructor_id"]
        feedback1 = request.form["feedback-1"]
        feedback2 = request.form["feedback-2"]
        feedback3 = request.form["feedback-3"]
        feedback4 = request.form["feedback-4"]

        if feedback1 == '' or feedback2 == '' or feedback3 == '' or feedback4 == '':
            flash("Please fill in all the box", "Failed")
            return redirect('/feedback')

        feedback = Feedback(
            instructor_id = instructor_id,
            feedback1 = feedback1,
            feedback2 = feedback2, 
            feedback3 = feedback3, 
            feedback4 = feedback4
            )

        db.session.add(feedback)
        db.session.commit()

        flash("Feedback submitted", "Success")
        return redirect('/feedback')
    


@app.route('/login', methods = ["GET", "POST"])
def login():
    if isInstructor(session) or isStudent(session):
         return redirect('/')
    
    if(request.method == "GET"):
        return render_template("login.html")

    if(request.method == "POST"):
        if('username' in request.form) and ('password' in request.form):

            input_username = request.form["username"]
            input_password = request.form["password"]
            input_status = request.form["status"]

            if(input_status == "Student"):
                student = Student.query.filter_by(username = input_username).first()
                if(student):
                    hashed_password = student.password
                    if bcrypt.check_password_hash(hashed_password, input_password):
                        session["auth"] = "Student"
                        session["name"] = student.name
                        session["student_id"] = student.id
                        return redirect("/")
            else:
                instructor = Instructor.query.filter_by(username = input_username).first()
                if(instructor):
                    hashed_password = instructor.password
                    if bcrypt.check_password_hash(hashed_password, input_password):
                        session["auth"] = "Instructor"
                        session["name"] = instructor.name
                        session["instructor_id"] = instructor.id
                        return redirect("/")
            
            flash("Login failed! Invalid credentials", "Failed")
            return redirect("/login")

    pass

@app.route('/register', methods = ["GET", "POST"])
def register():
    if isInstructor(session) or isStudent(session):
        return redirect('/')
    
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        lst_usernames = Student.query.with_entities(Student.username).all()

        input_username = request.form["username"]
        input_password = bcrypt.generate_password_hash(request.form["password"])
        input_name = request.form["name"]
        if (input_username == "" or input_password == "" or input_name ==""):
            flash("Invalid username and password!", "Invalid Input")
            return redirect('/register')
        
        if(input_username in lst_usernames):
            flash("Username already taken", "Invalid Input")
            return redirect('/register')
        
        # Done check now create
        new_student = Student(username = input_username, password = input_password, name = input_name)
        db.session.add(new_student)
        db.session.commit()

        flash("Account created! Please login", "Register Success")
        return redirect('/login')

@app.route('/logout')
def logout():
    if "auth" in session:
        session.pop("auth", default=None)
    if "name" in session:
        session.pop("name", default=None)
    return redirect('/')


@app.route('/grades')
def view():
    lst_tests = Test.query.all()
    lst_grades = None
    if(isInstructor(session)):
        students = Student.query.order_by(Student.name.asc()).all()
        return render_template("modify_assignment.html", lst_tests = lst_tests, grades = True, lst_grades = lst_grades)
    # grades = Grades.query.filter_by(username = session["username"]).get()

    if(isStudent(session)):
        grades = Grades.query.filter(Grades.student_id == session["student_id"]).all()
        lst_of_tuple = []

        for test in lst_tests:
            found = False
            for grade in grades:
                if grade.test.id == test.id:
                    found = True
                    lst_of_tuple.append((test, str(grade.grade) + '/100'))
            if not found:
                lst_of_tuple.append((test, 'Not graded yet'))

        return render_template("grades.html", lst_of_tuple = lst_of_tuple, lst_tests = lst_tests, grades = True, lst_grades = lst_grades)

    return redirect('/')

@app.route('/grades/<test_id>', methods = ["GET", "POST"])
def edit_grades(test_id):

    if(not isInstructor(session)):
        return redirect('/')
    
    if(request.method == "GET"):
        lst_student_grades = Grades.query.filter_by(test_id = test_id).all()
        lst_student = Student.query.order_by(Student.name.asc()).all()
        search = request.args.get('search')
        if search:
            lst_student = Student.query.order_by(Student.name.asc()).filter(Student.name.like(f"%{search}%")).all()
            lst_student.extend(Student.query.order_by(Student.name.asc()).filter(Student.id.like(f"%{search}%")).all())
        if not search:
            search = ''

        lst_tuple_student_grade = []
        for student in lst_student:
            found = False
            for grade in lst_student_grades:
                if student.id == grade.student.id:
                    found = True
                    lst_tuple_student_grade.append((student, grade.grade))
                    break

            if not found:
                lst_tuple_student_grade.append((student, None))

        return render_template('update_grades.html', search = search, lst_tuple_student_grade = lst_tuple_student_grade, test_id = test_id)

    if(request.method == "POST"):
        lst_students = Student.query.all()
        for student in lst_students:
            keyword = "student"+str(student.id)+"_grade"
            if keyword not in request.form or request.form[keyword] == '': 
                continue
            grade = request.form[keyword]
            grade_before = Grades.query.filter(Grades.student_id == student.id).filter(Grades.test_id == test_id).first()
            if(grade_before):
                db.session.query(Grades).filter(Grades.student_id == student.id and Grades.test_id == test_id).update({'grade' : grade})
            else:
                new_grade = Grades(student_id = student.id, test_id = test_id, grade = grade)
                db.session.add(new_grade)

        db.session.commit()
        flash("Successfuly updated student grade", "Success")
        return redirect('/grades/'+str(test_id))

@app.route('/grades/add', methods = ["GET", "POST"])
def addtest():
    if not isInstructor(session):
        return redirect('/')
    if request.method == 'GET':
        return render_template("tests_add.html")
    else:
        # Do something here
        name = request.form["name"]
        desc = request.form["desc"]
        weight = request.form["weight"]
        due_date = request.form["due_date"]

        # Convert to SQLite date
        if(due_date != ""):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        else:
            due_date = None
        test = Test(name = name, desc = desc, due_date = due_date, weight = weight)
        db.session.add(test)
        db.session.commit()

        flash("Successfully added " + name, "Success")
        return redirect('/grades')


@app.route('/grades/<test_id>/edit', methods = ["GET", "POST"])
def updatetest(test_id):
    if not isInstructor(session):
        return redirect('/')
    
    if request.method == 'GET':
        test = Test.query.filter_by(id = test_id).first()
        if(test.due_date):
            test.due_date = test.due_date.strftime('%Y-%m-%d')
        else:
            test.due_date = ''
        return render_template("tests_edit.html", test = test)
    else:
        # Do something here
        name = request.form["name"]
        desc = request.form["desc"]
        weight = request.form["weight"]
        due_date = request.form["due_date"]

        # Convert to SQLite date
        if(due_date != ""):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        else:
            due_date = None

        to_update = {
            'name': name,
            'desc': desc,
            'weight': weight,
            'due_date': due_date
        }

        db.session.query(Test).filter(Test.id == test_id).update(to_update)
        db.session.commit()

        flash("Successfully updated " + name, "Success")
        return redirect('/grades')


@app.route('/grades/<test_id>/delete')
def delete_test(test_id):
    if(not isInstructor(session)):
       return redirect('/')
    test = Test.query.filter_by(id = test_id).first()

    related_grades = Grades.query.filter_by(test_id = test_id).all()

    for grade in related_grades:
        db.session.delete(grade)
    db.session.delete(test)
    db.session.commit()

    flash("Delete succeed", "Success")
    return redirect("/grades")

if __name__ == "__main__":
    app.run(debug=True)


# app.app_context().push()
# student1 = Student(... = ....)
# db.session.add(student1)
# db.session.commit()
    

# student1 = Student(name = "Daniel Stevanus", username="student1", 
#                     password = bcrypt.generate_password_hash("student1"),
#                     )

# student2 = Student(name = "Bobby Adi Salim", username="student2", 
#                     password = bcrypt.generate_password_hash("student2"),
#                     )

# student3 = Student(name = "Ariella Siahaan", username="student3", 
#                     password = bcrypt.generate_password_hash("student3"),
#                     )
    
# instructor1 = Instructor(name = "Purva Gawde", username="instructor1", 
#                     password = bcrypt.generate_password_hash("instructor1"),
#                     )
    
# instructor2 = Instructor(name = "Pourya Moghadam", username="instructor2", 
#                     password = bcrypt.generate_password_hash("instructor2"),
#                     )