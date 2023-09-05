from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField

from flask import current_app, session

from database import get_db
from database import Database

from datetime import datetime
import os

class ParticipantEditForm(FlaskForm):
    participant = StringField("Participant", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])

class CoupleEditForm(FlaskForm):
    # def get_choices():
    #     db = Database(os.path.join(current_app.instance_path, 'group.sql'))
    #     user_id = session.get('user_id')
    #     participants = db.get_participants(user_id)
    #     choices = []
    #     for participant_key, participant in participants:
    #         choices.append(participant.participant)
    #     return choices
    partner_one = SelectField(validators=[DataRequired()])
    partner_two = SelectField(validators=[DataRequired()])
    # partner_one = StringField("Partner One", validators=[DataRequired()])
    # partner_two = StringField("Partner Two", validators=[DataRequired()])