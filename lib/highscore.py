import json
import os

from datetime import datetime
from operator import itemgetter

import tabulate


def score_file_path():
    """Return the file path to highscores"""
    score_file_path = "leaderboard.json"
    if not os.path.isfile(score_file_path):
        with open(score_file_path, "w") as f:
            pass
    return score_file_path


def get_score():
    """Return a list with highscores"""
    with open(score_file_path(), "r") as f:
        raw_data = f.read()

    if len(raw_data) > 0:
        return json.loads(raw_data)
    else:
        return []


def list_score():
    """Print a list with highscores"""
    highscore_data = get_score()
    table_data = [
        ['Rank', 'Score', 'Name', 'Date']
    ]
    for index, player in enumerate(highscore_data):
        table_data.append([
            str(index+1),
            player['score'],
            player['player'],
            player['date']
        ])

    print("=== LEADERBOARD ===")
    print(tabulate.tabulate(table_data))


def add_score(player, score):
    """Add a highscore"""
    data = get_score()
    date = datetime.today().strftime('%Y-%m-%d %H:%M')
    data.append({"player": player, "score": score, "date": date})
    sorted_data = sorted(data, key=itemgetter('score'), reverse=True)
    json_data = json.dumps(sorted_data)

    with open(score_file_path(), "w") as f:
        f.writelines(json_data)


def highest_score():
    """Return the highest highscore"""
    data = get_score()
    if len(data) < 1:
        return []
    return data[0]


def lowest_score():
    """Return the lowest highscore"""
    data = get_score()
    if len(data) < 1:
        return []
    return data[-1]


def maxed_score_card():
    return [
        {"id": 1, "name": "Ones", "score": 5},
        {"id": 2, "name": "Twos", "score": 10},
        {"id": 3, "name": "Threes", "score": 15},
        {"id": 4, "name": "Fours", "score": 20},
        {"id": 5, "name": "Fives", "score": 25},
        {"id": 6, "name": "Sixes", "score": 30},
        {"id": 7, "name": "One pair", "score": 12},
        {"id": 8, "name": "Two pairs", "score": 22},
        {"id": 9, "name": "Three of a kind", "score": 18},
        {"id": 10, "name": "Four of a kind", "score": 24},
        {"id": 11, "name": "Small straight", "score": 15},
        {"id": 12, "name": "Large straight", "score": 20},
        {"id": 13, "name": "Full house", "score": 28},
        {"id": 14, "name": "Chance", "score": 30},
        {"id": 15, "name": "Yatzy", "score": 50},
        {"id": 16, "name": "Bonus", "score": 50},
        {"id": 17, "name": "Total", "score": 374},
    ]
