from flask import Flask, render_template, request

import datetime
import views
from database import Database
from participants import Participant

messages = [{'name': 'name one',
             'email': 'email one'},
            {'name': 'name two',
             'email': 'email two'}
            ]

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/participants", view_func=views.participants_page)

    db = Database()
    db.add_participant(Participant("person1", email="123@aol.com"))
    db.add_participant(Participant("person2"))
    app.config["db"] = db

    @app.route('/')
    def index():
        # today = datetime.datetime()
        # day_name = today.strftime("%A")
        day_name='dayname'
        print(day_name)
        return render_template('index.html', day=day_name, messages=messages)

    @app.route('/participants')
    def participant_page():
        return render_template("participant.html")

    @app.route('/participant')
    def participant_add_page():
        if request.method == "GET":
            return render_template(
                "participant.html"
            )
            
        else:
            form_title = request.form["title"]
            person_name = request.form["name"]
            # email = Email(form_title, name=person_name if person_name else None)
    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)


#https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
