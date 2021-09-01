import helpers.team_helpers as helpers
import copy
import pdb

class Team:
    def __init__(self):
        self.players = []
        self.value = 0
        self.position_capacity = {"FOR": 2, "DEF": 4, "MID": 4, "GK": 1}
    
    def update_value(self):
        self.value = sum([player.get_points() for player in self.players])

    def add_player(self, player):
        if self.position_capacity[player.position] <= 0:
            raise Exception("cannot add this player, no capacity")
        self.players.append(player)
        self.update_value()
        self.position_capacity[player.position] -= 1
        

    def is_position_filled(self, position):
        return self.position_capacity[position] == 0

    def is_complete(self):
        result = True
        for position in self.position_capacity:
            if self.position_capacity[position] != 0:
                result = False
                break
        return result

    def can_afford_complete_team(self, remaining_players, pot):
        price = 0
        for position_index in self.position_capacity:
            capacity = self.position_capacity[position_index]
            players_in_position = helpers.get_players_by_position(remaining_players, position_index)
            cheapest_players = helpers.get_cheapest_players(players_in_position, capacity)
            price += helpers.cost(cheapest_players)
        return pot >= price
    
    def can_afford_player(self, remaining_players, pot):
        trial_team = helpers.copy_team(self)
        players = copy.copy(remaining_players)
        trial_team.add_player(players.pop())
        return trial_team.can_afford_complete_team(players, pot)

    def can_complete_team_with_remaining_players(self, remaining_players):
        result = True
        for position in self.position_capacity:
            capacity = self.position_capacity[position]
            remaining_in_position = len(helpers.get_players_by_position(remaining_players, position))
            if capacity > remaining_in_position:
                return False
        return True