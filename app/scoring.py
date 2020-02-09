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
            return 1, 0
        elif winner == 2:
            return 0, 1
