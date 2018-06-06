import random


class Player:
    def __init__(self, game, user):
        self.game = game
        self.user = user
        self.name = user.user

        self.answered = False

        self.score = 0


class ExamplesFactory:

    def __init__(self, dif):
        self.type = 'int'

        if dif == 'easy':
            self.signs = ['+', '-']
            self.count_range = [2, 3]
            self.num_range = [1, 100]
        elif dif == 'medium':
            self.signs = ['+', '-', '*']
            self.count_range = [3, 5]
            self.num_range = [-100, 100]
        elif dif == 'hard':
            self.signs = ['+', '-', '*']
            self.count_range = [3, 5]
            self.num_range = [-150, 150]
            self.type = 'float'
        elif dif == 'very_hard':
            self.signs = ['+', '-', '*', '/']
            self.count_range = [4, 6]
            self.num_range = [-200, 200]
            self.type = 'float'
        else:
            raise Exception('Bad difficult')

    def generate(self):
        count = random.randint(*self.count_range)
        if self.type == 'int':
            nums = [str(random.randint(*self.num_range)) for _ in range(count)]
        else:
            nums = [str(round(random.uniform(*self.num_range), 2)) for _ in range(count)]
        signs = [random.choice(self.signs) for _ in range(count - 1)]
        example = '%s'.join(nums)
        example = example % signs
        try:
            eval(example)
        except ZeroDivisionError:
            return self.generate()
        return [example, eval(example)]


class Game:
    max_players = 2

    def __init__(self, channel, creator, config):
        self.config = config

        self.name = config['name']
        self.slots = config['slots']
        self.creator = creator
        self.players = {}
        self.channel = channel
        self.started = False

        self.ended = False

        self.current_example = None
        self.factory = ExamplesFactory(config['dif'])

    def add_new_player(self, user):
        if len(self.players) >= self.slots:
            raise Exception('Players limit')
        player = Player(self, user)
        self.players[user.user] = player
        return player

    def start(self):
        self.change_example()
        self.channel.send({'type': 'game_started', 'data': ''})

    def change_example(self):
        for player in self.players:
            player.answered = False

        self.current_example = self.factory.generate()
        self.channel.send({'type': 'example', 'data': self.current_example})

    def check(self, player, result):
        if not self.started:
            raise Exception('Game hasn\'t started')
        if self.ended:
            raise Exception('Game has ended')
        if player.answered:
            raise Exception('Player has already answered')
        if result == self.current_example[1]:
            self.channel.send(
                {
                    'type': 'round_ended',
                    'data': {
                        'correct_answer': result,
                        'player': player.name
                    }
                }
            )
            player.score += 1
            self.change_example()
        else:
            player.answered = True
            self.channel.send(
                {
                    'type': 'player_answered',
                    'data': {
                        'wrong_answer': result,
                        'player': player.name
                    }
                }
            )
