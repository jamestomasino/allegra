import random
import re

error = 'Non capisco, Pappà. '

class Messages():
    def __init__(self):
        self.responses = [
            Response('test', 'Conosci mio Pappà?'),
            Response('english', 'I... think I remember that')
        ]

    def check(self, msg_byte_arr):
        try:
            msg = str(msg_byte_arr, 'utf-8')
        except:
            msg = ' ' # handle non-text characters

        response = ''
        for r in self.responses:
            if r.regex.match(msg):
                response = r.resp + '\n'
                break

        if response == '':
            response = error + '\n'
        return response.encode('utf-8')

class Response():
    def __init__(self, match_str, resp):
        self.regex = re.compile(match_str)
        self.resp = resp
