import random


class Dice:
    def __init__(self, sides, color):
        self.sides = sides
        self.color = color

    def get_color(self):
        return self.color

    def get_sides(self):
        return self.sides

    def roll(self):
        return random.randint(1, self.sides)
