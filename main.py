import pygame
from view.screen_manager import ScreenManager
from view.menu_screen import menu_loop
from view.chose_number_of_player import chose_number_of_player
from view.local_game_screen import local_game_loop
from view.load_game_screen import load_game_loop
from controller.game_controller import GameController


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Roi & Compagnie 👑")

    # Initialize screen manager
    screen_manager = ScreenManager(screen)

    # Register all screens
    screen_manager.register_screen("menu", menu_loop)
    screen_manager.register_screen("chose_players", chose_number_of_player)
    screen_manager.register_screen("local_game", local_game_loop)
    screen_manager.register_screen("load_game", load_game_loop)

    def handle_load_save(screen, save_name):
        """Charge une partie sauvegardée et lance le jeu"""
        game = GameController.load_game(save_name)
        if game:
            return local_game_loop(screen, game)
        return "menu"

    # Register special handlers
    screen_manager.register_screen("load_save", handle_load_save)

    # Start with the menu screen
    screen_manager.switch_screen("menu")

    # Run the game
    screen_manager.run()


if __name__ == "__main__":
    run_game()
