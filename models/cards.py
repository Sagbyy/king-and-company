import random


class Card:
    """Classe de base pour toutes les cartes."""

    def __init__(self, name, color, card_type):
        """
        name      : str, nom de la carte
        color     : str ou None, couleur associée
        card_type : str, "habitant", "lieu" ou "penalite"
        """
        self.name = name
        self.color = color
        self.card_type = card_type

    def __repr__(self):
        return f"<{self.card_type.title()} {self.name} ({self.color})>"

    def to_dict(self):
        """Convertit la carte en dictionnaire pour la sauvegarde"""
        return {"name": self.name, "color": self.color, "card_type": self.card_type}


class HabitantCard(Card):
    """Carte d'habitant, avec condition de combo de dés."""

    def __init__(self, name, color, combo):
        """
        combo : dict {face: min_count, …}
        ex. {6:3} pour « trois 6 », {2:2,5:1} pour « deux 2 + un 5 ».
        """
        super().__init__(name, color, "habitant")
        self.combo = combo

    def is_combo_met(self, dice_values):
        """
        Retourne True si dice_values (liste d'int) satisfait self.combo.
        """
        for face, needed in self.combo.items():
            if dice_values.count(face) < needed:
                return False
        return True

    def to_dict(self):
        data = super().to_dict()
        data["combo"] = self.combo
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["color"], data["combo"])


class LieuCard(Card):
    """Carte de lieu, éventuellement liée à un habitant préalable."""

    def __init__(self, name, color, prereq_habitant=None):
        """
        prereq_habitant : str ou None, nom d'habitant requis pour bonus.
        """
        super().__init__(name, color, "lieu")
        self.prereq_habitant = prereq_habitant

    def to_dict(self):
        data = super().to_dict()
        data["prereq_habitant"] = self.prereq_habitant
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["color"], data.get("prereq_habitant"))


class PenaliteCard(Card):
    """Carte de pénalité (malus)."""

    def __init__(self, name, penalty_points):
        """
        penalty_points : int, nombre de points négatifs.
        """
        super().__init__(name, None, "penalite")
        self.penalty_points = penalty_points

    def to_dict(self):
        data = super().to_dict()
        data["penalty_points"] = self.penalty_points
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["penalty_points"])


class Deck:
    """Gère une pioche + défausse de cartes."""

    def __init__(self, cards):
        """
        cards : liste d'instances de Card.
        """
        self.draw_pile = cards[:]  # copie
        self.discard = []

    def shuffle(self):
        """Mélange la pioche."""
        random.shuffle(self.draw_pile)

    def draw(self):
        """
        Pioche la carte du dessus (index 0).
        Retourne None si la pioche est vide.
        """
        if not self.draw_pile:
            return None
        return self.draw_pile.pop(0)

    def discard_card(self, card):
        """Ajoute une carte à la défausse."""
        self.discard.append(card)

    def to_dict(self):
        """Convertit le deck en dictionnaire pour la sauvegarde"""
        return {
            "draw_pile": [card.to_dict() if card else None for card in self.draw_pile],
            "discard": [card.to_dict() if card else None for card in self.discard],
        }

    @classmethod
    def from_dict(cls, data):
        """Crée un deck à partir d'un dictionnaire sauvegardé"""
        from models.cards import HabitantCard, LieuCard, PenaliteCard

        def create_card(card_dict):
            if card_dict is None:
                return None
            card_type = card_dict["card_type"]
            if card_type == "habitant":
                return HabitantCard.from_dict(card_dict)
            elif card_type == "lieu":
                return LieuCard.from_dict(card_dict)
            elif card_type == "penalite":
                return PenaliteCard.from_dict(card_dict)
            return None

        deck = cls([])
        deck.draw_pile = [create_card(card_dict) for card_dict in data["draw_pile"]]
        deck.discard = [create_card(card_dict) for card_dict in data["discard"]]
        return deck


# ————— Prototypes étendus de cartes —————

all_habitants = [
    HabitantCard("Chevalier", "rouge", {6: 3}),
    HabitantCard("Marchand", "bleu", {5: 2, 2: 1}),
    HabitantCard("Forgeron", "vert", {4: 3}),
    HabitantCard("Pêcheur", "bleu", {1: 2, 3: 2}),
    HabitantCard("Alchimiste", "vert", {2: 3}),
    HabitantCard("Moine", "rouge", {1: 4}),
    HabitantCard("Paysan", "jaune", {3: 2, 4: 1}),
    HabitantCard("Barde", "jaune", {2: 1, 6: 1}),
    HabitantCard("Apothicaire", "vert", {5: 3}),
    HabitantCard("Charpentier", "rouge", {2: 2, 4: 1}),
    HabitantCard("Messager", "jaune", {6: 1, 3: 1}),
    HabitantCard("Artisan", "bleu", {3: 3}),
    HabitantCard("Jardinier", "vert", {4: 2, 1: 1}),
    HabitantCard("Cuisinier", "jaune", {2: 3}),
    HabitantCard("Écuyer", "rouge", {6: 2, 5: 1}),
    HabitantCard("Scribe", "bleu", {1: 3, 2: 1}),
    HabitantCard("Guerrier", "vert", {3: 3}),
    HabitantCard("Sorcière", "rouge", {5: 1, 1: 1, 6: 1}),
]

all_lieux = [
    LieuCard("Château", "rouge", prereq_habitant="Chevalier"),
    LieuCard("Port", "bleu", prereq_habitant="Marchand"),
    LieuCard("Forge", "vert", prereq_habitant="Forgeron"),
    LieuCard("Abbaye", "rouge", prereq_habitant="Moine"),
    LieuCard("Place du Marché", "jaune", prereq_habitant="Marchand"),
    LieuCard("Taverne", "jaune", prereq_habitant="Barde"),
    LieuCard("Laboratoire", "vert", prereq_habitant="Alchimiste"),
    LieuCard("Jardin Royal", "vert", prereq_habitant="Jardinier"),
    LieuCard("Académie", "bleu", prereq_habitant="Scribe"),
    LieuCard("Tour d’Étude", "jaune", prereq_habitant="Guerrier"),
]

all_penalites = [
    PenaliteCard("Inondation", 1),
    PenaliteCard("Peste", 2),
    PenaliteCard("Sécheresse", 1),
    PenaliteCard("Tempête", 2),
    PenaliteCard("Famine", 3),
    PenaliteCard("Épidémie", 2),
    PenaliteCard("Éruption", 3),
    PenaliteCard("Raid Barbare", 2),
]

# ————— Création et mélange des decks pour chaque partie —————

habitant_deck = Deck(all_habitants)
lieu_deck = Deck(all_lieux)
penalite_deck = Deck(all_penalites)

habitant_deck.shuffle()
lieu_deck.shuffle()
penalite_deck.shuffle()
