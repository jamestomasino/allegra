import re

""" Response object
    regex to match string input
    array of boolean state checks for test
    array of state toggles to true
    array of state toggles to false
    response string if matched
"""
class Response():
    def __init__(self, match_str, resp, checks = [], exceptions = [], set_on = [], set_off = [], next = ''):
        self.regex = re.compile(match_str)
        self.resp = resp
        self.checks = checks
        self.exceptions = exceptions
        self.set_on = set_on
        self.set_off = set_off
        self.next = next
