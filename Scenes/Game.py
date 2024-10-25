from ursina import *
from ursina.shaders.screenspace_shaders.pixelation_shader import pixelation_shader
from Core.Scene import Scene

from Entities.Player.Player import Player

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        
        self.environment()
        
        self.player = Player()
        self.ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))
        
        # Add elements to the scene element list
        self.addElements()
        
    def addElements(self):
        self.add_element([self.editorCamera, self.sky, self.light, self.player, self.ground])
        
    def update(self):
        pass
        
    def environment(self):
        self.editorCamera = EditorCamera()
        self.sky = Sky()        
        # camera.shader = pixelation_shader
        
        self.light = DirectionalLight(shadows=True)
        self.light.look_at(Vec3(1,-1,1))

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")