from flask import Flask, render_template
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
def home():
    return render_template('index.html')
@app.route("/schedule")
def schedule():
    return render_template('schedule.html', events = events)