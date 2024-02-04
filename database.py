import sqlite3
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext

from participants import Participant
from couples import Couple
from assignments import Assignment

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('group.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def write_email(subject, toaddr, body):
    from dotenv import load_dotenv
    load_dotenv()

    FROM_EMAIL = os.getenv('FROM_EMAIL')
    EMAIL_APP_PASS = os.getenv('EMAIL_APP_PASS')

    msg = MIMEMultipart()

    msg['From'] = FROM_EMAIL
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(FROM_EMAIL, EMAIL_APP_PASS)
    except smtplib.SMTPAuthenticationError:
        print('SMTP AuthenticationError')
    text = msg.as_string()
    try:
        server.sendmail(FROM_EMAIL, toaddr, text)
    except smtplib.SMTPSenderRefused:
        print('SMTP SenderRefused')
    server.quit()

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_participant(self, user_id, participant):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO PARTICIPANT (user_id, PARTICIPANT, EMAIL) VALUES (?, ?, ?)"
            cursor.execute(query, (user_id, participant.participant, participant.email))
            connection.commit()
            participant_key = cursor.lastrowid
        return participant_key


    def update_participant(self, user_id, participant_key, participant):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE PARTICIPANT SET PARTICIPANT = ?, EMAIL = ? WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (participant.participant, participant.email, participant_key, user_id))
            connection.commit()
    
    def delete_participant(self, user_id, participant_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM PARTICIPANT WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (participant_key, user_id))
            connection.commit()
    
    def get_participant(self, user_id, participant_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT PARTICIPANT, EMAIL FROM PARTICIPANT WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (participant_key, user_id))
            participant, email = cursor.fetchone()
        participant_ = Participant(participant, email=email)
        return participant_
    
    def get_participants(self, user_id):
        participants = []
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, PARTICIPANT, EMAIL FROM PARTICIPANT WHERE (user_id = ?) ORDER BY ID"
            cursor.execute(query, (user_id,))
            for participant_key, participant, email in cursor:
                participants.append((participant_key, Participant(participant, email)))
        return participants

    ############## COUPLES #####################

    def add_couple(self, user_id, couple):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO COUPLE (user_id, PARTNERONE, PARTNERTWO) VALUES (?, ?, ?)"
            cursor.execute(query, (user_id, couple.partner_one, couple.partner_two))
            connection.commit()
            couple_key = cursor.lastrowid
        return couple_key
    
    def update_couple(self, user_id, couple_key, couple):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE COUPLE SET PARTNERONE = ?, PARTNERTWO = ? WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (couple.partner_one, couple.partner_two, couple_key, user_id))
            connection.commit()

    def delete_couple(self, user_id, couple_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM COUPLE WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (couple_key, user_id))
            connection.commit()
    
    def get_couple(self, user_id, couple_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT PARTNERONE, PARTNERTWO FROM COUPLE WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (couple_key, user_id))
            partner_one, partner_two = cursor.fetchone()
        couple_ = Couple(partner_one, partner_two=partner_two)
        return couple_
    
    def get_couples(self, user_id):
        couples = []
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, PARTNERONE, PARTNERTWO FROM COUPLE WHERE (user_id = ?) ORDER BY ID"
            cursor.execute(query, (user_id,))
            for couple_key, partner_one, partner_two in cursor:
                couples.append((couple_key, Couple(partner_one, partner_two)))
        return couples



    ############## ASSIGNMENTS #####################

    def add_assignment(self, user_id, assignment):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO ASSIGNMENT (user_id, NAMEONE, NAMETWO) VALUES (?, ?, ?)"
            cursor.execute(query, (user_id, assignment.name1, assignment.name2))
            connection.commit()
            assignment_key = cursor.lastrowid
        return assignment_key
    
    def update_assignment(self, user_id, assignment_key, assignment):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE ASSIGNMENT SET NAMEONE = ?, NAMETWO = ? WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (assignment.name1, assignment.name2, assignment_key, user_id))
            connection.commit()
    
    def delete_assignment(self, user_id, assignment_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM ASSIGNMENT WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (assignment_key, user_id))
            connection.commit()

    def get_assignment(self, user_id, assignment_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT NAMEONE, NAMETWO FROM ASSIGNMENT WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (assignment_key, user_id))
            name1, name2 = cursor.fetchone()
        assignment_ = Assignment(name1, name2=name2)
        return assignment_

    def get_assignments(self, user_id):
        assignments = [] 
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, NAMEONE, NAMETWO FROM ASSIGNMENT WHERE (user_id = ?) ORDER BY ID"
            cursor.execute(query, (user_id,))
            for assignment_key, name1, name2 in cursor:
                assignments.append((assignment_key, Assignment(name1, name2)))
        return assignments

    def get_latest_assignments(self, user_id):
        assignments = [] 
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, PARTICIPANT, EMAIL FROM PARTICIPANT WHERE (user_id = ?) ORDER BY ID"
            cursor.execute(query, (user_id,))
            number_of_latest_assignments = 0
            # use the number of participants to get the number of assignments
            for participant_key, participant, email in cursor:
                number_of_latest_assignments += 1
            query = f"SELECT ID, NAMEONE, NAMETWO FROM ASSIGNMENT WHERE (user_id = ?) ORDER BY ID DESC LIMIT {number_of_latest_assignments}"
            cursor.execute(query, (user_id,))
            for assignment_key, name1, name2 in cursor:
                # print(assignment_key, name1, name2)
                assignments.append((assignment_key, Assignment(name1, name2)))
        return assignments

    def send_email(self, user_id, assignment_key):

        #need to get all emails in a list
        #need to send each email with assigned name like "p1, you get a gift for p2"

        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT NAMEONE, NAMETWO FROM ASSIGNMENT WHERE (ID = ?) AND (user_id = ?)"
            cursor.execute(query, (assignment_key, user_id))
            name1, name2 = cursor.fetchone()

            cursor2 = connection.cursor()
            query2 = "SELECT EMAIL FROM PARTICIPANT WHERE PARTICIPANT = ? AND (user_id = ?)"
            cursor2.execute(query2, (name1, user_id))
            for email, in cursor2:
                subject = "Your Gift Exchange Assignment"
                toaddr = email
                body = name1 + ", you've been randomly assigned to get a gift for " + name2 + "!"
                write_email(subject, toaddr, body)
                # print('toaddr: ', toaddr)
                # print('email body: ', body)
        return
    

