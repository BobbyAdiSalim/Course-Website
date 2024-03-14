from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

@app.route("/<name>", methods = ["GET"])
def process_name(name):
    if name.isupper() and name.isalpha():
        greet = name.lower()
    elif name.islower() and name.isalpha():
        greet = name.upper()
    elif not name.isalpha():    
        greet = ''
        for char in name:
            if char.isalpha():
                greet = greet + char
    else:
            greet = name[:1].upper() + name[1:].lower()
    return "<html><body><h1>Welcome, "+ greet+ " to my CSCB20 website!</h1></body></html>"

if __name__ == "__main__":
    app.run(debug=True)