from ursina import *

from Core.Physic import Debugger, BoxCollider, MeshCollider
from panda3d.bullet import BulletWorld

from Core.Scene import Scene

from Entities.Player.PlayerCharacter import PlayerCharacter

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, -9.81, 0))
        
        self.debugger = Debugger(self.world, wireframe=True)
        
        self.create()
        self.addElements()
        
    def create(self):
        
        self.environment()
        
        self.player = PlayerCharacter(self.world)
        
        self.ground = Entity(
          model='cube', 
          position=(0, -3, 0), 
          scale=(20, 0.5, 20),
          color=color.gray,
          texture='white_cube'
        )
        BoxCollider(self.world, self.ground)
        
        self.box = Entity(model='cube', color=color.blue, position=(3, 5, 2))
        BoxCollider(self.world, self.box, mass=1, scale=(.5,.5,.5))
        
    def addElements(self):
        self.add_element([
            # self.editorCamera,
            self.sky, 
            self.light, 
            self.player,
            self.player.player_skin,
            self.ground,
            self.box
        ])
        
    def update(self):
        if not self.paused:
            dt = time.dt
            self.world.doPhysics(dt)
    
    def input(self, key):
        pass
        
    def environment(self):
        # self.editorCamera = EditorCamera()
        self.sky = Sky()
        
        self.light = DirectionalLight(shadows=True)
        self.light.look_at(Vec3(1,-1,1))

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")