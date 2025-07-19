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
        self.base_rolls = 3
        self.extra_rolls = 0
        self.rolls_left = self.base_rolls

        self.extra_turn_pending = False
        self.can_take_extra_card = False
        self.can_transfer_penalty = False

    def next_player(self):
        if not self.extra_turn_pending:
            self.current_player = (self.current_player % self.num_players) + 1
        self.extra_turn_pending = False
        self.rolls_left = self.base_rolls + self.extra_rolls
        self.extra_rolls = 0
        self.dice_set.unlock_all()
        self.can_take_extra_card = False
        self.can_transfer_penalty = False

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

    def apply_roll(self):
        dice_values = self.dice_set.get_values()
        dice_colors = [die.get_color() for die in self.dice_set.get_dice()]

        for card in self.visible_habitants:
            if isinstance(card, HabitantCard) and card.is_combo_met(
                dice_values, dice_colors
            ):
                return card
        return None

    def apply_card_effects(self, card):
        if not card or not isinstance(card, HabitantCard):
            return

        if card.name == "Elfe arrogant":
            self.extra_rolls = 1

        elif card.name == "Apprenti sorcier talentueux":
            self.extra_turn_pending = True

        elif card.name == "Hypnotiseur":
            self.can_take_extra_card = True

    def recruit_or_penalize(self):
        player = self.current_player
        card = self.apply_roll()

        if card:
            # Recruit habitant
            self.kingdoms[player].append(card)
            idx = self.visible_habitants.index(card)

            # Apply card effects
            self.apply_card_effects(card)

            # Check if lieu card available
            for loc_name, pile in self.lieu_piles.items():
                if pile and pile[-1].color == card.color:
                    self.kingdoms[player].append(pile.pop())
                    break

            # Handle Hypnotiseur effect
            if self.can_take_extra_card and idx < len(self.visible_habitants) - 1:
                extra_card = self.visible_habitants[idx + 1]
                self.kingdoms[player].append(extra_card)
                self.visible_habitants[idx + 1] = self.hab_deck.draw()

            # Replace habitant card
            self.visible_habitants[idx] = self.hab_deck.draw()
            return card, False
        else:
            # Penalty
            pen = self.pen_deck.draw()
            if pen:
                if pen.name == "Dragon":
                    self.can_transfer_penalty = True
                self.kingdoms[player].append(pen)

            # Remove rightmost habitant
            if self.visible_habitants:
                discarded = self.visible_habitants.pop(-1)
                if discarded:
                    self.hab_deck.discard_card(discarded)

            # Add new habitant on the left
            new_card = self.hab_deck.draw()
            if new_card:
                self.visible_habitants.insert(0, new_card)

            return pen, True

    def transfer_penalty(self, target_player):
        if not self.can_transfer_penalty or target_player == self.current_player:
            return False

        current_kingdom = self.kingdoms[self.current_player]
        target_kingdom = self.kingdoms[target_player]

        for i in range(len(current_kingdom) - 1, -1, -1):
            card = current_kingdom[i]
            if card.card_type == "penalite" and card.transferable:
                current_kingdom.pop(i)
                target_kingdom.append(card)
                self.can_transfer_penalty = False
                return True
        return False

    def get_visible_cards(self):
        return self.visible_habitants.copy(), {
            k: v[:] for k, v in self.lieu_piles.items()
        }

    def is_game_over(self):
        return (
            len(self.hab_deck.draw_pile) == 0 
            or len(self.pen_deck.draw_pile) == 0 
            or any(
                len(pile) == 0 for pile in self.lieu_piles.values()
            )
        )

    def calculate_scores(self):
        scores = {i: 0 for i in range(1, self.num_players + 1)}
        negative_points = {
            i: 0 for i in range(1, self.num_players + 1)
        }

        for player, cards in self.kingdoms.items():
            for card in cards:
                if card is not None:
                    if isinstance(card, HabitantCard) and card.variable_points:
                        points = card.calculate_points(cards)
                        scores[player] += points
                    else:
                        points = card.points
                        scores[player] += points
                        if points < 0:
                            negative_points[player] += abs(points)

        return scores, negative_points

    def get_winner(self):
        scores, negative_points = self.calculate_scores()
        if not scores:
            return [], 0

        max_score = max(scores.values())
        tied_players = [p for p, s in scores.items() if s == max_score]

        if len(tied_players) > 1:
            min_negative = min(negative_points[p] for p in tied_players)
            winners = [p for p in tied_players if negative_points[p] == min_negative]
        else:
            winners = tied_players

        return winners, max_score
