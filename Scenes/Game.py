from ursina import *

from physics3d import Debugger, BoxCollider, MeshCollider
from panda3d.bullet import BulletWorld

from Core.Scene import Scene

from Entities.Player.PlayerCharacter import PlayerCharacter

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, -9.81, 0))
        
        # self.debugger = Debugger(self.world, wireframe=True)
        
        self.create()
        self.addElements()
        
    def create(self):
        
        self.environment()
        
        self.player = PlayerCharacter(self.world)
        
        self.ground = Entity(
          model='cube', 
          position=(0, -3, 0), 
          scale=(100, 0.1, 100),
          color=color.gray,
          texture='grass'
        )
        BoxCollider(self.world, self.ground)
        
        self.box = Entity(model='cube', color=color.red, position=(3, 5, 2))
        MeshCollider(self.world, self.box, mass=1)
        
    def addElements(self):
        self.add_element([
            self.editorCamera, 
            self.sky, 
            self.light, 
            self.player,
            self.player.player_skin,
            self.ground,
            self.box
        ])
        
    def update(self):
        dt = time.dt
        self.world.doPhysics(dt)
    
    def input(self, key):
        pass
        
    def environment(self):
        self.editorCamera = EditorCamera()
        self.sky = Sky()        
        
        camera.position = (0, 5, -1)
        camera.rotation_x = -90
        camera.fov = 130
        
        self.light = DirectionalLight(shadows=True)
        self.light.look_at(Vec3(1,-1,1))

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")