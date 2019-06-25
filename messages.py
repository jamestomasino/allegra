import random

responses = {
    'test': 'monkey',
    'blerg': 'doom'
}

error = 'Non capisco, papà. '
error_responses = [
    'Dove siamo? Aiutami',
    'Non vedo niente',
    'Dove ti nascondi?'
]

class Messages():
    def check(self, msg_byte_arr):
        msg = str(msg_byte_arr, 'utf-8')
        if msg.lower() in responses:
            response = responses[msg.lower()] + '\n'
            return response.encode('utf-8')
        else:
            response = error + random.choice(error_responses) + '\n'
            return response.encode('utf-8')
