from ursina import *
from ursina.shaders.screenspace_shaders.pixelation_shader import pixelation_shader
from Core.Scene import Scene

from physics3d import Debugger, BoxCollider, MeshCollider
from physics3d.character_controller import CharacterController
from panda3d.bullet import BulletWorld

from Entities.Player.Player import Player
from Entities.Box.Box import Box

class TestScene(Scene):
    def __init__(self):
        super().__init__()
        
        self.world = BulletWorld()
        self.debugger = Debugger(self.world, wireframe=True)        
        self.world.setGravity(Vec3(0, -9.81, 0))
        
        self.environment()
        
        self.cube = Entity(model='cube', color=color.red)
        # MeshCollider(self.world, self.cube, mass=1)
        
        self.player = CharacterController(self.world, self.cube)
        
        self.ground = Entity(model='cube', position=(0, -3, 0), scale=(10, 0.1, 10), color=color.blue)
        BoxCollider(self.world, self.ground)
        
        # Add elements to the scene element list
        self.addElements()
        
    def addElements(self):
        self.add_element(
            [
                self.editorCamera, 
                self.sky, 
                self.light,
                self.ground,
                self.player
            ]
        )
        
    def update(self):
        dt = time.dt
        self.world.doPhysics(dt)
        
        self.player.move((0, 0, 0), True)
        
        if held_keys['w']:
            self.player.move((0, 0, 1), True)
        if held_keys['s']:
            self.player.move((0, 0, -1), True)
        if held_keys['space']:
            self.player.jump()
    
    def input(self, key):
        pass
        
    def environment(self):
        self.editorCamera = EditorCamera()
        self.sky = Sky()        
        
        # camera.shader = pixelation_shader
        camera.position = (0, 5, -10)
        camera.rotation_x = -90
        camera.fov = 120
        
        self.light = DirectionalLight(shadows=True)
        self.light.look_at(Vec3(1,-1,1))

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")