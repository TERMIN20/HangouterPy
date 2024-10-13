from flask import Flask, render_template
app = Flask('Hangouter')

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/schedule")
def schedule():
    return render_template('')