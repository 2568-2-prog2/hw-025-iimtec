import random

class Dice:
    def __init__(self, sides=6, probabilities=None):
        self.sides = sides
        self.faces = list(range(1, sides + 1))
        if probabilities is None:
            self.probabilities = [1 / sides] * sides
        else:
            if len(probabilities) != sides:
                raise ValueError("probabilities length must equal sides")
            if abs(sum(probabilities) - 1.0) > 1e-6:
                raise ValueError("probabilities must sum to 1.0")
            self.probabilities = probabilities

    def roll(self):
        return random.choices(self.faces, weights=self.probabilities, k=1)[0]

    def roll_many(self, n):
        return random.choices(self.faces, weights=self.probabilities, k=n)
