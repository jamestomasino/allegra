import re
"""
Response object
:param set_name: Name of the set to which the response belongs
:param match_str: String representation of regex for matching input
:param resp: String response displayed if matched
:param is_on: List of boolean states that must be true to match response
:param is_off: List of boolean states that must be false to match response
:param set_on: List of boolean states that will become true if matched
:param set_off: List of boolean states that will become false if matched
:param next: Optional response string to auto-trigger if this is matched
"""
class Response():

    SET_CHANGE = re.compile(r'\ballegra_set_change_')
    SET_EXIT = re.compile(r'exit')

    @staticmethod
    def get_set_change(msg):
        return re.sub(Response.SET_CHANGE, '', msg)

    def __init__(self, match_str, resp, is_on='', is_off='', set_on='', set_off='', next=''):
        self.regex = re.compile(r'\b%s\b' % match_str, re.I)
        self.resp = resp

        if is_on:
            self.is_on = is_on.split(',')
        else:
            self.is_on = []
        if is_off:
            self.is_off = is_off.split(',')
        else:
            self.is_off = []

        if set_on:
            self.set_on = set_on.split(',')
        else:
            self.set_on = []

        if set_off:
            self.set_off = set_off.split(',')
        else:
            self.set_off = []

        self.next = next
