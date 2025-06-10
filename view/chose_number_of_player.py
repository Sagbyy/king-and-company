import pygame, sys, os
from view.components.button import Button
from view.menu_screen import menu_loop
from view.local_game_screen import local_game_loop


def chose_number_of_player(screen):
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    bg = pygame.image.load(os.path.join("assets", "menu_background.jpg"))
    bg = pygame.transform.scale(bg, (width, height))

    font_path = os.path.join("assets", "fonts", "medieval.ttf")
    font = pygame.font.Font(font_path, 36)
    small_font = pygame.font.Font(font_path, 24)

    button_width = 200
    button_height = 60
    button_spacing = 20
    start_y = height // 2 - (button_height * 3 + button_spacing * 2) // 2

    player_buttons = []
    for i in range(2, 5):
        button = Button(
            x=width // 2 - button_width // 2,
            y=start_y + (i - 2) * (button_height + button_spacing),
            width=button_width,
            height=button_height,
            text=f"{i} Joueurs",
            font=font,
            callback=lambda x=i: local_game_loop(screen, x),
        )
        player_buttons.append(button)

    back_button = Button(
        x=20,
        y=20,
        width=100,
        height=40,
        text="Retour",
        font=small_font,
        callback=lambda: menu_loop(screen),
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            back_result = back_button.handle_event(event)
            if back_result == "back":
                return None

            for button in player_buttons:
                result = button.handle_event(event)
                if result is not None:
                    return result

        screen.blit(bg, (0, 0))

        title_text = "Choisissez le nombre de joueurs"
        title_surf = font.render(title_text, True, (30, 20, 0))
        title_rect = title_surf.get_rect(center=(width // 2, 100))
        screen.blit(title_surf, title_rect)

        for button in player_buttons:
            button.draw(screen)

        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
