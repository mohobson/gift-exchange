from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField

from datetime import datetime

class ParticipantEditForm(FlaskForm):
    participant = StringField("Participant", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])

class CoupleEditForm(FlaskForm):
    partner_one = StringField("Partner One", validators=[DataRequired()])
    partner_two = StringField("Partner Two", validators=[DataRequired()])