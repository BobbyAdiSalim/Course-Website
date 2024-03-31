from flask import (
    Flask, 
    render_template, 
    request, 
    url_for,
    session,
    abort,
    flash
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
    due_date = db.Column(db.Date)
    grades = db.relationship("Grades")

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable = False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable = False)

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, primary_key = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    name = db.Column(db.String(250), nullable = False)
    date_created = db.Column(db.Date)


@app.route("/")
def home():
    return render_template("index.html", home = True)

@app.route("/labs")
def labs():
    return render_template("labs.html", labs = True)

@app.route("/news")
def news():
    return render_template("news.html", news = True)

@app.route("/calendar")
def calendar():
    return render_template("calendar.html", calendar = True)

@app.route("/lectures")
def lectures():
    return render_template("lectures.html", lectures = True)

@app.route("/assignments")
def assignments():
    return render_template("assignments.html", assignments = True)

@app.route("/tests")
def tests():
    return render_template("tests.html", tests = True)

@app.route("/team")
def team():
    return render_template("team.html", team = True)

@app.route("/resources")
def resources():
    return render_template("resources.html", resources = True)

@app.route("/feedback")
def feedback():
    return render_template("feedback.html", feedback = True)

@app.route("/grades")
def grades():
    return render_template("grades.html", feedback = True)

@app.route('/tests/add', methods = ["GET", "POST"])
def addtest():
    if request.method == 'GET':
        return render_template("tests_add.html")
    else:
        # Do something here
        name = request.form["name"]
        desc = request.form["desc"]
        due_date = request.form["due_date"]

        # Convert to SQLite date
        if(due_date != ""):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

        test = Test(name = name, desc = desc, due_date = due_date)
        db.session.add(test)
        db.session.commit()

        return "Success"

@app.route('/grades')
def view():
    if(session["auth"] == 'instructor'):
        students = Student.query.all()
        return render_template("grades.html", students = students)
    grades = Grades.query.filter_by(username = session["username"]).get()
    tests = Test.query.all()
    return render_template("grades.html", tests = tests, grades = grades)

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