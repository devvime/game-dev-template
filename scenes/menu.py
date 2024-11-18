from ursina import *
from core.scene import Scene

class MenuScene(Scene):
    def __init__(self, scene_manager):
        super().__init__()
        
        self.scene_manager = scene_manager
        
        self.title = Text("Menu Scene", scale=2, position=(0, 0.4))
                
        self.start_button = Button(text="Start Game", scale=(0.2, 0.1), position=(0, 0.1), color=color.azure)
        self.start_button.on_click = self.start_game
        
        self.exit_button = Button(text="Exit", scale=(0.2, 0.1), position=(0, -0.1), color=color.red)
        self.exit_button.on_click = application.quit
        
        self.addElements()
        
    def addElements(self):
        self.add_element([self.title, self.start_button, self.exit_button])
        
    def update(self):
        if not self.paused:
            pass
    
    def input(self, key):
        pass
        
    def start_game(self):
        self.scene_manager.switch_to('game')

    def enable(self):
        super().enable()

    def disable(self):
        super().disable()
