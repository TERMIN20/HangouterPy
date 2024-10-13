from operator import index

from flask import Flask, render_template, request, redirect
import sqlite3
import socket


user = "anonymous"
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

# Add Tables to db
cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS eventdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    activityname VARCHAR(255) NOT NULL,
    date VARCHAR(255) NOT NULL
)
""")






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
    # connect to db server
    users = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    users.connect(("localhost", 9999))

    nullcode = "/~n"
    inputU = request.args["username"]
    inputP = request.args["password"]

    message = users.recv(1024).decode()
    while message != "UsernameReq":
        users.send(nullcode.encode())
        message = users.recv(1024).decode()
        print("lookingUserReq" + message)

    users.send(inputU.encode())
    message = users.recv(1024).decode()
    users.send(inputP.encode())
    print("sent")
    status = users.recv(1024).decode()
    if status == "successful":
        print("yay")
        user = inputU

    users.close()
    # Code to compare correct password with user input
    # username =
    # password =
    # if inputU == username:
    #     return render_template('schedule.html')
    # else:
    # Failed login case: I have it set to reload the login page as a placeholder for now
    return redirect('/schedule')

@app.route('/input')
def input():
    return render_template('input.html')
    #date = request.args["start"]
    #print(date)

def eventsUpdate():
    events.clear()
    for row in  cur.execute("SELECT activityname, date FROM eventdata ORDER BY id"):
        print(row[0], row[1])
        events.append({'activityName': row[0], 'date': row[1]})

@app.route('/submit2', methods =["GET"])
def submit2():
    users = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    users.connect(("localhost", 9999))

    activityName = request.args["activityName"]
    date = request.args["start"]
    print(date)

    message = users.recv(1024).decode()
    print(message)
    while message != "EventReq":
        users.send("/~n".encode())
        message = users.recv(1024).decode()
        print(message)
    users.send(activityName.encode())
    message = users.recv(1024).decode()
    print(message)
    users.send(date.encode())
    message = users.recv(1024).decode()
    print(message)
    users.send(user.encode())

    eventsUpdate()

    return redirect('/schedule')