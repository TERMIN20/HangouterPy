from flask import Flask, render_template, request

app = Flask('Hangouter')


@app.route("/")
# uses index.html webpage
def home():
    return render_template('index.html')


# returns username and password
def form():
    return render_template_string(open('login.html').read())


@app.route("/schedule")
def schedule():
    return render_template('')


@app.route("/login")
def login():
    return render_template('login.html')


# handles the submission of the login page
@app.route('/submit', methods=["GET"])
def submit():
    username = request.args.get["username"]
    password = request.args.get["password"]
    print(username)
    print(password)
