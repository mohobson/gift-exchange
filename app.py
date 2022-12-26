from flask import Flask, render_template
app = Flask(__name__)

messages = [{'name': 'name one',
             'email': 'email one'},
            {'name': 'name two',
             'email': 'email two'}
            ]

@app.route('/')
def index():
    return render_template('index.html', messages=messages)


#https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
