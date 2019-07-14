from response import Response
from state import State
import textwrap

error = 'I don\'t understand.'

class Messages():
    CODE_ERROR = '[error]'.encode('utf-8')
    CODE_EXIT = '[exit]'.encode('utf-8')

    MSG_CONNECT = b'Welcome. Type \'help\' to start or \'exit\' to quit.'
    MSG_ERROR = b'I don\'t understand.'
    MSG_NEWLINE = b'\n'
    MSG_PROMPT = b'> '

    def __init__(self):
        self.state = State()
        self.state.set_module('intro')
        self.wrapper = textwrap.TextWrapper(width=70)

    def check(self, msg_byte_arr):
        try:
            msg = str(msg_byte_arr, 'utf-8')
        except:
            msg = '' # handle non-text characters

        # check for set changes
        if Response.SET_CHANGE.search(msg):
            self.state.set_module(Response.get_set_change(msg))
            return (''.encode('utf-8'), 'allegra_set_start')
        elif Response.SET_EXIT.search(msg):
            return (Messages.CODE_EXIT, 'allegra_set_start')
        else:
            response = Messages.CODE_ERROR
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
                    # wrap text for pretty output
                    response = self.wrapper.fill(text = r.resp)
                    break
            return (response.encode('utf-8'), next)
