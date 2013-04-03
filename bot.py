from copy import deepcopy
from tripletown import TripleTown as tt
import random
import time

class Bot:
    def __init__(self):
        self.game = tt()
        self.gametree = {}

    def t(self, r=100):
        for x in xrange(r):
            self.game.start_game()
            print self.playout(self.game)

    def playout(self, gamestate):
        while gamestate.game_running():
            if gamestate.current_item == 53:
                move = (random.randrange(6), random.randrange(6))
            else:
                move = random.choice(list(gamestate.get_empty_nodes()))

            gamestate.play(move[0], move[1])

        if gamestate.score is None:
            gamestate.status()

        return gamestate.score

    def suggest_move(self, trials=1000):
        if not self.game.game_running():
            self.game.start_game()
            self.game.status()

        timer = time.time()
        trial_counter = 0
        tps = 0
        max_score = 0

        for i in xrange(trials):
            trial_counter += 1
            tps += 1
            timediff = time.time() - timer
            if timediff > 1:
                print "{} trials, {} trials/sec, max score of {}".format(trial_counter, tps / timediff, max_score)
                timer = time.time()
                tps = 0
            coord = random.choice(list(self.game.get_empty_nodes()))
            gamestate = deepcopy(self.game)
            gamestate.play(coord[0], coord[1])
            score = self.playout(gamestate)
            if score > max_score:
                max_score = score

            if coord in self.gametree:
                self.gametree[coord].append(score)
                self.gametree[coord][1] += 1
            else:
                self.gametree[coord] = [[score], 1]

        for move in self.gametree:
            if max_score in self.gametree[move][0]:
                return move
