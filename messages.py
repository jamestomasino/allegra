from response import Response

error = 'Non capisco, Pappà. '

class Messages():
    def __init__(self):
        self.state = {
            'english': False,
            'blue_key': False
        }

        self.responses = [
            Response('test', 'Conosci mio Pappà?'),
            Response('monkey', 'Doom', checks=['english'], set_on=['blue_key']),
            Response('english', 'I... think I remember that', set_on=['english'])

        ]

    def check(self, msg_byte_arr):
        try:
            msg = str(msg_byte_arr, 'utf-8')
        except:
            msg = ' ' # handle non-text characters

        response = ''
        for r in self.responses:
            # check if regex matches passed string
            if r.regex.match(msg):
                # check that all required checks for response are valid too
                for c in r.checks:
                    if not self.state[c]:
                        continue
                for on in r.set_on:
                    self.state[on] = True
                for off in r.set_off:
                    self.state[off] = False
                response = r.resp + '\n'
                break

        if response == '':
            response = error + '\n'
        return response.encode('utf-8')
