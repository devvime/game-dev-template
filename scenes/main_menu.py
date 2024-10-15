from ursina import Entity, Text, Button
from utils import load_settings

class MainMenu(Entity):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.title = Text(text="My Game", scale=2, position=(0, 0.4))

        self.play_button = Button(text="Play", position=(0, 0.1), scale=(0.2, 0.1))
        self.play_button.on_click = self.start_game

        self.settings_button = Button(text="Settings", position=(0, -0.1), scale=(0.2, 0.1))
        self.settings_button.on_click = self.go_to_settings

        self.quit_button = Button(text="Quit", position=(0, -0.3), scale=(0.2, 0.1))
        self.quit_button.on_click = self.quit_game

    def start_game(self):
        self.game.switch_scene('game')

    def go_to_settings(self):
        self.game.switch_scene('settings')

    def quit_game(self):
        exit()
