from ursina import *
from Core.Scene import Scene

class MenuScene(Scene):
    def __init__(self, scene_manager):
        super().__init__()
        self.scene_manager = scene_manager
        
        self.title = Text("Menu Scene", scale=2, position=(0, 0.4))
        self.add_element(self.title)
        
        self.start_button = Button(text="Iniciar Game", scale=(0.2, 0.1), position=(0, 0.1), color=color.azure)
        self.start_button.on_click = self.start_game
        self.add_element(self.start_button)
        
        self.exit_button = Button(text="Sair", scale=(0.2, 0.1), position=(0, -0.1), color=color.red)
        self.exit_button.on_click = application.quit
        self.add_element(self.exit_button)
        
    def start_game(self):
        self.scene_manager.switch_to('game')

    def enable(self):
        super().enable()
        print("Menu Scene enabled!")

    def disable(self):
        super().disable()
        print("Menu Scene disabled!")
