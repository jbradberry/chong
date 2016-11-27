import unittest

from chong import chong


board = chong.Board()


class IsLegalPlacementTestCase(unittest.TestCase):
    def test_simple_placement(self):
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(7, 4)]

        # p1 to move
        player = 1
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (3, 3, True)))

        # p2 to move
        player = 2
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (4, 4, True)))

    def test_p1_home_row(self):
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(1, 4)]

        # p1 to move
        player = 1
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (0, 4, True)))

        # p2 to move
        player = 2
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (0, 4, True)))

    def test_p2_home_row(self):
        p1 = board.positions[(6, 3)]
        p2 = board.positions[(7, 4)]

        # p1 to move
        player = 1
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (7, 3, True)))

        # p2 to move
        player = 2
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (7, 3, True)))

    def test_occupied_by_enemy_pawn(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 4, True)))

        # p2 to move
        player = 2
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 3, True)))

    def test_occupied_by_friendly_pawn(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 3, True)))

        # p2 to move
        player = 2
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 4, True)))

    def test_occupied_by_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (4, 4, True)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 3, True)))

    def test_occupied_by_friendly_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 4, True)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (3, 3, True)))

    def test_stones_exhausted(self):
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(7, 4)]

        # p1 to move
        player = 1
        stones = sum(board.positions[(1, x)] for x in xrange(6))
        history = [(p1, p2, stones, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 4, True)))

        # p2 to move
        player = 2
        stones = sum(board.positions[(6, x)] for x in xrange(7))
        history = [(p1, p2, 0, stones, player)]
        self.assertFalse(board.is_legal(history, (3, 3, True)))


class IsLegalMoveTestCase(unittest.TestCase):
    def test_north_simple(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (2, 3, False)))

        # p2 to move
        player = 2
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (3, 4, False)))

    def test_north_enemy_pawn_block(self):
        # p1 to move
        player = 1
        p1 = board.positions[(4, 3)]
        p2 = board.positions[(3, 3)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(4, 4)]
        p2 = board.positions[(5, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 4, False)))

    def test_north_enemy_stone_block(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        stone = board.positions[(2, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (2, 3, False)))

        # p2 to move
        player = 2
        stone = board.positions[(3, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 4, False)))

    def test_north_friendly_stone_block(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        stone = board.positions[(2, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (2, 3, False)))

        # p2 to move
        player = 2
        stone = board.positions[(3, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (3, 4, False)))

    def test_south_simple(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (4, 3, False)))

        # p2 to move
        player = 2
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (5, 4, False)))

    def test_south_enemy_pawn_block(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 3)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(5, 4)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 4, False)))

    def test_south_enemy_stone_block(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        stone = board.positions[(4, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (4, 3, False)))

        # p2 to move
        player = 2
        stone = board.positions[(5, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 4, False)))

    def test_south_friendly_stone_block(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        stone = board.positions[(4, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 3, False)))

        # p2 to move
        player = 2
        stone = board.positions[(5, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (5, 4, False)))

    def test_east_simple(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (3, 2, False)))

        # p2 to move
        player = 2
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (4, 3, False)))

    def test_east_enemy_pawn_block(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(3, 2)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 2, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(4, 3)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 3, False)))

    def test_east_enemy_stone_block(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        stone = board.positions[(3, 2)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (3, 2, False)))

        # p2 to move
        player = 2
        stone = board.positions[(4, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 3, False)))

    def test_east_friendly_stone_block(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        stone = board.positions[(3, 2)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 2, False)))

        # p2 to move
        player = 2
        stone = board.positions[(4, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (4, 3, False)))

    def test_west_simple(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (3, 4, False)))

        # p2 to move
        player = 2
        history = [(p1, p2, 0, 0, player)]
        self.assertTrue(board.is_legal(history, (4, 5, False)))

    def test_west_enemy_pawn_block(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(3, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 4, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(4, 5)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 5, False)))

    def test_west_enemy_stone_block(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        stone = board.positions[(3, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (3, 4, False)))

        # p2 to move
        player = 2
        stone = board.positions[(4, 5)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 5, False)))

    def test_west_friendly_stone_block(self):
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(4, 4)]

        # p1 to move
        player = 1
        stone = board.positions[(3, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 4, False)))

        # p2 to move
        player = 2
        stone = board.positions[(4, 5)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (4, 5, False)))


class IsLegalJumpTestCase(unittest.TestCase):
    def test_north_simple(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(2, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertTrue(board.is_legal(history, (1, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertTrue(board.is_legal(history, (2, 4, False)))

    def test_north_no_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (1, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (2, 4, False)))

    def test_north_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(2, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (1, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (2, 4, False)))

    def test_north_blocking_pawn(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(1, 3)]
        stone = board.positions[(2, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (1, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(2, 4)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (2, 4, False)))

    def test_north_blocking_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        p1_stone = board.positions[(2, 3)]
        p2_stone = board.positions[(1, 3)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (1, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        p1_stone = board.positions[(2, 4)]
        p2_stone = board.positions[(3, 4)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (2, 4, False)))

    def test_north_blocking_friendly_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(2, 3)] + board.positions[(1, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (1, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 4)] + board.positions[(2, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (2, 4, False)))

    def test_nw_simple(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(2, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertTrue(board.is_legal(history, (1, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 5)]
        history = [(p1, p2, 0, stone, player)]
        self.assertTrue(board.is_legal(history, (2, 6, False)))

    def test_nw_no_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (1, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (2, 6, False)))

    def test_nw_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(2, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (1, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 5)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (2, 6, False)))

    def test_nw_blocking_pawn(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(1, 5)]
        stone = board.positions[(2, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (1, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(2, 6)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 5)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (2, 6, False)))

    def test_nw_blocking_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        p1_stone = board.positions[(2, 4)]
        p2_stone = board.positions[(1, 5)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (1, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        p1_stone = board.positions[(2, 6)]
        p2_stone = board.positions[(3, 5)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (2, 6, False)))

    def test_nw_blocking_friendly_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(2, 4)] + board.positions[(1, 5)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (1, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 5)] + board.positions[(2, 6)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (2, 6, False)))

    def test_west_simple(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(3, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertTrue(board.is_legal(history, (3, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(4, 5)]
        history = [(p1, p2, 0, stone, player)]
        self.assertTrue(board.is_legal(history, (4, 6, False)))

    def test_west_no_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 6, False)))

    def test_west_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(3, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (3, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(4, 5)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 6, False)))

    def test_west_blocking_pawn(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(3, 5)]
        stone = board.positions[(3, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(4, 6)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(4, 5)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (4, 6, False)))

    def test_west_blocking_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        p1_stone = board.positions[(3, 4)]
        p2_stone = board.positions[(3, 5)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (3, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        p1_stone = board.positions[(4, 6)]
        p2_stone = board.positions[(4, 5)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (4, 6, False)))

    def test_west_blocking_friendly_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(3, 4)] + board.positions[(3, 5)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(4, 5)] + board.positions[(4, 6)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (4, 6, False)))

    def test_sw_simple(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertTrue(board.is_legal(history, (5, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 5)]
        history = [(p1, p2, 0, stone, player)]
        self.assertTrue(board.is_legal(history, (6, 6, False)))

    def test_sw_no_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (6, 6, False)))

    def test_sw_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (5, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 5)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (6, 6, False)))

    def test_sw_blocking_pawn(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(5, 5)]
        stone = board.positions[(4, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(6, 6)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 5)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (6, 6, False)))

    def test_sw_blocking_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        p1_stone = board.positions[(4, 4)]
        p2_stone = board.positions[(5, 5)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (5, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        p1_stone = board.positions[(6, 6)]
        p2_stone = board.positions[(5, 5)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (6, 6, False)))

    def test_sw_blocking_friendly_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 4)] + board.positions[(5, 5)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 5, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 5)] + board.positions[(6, 6)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (6, 6, False)))

    def test_south_simple(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertTrue(board.is_legal(history, (5, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertTrue(board.is_legal(history, (6, 4, False)))

    def test_south_no_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (6, 4, False)))

    def test_south_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (5, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 4)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (6, 4, False)))

    def test_south_blocking_pawn(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(5, 3)]
        stone = board.positions[(4, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(6, 4)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (6, 4, False)))

    def test_south_blocking_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        p1_stone = board.positions[(4, 3)]
        p2_stone = board.positions[(5, 3)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (5, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        p1_stone = board.positions[(6, 4)]
        p2_stone = board.positions[(5, 4)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (6, 4, False)))

    def test_south_blocking_friendly_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 3)] + board.positions[(5, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 3, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 4)] + board.positions[(6, 4)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (6, 4, False)))

    def test_se_simple(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 2)]
        history = [(p1, p2, stone, 0, player)]
        self.assertTrue(board.is_legal(history, (5, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertTrue(board.is_legal(history, (6, 2, False)))

    def test_se_no_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (6, 2, False)))

    def test_se_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 2)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (5, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (6, 2, False)))

    def test_se_blocking_pawn(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(5, 1)]
        stone = board.positions[(4, 2)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(6, 2)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (6, 2, False)))

    def test_se_blocking_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        p1_stone = board.positions[(4, 2)]
        p2_stone = board.positions[(5, 1)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (5, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        p1_stone = board.positions[(6, 2)]
        p2_stone = board.positions[(5, 3)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (6, 2, False)))

    def test_se_blocking_friendly_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(4, 2)] + board.positions[(5, 1)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (5, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(5, 3)] + board.positions[(6, 2)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (6, 2, False)))

    def test_east_simple(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(3, 2)]
        history = [(p1, p2, stone, 0, player)]
        self.assertTrue(board.is_legal(history, (3, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(4, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertTrue(board.is_legal(history, (4, 2, False)))

    def test_east_no_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 2, False)))

    def test_east_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(3, 2)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (3, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(4, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (4, 2, False)))

    def test_east_blocking_pawn(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(3, 1)]
        stone = board.positions[(3, 2)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(4, 2)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(4, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (4, 2, False)))

    def test_east_blocking_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        p1_stone = board.positions[(3, 2)]
        p2_stone = board.positions[(3, 1)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (3, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        p1_stone = board.positions[(4, 2)]
        p2_stone = board.positions[(4, 3)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (4, 2, False)))

    def test_east_blocking_friendly_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(3, 2)] + board.positions[(3, 1)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (3, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(4, 3)] + board.positions[(4, 2)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (4, 2, False)))

    def test_ne_simple(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(2, 2)]
        history = [(p1, p2, stone, 0, player)]
        self.assertTrue(board.is_legal(history, (1, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertTrue(board.is_legal(history, (2, 2, False)))

    def test_ne_no_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (1, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        history = [(p1, p2, 0, 0, player)]
        self.assertFalse(board.is_legal(history, (2, 2, False)))

    def test_ne_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(2, 2)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (1, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 3)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (2, 2, False)))

    def test_ne_blocking_pawn(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(1, 1)]
        stone = board.positions[(2, 2)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (1, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(2, 2)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 3)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (2, 2, False)))

    def test_ne_blocking_enemy_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        p1_stone = board.positions[(2, 2)]
        p2_stone = board.positions[(1, 1)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (1, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        p1_stone = board.positions[(2, 2)]
        p2_stone = board.positions[(3, 3)]
        history = [(p1, p2, p1_stone, p2_stone, player)]
        self.assertFalse(board.is_legal(history, (2, 2, False)))

    def test_ne_blocking_friendly_stone(self):
        # p1 to move
        player = 1
        p1 = board.positions[(3, 3)]
        p2 = board.positions[(7, 4)]
        stone = board.positions[(2, 2)] + board.positions[(1, 1)]
        history = [(p1, p2, stone, 0, player)]
        self.assertFalse(board.is_legal(history, (1, 1, False)))

        # p2 to move
        player = 2
        p1 = board.positions[(0, 3)]
        p2 = board.positions[(4, 4)]
        stone = board.positions[(3, 3)] + board.positions[(2, 2)]
        history = [(p1, p2, 0, stone, player)]
        self.assertFalse(board.is_legal(history, (2, 2, False)))
