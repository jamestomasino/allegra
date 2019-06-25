import random

responses = {
    'test': 'Conosci mio Pappà?',
    'english': 'I... think I remember that'
}

error_ita = 'Non capisco, Pappà. '
error_responses_ita = [
    'Dove siamo? Aiutami',
    'Non vedo niente',
    'Dove ti nascondi?'
]

error_eng = 'I don\'t understand, daddy. '
error_responses_eng = [
    'Where are we? Help me',
    'I can\'t see you',
    'Where are you hiding?'
]

class Messages():
    def __init__(self):
        self.is_italian = True

    def check(self, msg_byte_arr):
        msg = str(msg_byte_arr, 'utf-8')
        if msg.lower() in responses:
            if (msg.lower() == 'english'):
                self.is_italian = False
            response = responses[msg.lower()] + '\n'
            return response.encode('utf-8')
        else:
            if self.is_italian:
                response = error_ita + random.choice(error_responses_ita) + '\n'
            else:
                response = error_eng + random.choice(error_responses_eng) + '\n'
            return response.encode('utf-8')
