

class Game:
    max_players = 6

    def __init__(self, channel, creator, config):
        self.config = config

        self.name = config['name']
        self.slots = config['slots']
        self.creator = creator
        self.players = {}
        self.channel = channel
