from ursina import *
from Core.Scene import Scene

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.player = Entity(model='cube', color=color.azure, position=(0, 1, 0))
        self.ground = Entity(model='plane', scale=(10, 1, 10), texture='white_cube', collider='box')
        
        # Add elements to the scene element list
        self.add_element(self.player)
        self.add_element(self.ground)

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")