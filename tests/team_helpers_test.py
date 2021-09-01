from tests.dummy_team import players
from helpers.team_helpers import *
from classes.team import Team
import unittest


class TestTeamHelpers(unittest.TestCase):

    def setUp(self):
        self.team1 = Team()
        self.team2 = Team()
        for i in range(3):
            self.team1.add_player(players[i])
            self.team2.add_player(players[i + 3])

    def test_score(self):
        self.assertEqual(score(players), 8.8)

    def test_cost(self):
        self.assertEqual(cost(players), 9.2)

    def test_best_team(self):
        self.assertEqual(best_team(self.team1, self.team2), self.team2)

    def test_get_cheapest_player(self):
        self.assertEqual(get_cheapest_player(players).name, "Patrick")

    def test_get_cheapest_players(self):
        cheapest = get_cheapest_players(players, 3)
        self.assertEqual(len(cheapest), 3)
        self.assertEqual(cheapest[0].name, "Patrick")
        self.assertEqual(cheapest[1].name, "Dave")
        self.assertEqual(cheapest[2].name, "Jim")
    
    def test_get_cheapest_players_zero(self):
        cheapest = get_cheapest_players(players, 0)
        self.assertEqual(len(cheapest), 0)

    def test_get_players_by_position(self):
        actual = get_players_by_position(players, "FOR")
        expected = [players[0], players[3]]
        self.assertEqual(actual, expected)

    def test_copy_team(self):
        new_team = copy_team(self.team1)
        new_team.add_player(players[3])
        self.assertEqual(len(new_team.players), 4)
        self.assertEqual(len(self.team1.players), 3)