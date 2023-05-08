#! /usr/bin/env python3

import lib.highscore as hs
import tabulate
import re

from colorama import Fore, Style
from random import randrange


class yatzy(object):

    _players = 0
    _current_player_index = 0
    _current_game_round = 0
    _total_game_rounds = 15
    _scoreboard = {}
    _game_output = ""
    _current_dice_roll = 0
    _max_dice_roll = 3
    _saved_dice = []

    def __init__(self, players):
        super(yatzy, self).__init__()
        self.players = players

    def start_game(self):
        while self._current_game_round < self._total_game_rounds:
            self._current_game_round += 1
            for i, p in enumerate(range(len(self.players))):
                self._current_player_index = i
                self.start_dice_round()
                self.set_score()

        self.end_game()

    def start_dice_round(self):

        self._saved_dice = []
        self._current_dice_roll = 0
        dice_count = 5
        while self._current_dice_roll < self._max_dice_roll:
            self._current_dice_roll += 1

            if len(self._saved_dice) < 5:
                self.print_output("")
                output_str = "=== Round {}/{} | Player: {} | Roll {}/3"
                self.print_output(output_str.format(
                    self._current_game_round,
                    self._total_game_rounds,
                    self.players[self._current_player_index].name,
                    self._current_dice_roll)
                )

                if self._current_dice_roll < 2:
                    self.print_output("Current score card: ")
                    score_card = self.players[self._current_player_index].score_card

                    table_data = [
                        ['id', 'Box', 'Score'],
                    ]
                    for index, spot in enumerate(score_card):
                        if spot['id'] == 16 or spot['id'] == 17:
                            continue

                        if spot['score'] is None:
                            table_data.append([str(index+1), spot['name'], '-'])
                        else:
                            table_data.append([str(index+1), spot['name'], spot['score']])

                    results = tabulate.tabulate(table_data)
                    print(results)
                    self.print_output("")

                if self._current_dice_roll == 1:
                    input("Press enter to roll your dice ") or "0"

                rolled_dice = self.roll_dice(dice_count - len(self._saved_dice))

                if len(self._saved_dice) > 0:
                    self.print_output("Rolled dice: ")
                    self.print_dice("".join(map(str, rolled_dice))+"-"+"".join(map(str, self._saved_dice)))

                else:
                    self.print_output("Rolled dice:")
                    self.print_dice("".join(map(str, rolled_dice)))
                self._saved_dice = self.select_dice(rolled_dice)

        input("This was your last roll. Press enter to select where to save your score. ") or "0"
        self.print_output("")

        return self._saved_dice

    def roll_dice(self, num):
        dice = []
        for n in range(num):
            dice.append(randrange(1, 7))
        dice.sort()
        return dice

    def select_dice(self, dice):
        global _saved_dice, _current_dice_roll

        selection_valid = False
        if self._current_dice_roll >= 3:
            selected_dice = dice + self._saved_dice
            selected_dice = list(selected_dice)
            selected_dice.sort()
            return selected_dice
        else:
            selected_dice = input("Enter the dice you want to keep (eg: 123): ") or "0"

        if selected_dice == "0":
            return []

        dice = dice + self._saved_dice

        while not selection_valid:
            selected_dice = list(map(int, selected_dice))
            dice_copy = dice.copy()
            for d in selected_dice:
                if d in dice_copy:
                    dice_copy.remove(d)
                    selection_valid = True
                else:
                    selection_valid = False
                    self.print_output(f"""Error: You are trying to select a dice that's not avaliable; {d}.""")
                    selected_dice = input("Try again; Enter the dice you want to save: ") or "0"

                    break

        return list(selected_dice)

    def print_dice(self, dice):

        number = {
          "1": {0: " ..... ", 1: " ..1.. ", 2: " ..... "},
          "2": {0: " 2.... ", 1: " ..... ", 2: " ....2 "},
          "3": {0: " 3.... ", 1: " ..3.. ", 2: " ....3 "},
          "4": {0: " 4...4 ", 1: " ..... ", 2: " 4...4 "},
          "5": {0: " 5...5 ", 1: " ..5.. ", 2: " 5...5 "},
          "6": {0: " 6...6 ", 1: " 6...6 ", 2: " 6...6 "},
          "-": {0: "       ", 1: " ..... ", 2: "       "},
        }

        output = ""

        for i in range(3):
            output += "\n"
            for di, d in enumerate(dice):
                if di == 0:
                    output += "|"
                output += number[str(d)][i]+"|"
        output += "\n"

        print(output)

    def set_score(self):

        player = self.players[self._current_player_index]
        dice = self._saved_dice
        maxed_score_card = hs.maxed_score_card()

        # Show avaliable highscore categories
        self.print_output("Available boxes on your score card with temporary scores based on your dice\n")
        table_data = [
            ['id', 'Box', 'Tmp score', 'Max score']
        ]

        for index, spot in enumerate(player.score_card):
            if spot['id'] == 16 or spot['id'] == 17:
                continue

            if spot['score'] is not None:
                continue

            tmp_score = player.box_score(index, dice)
            maxed_score = maxed_score_card[index]['score']
            if tmp_score == maxed_score:
                table_data.append([spot['id'], spot['name'], Fore.GREEN + str(tmp_score) + Style.RESET_ALL, maxed_score])
            elif tmp_score == 0:
                table_data.append([spot['id'], spot['name'], "-", maxed_score])
            else:
                table_data.append([spot['id'], spot['name'], tmp_score, maxed_score])

        print(tabulate.tabulate(table_data))
        self.print_output("")

        # Prompt user for input
        dice_str = "-".join(map(str, dice))
        score_position = input("Select where to save your score ("+dice_str+"): ") or "0"

        score_position = int(score_position)
        score_position -= 1
        score = player.box_score(score_position, dice)

        # Score position not avaliable
        while player.score_card[score_position]['score']:
            score_position = input("That position is already used. Select a new position ("+dice_str+"): ")

        # Save player score
        self.players[self._current_player_index].add_score(score_position, score)

    def show_highscore(self):

        highest_score = 0
        winners = []
        is_tie = False

        table_data = [
            [''],  # 0
            ["Ones"],  # 1
            ["Twos"],  # 2
            ["Threes"],  # 3
            ["Fours"],  # 4
            ["Fives"],  # 5
            ["Sixes"],  # 6
            ["One pair"],  # 7
            ["Two pairs"],  # 8
            ["Three of a kind"],  # 9
            ["Four of a kind"],  # 10
            ["Small straight"],  # 11
            ["Large straight"],  # 12
            ["Full house"],  # 13
            ["Chance"],  # 14
            ["Yatzy"],  # 15
            ["--Bonus--"],  # 16
            ["--Total--"],  # 17
        ]

        for player_index, player in enumerate(self.players):

            player_score = player.total_score()
            table_data[0].append(player.name)

            # Add score to leaderboard
            hs.add_score(player.name, player_score)

            for row in player.score_card:
                if row['score'] is None:
                    table_data[int(row['id'])].append('0')
                else:
                    table_data[int(row['id'])].append(str(row['score']))

            if player_score > highest_score:
                highest_score = player_score
                winners = [player.name]
            elif player_score == highest_score:
                is_tie = True
                winners.append(player.name)

        print(tabulate.tabulate(table_data))
        print("\n")

        if is_tie:
            output = "It's a tie between {} with {} points."
            print(output.format(" and ".join(winners), highest_score))
        else:
            output = "The winner is {} with {} points."
            print(output.format(winners[0], highest_score))

        print("\n")

        show_leaderboard = input("Press y to see the leaderboard and n to end the game. ") or "y"
        print("\n")

        if show_leaderboard == "y":
            hs.list_score()

    def end_game(self):
        self.print_output("")
        self.print_output("=== End game ===")
        self.show_highscore()

    def print_output(self, *args):
        print(" ".join(map(str, args)))
