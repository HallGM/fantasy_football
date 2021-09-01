import unittest
from classes.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Patrick", "Liverpool", 3.2, 8.9, "FOR")

    def test_get_points(self):
        self.assertEqual(3.2, self.player.get_points())

    def test_get_cost(self):
        self.assertEqual(8.9, self.player.get_cost())

    def test_position_error(self):
        self.assertRaises(ValueError, Player, "test", "test", 0.1, 0.1, "ABC")
