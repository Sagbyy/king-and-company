import pygame
import os
from view.components.button import Button


def local_game_loop(screen, number_of_players, *args, **kwargs):
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    bg = pygame.image.load(os.path.join("assets", "menu_background.jpg"))
    bg = pygame.transform.scale(bg, (width, height))

    font_path = os.path.join("assets", "fonts", "medieval.ttf")
    font = pygame.font.Font(font_path, 36)
    small_font = pygame.font.Font(font_path, 24)

    current_player = 1

    back_button = Button(
        x=20,
        y=20,
        width=100,
        height=40,
        text="Retour",
        font=small_font,
        callback=lambda: ("menu", None),
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            back_result = back_button.handle_event(event)
            if back_result is not None:
                return back_result

        screen.blit(bg, (0, 0))

        player_text = f"Joueur {current_player}"
        text_surf = font.render(player_text, True, (30, 20, 0))
        text_rect = text_surf.get_rect(center=(width // 2, 50))
        screen.blit(text_surf, text_rect)

        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
