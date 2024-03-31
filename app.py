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

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    name = db.Column(db.String(250), nullable = False)
    date_created = db.Column(db.Date)

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
    return render_template("news.html", news = True)

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

@app.route("/feedback")
def feedback():
    if not isStudent(session):
        return redirect('/')
    return render_template("feedback.html", feedback = True)

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

        return "Success"



@app.route('/loginInstructor')
def login_instructor():
    session["auth"] = "Instructor"
    session["name"] = "Dummy Ins"
    return "You are instructor now, love you"


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
                        session["auth"] = "student"
                        session["name"] = student.name
                        return redirect("/")
            else:
                instructor = Instructor.query.filter_by(username = input_username).first()
                if(instructor):
                    hashed_password = instructor.password
                    if bcrypt.check_password_hash(hashed_password, input_password):
                        session["auth"] = "instructor"
                        session["name"] = instructor.name
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
        students = Student.query.all()
        return render_template("modify_assignment.html", lst_tests = lst_tests, grades = True, lst_grades = lst_grades)
    # grades = Grades.query.filter_by(username = session["username"]).get()
    return render_template("grades.html", lst_tests = lst_tests, grades = True, lst_grades = lst_grades)


@app.route('/grades/<test_id>', methods = ["GET", "POST"])
def edit_grades(test_id):

    if(not isInstructor(session)):
        return redirect('/')
    
    if(request.method == "GET"):
        lst_student_grades = Grades.query.filter_by(test_id = test_id).all()
        lst_student = Student.query.all()
        return render_template('update_grades.html', lst_student_grades = lst_student_grades, lst_student = lst_student, test_id = test_id)

    if(request.method == "POST"):
        lst_students = Student.query.all()
        for student in lst_students:
            grade = request.form["student"+str(student.id)+"_grade"]
            grade_before = Grades.query.f9ilter(Grades.student_id == student.id and Grades.test_id == test_id).first()
            if(grade_before):
                db.session.query(Grades).filter(Grades.student_id == student.id and Grades.test_id == test_id).update({'grade' : grade})
            else:
                new_grade = Grades(student_id = student.id, test_id = test_id, grade = grade)
                db.session.add(new_grade)

        db.session.commit()

@app.route('/grades/<test_id>/delete')
def delete_test(test_id):
    if(not isInstructor(session)):
       return redirect('/')
    test = Test.query.filter_by(id = test_id).first()
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