import random


class Dice:
    def __init__(self, color):
        self.sides = 6
        self.color = color
        self.value = None
        self.is_locked = False

    def get_color(self):
        return self.color

    def get_value(self):
        return self.value

    def is_locked(self):
        return self.is_locked

    def lock(self):
        self.is_locked = True

    def unlock(self):
        self.is_locked = False

    def roll(self):
        if not self.is_locked:
            self.value = random.randint(1, self.sides)
        return self.value


class DiceSet:

    def __init__(self):
        self.dice = []
        for color in ["red", "green", "blue"]:
            for _ in range(2):
                self.dice.append(Dice(color))

    def roll_all(self):
        return [die.roll() for die in self.dice]

    def get_values(self):
        return [die.value if die.value is not None else 0 for die in self.dice]

    def lock_die(self, index):
        if 0 <= index < len(self.dice):
            self.dice[index].lock()

    def unlock_all(self):
        for die in self.dice:
            die.unlock()

    def get_locked_indices(self):
        return [i for i, die in enumerate(self.dice) if die.is_locked]

    def get_dice(self):
        return self.dice
