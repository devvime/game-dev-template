from ursina import *

from physics3d.character_controller import CharacterController

from Core.Utils import FollowCharacterCamera

class PlayerCharacter(Entity):
    def __init__(self, world, **kwargs):
      super().__init__(**kwargs)
      
      self.player_skin = Entity(model='cube', color=color.red, scale=(1,2,1))        
      self.player = CharacterController(world, self.player_skin)
      self.player.jump_speed = 5.5
      
      self.speed = 1.8
      self.rotation_speed = 60
      
      self.followCharacterCamera = FollowCharacterCamera(self.player)

    def update(self):      
      self.movement()
      self.followCharacterCamera.update()
      
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
