#! /usr/bin/env python3

from random import randrange

_players_scoreboard = {}
_players = 0
_current_player = 0
_current_game_round = 0
_max_game_round = 15
_scoreboard = {}
_game_output = ""
_current_dice_roll = 0
_max_dice_roll = 3
_saved_dice = []


def start_game():
    global _current_game_round, _max_game_round, _players, _current_player
    global _current_dice_roll, _max_dice_roll, _saved_dice

    while _current_game_round < _max_game_round:
        _current_game_round += 1
        for p in range(int(_players)):
            _current_player = p
            player = "player_"+str(p+1)
            result = roll_dice_round()
            set_highscore(player, result)

    end_game()


def roll_dice_round():
    global _current_player, _current_dice_roll, _max_dice_roll, _saved_dice
    global _current_game_round, _max_game_round

    _saved_dice = []
    _current_dice_roll = 0
    dice_count = 5
    while _current_dice_roll < _max_dice_roll:
        _current_dice_roll += 1
        if len(_saved_dice) < 5:
            print_output("")
            print_output(f"""=== Round {_current_game_round}/{_max_game_round} | Player {_current_player+1} | Roll {_current_dice_roll}/3""")
            if _current_dice_roll < 2:
                show_player_scoreboard_avaliable_score_box("player_"+str(_current_player+1))
            rolled_dice = roll_dice(dice_count - len(_saved_dice))
            if len(_saved_dice) > 0:
                print_output(Rolled dice: )
                print_dice("".join(map(str, rolled_dice))+"-"+"".join(map(str, _saved_dice)))
            else:
                print_output("Rolled dice:")
                print_dice("".join(map(str, rolled_dice)))
            _saved_dice = select_dice(rolled_dice)
    input("This was your last roll. Press enter to save your score. ") or "0"
    print_output("")
    return _saved_dice


def roll_dice(num):
    dice = []
    for n in range(num):
        dice.append(randrange(1, 7))

    dice.sort()
    return dice


def select_dice(dice):
    global _saved_dice, _current_dice_roll

    selection_valid = False
    if _current_dice_roll >= 3:
        selected_dice = dice + _saved_dice
        selected_dice = list(selected_dice)
        selected_dice.sort()
        return selected_dice
    else:
        selected_dice = input("Enter the dice you want to keep (eg: 123): ") or "0"

    if selected_dice == "0":
        return []

    dice = dice + _saved_dice

    while not selection_valid:
        selected_dice = list(map(int, selected_dice))
        dice_copy = dice.copy()
        for d in selected_dice:
            if d in dice_copy:
                dice_copy.remove(d)
                selection_valid = True
            else:
                selection_valid = False
                print_output(f"""Error: You are trying to select a dice that's not avaliable; {d}.""")
                selected_dice = input("Try again; Enter the dice you want to save: ") or "0"

                break

    return list(selected_dice)


def print_dice(dice):

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


def set_highscore(player, dice):

    # Show avaliable highscore categories
    scoreboard = get_player_scoreboard(player)
    for index, spot in enumerate(scoreboard):
        if spot['score'] is not None:
            continue
        tmp_score = calcualte_category_score(index, dice)
        print_output(index+1, spot['name'], str(tmp_score)+"p")

    print_output("")

    # Prompt user for input
    dice_str = "-".join(map(str, dice))
    score_position = int(input("Select where to save your score ("+dice_str+"): "))
    score_position -= 1
    score = calcualte_category_score(score_position, dice)

    # Score position not avaliable
    if _players_scoreboard[player][score_position]['score']:
        score_position = input("That position is already used. Select a new position ("+dice_str+"): ")

    # Save player score
    set_player_score(player, score_position, score)


def set_player_score(player, category_id, score):
    if player not in _players_scoreboard:
        create_player_scoreboard(player)
    _players_scoreboard[player][category_id]['score'] = score


def get_player_scoreboard(player):
    if player not in _players_scoreboard:
        create_player_scoreboard(player)

    return _players_scoreboard[player]


def show_player_scoreboard_avaliable_score_box(player):
    scoreboard = get_player_scoreboard(player)
    print_output("Available score boxes: ")
    for index, spot in enumerate(scoreboard):
        if spot['score'] is None:
            print_output(str(index+1)+" "+spot['name'])

    print_output("")


def show_player_scoreboard(player):
    scoreboard = get_player_scoreboard(player)
    for index, spot in enumerate(scoreboard):
        if spot['score'] is None:
            score = "-"
        else:
            score = str(spot['score'])+"p"
        print_output(index+1, spot['name'], score)


def create_player_scoreboard(player):
    player_scoreboard = [
        {"name": "Ones", "score": None},
        {"name": "Twos", "score": None},
        {"name": "Threes", "score": None},
        {"name": "Fours", "score": None},
        {"name": "Fives", "score": None},
        {"name": "Sixes", "score": None},
        {"name": "One pair", "score": None},
        {"name": "Two pairs", "score": None},
        {"name": "Three of a kind", "score": None},
        {"name": "Four of a kind", "score": None},
        {"name": "Small straight", "score": None},
        {"name": "Large straight", "score": None},
        {"name": "Full house", "score": None},
        {"name": "Chance", "score": None},
        {"name": "Yatzy", "score": None},
    ]

    _players_scoreboard[player] = player_scoreboard.copy()


def calcualte_category_score(category_id, dice):
    # 0 Ones
    # 1 Twos
    # 2 Threes
    # 3 Fours
    # 4 Fives
    # 5 Sixes
    if category_id in range(0, 6):
        matches = [d for d in dice if d == category_id+1]
        score = sum(matches)
        return score

    # 6 One pair
    # Two dice showing the same number. Score: Sum of those two dice.
    elif category_id == 6:
        matches = [d for d in dice if dice.count(d) > 1]
        if not matches:
            return 0
        highest_value = max(matches)
        score = highest_value * 2
        return score

    # 7 Two pairs
    # Two different pairs of dice. Score: Sum of dice in those two pairs.
    elif category_id == 7:
        matches = [d for d in dice if dice.count(d) > 1]
        if not matches:
            return 0

        # Remove dupliactes
        matches = list(set(matches))
        if len(matches) < 2:
            return 0

        score = sum(matches) * 2
        return score

    # 8 Three of a kind
    # Three dice showing the same number. Score: Sum of those three dice.
    elif category_id == 8:
        matches = [d for d in dice if dice.count(d) > 2]
        if not matches:
            return 0
        highest_value = max(matches)
        score = highest_value * 3
        return score

    # 9 Four of a kind
    # Four dice with the same number. Score: Sum of those four dice.
    elif category_id == 9:
        matches = [d for d in dice if dice.count(d) > 3]
        if not matches:
            return 0
        highest_value = max(matches)
        score = highest_value * 4
        return score

    # 10 Small straight
    # The combination 1-2-3-4-5. Score: 15 points (sum of all the dice).
    elif category_id == 10:
        dice.sort()
        dice = "".join(map(str, dice))
        if "12345" == dice:
            return 15
        return 0

    # 11 Large straight
    # The combination 2-3-4-5-6. Score: 20 points (sum of all the dice).
    elif category_id == 11:
        dice.sort()
        dice = "".join(map(str, dice))
        if "23456" == dice:
            return 20
        return 0

    # 12 Full house
    # Any set of three combined with a different pair. Score: Sum of all the dice.
    elif category_id == 12:
        matches = [d for d in dice if dice.count(d) > 1 < 4]
        if not matches or len(matches) < 5:
            return 0
        score = sum(matches)
        return score

    # 13 Chance
    # Any combination of dice. Score: Sum of all the dice.
    elif category_id == 13:
        return sum(dice)

    # 14 Yatzy
    # All five dice with the same number. Score: 50 points.
    elif category_id == 14:
        matches = [d for d in dice if dice.count(d) == 5]
        if not matches:
            return 0
        return 50


def end_game():
    print_output("")
    print_output("=== End game")
    show_highscore()


def calculate_total_highscore():
    highscore = {}
    for player in _players_scoreboard:
        score = 0
        for sb in _players_scoreboard[player]:
            if not sb['score']:
                continue
            score += int(sb['score'])
        highscore[player] = score
    return highscore


def show_highscore():
    scores = calculate_total_highscore()
    for i, s in enumerate(scores):
        player = "Player "+str(i+1)
        print_output(player+":", str(scores[s])+"p")


def print_output(*args):
    print(" ".join(map(str, args)))


# Start game
_players = int(input("Enter players count: "))
start_game()
