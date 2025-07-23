import pygame
from view.components.button import Button
from models.save_manager import SaveManager


def load_game_loop(screen, *args, **kwargs):
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    # Charger la police
    font_path = pygame.font.get_default_font()
    font = pygame.font.Font(font_path, 24)
    title_font = pygame.font.Font(font_path, 36)

    # Charger le fond d'écran
    bg = pygame.Surface((width, height))
    bg.fill((50, 50, 50))  # Fond gris foncé

    # Titre
    title = title_font.render("Charger une partie", True, (255, 255, 255))
    title_rect = title.get_rect(center=(width // 2, 50))

    # Obtenir la liste des sauvegardes
    saves = SaveManager.get_save_files()

    # Créer les boutons pour chaque sauvegarde
    buttons = []
    button_height = 60
    button_spacing = 20
    start_y = 120

    for save in saves:
        save_text = f"{save['name']} - {save['date']}"
        b = Button(
            x=width // 2 - 200,
            y=start_y,
            width=400,
            height=button_height,
            text=save_text,
            font=font,
            callback=lambda s=save["name"]: ("load_save", s),
        )
        buttons.append(b)
        start_y += button_height + button_spacing

    # Bouton retour
    back_button = Button(
        x=width // 2 - 100,
        y=height - 80,
        width=200,
        height=50,
        text="Retour",
        font=font,
        callback=lambda: ("menu", None),
    )
    buttons.append(back_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            for button in buttons:
                result = button.handle_event(event)
                if result is not None:
                    return result

        # Dessiner
        screen.blit(bg, (0, 0))
        screen.blit(title, title_rect)

        # Message si pas de sauvegarde
        if not saves:
            no_saves = font.render(
                "Aucune sauvegarde disponible", True, (255, 255, 255)
            )
            no_saves_rect = no_saves.get_rect(center=(width // 2, height // 2))
            screen.blit(no_saves, no_saves_rect)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
