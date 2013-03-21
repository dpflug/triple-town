#!/usr/bin/env python2

import random


class TripleTown(object):
    item_weights = {
        1: 4193,
        2: 1070,
        51: 1044,
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
        'house': 1500,
        'mansion': 5000,
        'castle': 20000,
        'float': 100000,
        'church': 1000,
        'cathedral': 5000,
        'treasure': 10000,
        'gravestone': 0,
        'bear': 0,
        'ninja': 0,
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
        7: 'castle',
        8: 'floating castle',
        9: 'church',
        10: 'cathedral',
        11: 'mountain',
        12: 'grass',
        13: 'bush+',
        14: 'tree+',
        15: 'hut+',
        16: 'house+',
        17: 'mansion+',
        18: 'castle+',
        19: 'floating castle+',
        20: 'church+',
        21: 'cathedral+',
        50: 'gravestone',
        51: 'bear',
        52: 'ninja',
        53, 'bot',
    }

    item_num_display = {
        None: '_',
        0: 'r',
        1: 'w',
        2: 'o',
        3: 't',
        4: 's',
        5: 'h',
        6: 'm',
        7: 'c',
        8: 'f',
        9: '+',
        10: '=',
        11: '^',
        12: 'W',
        13: 'O',
        14: 'T',
        15: 'S',
        16: 'H',
        17: 'M',
        18: 'C',
        19: 'F',
        20: '%',
        21: '#',
        50: 'g',
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
            lx = random.randrange(6)
            ly = random.randrange(6)
            # But we don't want to place anything in storage
            while lx == 0 and ly == 0:
                lx = random.randrange(6)
                ly = random.randrange(6)

            self.place(lx, ly, random.randrange(6))

        self.current_item = self.weighted_random(self.item_weights)

        return self.current_board

    def clear_board(self):
        self.current_board = self.make_2d_board
        return True

    def place(self, x, y, item):
        self.current_board[x][y] = item

    def play(self, x, y):
        x -= 1
        y -= 1
        if x == 0 and y == 0:
            if self.current_board[0][0] is None:
                self.current_board[0][0] = self.current_item
            else:
                temp = self.current_item
                self.current_item = self.current_board[0][0]
                self.current_board[0][0] = temp
            return True

        elif self.current_item == 53:  # Bot
            target = self.current_board[x][y]
            if target == 51 or target == 52:  # Bear
                self.current_board[x][y] = 50  # Kilt
                self.update_board(x, y)
            elif target = None:
                return False
            else:
                self.current_board[x][y] = None
                return True

        elif self.current_board[x][y] is None:
            self.current_board[x][y] = self.current_item
            self.update_board(x, y)
            return True

        else:
            return False

    def update_board(self, x, y):
        group = self.find_group(x, y)

        if len(group) == 3:
            # Do stuff
            print(group)
            pass
        if len(group) > 3:
            # Do better stuff
            print(group)
            pass

        return group

    def find_group(self, x, y, group=set([]), bears=set([])):
        check_type = self.current_board[x][y]
        group.add((x, y))

        for neighbor in self.adjacent_nodes(x, y):
            node_x = neighbor[0]
            node_y = neighbor[1]
            node_type = self.current_board[neighbor[0]][neighbor[1]]
            if node_type == check_type and neighbor not in group:
                neighbor_group = self.find_group(node_x, node_y, group)
                group.add(neighbor_group)
            if node_type == 51:  # We found a bear!
                bears.add((node_x, node_y))

        if len(bears) > 0:
            return group, bears
        else:
            return group

    def adjacent_nodes(self, x, y):
        adj = []

        if x > 0:
            adj.append((x - 1, y))
        if y > 0:
            adj.append((x, y - 1))
        if x < 5:
            adj.append((x + 1, y))
        if y < 5:
            adj.append((x, y + 1))

        # 0,0 is the holding area. It has its own special rules.
        # As such, it doesn't count as adjacent to anything.
        if (0, 0) in adj:
            adj.remove((0, 0))

        return adj

    def show_current_board(self):
        for row in self.current_board:
            print " ".join(map(self.item_num_to_display, row))

    def item_num_to_name(self, item_type):
        return self.item_num_names[item_type]

    def item_num_to_display(self, item_type):
        return self.item_num_display[item_type]
