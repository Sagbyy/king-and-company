import json
import os
from datetime import datetime


class SaveManager:
    SAVES_DIR = "saves"

    @staticmethod
    def ensure_saves_directory():
        if not os.path.exists(SaveManager.SAVES_DIR):
            os.makedirs(SaveManager.SAVES_DIR)

    @staticmethod
    def save_game(game_controller, save_name=None):
        """Sauvegarde l'état du jeu dans un fichier JSON"""
        SaveManager.ensure_saves_directory()

        if save_name is None:
            save_name = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        save_data = {
            "num_players": game_controller.num_players,
            "current_player": game_controller.current_player,
            "kingdoms": {
                player: [card.to_dict() if card else None for card in cards]
                for player, cards in game_controller.kingdoms.items()
            },
            "visible_habitants": [
                card.to_dict() if card else None
                for card in game_controller.visible_habitants
            ],
            "visible_lieux": [
                card.to_dict() if card else None
                for card in game_controller.visible_lieux
            ],
            "hab_deck": game_controller.hab_deck.to_dict(),
            "lieu_deck": game_controller.lieu_deck.to_dict(),
            "pen_deck": game_controller.pen_deck.to_dict(),
        }

        file_path = os.path.join(SaveManager.SAVES_DIR, f"{save_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

        return file_path

    @staticmethod
    def load_game(save_name):
        """Charge une partie sauvegardée"""
        from controller.game_controller import GameController
        from models.cards import HabitantCard, LieuCard, PenaliteCard, Deck

        file_path = os.path.join(SaveManager.SAVES_DIR, f"{save_name}.json")
        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            save_data = json.load(f)

        # Crée une nouvelle instance de jeu
        game = GameController(save_data["num_players"])
        game.current_player = save_data["current_player"]

        # Restaure les decks
        game.hab_deck = Deck.from_dict(save_data["hab_deck"])
        game.lieu_deck = Deck.from_dict(save_data["lieu_deck"])
        game.pen_deck = Deck.from_dict(save_data["pen_deck"])

        # Restaure les cartes visibles
        def create_card(card_dict):
            if card_dict is None:
                return None
            card_type = card_dict["card_type"]
            if card_type == "habitant":
                return HabitantCard.from_dict(card_dict)
            elif card_type == "lieu":
                return LieuCard.from_dict(card_dict)
            elif card_type == "penalite":
                return PenaliteCard.from_dict(card_dict)
            return None

        game.visible_habitants = [
            create_card(card_dict) for card_dict in save_data["visible_habitants"]
        ]
        game.visible_lieux = [
            create_card(card_dict) for card_dict in save_data["visible_lieux"]
        ]

        # Restaure les royaumes
        game.kingdoms = {
            int(player): [create_card(card_dict) for card_dict in cards]
            for player, cards in save_data["kingdoms"].items()
        }

        return game

    @staticmethod
    def get_save_files():
        """Retourne la liste des sauvegardes disponibles"""
        SaveManager.ensure_saves_directory()
        saves = []
        for file in os.listdir(SaveManager.SAVES_DIR):
            if file.endswith(".json"):
                name = file[:-5]  # Enlève l'extension .json
                path = os.path.join(SaveManager.SAVES_DIR, file)
                modified = datetime.fromtimestamp(os.path.getmtime(path))
                saves.append(
                    {
                        "name": name,
                        "date": modified.strftime("%Y-%m-%d %H:%M:%S"),
                        "path": path,
                    }
                )
        return sorted(saves, key=lambda x: x["date"], reverse=True)
