from ursina import *
from ursina.shaders import lit_with_shadows_shader
from Core.Scene import Scene

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        EditorCamera()
        camera.shader = lit_with_shadows_shader
        light = DirectionalLight(shadows=True)
        light.look_at(Vec3(1,-1,1))
        
        self.player = Entity(model='cube', color=color.azure, position=(0, 1, 0), shader=lit_with_shadows_shader)
        self.ground = Entity(model='plane', scale=(10, 1, 10), texture='white_cube', collider='box', shader=lit_with_shadows_shader)
        
        # Add elements to the scene element list
        self.add_element(self.player)
        self.add_element(self.ground)

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")