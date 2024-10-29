from ursina import *

from Core.Physic.character_controller import CharacterController

from Core.Utils import FollowCharacterCamera, SlowParent

class PlayerCharacter(Entity):
    def __init__(self, world, **kwargs):
      super().__init__(**kwargs)
      
      self.player_skin = Entity(model='cube', color=color.red, scale=(1,2,1))        
      self.player = CharacterController(world, self.player_skin)
      self.player.jump_speed = 5.5
      
      self.speed = 1.8
      self.rotation_speed = 60
      
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

    def movement(self):
        self.player.move((0, 0, 0), True)
        
        if held_keys['w']:
            self.player.move((0, 0, self.speed), True)
        if held_keys['s']:
            self.player.move((0, 0, -self.speed), True)
            
        if held_keys['a']:
            self.player.rotate(-self.rotation_speed)
        if held_keys['d']:
            self.player.rotate(self.rotation_speed)
            
    def cameraFollowConfig(self):
      camera.position = (0, 3, -5)
      
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
      self.playerPivot.rotation_y = - Vec3(self.player.np.getHpr()).x
