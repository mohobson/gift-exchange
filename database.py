from participants import Participant
from couples import Couple

class Database:
    def __init__(self):
        self.participants = {}
        self.couples = {}
        self.assignments = {}

        self._last_participant_key = 0
        self._last_couple_key = 0
        self._last_assignment_key = 0

    def add_participant(self, participant):
        self._last_participant_key += 1
        self.participants[self._last_participant_key] = participant
        return self._last_participant_key
    
    def delete_participant(self, participant_key):
        if participant_key in self.participants:
            del self.participants[participant_key]
    
    def get_participant(self, participant_key):
        participant = self.participants.get(participant_key)
        if participant is None:
            return None
        participant_ = Participant(participant.participant, email=participant.email)
        return participant_
    
    def get_participants(self):
        participants = []
        for participant_key, participant in self.participants.items():
            participant_ = Participant(participant.participant, email=participant.email)
            participants.append((participant_key, participant_))
        return participants

    ############## WORKING ON COUPLES #####################

    def add_couple(self, couple):
            self._last_couple_key += 1
            self.participants[self._last_participant_key] = couple
            return self._last_couple_key
    
    def delete_couple(self, couple_key):
        if couple_key in self.couples:
            del self.couples[couple_key]
    
    def get_couple(self, couple_key):
        couple = self.couples.get(couple_key)
        if couple is None:
            return None
        couple_ = Couple(couple.partner_one, couple.partner_two)
        return couple_
    
    def get_couples(self):
        couples = []
        for couple_key, couple in self.couples.items():
            couple_ = Couple(couple.partner_one, couple.partner_two)
            couples.append((couple_key, couple_))
        return couples



    ############## WORKING ON COUPLES #####################


    def add_assignment(self, name1, name2):
        self._last_assignment_key += 1
        self.assignments[self._last_assignment_key] = [name1, name2]
        return self._last_assignment_key

    def get_assignments(self):
        assignments = []
        for assignment_key, assignment in self.assignments.items():
            assignments.append(assignment)
        return assignments




    
