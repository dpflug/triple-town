#!/usr/bin/env python2

import random


class TripleTown(object):
    item_weights = {
        'grass': 4193,
        'bush': 1070,
        'bear': 1044,
        'bot': 176,
        'crystal': 168,
        'tree': 136,
        'ninja': 99,
        'hut': 44,
    }

    item_scores = {
        'grass': 5,
        'bush': 20,
        'tree': 100,
        'hut': 500,
        'church': 1000,
        'house': 1500,
        'gravestone': 0,
        'cathedral': 5000,
    }

    item_num_names = {
        None: 'blank',
        0: 'rock',
        1: 'grass',
        2: 'bush',
        3: 'tree',
        4: 'hut',
        5: 'house',
        6: 'mansion',
        50: 'gravestone',
        51: 'bear',
        52: 'ninja',
    }

    item_num_display = {
        None: ' ',
        0: 'r',
        1: 'w',
        2: 'o',
        3: 't',
        4: 's',
        5: 'h',
        6: 'm',
        50: 'G',
        51: 'B',
        52: 'N',
    }

    def weighted_random(self, dict):
        '''
        Takes a dict of item: weight pairs.
        Returns a random item taking into account the weight given.
        '''
        total_weight = 0
        for k, v in dict.iteritems():
            total_weight += v

        choice = random.randrange(0, total_weight - 1)

        for k, v in sorted(dict.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if choice <= v:
                return k
            else:
                choice -= v

        #except "Shouldn't ever reach this"

    def make_2d_board(self, x, y):
        '''
        Returns a list of lists with the width and height requested.
        '''
        return [[None for i in xrange(x)] for j in range(y)]

    def start_game(self):
        self.current_board = self.make_2d_board(6, 6)

        for i in xrange(random.randrange(3, 12)):
            lx = random.randrange(1, 6)
            ly = random.randrange(1, 6)
            # But we don't want to place anything in storage
            while lx == 1 and ly == 1:
                lx = random.randrange(1, 6)
                ly = random.randrange(1, 6)

            self.play(lx, ly, random.randrange(6))

        return self.current_board

    def clear_board(self):
        self.current_board = self.make_2d_board
        return True

    def play(self, x, y, item_type):
        if self.current_board[x][y] is None:
            self.current_board[x][y] = item_type
            self.update_board(x, y)
            return True
        else:
            return False

    def update_board(self, x, y, check_type=None, group=[]):  # TODO
        if check_type is None:
            check_type = self.current_board[x][y]

        if self.current_board[x][y] == check_type and (x, y) not in group:
            group.append((x, y))
        else:
            return

    def show_current_board(self):
        for x in self.current_board:
          map(x, self.item_num_to_name)

    def item_num_to_name(self, item_type):
        return item_num_names[item_type]

    def display_type(self, item_type):
        return item_num_display[item_type]
