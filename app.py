#! /usr/bin/env python3

from lib.player import player
from lib.game import yatzy

# Start game
players_count = int(input("Enter the number of players: "))
players = []

for p in range(players_count):
    p_name = input("Enter player {}'s name: ".format(p+1)) or "Player {}".format(p+1)
    players.append(player(p_name))

ya = yatzy(players)
ya.start_game()
