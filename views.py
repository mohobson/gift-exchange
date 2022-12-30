from datetime import datetime

from flask import render_template
from flask import current_app, render_template


def home_page():
    # today = datetime.today()
    # day_name = today.strftime("%A")
    day_name = 'day name'
    return render_template("index.html", day=day_name)


def participants_page():
    db = current_app.config["db"]
    participants = db.get_participants()
    return render_template("participants.html", participants=sorted(participants))
