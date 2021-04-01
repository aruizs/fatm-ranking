from abc import ABC, abstractmethod


class Scoring(ABC):
    @abstractmethod
    def calculate(self, score1, score2, winner):
        if winner != 1 and winner != 2:
            print("Winner must be 1 or 2")


class BasicScoring(Scoring):
    def calculate(self, score1, score2, winner):
        super().calculate(score1, score2, winner)
        if winner == 1:
            return score1 + 1, score2
        elif winner == 2:
            return score1, score2 + 1


class EloScoring(Scoring):
    def calculate(self, score1, score2, winner):
        super().calculate(score1, score2, winner)
        transformed_rating1 = pow(10, score1 / 400)
        transformed_rating2 = pow(10, score2 / 400)
        expected_score1 = transformed_rating1 / (transformed_rating1 + transformed_rating2)
        expected_score2 = transformed_rating2 / (transformed_rating1 + transformed_rating2)
        k = 32
        if winner == 1:
            a = 1 - expected_score1
            b = 0 - expected_score2
            score1 = score1 + k * a
            score2 = score2 + k * b
        elif winner == 2:
            a = 0 - expected_score1
            b = 1 - expected_score2
            score1 = score1 + k * a
            score2 = score2 + k * b

        return round(score1, 2), round(score2, 2)


class FatmScoring(Scoring):
    def calculate(self, score1, score2, winner):
        super().calculate(score1, score2, winner)
        if winner == 1:
            score_diff = score1 - score2
        elif winner == 2:
            score_diff = score2 - score1
        if score_diff >= 750:
            score = 1
        elif score_diff >= 500:
            score = 2
        elif score_diff >= 400:
            score = 3
        elif score_diff >= 300:
            score = 4
        elif score_diff >= 200:
            score = 5
        elif score_diff >= 150:
            score = 6
        elif score_diff >= 100:
            score = 7
        elif score_diff >= 50:
            score = 8
        elif score_diff >= 25:
            score = 9
        elif score_diff >= -24:
            score = 10
        elif score_diff >= -49:
            score = 12
        elif score_diff >= -99:
            score = 14
        elif score_diff >= -149:
            score = 16
        elif score_diff >= -199:
            score = 18
        elif score_diff >= -299:
            score = 20
        elif score_diff >= -399:
            score = 22
        elif score_diff >= -499:
            score = 24
        elif score_diff >= -749:
            score = 26
        else:
            score = 28

        if winner == 1:
            score1 = score1 + score
            score2 = score2 - score
        elif winner == 2:
            score1 = score1 - score
            score2 = score2 + score

        return score1, score2
