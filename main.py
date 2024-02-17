# from ui.menu import main_menu
from ui.ui_manager import UIManager
from gamemanager import GameManager

if __name__ == "__main__":
    # menu = UIManager()
    # menu.run()
    # main_menu()
    game = GameManager()
    game.run()
