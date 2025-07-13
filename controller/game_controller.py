# controller/game_controller.py

from models.cards import (
    Deck,
    all_habitants,
    all_lieux,
    all_penalites,
    HabitantCard,
)

class GameController:
    """
    Gère :
      - l’ordre des joueurs (1…N)
      - les decks et leurs πoche + défausse
      - cartes habitants et cartes lieux visibles
      - recrutement / pénalité
      - fin de partie + calcul de scores/gagnants
    """
    def __init__(self, num_players):
        self.num_players = num_players
        self.current_player = 1
        self.kingdoms = {i: [] for i in range(1, num_players + 1)}

        # Crée des decks INDEPENDANTS pour chaque partie
        self.hab_deck   = Deck(list(all_habitants))
        self.lieu_deck  = Deck(list(all_lieux))
        self.pen_deck   = Deck(list(all_penalites))
        self.hab_deck.shuffle()
        self.lieu_deck.shuffle()
        self.pen_deck.shuffle()

        # Cartes habitants visibles (4) et lieux visibles (4)
        self.visible_habitants = [self.hab_deck.draw() for _ in range(4)]
        self.visible_lieux     = [self.lieu_deck.draw() for _ in range(4)]

    def next_player(self):
        """Passe au joueur suivant (1→2→…→N→1)."""
        self.current_player = (self.current_player % self.num_players) + 1

    def apply_roll(self, dice_values):
        """Retourne la première HabitantCard satisfaite, ou None."""
        for card in self.visible_habitants:
            if isinstance(card, HabitantCard) and card.is_combo_met(dice_values):
                return card
        return None

    def recruit_or_penalize(self, dice_values):
        """
        Si combo trouvé : recrutement, sinon pénalité.
        Met à jour kingdoms, visible_habitants et visible_lieux.
        """
        player = self.current_player
        card = self.apply_roll(dice_values)

        if card:
            # Recruter l’habitant
            self.kingdoms[player].append(card)
            idx = self.visible_habitants.index(card)
            self.visible_habitants[idx] = self.hab_deck.draw()
            # Si couleur match un lieu visible, on pourrait gérer bonus ici
            return card, False
        else:
            # Pénalité
            pen = self.pen_deck.draw()
            if pen:
                self.kingdoms[player].append(pen)
            # Remplace la dernière habitant
            discarded = self.visible_habitants.pop(-1)
            if discarded:
                self.hab_deck.discard_card(discarded)
            self.visible_habitants.insert(0, self.hab_deck.draw())
            # Remplace la dernière lieu
            discarded_l = self.visible_lieux.pop(-1)
            if discarded_l:
                self.lieu_deck.discard_card(discarded_l)
            self.visible_lieux.insert(0, self.lieu_deck.draw())
            return pen, True

    def get_visible_cards(self):
        """Retourne (hab, lieux)."""
        return self.visible_habitants.copy(), self.visible_lieux.copy()

    def is_game_over(self):
        """Vrai quand on ne peut plus réapprovisionner les habitants."""
        return len(self.hab_deck.draw_pile) == 0

    def calculate_scores(self):
        """
        Score = #habitants +3×#lieux – pénalités.
        """
        scores = {i: 0 for i in range(1, self.num_players + 1)}
        for player, cards in self.kingdoms.items():
            for c in cards:
                if c is None:
                    continue
                if c.card_type == "habitant":
                    scores[player] += 1
                elif c.card_type == "lieu":
                    scores[player] += 3
                elif c.card_type == "penalite":
                    scores[player] -= c.penalty_points
        return scores

    def get_winner(self):
        scores = self.calculate_scores()
        if not scores:
            return [], 0
        max_score = max(scores.values())
        winners = [p for p, s in scores.items() if s == max_score]
        return winners, max_score
