import random


class Card:

    def __init__(self, name, color, card_type, points=0):
        self.name = name
        self.color = color
        self.card_type = card_type
        self.points = points

    def __repr__(self):
        return (
            f"<{self.card_type.title()} {self.name} ({self.color}) [{self.points}pts]>"
        )


class HabitantCard(Card):

    def __init__(self, name, color, combo, points=1):
        super().__init__(name, color, "habitant", points)
        self.combo = combo

    def is_combo_met(self, dice_values):
        for face, needed in self.combo.items():
            if dice_values.count(face) < needed:
                return False
        return True


class LieuCard(Card):

    def __init__(self, name, color, value):
        super().__init__(name, color, "lieu", points=value)
        self.value = value


class PenaliteCard(Card):

    def __init__(self, name, penalty_points):
        super().__init__(name, None, "penalite", points=-penalty_points)
        self.penalty_points = penalty_points


class Deck:

    def __init__(self, cards):
        self.draw_pile = cards[:] 
        self.discard = []

    def shuffle(self):
        random.shuffle(self.draw_pile)

    def draw(self):
        if not self.draw_pile:
            if self.discard:
                self.draw_pile = self.discard[:]
                self.discard = []
                self.shuffle()
            else:
                return None
        return self.draw_pile.pop(0)

    def discard_card(self, card):
        self.discard.append(card)


LOCATIONS = {
    "Ville": "blue",
    "Mine": "red",
    "Atelier": "green",
    "Village des orcs": "red",
    "Forêt enchantée": "green",
}

all_lieux = []
for name, color in LOCATIONS.items():
    for value in [2, 3, 4]:
        all_lieux.append(LieuCard(name, color, value))

all_habitants = [
    HabitantCard("Marchand", "blue", {5: 2, 2: 1}),
    HabitantCard("Artisan", "blue", {3: 3}),
    HabitantCard("Pêcheur", "blue", {1: 2, 3: 2}),
    HabitantCard("Scribe", "blue", {1: 3, 2: 1}),
    HabitantCard("Noble", "blue", {6: 2, 4: 1}),
    HabitantCard("Architecte", "blue", {4: 2, 5: 1}),
    HabitantCard("Marin", "blue", {2: 2, 3: 1}),
    HabitantCard("Érudit", "blue", {5: 3}),
    HabitantCard("Mineur", "red", {4: 3}),
    HabitantCard("Forgeron", "red", {6: 2, 3: 1}),
    HabitantCard("Guerrier", "red", {5: 2, 1: 1}),
    HabitantCard("Chef Orc", "red", {6: 3}),
    HabitantCard("Chasseur", "red", {3: 2, 4: 1}),
    HabitantCard("Éclaireur", "red", {2: 2, 5: 1}),
    HabitantCard("Berserker", "red", {1: 4}),
    HabitantCard("Chamane", "red", {4: 2, 6: 1}),
    HabitantCard("Alchimiste", "green", {5: 2, 2: 1}),
    HabitantCard("Herboriste", "green", {3: 2, 1: 2}),
    HabitantCard("Druide", "green", {4: 3}),
    HabitantCard("Enchanteur", "green", {6: 2, 5: 1}),
    HabitantCard("Elfe", "green", {2: 3}),
    HabitantCard("Ranger", "green", {1: 2, 6: 1}),
    HabitantCard("Sage", "green", {3: 3}),
    HabitantCard("Apprenti", "green", {4: 2, 2: 1}),
]

all_penalites = [
    PenaliteCard("Dragon", 3),
    PenaliteCard("Peste", 2),
    PenaliteCard("Sécheresse", 1),
    PenaliteCard("Tempête", 2),
    PenaliteCard("Famine", 2),
    PenaliteCard("Invasion", 3),
    PenaliteCard("Trahison", 2),
    PenaliteCard("Malédiction", 1),
    PenaliteCard("Brigands", 2),
    PenaliteCard("Incendie", 2),
]

habitant_deck = Deck(all_habitants)
lieu_deck = Deck(all_lieux)
penalite_deck = Deck(all_penalites)

habitant_deck.shuffle()
lieu_deck.shuffle()
penalite_deck.shuffle()
