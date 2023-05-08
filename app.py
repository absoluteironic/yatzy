#! /usr/bin/env python3

from lib.player import player
from lib.game import yatzy

# Start game
players_count = input("Enter the number of players: ")
players_count_is_int = False

while not players_count_is_int:
    try:
        int(players_count)
    except ValueError:
        print("You can only provide a number. Try again.")
        players_count = input("Enter the number of players: ")
    else:
        players_count_is_int = True

players = []
for p in range(int(players_count)):
    p_name = input("Enter player {}'s name: ".format(p+1)) or "Player {}".format(p+1)
    players.append(player(p_name))

ya = yatzy(players)
ya.start_game()
