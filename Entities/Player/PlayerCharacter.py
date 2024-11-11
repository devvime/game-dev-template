from ursina import *
from direct.actor.Actor import Actor

from Core.Physic.character_controller import CharacterController

class PlayerCharacter(Entity):
    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        
        self.player_skin = Entity(scale=1.8, position=(0,-1.6,0), rotation=(0,-180,0))
        
        self.player_actor = Actor("../Assets/Models/Player/player.glb")
        self.player_actor.reparentTo(self.player_skin)
        self.player_actor_anims = ['idle', 'walk', 'run', 'jump']
        
        self.player = CharacterController(world, self.player_skin, radius=0.8, height=4.95)        
        self.player.jump_speed = 6
        
        self.speed = 1.8
        self.rotation_speed = 180
        self.lastDir = ''
        self.isWalking = False
        self.isRunning = False
        self.isJumping = False
        
        self.cameraFollowConfig()
        self.loopAnim('idle')

    def update(self):      
        self.movement()
        self.cameraFollow()
      
    def input(self, key):
        if key == 'shift':
            self.speed = self.speed * 2
            self.isRunning = True
        
        if key == 'shift up':
            self.speed = self.speed / 2
            self.isRunning = False
        
        if key == 'space':
            self.isJumping = True
            self.loopAnim('jump')
            invoke(self.jump, delay=0.8)
            invoke(self.stopJump, delay=2)
                
        self.animation(key)

    def movement(self):
        self.player.move((0, 0, 0), True)
                
        if held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']:
            self.isWalking = True
            self.player.move((0, 0, self.speed), True)
        else:
            self.isWalking = False
        
        if held_keys['s']:
            if (self.lastDir == 'left'):
                self.player.rotate(-self.rotation_speed)
            if (self.lastDir == 'right'):
                self.player.rotate(self.rotation_speed)
                
        if held_keys['a']:
            self.player.rotate(-self.rotation_speed)
            self.lastDir = 'left'
        
        if held_keys['d']:
            self.player.rotate(self.rotation_speed)
            self.lastDir = 'right'
            
    def jump(self):
        self.player.jump()
        
    def stopJump(self):
        self.isJumping = False
        if self.isWalking:
            self.loopAnim('walk')
        elif self.isRunning:
            self.loopAnim('run')
        else:
            self.loopAnim('idle')
            
    def animation(self, key):
        if held_keys['w'] or held_keys['a'] or held_keys['d'] or held_keys['s']:
            if self.isRunning:
                if not self.player_actor.getAnimControl('run').isPlaying() and not self.isJumping:
                    self.loopAnim('run')
            else:
                if (not self.player_actor.getAnimControl('walk').isPlaying() and not self.isJumping):
                    self.loopAnim('walk')   
        else:
            if not self.isJumping:
                self.loopAnim('idle')
                self.player_actor.disableBlend()
            
    def loopAnim(self, name):
        for anim in self.player_actor_anims:
            self.player_actor.stop(anim)
                      
        self.player_actor.loop(name)
            
    def cameraFollowConfig(self):
        camera.position = (0, 1, -1.5)
        
        self.playerPivot = Entity(model='sphere', scale=3)
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
