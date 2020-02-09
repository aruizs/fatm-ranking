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

