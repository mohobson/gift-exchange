from flask import Flask, render_template, request

import datetime
import views
from database import Database
from participants import Participant
from couples import Couple

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
    app.add_url_rule("/participants/<int:participant_key>", view_func=views.participant_page)
    app.add_url_rule("/new-participant", view_func=views.participant_add_page, methods=["GET", "POST"])

    app.add_url_rule("/couples", view_func=views.couples_page)
    app.add_url_rule("/couple/<int:couple_key>", view_func=views.couple_page)
    app.add_url_rule("/new-couple", view_func=views.couple_add_page, methods=["GET", "POST"])


    db = Database()

    # add some temporary participants and one couple for testing purposes
    db.add_participant(Participant("mo", email="mo@aol.com"))
    db.add_participant(Participant("number2", email="number2@aol.com"))
    db.add_participant(Participant("number3", email="number3@aol.com"))
    db.add_participant(Participant("number4", email="number4@aol.com"))


    db.add_couple(Couple("mo", "number2"))

    app.config["db"] = db
    
    return app


# if __name__ == "__main__":
app = create_app()
# port = app.config.get("PORT", 5000)
# app.run(host='0.0.0.0', port=port, debug=True)

# helpful links:
# https://web.itu.edu.tr/uyar/fad/data-model.html
# https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
