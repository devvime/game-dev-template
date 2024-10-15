from ursina import Entity, Text, Button
from utils import load_settings

class GameScene(Entity):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def dot_to_menu(self):
        self.game.switch_scene('menu')

    def go_to_settings(self):
        self.game.switch_scene('settings')

    def quit_game(self):
        exit()
