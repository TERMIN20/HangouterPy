from flask import Flask, render_template, request

app = Flask('Hangouter')

events = [
    {
        'activityName' : 'sample Name',
        'date' : '2024-10-13',
    },
    {
        'activityName' : 'sleepy',
        'date' : '2024-10-12',
    }
]


@app.route("/")
# uses index.html webpage
def home():
    return render_template('index.html')


# returns username and password
def get():
    return render_template_string(open('login.html').read())


@app.route("/schedule")
def schedule():
    return render_template('schedule.html', events=events)


@app.route("/login")
def login():
    return render_template('login.html')


# handles the submission of the login page
@app.route('/submit', methods=["GET"])
def submit():
    inputU = request.args["username"]
    inputP = request.args["password"]
    # Code to compare correct password with user input
    # username =
    # password =
    # if inputU == username:
    #     return render_template('schedule.html')
    # else:
    #     return render_template('login.html')
app.route('/input', methods=["GET"])
def input():
    date = request.args.get["start"]
    print(date)