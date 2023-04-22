
class player():
    """docstring for Player"""

    def __init__(self, name):
        self.name = name
        self.score_card = [
            {"id": 1, "name": "Ones", "score": None},
            {"id": 2, "name": "Twos", "score": None},
            {"id": 3, "name": "Threes", "score": None},
            {"id": 4, "name": "Fours", "score": None},
            {"id": 5, "name": "Fives", "score": None},
            {"id": 6, "name": "Sixes", "score": None},
            {"id": 7, "name": "One pair", "score": None},
            {"id": 8, "name": "Two pairs", "score": None},
            {"id": 9, "name": "Three of a kind", "score": None},
            {"id": 10, "name": "Four of a kind", "score": None},
            {"id": 11, "name": "Small straight", "score": None},
            {"id": 12, "name": "Large straight", "score": None},
            {"id": 13, "name": "Full house", "score": None},
            {"id": 14, "name": "Chance", "score": None},
            {"id": 15, "name": "Yatzy", "score": None},
            {"id": 16, "name": "Bonus", "score": None},
            {"id": 17, "name": "Total", "score": None},
        ]

    def add_score(self, box_id, score):
        self.score_card[box_id]["score"] = score
        pass

    def total_score(self):

        if self.score_card[16]['score'] is not None:
            return self.score_card[16]['score']

        _total_score = 0
        _total_score_upper = 0

        for box in self.score_card:

            if box['score'] is None:
                continue

            if box['id'] in range(0, 6):
                _total_score_upper += box['score']

            _total_score += box['score']

        # Bonus
        if _total_score_upper >= 63:
            _total_score += 50
            self.score_card[15]['score'] = 50

        # Total score
        self.score_card[16]['score'] = _total_score

        return _total_score

    def box_score(self, box_id, dice):
        # 0 Ones
        # 1 Twos
        # 2 Threes
        # 3 Fours
        # 4 Fives
        # 5 Sixes
        if box_id in range(0, 6):
            matches = [d for d in dice if d == box_id+1]
            score = sum(matches)
            return score

        # 6 One pair
        # Two dice showing the same number. Score: Sum of those two dice.
        elif box_id == 6:
            matches = [d for d in dice if dice.count(d) > 1]
            if not matches:
                return 0
            highest_value = max(matches)
            score = highest_value * 2
            return score

        # 7 Two pairs
        # Two different pairs of dice. Score: Sum of dice in those two pairs.
        elif box_id == 7:
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
        elif box_id == 8:
            matches = [d for d in dice if dice.count(d) > 2]
            if not matches:
                return 0
            highest_value = max(matches)
            score = highest_value * 3
            return score

        # 9 Four of a kind
        # Four dice with the same number. Score: Sum of those four dice.
        elif box_id == 9:
            matches = [d for d in dice if dice.count(d) > 3]
            if not matches:
                return 0
            highest_value = max(matches)
            score = highest_value * 4
            return score

        # 10 Small straight
        # The combination 1-2-3-4-5. Score: 15 points (sum of all the dice).
        elif box_id == 10:
            dice.sort()
            dice = "".join(map(str, dice))
            if "12345" == dice:
                return 15
            return 0

        # 11 Large straight
        # The combination 2-3-4-5-6. Score: 20 points (sum of all the dice).
        elif box_id == 11:
            dice.sort()
            dice = "".join(map(str, dice))
            if "23456" == dice:
                return 20
            return 0

        # 12 Full house
        # Any set of three combined with a different pair. Score: Sum of all the dice.
        elif box_id == 12:
            matches = [d for d in dice if dice.count(d) > 1 < 4]
            if not matches or len(matches) < 5:
                return 0
            score = sum(matches)
            return score

        # 13 Chance
        # Any combination of dice. Score: Sum of all the dice.
        elif box_id == 13:
            return sum(dice)

        # 14 Yatzy
        # All five dice with the same number. Score: 50 points.
        elif box_id == 14:
            matches = [d for d in dice if dice.count(d) == 5]
            if not matches:
                return 0
            return 50
