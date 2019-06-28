from db import DB

error = 'I don\'t understand.'

class Messages():
    def __init__(self):
        self.db = DB()
        self.set_module('intro')

    def set_module(self, set_name):
        self.responses = self.db.getResponses(set_name)
        self.state = self.db.getState(set_name)

    def check(self, msg_byte_arr):
        try:
            msg = str(msg_byte_arr, 'utf-8')
        except:
            msg = ' ' # handle non-text characters

        response = ''
        next = ''
        for r in self.responses:
            # check if regex matches passed string
            if r.regex.search(msg):
                # check that all required checks for response are valid too
                if not self.test_conditions(r.is_on):
                    continue
                if not self.test_exceptions(r.is_off):
                    continue
                for on in r.set_on:
                    self.state[on] = True
                for off in r.set_off:
                    self.state[off] = False
                response = r.resp + '\n'
                if r.next:
                    next = r.next
                else:
                    response += '> '
                break

        if response == '':
            response = error + '\n> '
        return (response.encode('utf-8'), next)

    def test_conditions(self, is_on):
        for c in is_on:
            try:
                if not self.state[c]:
                    return False
            except KeyError:
                return False
        return True

    def test_exceptions(self, is_off):
        for c in is_off:
            try:
                if self.state[c]:
                    return False
            except KeyError:
                continue
        return True
