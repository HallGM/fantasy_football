from classes.player import Player
from helpers.team_helpers import *
from functools import reduce
from random import random
from copy import copy
import math
import csv
import pdb

BUDGET = 83.8
ITERATIONS = 10000
POPULATION_SIZE = 50

players = []

with open("data.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == "Player":
            continue
        players.append(Player(*row))

team =[]

team_by_positions = {}
for position in ["GK", "DEF", "FOR", "MID"]:
    team_by_positions[position] = get_players_by_position(players, position)

def random_pick(players):
    ran = math.floor(random() * len(players))
    return players[ran]

def random_pick_multiple(players, num):
    result = []
    players_copy = copy(players)
    for i in range(num):
        ran_player = random_pick(players_copy)
        result.append(ran_player)
        players_copy.remove(ran_player)
    return result

def random_pick_multiple_copyless(players, num):
    result = []
    for i in range(num):
        ran_player = random_pick(players)
        result.append(ran_player)
        players.remove(ran_player)
    return result    

def generate_random_team():
    team = []
    team.append(random_pick(team_by_positions["GK"]))
    team += random_pick_multiple(team_by_positions["DEF"], 4)
    team += random_pick_multiple(team_by_positions["MID"], 4)
    team += random_pick_multiple(team_by_positions["FOR"], 2)
    return team

def determine_team_cost(team):
    return sum([player.get_cost() for player in team])

def determine_team_score(team):
    total_cost = sum([player.get_cost() for player in team])
    if total_cost > BUDGET:
        return 0
    else: 
        return sum([player.get_points() for player in team])

def generate_all_teams():
    return [generate_random_team() for i in range(POPULATION_SIZE)]

def get_best_team(teams):
    def better_team(team1, team2):
        return team1 if determine_team_score(team1) > determine_team_score(team2) else team2
    return reduce(better_team, teams)

def get_best_2_teams(teams):
    teams_copy = copy(teams)
    team1 = get_best_team(teams_copy)
    teams_copy.remove(team1)
    team2 = get_best_team(teams_copy)
    return [team1, team2]

def breed(team1, team2):
    positions = list(range(11))
    mother = random_pick_multiple_copyless(positions, 5)
    father = random_pick_multiple_copyless(positions, 5)
    mutation_index = positions[0]
    child = list(range(11))
    for index in mother:
        child[index] = team1[index]
    for index in father:
        if team2[index] in team1:
            child[index] = team1[index]
        else:
            child[index] = team2[index]
    mutation_position = team1[mutation_index].position
    picked_player = random_pick(team_by_positions[mutation_position])
    if picked_player in child: 
        if team1[mutation_index] not in child:
            child[mutation_index] = team1[mutation_index]
        else:
            child[mutation_index] = team2[mutation_index]
    else:
        child[mutation_index] = picked_player
    return child

def breed_all_children(best_2_teams):
    return [breed(*best_2_teams) for i in range(POPULATION_SIZE)]

count = [0]
def runner(teams):
    best_team = get_best_team(teams)
    best_2_teams = get_best_2_teams(teams)
    children = breed_all_children(best_2_teams)
    return [best_team, children]

current_teams = generate_all_teams()
highest_scoring_team = [None]
highest_scoring_team[0] = get_best_team(current_teams)
high_score = [0]
high_score[0] = determine_team_score(highest_scoring_team[0])
for i in range(ITERATIONS):
    result = runner(current_teams)
    current_teams = result[1]
    best_team = result[0]
    team_score = determine_team_score(result[0])
    if team_score > high_score[0]:
        high_score[0] = team_score
        highest_scoring_team[0] = best_team
        print("new high score!")
        print(team_score)

    
print("\nBest Team: ")
[print(str(player.position) + ": " + str(player.name)) for player in highest_scoring_team[0]]
print("score: " + str(high_score[0]))

with open('selection.csv', mode="w") as file:
    writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Player', 'Team', 'Points', 'Cost', 'Position'])
    for player in highest_scoring_team[0]:
        writer.writerow([player.name, player.team, player.get_points(), player.cost, player.position])


