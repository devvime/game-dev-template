from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.shaders.screenspace_shaders.pixelation_shader import pixelation_shader
from Core.Scene import Scene

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        
        self.environment()
        
        self.player = Entity(model='cube', texture='white_cube', position=(0, 1, 0), shader=lit_with_shadows_shader)
        self.ground = Entity(model='plane', scale=(10, 1, 10), texture='white_cube', collider='box', shader=lit_with_shadows_shader)
        
        # Add elements to the scene element list
        self.add_element(self.player)
        self.add_element(self.ground)
        
    def environment(self):
        editorCamera = EditorCamera()
        sky = Sky()        
        # camera.shader = pixelation_shader
        
        light = DirectionalLight(shadows=True)
        light.look_at(Vec3(1,-1,1))
        
        self.add_element(editorCamera)
        self.add_element(sky)
        self.add_element(light)
        
    def update(self):
        print('aaaaaa')

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")