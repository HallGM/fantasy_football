import unittest
from classes.team import Team
from tests.dummy_team import players

class TestTeam(unittest.TestCase):
    def setUp(self):
        self.team = Team()
        self.team.add_player(players[0])
        self.team.add_player(players[1])
    
    def test_update_value(self):
        self.assertAlmostEqual(self.team.value, 0.3)
        self.team.add_player(players[2])
        self.assertAlmostEqual(self.team.value, 0.8)
    
    def test_add_player(self):
        self.team.add_player(players[2])
        is_on_team = players[2] in self.team.players
        self.assertEqual(is_on_team, True)
    
    def test_is_position_filled(self):
        self.team.add_player(players[2])
        gk_filled = self.team.is_position_filled("GK")
        self.assertEqual(gk_filled, True)

    def test_is_team_completed(self):
        self.assertEqual(self.team.is_complete(), False)
        for player in players[2:11]:
            self.team.add_player(player)
        self.assertEqual(self.team.is_complete(), True)

    def test_can_afford_complete_team(self):
        actual = self.team.can_afford_complete_team(players[2:], 10)
        self.assertEqual(actual, True)
        actual = self.team.can_afford_complete_team(players[2:], 8.5)
        self.assertEqual(actual, True)
        actual = self.team.can_afford_complete_team(players[2:], 8.4)
        self.assertEqual(actual, False)
        actual = self.team.can_afford_complete_team(players[2:], 0)
        self.assertEqual(actual, False)

    def test_can_afford_player(self):
        actual = self.team.can_afford_player(players[2:], 0)
        self.assertEqual(actual, False)
        actual = self.team.can_afford_player(players[2:], 8.5)
        self.assertEqual(actual, True)
    
    def test_can_complete_team_with_remaining_players(self):
        actual = self.team.can_complete_team_with_remaining_players(players[2:])
        self.assertEqual(actual, True)
        actual = self.team.can_complete_team_with_remaining_players(players[3:])
        self.assertEqual(actual, False)
        test_team = Team()
        test_team.add_player(players[0])
        actual = test_team.can_complete_team_with_remaining_players([*players[2:], players[2]])
        self.assertEqual(actual, False)
        
