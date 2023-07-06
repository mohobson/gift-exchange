import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from participants import Participant
from couples import Couple
from assignments import Assignment

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

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_participant(self, participant):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO PARTICIPANT (PARTICIPANT, EMAIL) VALUES (?, ?)"
            cursor.execute(query, (participant.participant, participant.email))
            connection.commit()
            participant_key = cursor.lastrowid
        return participant_key


    def update_participant(self, participant_key, participant):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE PARTICIPANT SET PARTICIPANT = ?, EMAIL = ? WHERE (ID = ?)"
            cursor.execute(query, (participant.participant, participant.email, participant_key))
            connection.commit()
    
    def delete_participant(self, participant_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM PARTICIPANT WHERE (ID = ?)"
            cursor.execute(query, (participant_key,))
            connection.commit()
    
    def get_participant(self, participant_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT PARTICIPANT, EMAIL FROM PARTICIPANT WHERE (ID = ?)"
            cursor.execute(query, (participant_key,))
            participant, email = cursor.fetchone()
        participant_ = Participant(participant, email=email)
        return participant_
    
    def get_participants(self):
        participants = []
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, PARTICIPANT, EMAIL FROM PARTICIPANT ORDER BY ID"
            cursor.execute(query)
            for participant_key, participant, email in cursor:
                participants.append((participant_key, Participant(participant, email)))
        return participants

    ############## COUPLES #####################

    def add_couple(self, couple):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO COUPLE (PARTNERONE, PARTNERTWO) VALUES (?, ?)"
            cursor.execute(query, (couple.partner_one, couple.partner_two))
            connection.commit()
            couple_key = cursor.lastrowid
        return couple_key
    
    def update_couple(self, couple_key, couple):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE COUPLE SET PARTNERONE = ?, PARTNERTWO = ? WHERE (ID = ?)"
            cursor.execute(query, (couple.partner_one, couple.partner_two, couple_key))
            connection.commit()

    def delete_couple(self, couple_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM COUPLE WHERE (ID = ?)"
            cursor.execute(query, (couple_key,))
            connection.commit()
    
    def get_couple(self, couple_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT PARTNERONE, PARTNERTWO FROM COUPLE WHERE (ID = ?)"
            cursor.execute(query, (couple_key,))
            partner_one, partner_two = cursor.fetchone()
        couple_ = Couple(partner_one, partner_two=partner_two)
        return couple_
    
    def get_couples(self):
        couples = []
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, PARTNERONE, PARTNERTWO FROM COUPLE ORDER BY ID"
            cursor.execute(query)
            for couple_key, partner_one, partner_two in cursor:
                couples.append((couple_key, Couple(partner_one, partner_two)))
        return couples



    ############## ASSIGNMENTS #####################

    def add_assignment(self, assignment):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO ASSIGNMENT (NAMEONE, NAMETWO) VALUES (?, ?)"
            cursor.execute(query, (assignment.name1, assignment.name2))
            connection.commit()
            assignment_key = cursor.lastrowid
        return assignment_key
    
    def update_assignment(self, assignment_key, assignment):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE ASSIGNMENT SET NAMEONE = ?, NAMETWO = ? WHERE (ID = ?)"
            cursor.execute(query, (assignment.name1, assignment.name2, assignment_key))
            connection.commit()
    
    def delete_assignment(self, assignment_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM ASSIGNMENT WHERE (ID = ?)"
            cursor.execute(query, (assignment_key,))
            connection.commit()

    def get_assignment(self, assignment_key):
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT NAMEONE, NAMETWO FROM ASSIGNMENT WHERE (ID = ?)"
            cursor.execute(query, (assignment_key,))
            name1, name2 = cursor.fetchone()
        assignment_ = Assignment(name1, name2=name2)
        return assignment_

    def get_assignments(self):
        assignments = [] 
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, NAMEONE, NAMETWO FROM ASSIGNMENT ORDER BY ID"
            cursor.execute(query)
            for assignment_key, name1, name2 in cursor:
                assignments.append((assignment_key, Assignment(name1, name2)))
        return assignments

    def get_latest_assignments(self):
        assignments = [] 
        with sqlite3.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, PARTICIPANT, EMAIL FROM PARTICIPANT ORDER BY ID"
            cursor.execute(query)
            number_of_latest_assignments = 0
            # use the number of participants to get the number of assignments
            for participant_key, participant, email in cursor:
                number_of_latest_assignments += 1
            query = f"SELECT ID, NAMEONE, NAMETWO FROM ASSIGNMENT ORDER BY ID DESC LIMIT {number_of_latest_assignments}"
            cursor.execute(query)
            for assignment_key, name1, name2 in cursor:
                print(assignment_key, name1, name2)
                assignments.append((assignment_key, Assignment(name1, name2)))
        return assignments



    
