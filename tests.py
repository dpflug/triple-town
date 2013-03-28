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
        self.assertTrue(self.game.place(5, 5, 1))
        self.assertEqual(self.game.get(5, 5), 1)

    def test_get(self):
        self.assertIsNone(self.game.get(0, 0))

    def test_empty(self):
        self.assertTrue(self.game.coord_empty(0, 0))

    def test_6x6(self):
        self.assertTrue(self.game.coord_empty(0, 0))
        self.assertTrue(self.game.coord_empty(5, 5))
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

    def test_storage(self):
        self.game.place(0, 0, 1)
        self.game.current_item = 2
        self.game.play(0, 0)
        self.assertEqual(self.game.get(0, 0), 2)
        self.assertEqual(self.game.current_item, 1)

    def test_play_nomatch(self):
        self.game.place(2, 3, 1)
        self.game.place(3, 3, 1)
        self.game.current_item = 1
        self.game.play(1, 1)
        self.assertEqual(self.game.get(1, 1), 1)
        self.assertEqual(self.game.get(2, 3), 1)
        self.assertEqual(self.game.get(3, 3), 1)
        self.assertEqual(self.game.score, 5)

    def test_play_storage_nomatch(self):
        self.game.place(0, 0, 1)
        self.game.place(1, 0, 1)
        self.game.current_item = 1
        self.game.play(2, 0)
        self.assertEqual(self.game.get(0, 0), 1)
        self.assertEqual(self.game.get(1, 0), 1)
        self.assertEqual(self.game.get(2, 0), 1)
        self.assertEqual(self.game.score, 5)

    def test_play_match_3(self):
        self.game.place(2, 3, 1)
        self.game.place(3, 3, 1)
        self.game.current_item = 1
        self.game.play(4, 3)
        self.assertEqual(self.game.get(4, 3), 2)
        self.assertEqual(self.game.score, 25)

    def test_play_match_3_all(self):
        for x in xrange(2, 8):
            self.game.place(4, 3, None)
            self.game.place(2, 3, x)
            self.game.place(3, 3, x)
            self.game.current_item = x
            self.game.play(4, 3)
            self.assertEqual(self.game.get(4, 3), x + 1)

    def test_play_match_4(self):
        self.game.place(2, 3, 1)
        self.game.place(3, 3, 1)
        self.game.place(4, 3, 1)
        self.game.current_item = 1
        self.game.play(5, 3)
        self.assertEqual(self.game.get(5, 3), 13)
        self.assertEqual(self.game.score, 45)

    def test_play_match_4_all(self):
        for x in xrange(2, 8):
            self.game.place(5, 3, None)
            self.game.place(2, 3, x)
            self.game.place(3, 3, x)
            self.game.place(4, 3, x)
            self.game.current_item = x
            self.game.play(5, 3)
            self.assertEqual(self.game.get(5, 3), x + 12)


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
        self.game.place(2, 1, 2)
        self.game.place(3, 2, 2)
        self.game.play(2, 2)
        self.assertEqual(self.game.get(2, 2), 3)
        self.assertEqual(self.game.score, 125)

    def test_play_match_4_chain_3(self):
        self.game.place(1, 2, 1)
        self.game.place(2, 1, 2)
        self.game.place(3, 2, 2)
        self.game.play(2, 2)
        self.assertEqual(self.game.get(2, 2), 3)
        self.assertEqual(self.game.score, 145)

    def test_play_match_3_chain_4(self):
        self.game.place(1, 2, 2)
        self.game.place(2, 1, 2)
        self.game.place(3, 2, 2)
        self.game.play(2, 2)
        self.assertEqual(self.game.get(2, 2), 14)
        self.assertEqual(self.game.score, 225)

    def test_play_match_4_chain_4(self):
        self.game.place(1, 2, 2)
        self.game.place(2, 1, 2)
        self.game.place(3, 2, 2)
        self.game.place(4, 3, 1)
        self.game.play(2, 2)
        self.assertEqual(self.game.get(2, 2), 14)
        self.assertEqual(self.game.score, 245)

    def test_play_match_3_multichain(self):
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
        self.game.place(2, 3, 0)
        self.game.play(2, 3)
        self.assertIsNone(self.game.get(2, 3))
        self.assertEqual(self.game.score, 100000)

    def test_bot_grass(self):
        self.game.place(2, 3, 1)
        self.game.play(2, 3)
        self.assertIsNone(self.game.get(2, 3))
        self.assertEqual(self.game.score, 100000 - 10)

    def test_bot_bear(self):
        self.game.place(2, 3, 51)
        self.game.play(2, 3)
        self.assertEqual(self.game.get(2, 3), 50)
        self.assertEqual(self.game.score, 100000)

    def test_bot_ninja(self):
        self.game.place(2, 3, 52)
        self.game.play(2, 3)
        self.assertEqual(self.game.get(2, 3), 50)
        self.assertEqual(self.game.score, 100000)

    def test_bot_blank(self):
        self.assertFalse(self.game.play(2, 3))

    def test_bot_castles(self):
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
        self.game.play(3, 3)
        self.assertEqual(self.game.get(3, 3), 0)
        self.assertEqual(self.game.score, 0)

    def test_crystal_match_3(self):
        for x in xrange(1, 8):
            self.game.current_item = 0
            self.game.place(3, 3, None)
            self.game.place(2, 3, x)
            self.game.place(3, 2, x)
            self.game.play(3, 3)
            self.assertEqual(self.game.get(3, 3), x + 1)

    def test_crystal_match_4(self):
        for x in xrange(1, 8):
            self.game.current_item = 0
            self.game.place(3, 3, None)
            self.game.place(2, 3, x)
            self.game.place(1, 3, x)
            self.game.place(3, 2, x)
            self.game.play(3, 3)
            self.assertEqual(self.game.get(3, 3), x + 12)

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
        self.game.play(3, 3)
        # They never choose to stay put.
        self.assertIsNone(self.game.get(3, 3))


if __name__ == '__main__':
    unittest.main()
