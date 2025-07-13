import pygame
import os
from view.components.button import Button
from controller.game_controller import GameController
from models.dice import Dice

def local_game_loop(screen, number_of_players, *args, **kwargs):
    """
    Écran de jeu local avec gestion des images de cartes manquantes.
    """
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    controller = GameController(number_of_players)

    # Fond
    bg = pygame.image.load(os.path.join("assets", "menu_background.jpg")).convert()
    bg = pygame.transform.scale(bg, (width, height))

    # Polices
    font_path   = os.path.join("assets", "fonts", "medieval.ttf")
    title_font  = pygame.font.Font(font_path, 36)
    small_font  = pygame.font.Font(font_path, 24)

    # État du tour
    rolls_remaining = 3
    dice_list       = [Dice(6, "white") for _ in range(6)]
    dice_values     = [0]*6
    validated       = False
    result_card     = None
    is_penalty      = False

    # Fin de partie
    game_over     = False
    winners       = []
    winning_score = None

    # Cache pour images et placeholders
    image_cache = {}

    def load_card_image(card, ctype, size=(120,160)):
        """
        Tente de charger assets/cards/{ctype}/{card.name}.png
        Si absent, retourne un placeholder coloré avec le texte.
        """
        key = (card.name, ctype)
        if key in image_cache:
            return image_cache[key]

        path = os.path.join("assets", "cards", ctype, f"{card.name}.png")
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, size)
        except FileNotFoundError:
            # fallback : rectangle + nom
            img = pygame.Surface(size)
            # couleur selon type
            if ctype == "habitant":
                img.fill((70, 130, 180))  # steelblue
            else:
                img.fill((139, 69, 19))   # saddlebrown
            # nom centré
            txt = small_font.render(card.name, True, (255,255,255))
            tr = txt.get_rect(center=(size[0]//2, size[1]//2))
            img.blit(txt, tr)
        image_cache[key] = img
        return img

    # Callbacks
    def do_roll():
        nonlocal rolls_remaining, dice_values
        if rolls_remaining>0 and not validated and not game_over:
            for i, die in enumerate(dice_list):
                dice_values[i] = die.roll()
            rolls_remaining -= 1
        return None

    def validate_action():
        nonlocal validated, result_card, is_penalty, game_over, winners, winning_score
        if not validated and not game_over:
            result_card, is_penalty = controller.recruit_or_penalize(dice_values)
            validated = True
            if controller.is_game_over():
                game_over = True
                winners, winning_score = controller.get_winner()
        return None

    def next_turn_action():
        nonlocal rolls_remaining, dice_values, validated, result_card, is_penalty
        if not game_over:
            controller.next_player()
            rolls_remaining = 3
            dice_values     = [0]*6
            validated       = False
            result_card     = None
            is_penalty      = False
        else:
            return "menu", None
        return None

    # Boutons
    back_button     = Button(20, 210, 100, 40, "Retour",   small_font, callback=lambda:("menu",None))
    roll_button     = Button(width//2-75, height-180, 150,50, "Lancer",  small_font, callback=do_roll)
    validate_button = Button(width//2-75, height-120, 150,50, "Valider", small_font, callback=validate_action)
    next_button     = Button(width-150,  height-70,  130,50, "Suivant", small_font, callback=next_turn_action)

    # Boucle principale
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            for btn in (back_button, roll_button, validate_button, next_button):
                res = btn.handle_event(event)
                if res is not None:
                    return res

        screen.blit(bg, (0, 0))

        # Scores à gauche
        scores = controller.calculate_scores()
        panel = pygame.Surface((200, height), pygame.SRCALPHA)
        panel.fill((30,30,30,200))
        screen.blit(panel, (0,0))
        for i in range(1, number_of_players+1):
            txt = small_font.render(f"Joueur {i}: {scores[i]} pts", True, (255,255,255))
            screen.blit(txt, (10, 20 + (i-1)*30))

        # Cartes visibles en haut
        vis_hab, vis_lieu = controller.get_visible_cards()
        card_w, card_h = 120, 160
        start_x = 210
        y_hab = 20
        for idx, card in enumerate(vis_hab):
            if card:
                img = load_card_image(card, "habitant", (card_w,card_h))
                screen.blit(img, (start_x + idx*(card_w+10), y_hab))
        y_lieu = y_hab + card_h + 10
        for idx, card in enumerate(vis_lieu):
            if card:
                img = load_card_image(card, "lieu", (card_w,card_h))
                screen.blit(img, (start_x + idx*(card_w+10), y_lieu))

        if not game_over:
            # Dés
            for idx, val in enumerate(dice_values):
                x = width//2 -180 + (idx%3)*120
                y = height//2 -50  + (idx//3)*100
                rect = pygame.Rect(x-25,y-25,50,50)
                pygame.draw.rect(screen,(200,200,200),rect,2)
                txt = small_font.render(str(val), True, (255,255,255))
                screen.blit(txt, txt.get_rect(center=(x,y)))

            # Infos du tour
            p_txt = title_font.render(f"Joueur {controller.current_player}", True, (30,20,0))
            screen.blit(p_txt, p_txt.get_rect(center=(width//2,50)))
            rem = small_font.render(f"Relances : {rolls_remaining}", True, (255,255,0))
            screen.blit(rem, (220, height-40))

            if validated and result_card:
                label = (f"+ {result_card.name}" if not is_penalty else f"- {result_card.name}")
                clr   = (0,200,0) if not is_penalty else (200,0,0)
                info  = small_font.render(label, True, clr)
                screen.blit(info, info.get_rect(center=(width//2, height//2+150)))

        else:
            # Overlay fin de partie
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (0,0))

            over_surf = title_font.render("PARTIE TERMINÉE", True, (255,255,255))
            screen.blit(over_surf, over_surf.get_rect(center=(width//2, height//2-100)))

            win_str = "Gagnant" + ("s" if len(winners)>1 else "")
            win_surf = small_font.render(
                f"{win_str} : {', '.join('Joueur '+str(w) for w in winners)}", True, (255,255,0)
            )
            screen.blit(win_surf, win_surf.get_rect(center=(width//2, height//2-50)))

            score_surf = small_font.render(f"Score : {winning_score}", True, (255,255,0))
            screen.blit(score_surf, score_surf.get_rect(center=(width//2, height//2)))

        back_button.draw(screen)
        roll_button.draw(screen)
        validate_button.draw(screen)
        next_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
