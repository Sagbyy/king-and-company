from models.cards import (
    Deck,
    all_habitants,
    all_lieux,
    all_penalites,
    HabitantCard,
    LOCATIONS,
)
from models.dice import DiceSet


class GameController:

    def __init__(self, num_players):
        self.num_players = num_players
        self.current_player = 1
        self.kingdoms = {i: [] for i in range(1, num_players + 1)}

        self.hab_deck = Deck(list(all_habitants))
        self.lieu_deck = Deck(list(all_lieux))
        self.pen_deck = Deck(list(all_penalites))
        self.hab_deck.shuffle()
        self.lieu_deck.shuffle()
        self.pen_deck.shuffle()

        self.lieu_piles = {}
        for loc_name, color in LOCATIONS.items():
            self.lieu_piles[loc_name] = []
            for value in [4, 3, 2]:
                for card in self.lieu_deck.draw_pile:
                    if card.name == loc_name and card.value == value:
                        self.lieu_piles[loc_name].append(card)
                        self.lieu_deck.draw_pile.remove(card)
                        break

        self.visible_habitants = [self.hab_deck.draw() for _ in range(5)]

        self.dice_set = DiceSet()
        self.rolls_left = 3

    def next_player(self):
        self.current_player = (self.current_player % self.num_players) + 1
        self.rolls_left = 3
        self.dice_set.unlock_all()

    def roll_dice(self, locked_indices=None):
        if self.rolls_left <= 0:
            return False

        self.dice_set.unlock_all()
        if locked_indices:
            for idx in locked_indices:
                self.dice_set.lock_die(idx)

        self.dice_set.roll_all()
        self.rolls_left -= 1
        return True

    def get_dice_state(self):
        return (
            self.dice_set.get_values(),
            self.dice_set.get_locked_indices(),
            self.rolls_left,
        )

    def apply_roll(self, dice_values):
        for card in self.visible_habitants:
            if isinstance(card, HabitantCard) and card.is_combo_met(dice_values):
                return card
        return None

    def recruit_or_penalize(self):
        """
        If combo found: recruitment, else penalty.
        Updates kingdoms, visible_habitants and lieu_piles.
        Returns (card, was_penalty).
        """
        player = self.current_player
        dice_values = self.dice_set.get_values()
        card = self.apply_roll(dice_values)

        if card:
            self.kingdoms[player].append(card)
            idx = self.visible_habitants.index(card)

            for loc_name, pile in self.lieu_piles.items():
                if pile and pile[-1].color == card.color:
                    self.kingdoms[player].append(pile.pop())
                    break

            self.visible_habitants[idx] = self.hab_deck.draw()
            return card, False
        else:
            # Penalty
            pen = self.pen_deck.draw()
            if pen:
                self.kingdoms[player].append(pen)

            if self.visible_habitants:
                discarded = self.visible_habitants.pop(-1)
                if discarded:
                    self.hab_deck.discard_card(discarded)

            new_card = self.hab_deck.draw()
            if new_card:
                self.visible_habitants.insert(0, new_card)

            return pen, True

    def get_visible_cards(self):
        return self.visible_habitants.copy(), {
            k: v[:] for k, v in self.lieu_piles.items()
        }

    def is_game_over(self):
        return len(self.hab_deck.draw_pile) == 0 or all(
            len(pile) == 0 for pile in self.lieu_piles.values()
        )

    def calculate_scores(self):
        scores = {i: 0 for i in range(1, self.num_players + 1)}
        for player, cards in self.kingdoms.items():
            for card in cards:
                if card is not None:
                    scores[player] += card.points
        return scores

    def get_winner(self):
        scores = self.calculate_scores()
        if not scores:
            return [], 0
        max_score = max(scores.values())
        winners = [p for p, s in scores.items() if s == max_score]
        return winners, max_score
