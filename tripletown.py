#!/usr/bin/env python2

import random


class TripleTown(object):
    item_weights = {
        1: 4193,
        2: 1070,
        51: 1044,
        53: 176,
        0: 168,  # 0 is a crystal, turns into rock if not grouped
        3: 136,
        52: 99,
        4: 44,
    }

    item_scores = {
        0: 0,
        1: 5,
        2: 20,
        3: 100,
        4: 500,
        5: 1500,
        6: 5000,
        7: 20000,
        8: 100000,
        9: 1000,
        10: 5000,
        11: 0,
        12: 5,
        13: 40,
        14: 200,
        15: 1000,
        16: 3000,
        17: 10000,
        18: 40000,
        19: 200000,
        20: 2000,
        21: 10000,
        40: 10000,
        50: 0,
        51: 0,
        53: 0,
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
        40: 'treasure',
        50: 'gravestone',
        51: 'bear',
        52: 'ninja',
        53: 'bot',
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

    def weighted_random(self, item_dict):
        '''
        Takes a dict of item: weight pairs.
        Returns a random item taking into account the weight given.
        '''
        total_weight = 0
        for k, v in item_dict.iteritems():
            total_weight += v

        choice = random.randrange(0, total_weight - 1)

        for k, v in sorted(
                item_dict.iteritems(),
                key=lambda (k, v): (v, k),
                reverse=True):
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
        '''
        Creates a new current_board, fills it with 3-12 items, sets
        score=0 and current_item to something random.

        Returns the board, just because it can.
        '''
        self.score = 0
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
        '''
        Empties the current board
        '''
        self.current_board = self.make_2d_board
        return True

    def place(self, x, y, item):
        '''
        Puts an item at a place. Overwrites with impunity.
        '''
        self.current_board[x][y] = item
        return True

    def play(self, x, y):
        '''
        Plays an item at a place.

        Returns True if the move is made successfully, False if not.

        This has the side effect of updating the board according to the rules.
        '''
        if x == 0 and y == 0:
            if self.current_board[0][0] is None:
                self.place(0, 0, self.current_item)
                self.current_item = self.weighted_random(self.item_weights)
            else:
                temp = self.current_item
                self.current_item = self.current_board[0][0]
                self.place(0, 0, temp)
            return True

        elif self.current_item == 53:  # Bot
            target = self.current_board[x][y]
            if target == 51 or target == 52:  # Bear
                self.place(x, y, 50)  # Kilt
                self.update_board(x, y)
            elif target is None:
                return False
            else:
                self.current_board[x][y] = None
                return True

            self.current_item = self.weighted_random(self.item_weights)

        elif self.current_item == 0:  # Crystal
            # How should I do wildcard matches?
            # Maybe for each in adjacent, check for groups, then call
            # play() with the type that has the highest number/type
            # TODO
            return False

        elif self.current_board[x][y] is None:
            self.place(x, y, self.current_item)
            self.score += self.item_scores[self.current_item]
            self.update_board(x, y)
            self.current_item = self.weighted_random(self.item_weights)

        else:
            return False

    def update_board(self, x, y):
        '''
        Updates the board, given the coords of the placed item.
        '''
        loop = False
        # For some reason, I have to pass an empty set to find_group. Why?
        # Is group not being reinitialized?
        # No, it's not. set() is evaluated at compile time and never again.
        # Price of being in a function definition?
        group = self.find_group(x, y, set([]))
        type = self.current_board[x][y]

        if len(group) >= 3:
            # Do stuff
            for node in group:
                self.current_board[node[0]][node[1]] = None
            if type is None:
                raise Exception("update_board() called on empty cell ({}, {}).".format(x, y))
            elif type == 0:  # Rocks become mountains
                self.place(x, y, 11)
            elif 0 < type < 8 or type == 10:  # Normal upgrades
                if len(group) == 3:
                    offset = 1  # Used to compute which upgrade to give
                else:
                    offset = 11
                new_type = type % 11 + offset
                self.place(x, y, new_type)
                self.score += self.item_scores[new_type]
                loop = True
            else:
                self.status()
                raise Exception("Unsure what to do. Group {} originating at ({}, {}) is type {}.".format(group, x, y, type))

        self.move_bears()

        if loop:
            self.update_board(x, y)

        return group

    def move_bears(self):
        pass

    def find_group(self, x, y, group=set([])):
        '''
        Given coordinates, returns a list of coordinates of connected
        items matching that type.
        '''
        check_type = self.current_board[x][y]
        if check_type is None:
            return False
        group.add((x, y))

        for neighbor in self.adjacent_nodes(x, y):
            node_x = neighbor[0]
            node_y = neighbor[1]
            node_type = self.current_board[neighbor[0]][neighbor[1]]
            # This is big and ugly. Can I improve it?
            # Currently have to check that I've not checked before,
            # that the space isn't empty, and that it's of appropriate type.
            if neighbor not in group and node_type is not None and (check_type % 11) == (node_type % 11) and node_type < 40:
                neighbor_group = self.find_group(node_x, node_y, group)
                group.union(neighbor_group)

        return group

    def adjacent_nodes(self, x, y):
        '''
        Given x and y, returns a list of coordinates adjacent to it,
        handling literal edge cases and the fact that 0,0 is a storage area
        rather than play area.
        '''
        adj = []

        if x > 0:
            adj.append((x - 1, y))
        if y > 0:
            adj.append((x, y - 1))
        if x < 5:
            adj.append((x + 1, y))
        if y < 5:
            adj.append((x, y + 1))

        # 0,0 is the storage area. It has its own special rules.
        # As such, it doesn't count as adjacent to anything.
        if (0, 0) in adj:
            adj.remove((0, 0))

        return adj

    def show_current_board(self):
        '''
        Pretty prints the board
        '''
        for row in self.current_board:
            print " ".join(map(self.item_num_to_display, row))

    def status(self):
        '''
        Prints the game status.
        '''
        self.show_current_board()
        print ""
        print "Current item: {}".format(self.item_num_names[self.current_item])
        print "Score: {}".format(self.score)

    def game_running(self):
        '''
        Returns True if there's a blank spot on the board, otherwise False.
        '''

        # Protect storage, but keep from triggering false positive
        temp = self.current_board[0][0]
        self.current_board[0][0] = 1

        for x in xrange(6):
            if None in self.current_board[x]:
                self.current_board[0][0] = temp
                return True

        self.current_board[0][0] = temp
        return False

    def run(self):
        '''
        Loops on input from user, plays game.
        '''
        self.start_game()
        while self.game_running():
            self.status()
            print ""
            try:
                play = raw_input("> ")
            except EOFError:
                break
            if play[0].lower() == "q":  # Allow user to quit
                break

            coords = play.split(",")

            # Adjust for 0-indexed arrays and x/y reversal
            t = int(coords[0]) - 1
            coords[0] = int(coords[1]) - 1
            coords[1] = t
            self.play(coords[0], coords[1])

    def item_num_to_display(self, item_type):
        '''
        Given the item number, returns an ASCII representation of it.
        '''
        return self.item_num_display[item_type]
