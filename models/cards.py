import random
from typing import List, Dict, Optional, Callable


class Card:
    def __init__(
        self,
        name: str,
        color: str,
        card_type: str,
        points: int = 0,
        effect: Optional[str] = None,
    ):
        self.name = name
        self.color = color
        self.card_type = card_type
        self.points = points
        self.effect = effect

    def __repr__(self):
        return (
            f"<{self.card_type.title()} {self.name} ({self.color}) [{self.points}pts]>"
        )


class HabitantCard(Card):
    def __init__(
        self,
        name: str,
        color: str,
        combo_checker: Callable[[List[int], List[str]], bool],
        points: int = 1,
        effect: Optional[str] = None,
        variable_points: bool = False,
    ):
        super().__init__(name, color, "habitant", points, effect)
        self.combo_checker = combo_checker
        self.variable_points = variable_points

    def is_combo_met(self, dice_values: List[int], dice_colors: List[str]) -> bool:
        return self.combo_checker(dice_values, dice_colors)

    def calculate_points(self, kingdom_cards: List["Card"]) -> int:
        if not self.variable_points:
            return self.points

        if self.name == "Fée zélée":
            count = sum(
                1
                for card in kingdom_cards
                if isinstance(card, HabitantCard) and card.name == "Fée zélée"
            )
            return count * count

        return self.points


class LieuCard(Card):
    def __init__(self, name: str, color: str, value: int):
        super().__init__(name, color, "lieu", points=value)
        self.value = value


class PenaliteCard(Card):
    def __init__(self, name: str, penalty_points: int, transferable: bool = False):
        super().__init__(name, None, "penalite", points=-penalty_points)
        self.penalty_points = penalty_points
        self.transferable = transferable


class Deck:
    def __init__(self, cards: List[Card]):
        self.draw_pile = cards[:]
        self.discard = []

    def shuffle(self):
        random.shuffle(self.draw_pile)

    def draw(self) -> Optional[Card]:
        if not self.draw_pile:
            if self.discard:
                self.draw_pile = self.discard[:]
                self.discard = []
                self.shuffle()
            else:
                return None
        return self.draw_pile.pop(0)

    def discard_card(self, card: Card):
        self.discard.append(card)


def check_color_count(colors: List[str], target_color: str, count: int) -> bool:
    return colors.count(target_color) >= count


def check_value_count(values: List[int], target_value: int, count: int) -> bool:
    return values.count(target_value) >= count


def check_consecutive_sequence(values: List[int], length: int) -> bool:
    unique_values = sorted(set(values))
    for i in range(len(unique_values) - length + 1):
        if unique_values[i : i + length] == list(
            range(unique_values[i], unique_values[i] + length)
        ):
            return True
    return False


def check_all_even_or_odd(values: List[int]) -> bool:
    return all(v % 2 == 0 for v in values) or all(v % 2 == 1 for v in values)


def check_same_value_sets(values: List[int], set_size: int, num_sets: int) -> bool:
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return sum(1 for count in counts.values() if count >= set_size) >= num_sets


LOCATIONS = {
    "Ville": "blue",
    "Mine": "red",
    "Atelier": "green",
    "Village des orcs": "red",
    "Foret enchantee": "green",
}

all_lieux = []
for name, color in LOCATIONS.items():
    for value in [2, 3, 4]:
        all_lieux.append(LieuCard(name, color, value))

all_habitants = [
    HabitantCard(
        "Gnome toque",
        "blue",
        lambda v, c: check_color_count(c, "blue", 4),
        3,
        "Necessite 4 des bleus",
    ),
    HabitantCard(
        "Nain grincheux",
        "red",
        lambda v, c: check_value_count(v, 5, 3),
        3,
        "Necessite trois 5",
    ),
    HabitantCard(
        "Elfe arrogant",
        "green",
        lambda v, c: check_consecutive_sequence(v, 4),
        4,
        "Necessite une suite de 4 nombres. Tour suivant: 4 lancers.",
    ),
    HabitantCard(
        "Bourgeois vaniteux",
        "blue",
        lambda v, c: check_all_even_or_odd(v),
        4,
        "Tous les des doivent etre pairs ou impairs",
    ),
    HabitantCard(
        "Champikobold fabuleux",
        "red",
        lambda v, c: check_color_count(c, "red", 5),
        3,
        "Necessite 5 des rouges",
    ),
    HabitantCard(
        "Orc affectueux",
        "red",
        lambda v, c: check_same_value_sets(v, 3, 2),
        4,
        "Necessite deux groupes de trois nombres identiques",
    ),
    HabitantCard(
        "Apprenti sorcier",
        "green",
        lambda v, c: (
            check_color_count(c, "red", 2) and check_color_count(c, "green", 2)
        ),
        5,
        "Necessite 2 des rouges et 2 verts. Rejouer un tour.",
    ),
    HabitantCard(
        "Hypnotiseur",
        "blue",
        lambda v, c: sum(v) <= 12,
        1,
        "Somme des des <= 12. Prendre la carte suivante.",
    ),
    HabitantCard(
        "Fee zelee",
        "green",
        lambda v, c: (
            check_color_count(c, "blue", 2) and check_color_count(c, "green", 2)
        ),
        1,
        "Necessite 2 des bleus et 2 verts. Points selon nombre de Fees.",
        variable_points=True,
    ),
]

standard_habitants = [
    HabitantCard("Marchand", "blue", lambda v, c: check_value_count(v, 5, 2), 2),
    HabitantCard("Artisan", "blue", lambda v, c: check_value_count(v, 3, 3), 2),
    HabitantCard(
        "Pecheur",
        "blue",
        lambda v, c: check_value_count(v, 1, 2) and check_value_count(v, 3, 2),
        2,
    ),
    HabitantCard("Forgeron", "blue", lambda v, c: check_value_count(v, 4, 3), 3),
    HabitantCard(
        "Architecte", "blue", lambda v, c: check_consecutive_sequence(v, 3), 2
    ),
    HabitantCard("Marin", "blue", lambda v, c: check_value_count(v, 2, 4), 3),
    HabitantCard("Alchimiste", "blue", lambda v, c: check_same_value_sets(v, 2, 2), 2),
    HabitantCard("Sage", "blue", lambda v, c: check_all_even_or_odd(v), 3),
    HabitantCard("Guerrier", "red", lambda v, c: check_value_count(v, 6, 2), 2),
    HabitantCard(
        "Chasseur",
        "red",
        lambda v, c: check_value_count(v, 4, 2) and check_value_count(v, 2, 2),
        3,
    ),
    HabitantCard("Berserker", "red", lambda v, c: check_color_count(c, "red", 4), 3),
    HabitantCard("Eclaireur", "red", lambda v, c: check_consecutive_sequence(v, 3), 2),
    HabitantCard("Champion", "red", lambda v, c: check_same_value_sets(v, 3, 1), 2),
    HabitantCard("Garde", "red", lambda v, c: check_value_count(v, 5, 2), 2),
    HabitantCard("Mercenaire", "red", lambda v, c: check_all_even_or_odd(v), 3),
    HabitantCard("Barbare", "red", lambda v, c: check_value_count(v, 1, 3), 2),
    HabitantCard("Druide", "green", lambda v, c: check_color_count(c, "green", 3), 2),
    HabitantCard("Ranger", "green", lambda v, c: check_consecutive_sequence(v, 3), 2),
    HabitantCard("Herboriste", "green", lambda v, c: check_value_count(v, 2, 3), 2),
    HabitantCard("Chaman", "green", lambda v, c: check_same_value_sets(v, 2, 2), 3),
    HabitantCard("Gardien", "green", lambda v, c: check_all_even_or_odd(v), 2),
    HabitantCard("Cultivateur", "green", lambda v, c: check_value_count(v, 3, 2), 1),
    HabitantCard("Eleveur", "green", lambda v, c: check_value_count(v, 4, 2), 2),
    HabitantCard(
        "Diplomate",
        "blue",
        lambda v, c: check_color_count(c, "red", 2) and check_color_count(c, "blue", 2),
        3,
    ),
    HabitantCard(
        "Explorateur",
        "red",
        lambda v, c: check_color_count(c, "red", 2)
        and check_color_count(c, "green", 2),
        3,
    ),
    HabitantCard(
        "Ermite",
        "green",
        lambda v, c: check_color_count(c, "green", 2)
        and check_color_count(c, "blue", 2),
        3,
    ),
    HabitantCard(
        "Maitre Artisan", "blue", lambda v, c: sum(v) >= 25, 4, "Somme des dés >= 25"
    ),
    HabitantCard(
        "Stratege",
        "red",
        lambda v, c: len(set(v)) >= 5,
        3,
        "Au moins 5 valeurs différentes",
    ),
    HabitantCard(
        "Sage-Femme", "green", lambda v, c: sum(v) <= 15, 3, "Somme des dés <= 15"
    ),
    HabitantCard(
        "Marchand Royal",
        "blue",
        lambda v, c: all(x >= 4 for x in v),
        4,
        "Tous les dés >= 4",
    ),
    HabitantCard(
        "Assassin", "red", lambda v, c: all(x <= 3 for x in v), 4, "Tous les dés <= 3"
    ),
    HabitantCard(
        "Enchanteur",
        "green",
        lambda v, c: len(set(c)) == 3,
        4,
        "Un dé de chaque couleur",
    ),
    HabitantCard(
        "Grand Pretre",
        "blue",
        lambda v, c: check_same_value_sets(v, 4, 1),
        5,
        "Quatre dés de même valeur",
    ),
    HabitantCard(
        "Seigneur de Guerre",
        "red",
        lambda v, c: check_consecutive_sequence(v, 5),
        5,
        "Suite de 5 nombres",
    ),
    HabitantCard(
        "Archidruide",
        "green",
        lambda v, c: check_color_count(c, "green", 5),
        5,
        "5 dés verts",
    ),
]

all_habitants.extend(standard_habitants)

all_penalites = [
    PenaliteCard("Dragon", 4, transferable=True),
    PenaliteCard("Peste", 2),
    PenaliteCard("Secheresse", 1),
    PenaliteCard("Tempete", 2),
    PenaliteCard("Famine", 2),
    PenaliteCard("Invasion", 3),
    PenaliteCard("Trahison", 2),
    PenaliteCard("Malediction", 1),
    PenaliteCard("Brigands", 2),
    PenaliteCard("Incendie", 2),
]

habitant_deck = Deck(all_habitants)
lieu_deck = Deck(all_lieux)
penalite_deck = Deck(all_penalites)

habitant_deck.shuffle()
lieu_deck.shuffle()
penalite_deck.shuffle()
