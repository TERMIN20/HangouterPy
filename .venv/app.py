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
#def get():
    #return render_template_string(open('login.html').read())


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
    print(inputP)
    # Code to compare correct password with user input
    # username =
    # password =
    # if inputU == username:
    return render_template('schedule.html', events=events)
    # else:
    #     return render_template('login.html')

@app.route('/input')
def input():
    return render_template('input.html')
    #date = request.args["start"]
    #print(date)

@app.route('/submit2', methods =["GET"])
def submit2():
    ctivityName = request.args["activityName"]
    date = request.args["start"]
    print(date)
    events.append({'activityName' : ctivityName,
                     'date' : date})
    return render_template('schedule.html', events=events)
