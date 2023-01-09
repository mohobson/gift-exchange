from participants import Participant

class Database:
    def __init__(self):
        self.participants = {}
        self._last_participant_key = 0
    
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

    
