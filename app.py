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

# currently on 3
# https://web.itu.edu.tr/uyar/fad/data-model.html
def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/participants", view_func=views.participants_page)
    app.add_url_rule("/participants/<int:participant_key>", view_func=views.participant_page)
    app.add_url_rule("/new-participant", view_func=views.participant_add_page, methods=["GET", "POST"])

    db = Database()
    app.config["db"] = db

    @app.route('/')
    def index():
        # today = datetime.datetime()
        # day_name = today.strftime("%A")
        day_name='dayname'
        print(day_name)
        return render_template('index.html', day=day_name, messages=messages)
    
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host='0.0.0.0', port=port, debug=True)


#https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
