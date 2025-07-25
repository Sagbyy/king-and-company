import pygame, sys, os
from view.components.button import Button


def menu_loop(screen, *args, **kwargs):
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    pygame.mixer.music.load(os.path.join("assets", "menu_song.mp3"))
    pygame.mixer.music.play(-1)

    font_path = os.path.join("assets", "fonts", "medieval.ttf")
    font = pygame.font.Font(font_path, 36)

    bg = pygame.image.load(os.path.join("assets", "menu_background.jpg"))
    bg = pygame.transform.scale(bg, (width, height))

    banner_image = pygame.image.load(os.path.join("assets", "menu_banner.png"))
    banner_image = pygame.transform.scale(
        banner_image, (banner_image.get_width() / 2, banner_image.get_height() / 2)
    )
    banner_rect = banner_image.get_rect(center=(width // 2, height // 5))

    buttons = []
    labels = ["Nouvelle Partie", "Charger Partie", "Contre IA", "Quitter"]
    actions = [
        lambda: ("chose_players", None),
        lambda: ("load_game", None),
        lambda: print(">> IA"),
        lambda: "quit",
    ]

    for i, (label, action) in enumerate(zip(labels, actions)):
        b = Button(
            x=width // 2 - 100,
            y=height // 2 - 100 + i * 80,
            width=200,
            height=50,
            text=label,
            font=font,
            callback=action,
        )
        buttons.append(b)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            for button in buttons:
                result = button.handle_event(event)
                if result is not None:
                    return result

        screen.blit(bg, (0, 0))
        screen.blit(banner_image, banner_rect)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
