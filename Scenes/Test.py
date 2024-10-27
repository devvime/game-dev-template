from ursina import *
from ursina.vec3 import Vec3
from ursina.shaders.screenspace_shaders.pixelation_shader import pixelation_shader

from physics3d import Debugger, BoxCollider, MeshCollider
from physics3d.character_controller import CharacterController
from panda3d.bullet import BulletWorld

from Core.Scene import Scene
from Core.Utils import FollowCharacterCamera

class TestScene(Scene):
    def __init__(self):
        super().__init__()
        
        self.world = BulletWorld()
        # self.debugger = Debugger(self.world, wireframe=True)
        self.world.setGravity(Vec3(0, -9.81, 0))
        
        self.environment()
        
        self.player_skin = Entity(model='cube', color=color.red, scale=(1,2,1))        
        self.player = CharacterController(self.world, self.player_skin)
        self.player.jump_speed = 5.5
        
        self.follow_character = FollowCharacterCamera(self.player)
        
        self.box = Entity(model='cube', color=color.red, position=(3, 5, 2))
        MeshCollider(self.world, self.box, mass=1)
        
        self.ground = Entity(
          model='cube', 
          position=(0, -3, 0), 
          scale=(100, 0.1, 100),
          color=color.gray,
          texture='grass'
        )
        BoxCollider(self.world, self.ground)
        
        # Add elements to the scene element list
        self.addElements()
        
    def addElements(self):
        self.add_element(
            [
                # self.editorCamera, 
                self.sky, 
                self.light,
                self.ground,
                self.player_skin,
                self.player,
            ]
        )
        
    def update(self):
        dt = time.dt
        self.world.doPhysics(dt)
        
        camera.position = (0, 4, -5)
        camera.rotation_x = 25
        camera.fov = 120
        
        self.player.move((0, 0, 0), True)
        
        if held_keys['w']:
            self.player.move((0, 0, 1.5), True)
        if held_keys['s']:
            self.player.move((0, 0, -1.5), True)
            
        if held_keys['a']:
            self.player.rotate(-30)
        if held_keys['d']:
            self.player.rotate(30)
            
        self.follow_character.update()
                
    def input(self, key):
      if key == 'space':
        self.player.jump()
        
    def environment(self):
        # self.editorCamera = EditorCamera()
        self.sky = Sky()
        
        # camera.shader = pixelation_shader
        
        self.light = AmbientLight(shadows=True)
        self.light.look_at(Vec3(1,-1,1))

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")