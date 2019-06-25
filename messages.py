from response import Response

error = 'I don\'t understand.'

class Messages():
    def __init__(self):
        self.state = {
            'room1': True,
            'room2': False,
            'room3': False,
            'blue_key': False,
            'chest_open': False,
            'ring': False
        }

        self.responses = [
            # Key
            Response('.', 'You can\'t seem to take your eyes off the ring. It\'s so pretty.', checks=['ring']),

            # Help
            Response('help', 'Try looking around.', checks=['room1']),
            Response('help', 'How did you get here without learning to look around?', exceptions=['room1']),

            # Room 1
            Response('look', 'You are in a dusty cave. There is a door to the north and a door to the west.', checks=['room1']),
            Response('north', 'You move north through the doorway. Things don\'t smell so good.', checks=['room1'], set_on=['room2'], set_off=['room1']),
            Response('west', 'You go west, my friend.', checks=['room1'], set_on=['room3'], set_off=['room1']),

            # Room 2 (north)
            Response('look', 'This room is filled with piles of trash. Amongst the trash is a lovely blue key.', checks=['room2'], exceptions=['blue_key']),
            Response('look', 'This room is filled with piles of trash.', checks=['room2','blue_key']),
            Response('back', 'You return the way you came. That was a gross place.', checks=['room2'], set_on=['room1'], set_off=['room2']),
            Response('south', 'Down we go...', checks=['room2'], set_on=['room1'], set_off=['room2']),
            Response('key|blue', 'You snatch up the blue key. It\'s pretty!', checks=['room2'], set_on=['blue_key']),

            # Room 3 (west)
            Response('look', 'A small chest is sitting in the middle of this empty room. There is a lock on it. The only exit is the way you entered.', checks=['room3'], exceptions=['chest_open']),
            Response('look', 'An open chest is sitting in the middle of this empty room. The door to the east returns the way you came.', checks=['room3','chest_open'], set_on=['ring']),
            Response('back', 'You return the way you came. That room was creepy anyway.', checks=['room3'], set_on=['room1'], set_off=['room3']),
            Response('east', 'You walk through the eastern door.', checks=['room3'], set_on=['room1'], set_off=['room3']),
            Response('key|lock|chest', 'You try to open the chest, but it won\'t budge. Perhaps if you had the key?', checks=['room3'], exceptions=['blue_key']),
            Response('key|lock|chest', 'You open the chest to reveal a beautiful golden ring. Plucking it from the velvety interior, you slip in onto your finger. It feels cool and heavy, and you have the sense that this was a mistake.', checks=['room3', 'blue_key'], set_on=['ring']),

            # Fallback errors for movement that isn't valid
            Response('north|south|east|west', 'You can\'t go that way.')
        ]

    def check(self, msg_byte_arr):
        try:
            msg = str(msg_byte_arr, 'utf-8')
        except:
            msg = ' ' # handle non-text characters

        response = ''
        for r in self.responses:
            # check if regex matches passed string
            if r.regex.search(msg):
                # check that all required checks for response are valid too
                if not self.test_conditions(r.checks):
                    continue
                if not self.test_exceptions(r.exceptions):
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

    def test_conditions(self, checks):
        for c in checks:
            if not self.state[c]:
                return False
        return True

    def test_exceptions(self, checks):
        for c in checks:
            if self.state[c]:
                return False
        return True
