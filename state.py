from db import DB

class State():
    def __init__(self):
        self.db = DB()
        self.module = ''
        self.responses = {}
        self.state = {}

    def set_module(self, set_name):
        self.module = set_name
        if not self.module in self.responses:
            self.responses[self.module] = self.db.getResponses(set_name)
        if not self.module in self.state:
            self.state[self.module] = self.db.getState(set_name)

    def get_responses(self):
        try:
            ret = self.responses[self.module]
        except KeyError:
            ret = []
        return ret

    def get_state(self):
        try:
            ret = self.state[self.module]
        except KeyError:
            ret = []
        return ret

    def test_conditions(self, is_on):
        for c in is_on:
            try:
                if not self.state[self.module][c]:
                    return False
            except KeyError:
                return False
        return True

    def test_exceptions(self, is_off):
        for c in is_off:
            try:
                if self.state[self.module][c]:
                    return False
            except KeyError:
                continue
        return True

    def enable(self, key):
        self.state[self.module][key] = True

    def disable(self, key):
        self.state[self.module][key] = False
