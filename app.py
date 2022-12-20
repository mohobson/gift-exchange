from flask import Flask, render_template
app = Flask(__name__)

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route('/')
def hello_world():
    return render_template('index.html', messages=messages)


#https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
