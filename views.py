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
    if request.method == "GET":
        participants = db.get_participants()
        couples = db.get_couples()
        assignments = drawing(participants, couples)
        return render_template("participants.html", participants=sorted(participants), couples=couples, assignments=assignments)
    else:
        form_participant_keys = request.form.getlist("participantKeys")
        form_couple_keys = request.form.getlist("coupleKeys")
        # print(form_participant_keys)
        for form_participant_key in form_participant_keys:
            db.delete_participant(int(form_participant_key))
        for form_couple_key in form_couple_keys:
            db.delete_couple(int(form_couple_key))
        return redirect(url_for("participants_page"))

def participant_page(participant_key):
    db = current_app.config["db"]
    participant = db.get_participant(participant_key)
    if participant is None:
        abort(404)
    return render_template("participant.html", participant=participant)

def participant_add_page():
    if request.method == "GET":
        values = {"participantName": "", "email": ""}
        return render_template("participant_edit.html", values=values)
        
    else:
        form_participant = request.form["participantName"]
        form_email = request.form["email"]
        participant = Participant(form_participant, email=form_email if form_email else None)
        db = current_app.config["db"]
        participant_key = db.add_participant(participant)
        return redirect(url_for("participant_page", participant_key=participant_key))

def participant_edit_page(participant_key):
    if request.method == "GET":
        db = current_app.config["db"]
        participant = db.get_participant(participant_key)
        if participant is None:
            abort(404)
        values = {"participantName": participant.participant, "email": participant.email}
        return render_template("participant_edit.html", values=values)
    else:
        form_participant = request.form["participantName"]
        form_email = request.form["email"]
        participant = Participant(form_participant, email=form_email if form_email else None)
        db = current_app.config["db"]
        db.update_participant(participant_key, participant)
        return redirect(url_for("participant_page", participant_key=participant_key))

##############

def couples_page():
    db = current_app.config["db"]
    if request.method == "GET":
        couples = db.get_couples()
        return render_template("couples.html", couples=sorted(couples))
    else:
        form_couple_keys = request.form.getlist("coupleKeys")
        for form_couple_key in form_couple_keys:
            db.delete_couple(int(form_couple_key))
        return redirect(url_for("couples_page"))

def couple_page(couple_key):
    db = current_app.config["db"]
    couple = db.get_couple(couple_key)
    if couple is None:
        abort(404)
    return render_template("couple.html", couple=couple)

def couple_add_page():
    if request.method == "GET":
        values = {"partner_one": "", "partner_two": ""}
        return render_template("couples_edit.html", values=values)
        
    else:
        form_partner_one = request.form["partner one"]
        form_partner_two = request.form["partner two"]
        couple = Couple(form_partner_one, form_partner_two)
        db = current_app.config["db"]
        couple_key = db.add_couple(couple)
        return redirect(url_for("couple_page", couple_key=couple_key))
    
def couple_edit_page(couple_key):
    if request.method == "GET":
        db = current_app.config["db"]
        couple = db.get_couple(couple_key)
        if couple is None:
            abort(404)
        values = {"partner_one": couple.partner_one, "partner_two": couple.partner_two}
        return render_template("couples_edit.html", values=values)
    else:
        form_partner_one = request.form["partner one"]
        form_partner_two = request.form["partner two"]
        couple = Couple(form_partner_one, partner_two=form_partner_two if form_partner_two else None)
        db = current_app.config["db"]
        db.update_couple(couple_key, couple)
        return redirect(url_for("couple_page", couple_key=couple_key))
#######################

