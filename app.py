from flask import Flask, render_template, request

import os
import datetime
import views
from database import Database
from participants import Participant
from couples import Couple


# how to add Flask mail service:
# https://mailtrap.io/blog/flask-email-sending/

# how to add blueprints
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/


messages = [{'name': 'name one',
             'email': 'email one'},
            {'name': 'name two',
             'email': 'email two'}
            ]

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("settings")

    # home_dir = os.path.expanduser("~")
    # print(home_dir)
    # print(app.instance_path)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'group.sql')
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    import database
    database.init_app(app)

    # db = Database(os.path.join(home_dir, "group.sql"))
    # app.config["db"] = db

    app.add_url_rule("/", view_func=views.home_page)

    app.add_url_rule("/participants", view_func=views.participants_page, methods=["GET", "POST"])
    app.add_url_rule("/participants/<int:participant_key>", view_func=views.participant_page)
    app.add_url_rule("/participants/<int:participant_key>/edit", view_func=views.participant_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/new-participant", view_func=views.participant_add_page, methods=["GET", "POST"])

    app.add_url_rule("/couples", view_func=views.couples_page, methods=["GET", "POST"])
    app.add_url_rule("/couples/<int:couple_key>", view_func=views.couple_page)
    app.add_url_rule("/couples/<int:couple_key>/edit", view_func=views.couple_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/new-couple", view_func=views.couple_add_page, methods=["GET", "POST"])

    # add some temporary participants and one couple for testing purposes
    # db.add_participant(Participant("Participant 1", email="p1@aol.com"))
    # db.add_participant(Participant("Participant 2", email="p2@aol.com"))
    # db.add_participant(Participant("Participant 3", email="p3@aol.com"))
    # db.add_participant(Participant("Participant 4", email="p4@aol.com"))


    # db.add_couple(Couple("Participant 1", "Participant 2"))

    import auth
    app.register_blueprint(auth.bp)

    return app


if __name__ == "__main__":
    app = create_app()
    # port = app.config.get("PORT", 5000)
    app.run()

# helpful links:
# https://web.itu.edu.tr/uyar/fad/data-model.html
# https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
