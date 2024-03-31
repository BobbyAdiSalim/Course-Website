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
    grades = db.relationship("Grades")

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = True)
    name = db.Column(db.String(250), nullable = False)
    desc = db.Column(db.Text)
    weight = db.Column(db.Integer, nullable = False)
    due_date = db.Column(db.Date)
    grades = db.relationship("Grades")

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable = False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable = False)

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    name = db.Column(db.String(250), nullable = False)
    date_created = db.Column(db.Date)


@app.route("/")
def home():
    return render_template("index.html", home = True)

@app.route("/labs")
def labs():
    if "auth" not in session:
        return redirect('/')
    return render_template("labs.html", labs = True)

@app.route("/news")
def news():
    if "auth" not in session:
        return redirect('/')
    return render_template("news.html", news = True)

@app.route("/calendar")
def calendar():
    if "auth" not in session:
        return redirect('/')
    return render_template("calendar.html", calendar = True)

@app.route("/lectures")
def lectures():
    if "auth" not in session:
        return redirect('/')
    return render_template("lectures.html", lectures = True)

@app.route("/assignments")
def assignments():
    if "auth" not in session:
        return redirect('/')
    return render_template("assignments.html", assignments = True)

@app.route("/tests")
def tests():
    if "auth" not in session:
        return redirect('/')
    return render_template("tests.html", tests = True)

@app.route("/team")
def team():
    if "auth" not in session:
        return redirect('/')
    return render_template("team.html", team = True)

@app.route("/resources")
def resources():
    if "auth" not in session:
        return redirect('/')
    return render_template("resources.html", resources = True)

@app.route("/feedback")
def feedback():
    if "auth" not in session:
        return redirect('/')
    return render_template("feedback.html", feedback = True)

@app.route('/tests/add', methods = ["GET", "POST"])
def addtest():
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

@app.route('/grades')
def view():
    if("auth" in session and session["auth"] == 'instructor'):
        students = Student.query.all()
        return render_template("modify_grades.html", students = students)
        return render_template("modify_grades.html", students = students)
    lst_grades = None 
    # grades = Grades.query.filter_by(username = session["username"]).get()
    lst_tests = Test.query.all()
    return render_template("grades.html", lst_tests = lst_tests, grades = True, lst_grades = lst_grades)


@app.route('/loginInstructor')
def login_instructor():
    session["auth"] = "instructor"
    return "You are instructor now, love you"


@app.route('/login', methods = ["GET", "POST"])
def login():
    if "auth" in session:
        return redirect('/')
    
    if(request.method == "GET"):
        return render_template("login.html")

    if(request.method == "POST"):
        if('username' in request.form) and ('password' in request.form):

            input_username = request.form["username"]
            input_password = request.form["password"]
            
            student = Student.query.filter_by(username = input_username).first()
            if(student):
                hashed_password = student.password
                if bcrypt.check_password_hash(hashed_password, input_password):
                    session["auth"] = "student"
                    session["name"] = student.name
                    return redirect("/")
                
            return "login failed"

    pass

@app.route('/register', methods = ["GET", "POST"])
def register():
    pass


@app.route('/modify_grades')
def modify_grade():
    return render_template("modify_grades.html", grades = True)

@app.route('/logout')
def logout():
    session.pop("auth", default=None)
    session.pop("name", default=None)
    return redirect('/')
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