from response import Response
from state import State

error = 'I don\'t understand.'

class Messages():
    connect_message = b'Welcome. Type \'help\' to start or close your connection to quit.'
    error_message = b'I don\'t understand.'
    newline_message = b'\n'
    prompt_message = b'> '

    def __init__(self):
        self.state = State()
        self.state.set_module('intro')

    def check(self, msg_byte_arr):
        try:
            msg = str(msg_byte_arr, 'utf-8')
        except:
            msg = ' ' # handle non-text characters

        # check for set changes
        if Response.SET_CHANGE.search(msg):
            self.state.set_module(Response.get_set_change(msg))
            return (''.encode('utf-8'), 'allegra_set_start')
        else:
            response = ''
            next = ''
            for r in self.state.get_responses():
                # check if regex matches passed string
                if r.regex.search(msg):
                    # check that all required checks for response are valid too
                    if not self.state.test_conditions(r.is_on):
                        continue
                    if not self.state.test_exceptions(r.is_off):
                        continue
                    for on in r.set_on:
                        self.state.enable(on)
                    for off in r.set_off:
                        self.state.disable(off)
                    if r.next:
                        next = r.next
                    break
            return (r.resp.encode('utf-8'), next)
