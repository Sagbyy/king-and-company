import pygame
import os
from view.components.button import Button
from controller.game_controller import GameController
from models.dice import DiceSet


def local_game_loop(screen, number_of_players, *args, **kwargs):
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    controller = GameController(number_of_players)

    bg = pygame.image.load(os.path.join("assets", "menu_background.jpg")).convert()
    bg = pygame.transform.scale(bg, (width, height))

    font_path = os.path.join("assets", "fonts", "medieval.ttf")
    title_font = pygame.font.Font(font_path, 36)
    small_font = pygame.font.Font(font_path, 24)

    dice_values = [0] * 6
    locked_dice = []
    validated = False
    result_card = None
    is_penalty = False

    game_over = False
    winners = []
    winning_score = None

    image_cache = {}

    def load_card_image(card, ctype, size=(120, 160)):
        key = (card.name, ctype)
        if key in image_cache:
            return image_cache[key]

        path = os.path.join("assets", "cards", ctype, f"{card.name}.png")
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, size)
        except FileNotFoundError:
            img = pygame.Surface(size)
            if ctype == "habitant":
                img.fill((70, 130, 180))  # Blue
            else:
                img.fill((139, 69, 19))  # Saddlebrown

            txt = small_font.render(card.name, True, (255, 255, 255))
            tr = txt.get_rect(center=(size[0] // 2, size[1] // 4))
            img.blit(txt, tr)

            points_txt = small_font.render(
                f"{card.points:+d} points", True, (255, 255, 0)
            )
            points_rect = points_txt.get_rect(center=(size[0] // 2, size[1] // 2))
            img.blit(points_txt, points_rect)

            if hasattr(card, "effect") and card.effect:
                words = card.effect.split()
                lines = []
                current_line = []
                current_length = 0
                max_chars = 15

                for word in words:
                    if current_length + len(word) + 1 <= max_chars:
                        current_line.append(word)
                        current_length += len(word) + 1
                    else:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                        current_length = len(word)
                if current_line:
                    lines.append(" ".join(current_line))

                tiny_font = pygame.font.Font(font_path, 12)
                y_offset = size[1] * 2 // 3
                for line in lines:
                    effect_txt = tiny_font.render(line, True, (200, 200, 200))
                    effect_rect = effect_txt.get_rect(center=(size[0] // 2, y_offset))
                    img.blit(effect_txt, effect_rect)
                    y_offset += 15

            if hasattr(card, "variable_points") and card.variable_points:
                var_txt = tiny_font.render("(Points variables)", True, (255, 165, 0))
                var_rect = var_txt.get_rect(center=(size[0] // 2, size[1] - 15))
                img.blit(var_txt, var_rect)

        image_cache[key] = img
        return img

    def do_roll():
        nonlocal dice_values, locked_dice
        if controller.rolls_left > 0 and not validated and not game_over:
            success = controller.roll_dice(locked_dice)
            if success:
                dice_values = controller.dice_set.get_values()
        return None

    def toggle_die(idx):
        nonlocal locked_dice
        if idx in locked_dice:
            locked_dice.remove(idx)
        else:
            locked_dice.append(idx)

    def validate_action():
        nonlocal validated, result_card, is_penalty, game_over, winners, winning_score
        if not validated and not game_over:
            result_card, is_penalty = controller.recruit_or_penalize()
            validated = True
            if controller.is_game_over():
                game_over = True
                winners, winning_score = controller.get_winner()
        return None

    def next_turn_action():
        nonlocal dice_values, locked_dice, validated, result_card, is_penalty
        if not game_over:
            controller.next_player()
            dice_values = [0] * 6
            locked_dice = []
            validated = False
            result_card = None
            is_penalty = False
        else:
            return "menu", None
        return None

    # Buttons
    back_button = Button(
        20, 210, 100, 40, "Retour", small_font, callback=lambda: ("menu", None)
    )
    roll_button = Button(
        width // 2 - 75, height - 180, 150, 50, "Lancer", small_font, callback=do_roll
    )
    validate_button = Button(
        width // 2 - 75,
        height - 120,
        150,
        50,
        "Valider",
        small_font,
        callback=validate_action,
    )
    next_button = Button(
        width - 150,
        height - 70,
        130,
        50,
        "Suivant",
        small_font,
        callback=next_turn_action,
    )

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for idx in range(6):
                    x = width // 2 - 180 + (idx % 3) * 120
                    y = height // 2 - 50 + (idx // 3) * 100
                    rect = pygame.Rect(x - 25, y - 25, 50, 50)
                    if rect.collidepoint(mouse_pos) and not validated:
                        toggle_die(idx)
            for btn in (back_button, roll_button, validate_button, next_button):
                res = btn.handle_event(event)
                if res is not None:
                    return res

        screen.blit(bg, (0, 0))

        scores, negative_points = controller.calculate_scores()
        panel = pygame.Surface((200, height), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        screen.blit(panel, (0, 0))
        for i in range(1, number_of_players + 1):
            txt = small_font.render(
                f"Joueur {i}: {scores[i]} points", True, (255, 255, 255)
            )
            screen.blit(txt, (10, 20 + (i - 1) * 30))
            if negative_points[i] > 0:
                neg_txt = small_font.render(
                    f"(Malus: -{negative_points[i]})", True, (255, 100, 100)
                )
                screen.blit(neg_txt, (10, 40 + (i - 1) * 30))

        vis_hab, lieu_piles = controller.get_visible_cards()
        card_w, card_h = 120, 160
        start_x = 210
        y_hab = 20
        for idx, card in enumerate(vis_hab):
            if card:
                img = load_card_image(card, "habitant", (card_w, card_h))
                screen.blit(img, (start_x + idx * (card_w + 10), y_hab))

        y_lieu = y_hab + card_h + 10
        x_offset = 0
        for loc_name, pile in lieu_piles.items():
            if pile:
                img = load_card_image(pile[-1], "lieu", (card_w, card_h))
                screen.blit(img, (start_x + x_offset * (card_w + 10), y_lieu))
                x_offset += 1

        if not game_over:
            dice_colors = {
                0: (255, 0, 0),  # Rouge
                1: (255, 0, 0),  # Rouge
                2: (0, 255, 0),  # Vert
                3: (0, 255, 0),  # Vert
                4: (0, 0, 255),  # Bleu
                5: (0, 0, 255),  # Bleu
            }
            for idx, val in enumerate(dice_values):
                x = width // 2 - 180 + (idx % 3) * 120
                y = height // 2 - 50 + (idx // 3) * 100
                rect = pygame.Rect(x - 25, y - 25, 50, 50)
                color = dice_colors[idx]
                if idx in locked_dice:
                    pygame.draw.rect(screen, color, rect)
                else:
                    pygame.draw.rect(screen, color, rect, 2)
                txt = small_font.render(str(val), True, (255, 255, 255))
                screen.blit(txt, txt.get_rect(center=(x, y)))

            p_txt = title_font.render(
                f"Joueur {controller.current_player}", True, (30, 20, 0)
            )
            screen.blit(p_txt, p_txt.get_rect(center=(width // 2, 50)))
            rem = small_font.render(
                f"Lancers restants: {controller.rolls_left}", True, (255, 255, 0)
            )
            screen.blit(rem, (220, height - 40))

            if validated and result_card:
                label = (
                    f"+ {result_card.name}"
                    if not is_penalty
                    else f"- {result_card.name}"
                )
                clr = (0, 200, 0) if not is_penalty else (200, 0, 0)
                info = small_font.render(label, True, clr)
                screen.blit(info, info.get_rect(center=(width // 2, height // 2 + 150)))

        else:
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            over_surf = title_font.render("PARTIE TERMINEE", True, (255, 255, 255))
            screen.blit(
                over_surf, over_surf.get_rect(center=(width // 2, height // 2 - 100))
            )

            win_str = "Gagnant" + ("s" if len(winners) > 1 else "")
            win_surf = small_font.render(
                f"{win_str}: {', '.join('Joueur '+str(w) for w in winners)}",
                True,
                (255, 255, 0),
            )
            screen.blit(
                win_surf, win_surf.get_rect(center=(width // 2, height // 2 - 50))
            )

            score_surf = small_font.render(
                f"Score: {winning_score}", True, (255, 255, 0)
            )
            screen.blit(
                score_surf, score_surf.get_rect(center=(width // 2, height // 2))
            )

        back_button.draw(screen)
        roll_button.draw(screen)
        validate_button.draw(screen)
        next_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
