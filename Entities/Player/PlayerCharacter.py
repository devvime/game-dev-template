from ursina import *
from direct.actor.Actor import Actor

from Core.Physic.character_controller import CharacterController

class PlayerCharacter(Entity):
    def __init__(self, world, **kwargs):
      super().__init__(**kwargs)
      
      self.player_skin = Entity(scale=1.8, position=(0,-1.6,0), rotation=(0,-180,0))
      self.player_actor = Actor("../Assets/Models/Player/player.glb")
      self.player_actor.reparentTo(self.player_skin)      
      self.player = CharacterController(world, self.player_skin, radius=0.8, height=4.95)
      
      self.player.jump_speed = 5.5      
      self.speed = 1.8
      self.rotation_speed = 100
      self.lastDir = ''
      self.isMoving = False
      
      self.player_actor.loop('idle')      
      self.cameraFollowConfig()

    def update(self):      
      self.movement()
      self.cameraFollow()
      
    def input(self, key):
        if key == 'shift':
            self.speed = self.speed * 2
        
        if key == 'shift up':
            self.speed = self.speed / 2
        
        if key == 'space':
            self.player.jump()
        
        self.animate(key)

    def movement(self):
        self.player.move((0, 0, 0), True)
        
        if held_keys['w'] or held_keys['a'] or held_keys['d'] or held_keys['s']:
            self.player.move((0, 0, self.speed), True)
            self.isMoving = True
        else: 
            self.isMoving = False
        
        if held_keys['s']:
            self.isMoving = True
            if (self.lastDir == 'left'):
                self.player.rotate(-self.rotation_speed * 2)
            if (self.lastDir == 'right'):
                self.player.rotate(self.rotation_speed * 2)
        else: 
            self.isMoving = False
            
        if held_keys['a']:
            self.player.rotate(-self.rotation_speed)
            self.lastDir = 'left'
            self.isMoving = True
        else: 
            self.isMoving = False
        
        if held_keys['d']:
            self.player.rotate(self.rotation_speed)
            self.lastDir = 'right'
            self.isMoving = True
        else: 
            self.isMoving = False
            
    def animate(self, key):
        if key == 'w' or key == 'a' or key == 's' or key == 'd':
            self.loopAnim('walk')
            
        if key == 'w up' or key == 'a up' or key == 's up' or key == 'd up':
            self.loopAnim('idle')
            
        
        if key == 'space':
            self.player.jump()
            self.player_actor.play('jump')            
            invoke(self.stopAnim, delay=0.8)
            
    def loopAnim(self, name):
        self.player_actor.stop()
        self.player_actor.loop(name)
                
    def stopAnim(self):
        self.player_actor.stop()
        self.player_actor.loop('idle')            
            
    def cameraFollowConfig(self):
      camera.position = (0, 1, -1.5)
      
      self.playerPivot = Entity(model='sphere', scale=(2, 2, 2))
      self.playerPivot.visible_self = False
      
      self.lag = 0.05
      self.camera_target_position = Vec3(self.player.np.getPos())
      
    def cameraFollow(self):
        camera.rotation_x = 10
        camera.fov = 120
        camera.parent = self.playerPivot
        
        self.camera_target_position = Vec3(lerp(self.camera_target_position, Vec3(self.player.np.getPos()), self.lag))
        self.playerPivot.position = self.camera_target_position      
        # self.playerPivot.rotation_y = - Vec3(self.player.np.getHpr()).x
