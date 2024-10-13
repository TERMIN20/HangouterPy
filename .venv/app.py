from operator import index

from flask import Flask, render_template, request, redirect
import sqlite3
import socket

conn = sqlite3.connect("users.db")
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


#connect to db server
users = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
users.connect(("localhost", 9999))


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
    message = users.recv(1024).decode()
    users.send(inputU.encode())
    message = users.recv(1024).decode()
    users.send(inputP.encode())
    status = users.recv(1024).decode()
    if status == "successful":
        print("yay")
    # Code to compare correct password with user input
    # username =
    # password =
    # if inputU == username:
    #     return render_template('schedule.html')
    # else:
    # Failed login case: I have it set to reload the login page as a placeholder for now
    return render_template('login.html')

@app.route('/input')
def input():
    return render_template('input.html')
    #date = request.args["start"]
    #print(date)

@app.route('/submit2', methods =["GET"])
def submit2():
    activityName = request.args["activityName"]
    date = request.args["start"]
    print(date)
    return redirect('/schedule')