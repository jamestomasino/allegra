import re

class Response():
    def __init__(self, match_str, resp):
        self.regex = re.compile(match_str)
        self.resp = resp
