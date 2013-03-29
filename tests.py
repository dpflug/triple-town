import unittest
from tripletown import TripleTown


class TestBoard(unittest.TestCase):
    '''
    Test that we can create a board,
    that it's truly 6x6,
    and we can put items in it.
    '''

    def setUp(self):
        self.game = TripleTown()
        self.game.current_board = self.game.make_2d_board(6, 6)

    def test_place(self):
        # We can place items on it.
        self.assertTrue(self.game.place(5, 5, 1))
        self.assertEqual(self.game.get(5, 5), 1)

    def test_get(self):
        # It's created empty.
        for x in xrange(6):
            for y in xrange(6):
                self.assertIsNone(self.game.get(x, y))

    def test_empty(self):
        # We can check it for empty.
        self.assertIsNone(self.game.get(0, 0))
        self.assertTrue(self.game.coord_empty(0, 0))
        self.game.place(0, 0, 1)
        self.assertFalse(self.game.coord_empty(0, 0))

    def test_6x6(self):
        # It's only 6x6.
        self.assertRaises(IndexError, self.game.coord_empty, 0, 6)
        self.assertRaises(IndexError, self.game.coord_empty, 6, 0)


class TestGroup(TestBoard):
    '''
    Test that we can play pieces,
    that groups of 3 and 4 are handled correctly,
    and that we're scoring right.
    '''

    def setUp(self):
        self.game = TripleTown()
        self.game.current_board = self.game.make_2d_board(6, 6)
        self.game.score = 0

    def test_play_nomatch(self):
        # They only match if adjacent.
        self.game.place(2, 3, 1)
        self.game.place(3, 3, 1)
        self.game.current_item = 1
        self.game.play(1, 1)
        self.assertEqual(self.game.get(1, 1), 1)
        self.assertEqual(self.game.get(2, 3), 1)
        self.assertEqual(self.game.get(3, 3), 1)
        self.assertEqual(self.game.score, 5)

    def test_play_storage_nomatch(self):
        # They don't match with storage.
        self.game.place(0, 0, 1)
        self.game.place(1, 0, 1)
        self.game.current_item = 1
        self.game.play(2, 0)
        self.assertEqual(self.game.get(0, 0), 1)
        self.assertEqual(self.game.get(1, 0), 1)
        self.assertEqual(self.game.get(2, 0), 1)
        self.assertEqual(self.game.score, 5)

    def test_play_match_3(self):
        # They match in 3s, become next item.
        self.game.place(2, 3, 1)
        self.game.place(3, 3, 1)
        self.game.current_item = 1
        self.game.play(4, 3)
        self.assertEqual(self.game.get(4, 3), 2)
        self.assertEqual(self.game.score, 25)

    def test_play_match_3_all(self):
        # This works for a range of items.
        for x in range(2, 8) + [9, 40]:
            self.game.place(4, 3, None)
            self.game.place(2, 3, x)
            self.game.place(3, 3, x)
            self.game.current_item = x
            self.game.play(4, 3)
            self.assertEqual(self.game.get(4, 3), x + 1)

    def test_play_match_3_mtn_chain(self):
        # Mountains become treasure.
        self.game.place(5, 5, 11)
        self.game.place(5, 4, 11)
        self.game.place(4, 4, 0)
        self.game.place(4, 3, 0)
        self.game.current_item = 0
        self.game.play(4, 5)
        self.assertIsNone(self.game.get(4, 4))
        self.assertIsNone(self.game.get(5, 5))
        self.assertEqual(self.game.get(4, 5), 40)

    def test_play_match_4(self):
        # Big groups get bonuses.
        self.game.place(2, 3, 1)
        self.game.place(3, 3, 1)
        self.game.place(4, 3, 1)
        self.game.current_item = 1
        self.game.play(5, 3)
        self.assertEqual(self.game.get(5, 3), 13)
        self.assertEqual(self.game.score, 45)

    def test_play_match_4_all(self):
        # This works for many items.
        for x in xrange(2, 8):
            self.game.place(5, 3, None)
            self.game.place(2, 3, x)
            self.game.place(3, 3, x)
            self.game.place(4, 3, x)
            self.game.current_item = x
            self.game.play(5, 3)
            self.assertEqual(self.game.get(5, 3), x + 12)


class TestStorage(unittest.TestCase):
    '''
    Test that storage works correctly.
    '''

    def setUp(self):
        self.game = TripleTown()
        self.game.current_board = self.game.make_2d_board(6, 6)
        self.game.score = 0

    def test_storage(self):
        # It stores items.
        self.game.current_item = 15
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 15)
        self.assertEqual(self.game.score, 0)

    def test_storage_swap(self):
        # The current item gets swapped.
        self.game.current_item = 13
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 13)
        self.game.current_item = 15
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 15)
        self.assertEqual(self.game.current_item, 13)
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 13)
        self.assertEqual(self.game.current_item, 15)
        self.assertEqual(self.game.score, 0)

    def test_storage_bot(self):
        # The bot works, too.
        self.game.current_item = 53
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 53)
        self.game.current_item = 15
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 15)
        self.assertEqual(self.game.current_item, 53)
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 53)
        self.assertEqual(self.game.current_item, 15)
        self.assertEqual(self.game.score, 0)

    def test_storage_crystal(self):
        # So does the crystal.
        self.game.current_item = 0
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 0)
        self.game.current_item = 15
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 15)
        self.assertEqual(self.game.current_item, 0)
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 0)
        self.assertEqual(self.game.current_item, 15)
        self.assertEqual(self.game.score, 0)


class TestChaining(unittest.TestCase):
    '''
    Test that chained matches are working correctly.
    '''

    def setUp(self):
        self.game = TripleTown()
        self.game.current_board = self.game.make_2d_board(6, 6)
        self.game.score = 0
        self.game.place(2, 3, 1)
        self.game.place(3, 3, 1)
        self.game.current_item = 1

    def test_play_match_3_with_useless_neighbors(self):
        # Grouping isn't confused by strangers.
        for x in xrange(3, 11):
            self.game.current_item = 1
            self.game.place(2, 2, None)
            self.game.place(2, 3, 1)
            self.game.place(3, 3, 1)
            self.game.place(2, 1, x)
            self.game.place(3, 2, x)
            self.game.place(1, 2, x)
            self.game.play(2, 2)
            self.assertEqual(self.game.get(2, 1), x)
            self.assertEqual(self.game.get(3, 2), x)
            self.assertEqual(self.game.get(1, 2), x)
            self.assertEqual(self.game.get(2, 2), 2)

    def test_play_match_3_chain_3(self):
        # Chains of groups work.
        self.game.place(2, 1, 2)
        self.game.place(3, 2, 2)
        self.game.play(2, 2)
        self.assertEqual(self.game.get(2, 2), 3)
        self.assertEqual(self.game.score, 125)

    def test_play_match_4_chain_3(self):
        # And work with bonuses.
        self.game.place(1, 2, 1)
        self.game.place(2, 1, 2)
        self.game.place(3, 2, 2)
        self.game.play(2, 2)
        self.assertEqual(self.game.get(2, 2), 3)
        self.assertEqual(self.game.score, 145)

    def test_play_match_3_chain_4(self):
        # Both ways.
        self.game.place(1, 2, 2)
        self.game.place(2, 1, 2)
        self.game.place(3, 2, 2)
        self.game.play(2, 2)
        self.assertEqual(self.game.get(2, 2), 14)
        self.assertEqual(self.game.score, 225)

    def test_play_match_4_chain_4(self):
        # Double bonus!
        self.game.place(1, 2, 2)
        self.game.place(2, 1, 2)
        self.game.place(3, 2, 2)
        self.game.place(4, 3, 1)
        self.game.play(2, 2)
        self.assertEqual(self.game.get(2, 2), 14)
        self.assertEqual(self.game.score, 245)

    def test_play_match_3_multichain(self):
        # And the only limit to chaining is available space.
        self.game.place(1, 3, 2)
        self.game.place(1, 2, 2)
        self.game.place(1, 1, 3)
        self.game.place(2, 1, 3)
        self.game.place(3, 1, 4)
        self.game.place(3, 2, 4)
        self.game.current_item = 1
        self.game.play(2, 2)
        self.assertEqual(self.game.get(2, 2), 5)
        self.assertIsNone(self.game.get(1, 3))
        self.assertIsNone(self.game.get(1, 2))
        self.assertIsNone(self.game.get(1, 1))
        self.assertIsNone(self.game.get(2, 1))
        self.assertIsNone(self.game.get(3, 1))
        self.assertIsNone(self.game.get(3, 2))


class TestImperialBot(unittest.TestCase):
    '''
    Test that the Imperial Bot kills bears, removes items,
    penalizes destruction, and cannot be wasted.

    However, the penalties are hand-assigned in the G+ and
    Facebook versions of the game.
    https://spryfox.zendesk.com/entries/22264993-What-are-the-point-penalties-for-botting-structures-
    '''

    def setUp(self):
        self.game = TripleTown()
        self.game.current_board = self.game.make_2d_board(6, 6)
        self.game.score = 100000
        self.game.current_item = 53

    def test_bot_rock(self):
        # The bot removes rocks for free.
        self.game.place(2, 3, 0)
        self.game.play(2, 3)
        self.assertIsNone(self.game.get(2, 3))
        self.assertEqual(self.game.score, 100000)

    def test_bot_mountain(self):
        # Mountains become treasure and give 1000 points.
        self.game.place(2, 3, 11)
        self.game.play(2, 3)
        self.assertEqual(self.game.get(2, 3), 40)
        self.assertEqual(self.game.score, 101000)

    def test_bot_grass(self):
        # Grass has a penalty, though.
        self.game.place(2, 3, 1)
        self.game.play(2, 3)
        self.assertIsNone(self.game.get(2, 3))
        self.assertEqual(self.game.score, 100000 - 10)

    def test_bot_bear(self):
        # Bears die.
        self.game.place(2, 3, 51)
        self.game.play(2, 3)
        self.assertEqual(self.game.get(2, 3), 50)
        self.assertEqual(self.game.score, 100000)

    def test_bot_ninja(self):
        # Ninjas, too.
        self.game.place(2, 3, 52)
        self.game.play(2, 3)
        self.assertEqual(self.game.get(2, 3), 50)
        self.assertEqual(self.game.score, 100000)

    def test_bot_blank(self):
        # And we can't remove nothing.
        self.assertFalse(self.game.play(2, 3))

    def test_bot_castles(self):
        # Castles stick around, too.
        for item in [7, 8, 18, 19]:
            self.game.place(2, 3, item)
            self.game.current_item = 53
            self.assertFalse(self.game.play(2, 3))


class TestCrystal(unittest.TestCase):
    '''
    Test that the crystal matches correctly, turns into a rock without match.
    '''

    def setUp(self):
        self.game = TripleTown()
        self.game.current_board = self.game.make_2d_board(6, 6)
        self.game.score = 0
        self.game.current_item = 0

    def test_crystal_rock(self):
        # They become rocks when placed.
        # Note, this doesn't change much for my method. :P
        self.game.play(3, 3)
        self.assertEqual(self.game.get(3, 3), 0)
        self.assertEqual(self.game.score, 0)

    def test_crystal_match_3(self):
        # They match anything upgradable.
        for x in xrange(1, 8):
            self.game.current_item = 0
            self.game.place(3, 3, None)
            self.game.place(2, 3, x)
            self.game.place(3, 2, x)
            self.game.play(3, 3)
            self.assertEqual(self.game.get(3, 3), x + 1)

    def test_crystal_match_3b(self):
        # Upgraded items get downgraded correctly.
        for x in xrange(12, 19):
            self.game.current_item = 0
            self.game.place(3, 3, None)
            self.game.place(2, 3, x)
            self.game.place(3, 2, x)
            self.game.play(3, 3)
            self.assertEqual(self.game.get(3, 3), (x % 11) + 1)

    def test_crystal_match_4(self):
        # As well as grouping into upgrades.
        for x in xrange(1, 8):
            self.game.current_item = 0
            self.game.place(3, 3, None)
            self.game.place(2, 3, x)
            self.game.place(1, 3, x)
            self.game.place(3, 2, x)
            self.game.play(3, 3)
            self.assertEqual(self.game.get(3, 3), x + 12)

    def test_crystal_match_3_chain(self):
        # And chaining.
        self.game.place(2, 3, 1)
        self.game.place(4, 3, 1)
        self.game.place(3, 2, 2)
        self.game.place(3, 4, 2)
        self.game.play(3, 3)
        self.assertEqual(self.game.get(3, 3), 3)
        self.assertIsNone(self.game.get(2, 3))
        self.assertIsNone(self.game.get(4, 3))
        self.assertIsNone(self.game.get(3, 2))
        self.assertIsNone(self.game.get(3, 4))
        self.assertEqual(self.game.score, 125)


class TestBear(unittest.TestCase):
    '''
    Test that bears move when placed,
    die when trapped,
    don't move when trapped by other bears,
    and their graves combine to churches at
    the location of the most recent bear.
    '''

    def setUp(self):
        self.game = TripleTown()
        self.game.current_board = self.game.make_2d_board(6, 6)
        self.game.score = 0
        self.game.current_item = 51

    def test_bear_move(self):
        # They move.
        self.game.play(3, 3)
        # They never choose to stay put.
        self.assertIsNone(self.game.get(3, 3))

    def test_bear_move_storage(self):
        # They should move when we put something in storage.
        self.game.place(1, 1, 51)
        self.game.current_item = 1
        self.game.play(0, 0)
        self.assertIsNone(self.game.get(1, 1))

    def test_bear_move_crowded(self):
        # They move correctly when crowded by other bears.
        self.game.place(0, 2, 1)
        self.game.place(1, 0, 1)
        self.game.place(1, 2, 1)
        self.game.place(1, 1, 51)
        self.game.play(0, 1)
        self.assertEqual(self.game.get(0, 1), 51)
        self.assertIsNone(self.game.get(1, 1))

    def test_bear_live_crowded(self):
        # They don't die when crowded by other bears.
        self.game.place(0, 2, 1)
        self.game.place(1, 0, 1)
        self.game.place(1, 2, 1)
        self.game.place(0, 1, 51)
        self.game.play(1, 1)
        self.assertEqual(self.game.get(0, 1), 51)
        self.assertIsNone(self.game.get(1, 1))
        self.assertEqual(self.game.get(2, 1), 51)

    def test_bear_grass_trap(self):
        # Trap on all 4 sides
        self.game.place(3, 3, 51)
        self.game.place(2, 3, 1)
        self.game.place(3, 2, 1)
        self.game.place(4, 3, 1)
        self.game.current_item = 1
        self.game.play(3, 4)
        self.assertEqual(self.game.get(3, 3), 50)

    def test_bear_corner_grass_trap(self):
        # Trap in a corner
        self.game.place(5, 5, 51)
        self.game.place(4, 5, 1)
        self.game.current_item = 1
        self.game.play(5, 4)
        self.assertEqual(self.game.get(5, 5), 50)

    def test_bear_bear_trap(self):
        # Fill empty spot with bear
        self.game.place(3, 3, 51)
        self.game.place(3, 2, 1)
        self.game.place(2, 3, 1)
        self.game.place(3, 4, 1)
        self.game.place(4, 4, 1)
        self.game.place(4, 2, 1)
        self.game.place(5, 3, 1)
        self.game.play(4, 3)
        self.assertEqual(self.game.get(4, 3), 50)
        self.assertEqual(self.game.get(3, 3), 50)

    def test_bear_corner_bear_trap(self):
        # Fill empty spot in corner with bear
        self.game.place(5, 4, 1)
        self.game.place(4, 5, 1)
        self.game.play(5, 5)
        self.assertEqual(self.game.get(5, 5), 50)

    def test_bear_trap_chain(self):
        # Trap 3 bears
        self.game.place(5, 4, 1)
        self.game.place(4, 4, 2)
        self.game.place(3, 4, 3)
        self.game.place(2, 4, 4)
        self.game.place(1, 5, 5)
        self.game.place(5, 5, 51)
        self.game.place(4, 5, 51)
        self.game.place(3, 5, 51)
        self.game.current_item = 1
        self.game.play(2, 5)
        self.assertEqual(self.game.get(3, 5), 9)

    def test_bear_trap_bear_chain(self):
        # Trap 4 bears with bear
        self.game.place(5, 4, 1)
        self.game.place(4, 4, 2)
        self.game.place(3, 4, 3)
        self.game.place(2, 4, 4)
        self.game.place(1, 5, 5)
        self.game.place(5, 5, 51)
        self.game.place(4, 5, 51)
        self.game.place(3, 5, 51)
        self.game.play(2, 5)
        self.assertEqual(self.game.get(2, 5), 20)

    def test_bear_trap_chain_2(self):
        # Trap 3 bears with 2 churches adjacent
        self.game.place(5, 4, 9)
        self.game.place(4, 4, 9)
        self.game.place(3, 4, 1)
        self.game.place(2, 5, 1)
        self.game.place(3, 5, 51)
        self.game.place(4, 5, 51)
        self.game.play(5, 5)
        self.assertEqual(self.game.get(5, 5), 10)

    def test_bear_trap_4_chain(self):
        # Trap 4 bears with 2 churches adjacent
        self.game.place(5, 4, 9)
        self.game.place(4, 4, 9)
        self.game.place(3, 4, 1)
        self.game.place(2, 4, 1)
        self.game.place(1, 5, 1)
        self.game.place(2, 5, 51)
        self.game.place(3, 5, 51)
        self.game.place(4, 5, 51)
        self.game.play(5, 5)
        self.assertEqual(self.game.get(5, 5), 10)

    def test_bear_trap_3_chain_3(self):
        # Trap 3 bears with 3 churches adjacent
        self.game.place(5, 4, 9)
        self.game.place(4, 4, 9)
        self.game.place(3, 4, 9)
        self.game.place(2, 5, 1)
        self.game.place(3, 5, 51)
        self.game.place(4, 5, 51)
        self.game.play(5, 5)
        self.assertEqual(self.game.get(5, 5), 10)

if __name__ == '__main__':
    unittest.main()
