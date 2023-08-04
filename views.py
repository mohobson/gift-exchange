from datetime import datetime, date
import os

from flask import abort, current_app, render_template, request, redirect, url_for, session
from participants import Participant
from couples import Couple
from drawing import drawing
from forms import ParticipantEditForm, CoupleEditForm

from database import get_db
from database import Database

from auth import login_required

def home_page():
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day
    
    today = date(current_year, current_month, current_day)
    christmas = date(2023, 12, 25)
    days_until_christmas = christmas - today
    #day_name = today.strftime("%A")

    return render_template("home.html", days=days_until_christmas.days)

@login_required
def participants_page():
    db = Database(os.path.join(current_app.instance_path, 'group.sql'))
    user_id = session.get('user_id')
    if request.method == "GET":
        participants = db.get_participants(user_id)
        couples = db.get_couples(user_id)
        assignments = drawing(participants, couples)
        return render_template("participants.html", participants=sorted(participants), couples=couples, assignments=assignments)
    else:
        form_participant_keys = request.form.getlist("participantKeys")
        form_couple_keys = request.form.getlist("coupleKeys")
        # print(form_participant_keys)
        for form_participant_key in form_participant_keys:
            db.delete_participant(user_id, int(form_participant_key))
        for form_couple_key in form_couple_keys:
            db.delete_couple(user_id, int(form_couple_key))
        return redirect(url_for("participants_page"))

@login_required
def participant_page(participant_key):
    db = Database(os.path.join(current_app.instance_path, 'group.sql'))
    user_id = session.get('user_id')
    participant = db.get_participant(user_id, participant_key)
    if participant is None:
        abort(404)
    return render_template("participant.html", participant=participant)

@login_required
def participant_add_page():
    form = ParticipantEditForm()
    if form.validate_on_submit():
        participant_name = form.data["participant"]
        email = form.data["email"]
        participant = Participant(participant_name, email=email)
        db = Database(os.path.join(current_app.instance_path, 'group.sql'))
        user_id = session.get('user_id')
        participant_key = db.add_participant(user_id, participant)
        return redirect(url_for("participant_page", participant_key=participant_key))
    return render_template("participant_edit.html", form=form)

@login_required
def participant_edit_page(participant_key):
    db = Database(os.path.join(current_app.instance_path, 'group.sql'))
    user_id = session.get('user_id')
    participant = db.get_participant(user_id, participant_key)
    form = ParticipantEditForm()
    if form.validate_on_submit():
        participant_name = form.data["participant"]
        email = form.data["email"]
        participant = Participant(participant_name, email=email)
        db.update_participant(user_id, participant_key, participant)
        return redirect(url_for("participant_page", participant_key=participant_key))
    form.participant.data = participant.participant
    form.email.data = participant.email if participant.email else ""
    return render_template("participant_edit.html", form=form)


##############

@login_required
def couples_page():
    db = Database(os.path.join(current_app.instance_path, 'group.sql'))
    user_id = session.get('user_id')
    if request.method == "GET":
        couples = db.get_couples(user_id)
        return render_template("couples.html", couples=sorted(couples))
    else:
        form_couple_keys = request.form.getlist("coupleKeys")
        for form_couple_key in form_couple_keys:
            db.delete_couple(user_id, int(form_couple_key))
        return redirect(url_for("couples_page"))

@login_required
def couple_page(couple_key):
    db = Database(os.path.join(current_app.instance_path, 'group.sql'))
    user_id = session.get('user_id')
    couple = db.get_couple(user_id, couple_key)
    if couple is None:
        abort(404)
    return render_template("couple.html", couple=couple)

@login_required
def couple_add_page():
    form = CoupleEditForm()
    if form.validate_on_submit():
        partner_one = form.data["partner_one"]
        partner_two = form.data["partner_two"]
        couple = Couple(partner_one, partner_two=partner_two)
        db = Database(os.path.join(current_app.instance_path, 'group.sql'))
        user_id = session.get('user_id')
        couple_key = db.add_couple(user_id, couple)
        return redirect(url_for("couple_page", couple_key=couple_key))
    return render_template("couples_edit.html", form=form)
    
@login_required
def couple_edit_page(couple_key):
    db = Database(os.path.join(current_app.instance_path, 'group.sql'))
    user_id = session.get('user_id')
    couple = db.get_couple(user_id, couple_key)
    form = CoupleEditForm()
    if form.validate_on_submit():
        partner_one = form.data["partner_one"]
        partner_two = form.data["partner_two"]
        couple = Couple(partner_one, partner_two=partner_two)
        db.update_couple(user_id, couple_key, couple)
        return redirect(url_for("couple_page", couple_key=couple_key))
    form.partner_one.data = couple.partner_one
    form.partner_two.data = couple.partner_two if couple.partner_two else ""
    return render_template("couples_edit.html", form=form)
#######################

########### VALIDATION ###########

def validate_participant_form(form):
    form.data = {}
    form.errors = {}

    form_participant = form.get("participantName", "").strip()
    if len(form_participant) == 0:
        form.errors["participantName"] = "Field cannot be blank."
    else:
        form.data["participantName"] = form_participant
    
    form_email = form.get("email")
    if not form_email:
        form.data["email"] = None
    else:
        form.data["email"] = form_email
    
    return len(form.errors) == 0

def validate_couple_form(form):
    form.data = {}
    form.errors = {}

    form_partner_one = form.get("partner_one", "").strip()
    if len(form_partner_one) == 0:
        form.errors["partner_one"] = "Field cannot be blank."
    else:
        form.data["partner_one"] = form_partner_one
    
    form_partner_two = form.get("partner_two")
    if len(form_partner_two) == 0:
        form.errors["partner_two"] = "Field cannot be blank."
    else:
        form.data["partner_two"] = form_partner_two
    
    return len(form.errors) == 0