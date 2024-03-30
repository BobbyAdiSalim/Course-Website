from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
