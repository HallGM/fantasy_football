import csv
from classes.player import Player
from classes.team import Team
import helpers.team_helpers as team_helpers

BUDGET = 83.8

players = []
with open("data.csv") as File:
    reader = csv.reader(File)
    for row in reader:
        if row[0] == "Player":
            continue
        players.append(Player(*row))


memo = {}
highest_team = [Team()]


def find_optimal_team(index, pot, team):
    # memoization
    id = (
        str(index)
        + str(team.position_capacity["FOR"])
        + str(team.position_capacity["DEF"])
        + str(team.position_capacity["MID"])
        + str(team.position_capacity["GK"])
    )
    if id in memo:
        for item in memo[id]:
            if pot <= item["max"] and pot >= item["min"]:
                for player in item["add_players"]:
                    team.add_player(player)
                return team

    # main algorithm
    if team.is_complete():
        return team
    elif index >= len(players):
        team.value = 0
        return team
    elif not team.can_complete_team_with_remaining_players(players[index:]):
        team.value = 0
        return team
    elif not team.can_afford_complete_team(players[index:], pot):
        team.value = 0
        return team
    elif team.is_position_filled(players[index].position) or not team.can_afford_player(
        players[index:], pot
    ):
        find_optimal_team(index + 1, pot, team_helpers.copy_team(team))
    else:
        test1 = find_optimal_team(index + 1, pot, team_helpers.copy_team(team))
        new_team = team_helpers.copy_team(team)
        new_team.add_player(players[index])
        test2 = find_optimal_team(index + 1, pot - players[index].get_cost(), new_team)
        best_team = team_helpers.best_team(test1, test2)
        if best_team.value > highest_team[0].value:
            highest_team[0] = best_team
            team_helpers.print_out_team(highest_team[0])

        # memoization
        if id not in memo:
            players_to_add = []
            for player in best_team.players:
                if player not in team.players:
                    players_to_add.append(player)
            memo[id] = [
                {
                    "max": pot,
                    "min": team_helpers.cost(best_team.players),
                    "add_players": players_to_add,
                }
            ]
        else:
            memo[id].append({"max": pot, "min": team_helpers.cost(best_team.players)})
            
        return best_team


print(find_optimal_team(0, BUDGET, Team()))