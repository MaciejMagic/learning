# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # Read teams into memory from file
    # open csv file
    with open(sys.argv[1]) as file:
        # call reader method
        reader = csv.DictReader(file)
        # read each row from file as a dictionary with two keys
        for team in reader:
            # convert rating key to integer type
            team["rating"] = int(team["rating"])
            # add dict to teams list
            teams.append(team)

    counts = {}
    # Simulate N tournaments and keep track of win counts
    for i in range(N):
        # determine team name from simulate function
        winner = simulate_tournament(teams)
        # add a win to deteremined team
        if winner in counts:
            counts[winner] += 1
        else:
            counts[winner] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # call sim round function until there is only one team
    while len(teams) > 1:
        teams = simulate_round(teams)

    return teams[0]["team"]


if __name__ == "__main__":
    main()
