from functools import reduce
import copy
import pdb

def score(players):
    return sum([player.get_points() for player in players])

def cost(team):
    return sum([player.get_cost() for player in team])

def best_team(team1, team2):
    if team2 == None:
        return team1
    return team1 if score(team1.players) > score(team2.players) else team2

def get_cheapest_player(players):
    def cheaper(player1,player2):
        return player1 if player1.cost < player2.cost else player2
    return reduce(cheaper, players)

def get_cheapest_players(players, no_of_players):
    group = [*players]
    cheapest_players = []
    for i in range(no_of_players):
        cheapest_player = get_cheapest_player(group)
        cheapest_players.append(cheapest_player)
        group.remove(cheapest_player)
    return cheapest_players

def get_players_by_position(players, position):
    return list(filter(lambda player: player.position == position, players))

def copy_team(team):
    new_team = copy.copy(team)
    new_team.players = copy.copy(team.players)
    new_team.position_capacity = copy.deepcopy(team.position_capacity)
    return new_team

def print_out_team(team):
    print('')
    print('Players: ')
    print(", ".join([str(player.position) + ": " + str(player.name) for player in team.players]))
    print('Value: ')
    print(team.value)
    print("Position Capacity: ")
    print(team.position_capacity)
