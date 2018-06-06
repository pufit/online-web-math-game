

def check(self, data):
    self.game.check(self, data)
    if self.player.score >= self.game.max_score:
        self.temp.give_score(self)
