import pygame
from view.menu_screen import menu_loop


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Roi & Compagnie 👑")
    menu_loop(screen)
    pygame.quit()


if __name__ == "__main__":
    run_game()
