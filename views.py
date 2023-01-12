from datetime import datetime

from flask import abort, current_app, render_template, request, redirect, url_for
from participants import Participant
from drawing import drawing

def home_page():
    # today = datetime.today()
    # day_name = today.strftime("%A")
    day_name = 'day name'
    return render_template("index.html", day=day_name)


def participants_page():
    db = current_app.config["db"]
    participants = db.get_participants()
    assignments = drawing(participants)
    return render_template("participants.html", participants=sorted(participants), assignments=assignments)

def participant_page(participant_key):
    db = current_app.config["db"]
    participant = db.get_participant(participant_key)
    if participant is None:
        abort(404)
    return render_template("participant.html", participant=participant)

def participant_add_page():
    if request.method == "GET":
        return render_template("participant_edit.html")
        
    else:
        form_participant = request.form["participant name"]
        form_email = request.form["email"]
        participant = Participant(form_participant, email=form_email if form_email else None)
        db = current_app.config["db"]
        participant_key = db.add_participant(participant)
        return redirect(url_for("participant_page", participant_key=participant_key))
