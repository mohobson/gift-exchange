from datetime import datetime

from flask import abort, current_app, render_template, request, redirect, url_for
from participants import Participant
from couples import Couple
from drawing import drawing

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def participants_page():
    db = current_app.config["db"]
    participants = db.get_participants()
    couples = db.get_couples()
    assignments = drawing(participants, couples)
    return render_template("participants.html", participants=sorted(participants), couples=couples, assignments=assignments)

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


##############

def couples_page():
    db = current_app.config["db"]
    couples = db.get_couples()
    return render_template("couples.html", couples=sorted(couples))

def couple_page(couple_key):
    db = current_app.config["db"]
    couple = db.get_couple(couple_key)
    if couple is None:
        abort(404)
    return render_template("couple.html", couple=couple)

def couple_add_page():
    if request.method == "GET":
        return render_template("couples_edit.html")
        
    else:
        form_partner_one = request.form["partner one"]
        form_partner_two = request.form["partner two"]
        couple = Couple(form_partner_one, form_partner_two)
        db = current_app.config["db"]
        couple_key = db.add_couple(couple)
        return redirect(url_for("couple_page", couple_key=couple_key))
    

#######################

