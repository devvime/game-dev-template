from ursina import *
from direct.actor.Actor import Actor
import random

from Core.Physic.character_controller import CharacterController

class PlayerCharacter(Entity):
    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        
        self.bindKeys()
        
        self.player_entity = Entity(scale=1.8, position=(0,-1.6,0), rotation=(0,-180,0))
        
        self.player_actor = Actor("../Assets/Models/Player/player.glb")
        self.player_actor.reparentTo(self.player_entity)
        self.player_actor_anims = ['idle', 'walk', 'run', 'jump', 'attack1', 'attack2', 'attack3', 'attack4', 'hit', 'death']
        
        self.player = CharacterController(world, self.player_entity, radius=0.8, height=4.95)        
        self.player.jump_speed = 6
        
        self.speed = 1.8
        self.rotation_speed = 180
        self.lastDir = ''
        self.isWalking = False
        self.isRunning = False
        self.isJumping = False
        self.isAttaking = False
        self.isDead = False
        self.isArmed = False
        self.life = 100
        
        self.cameraFollowConfig()
        self.loopAnim('idle')
        
    def bindKeys(self):
        input_handler.bind('w', 'forward')
        input_handler.bind('s', 'backward')
        input_handler.bind('a', 'left')
        input_handler.bind('d', 'right')
        input_handler.bind('space', 'jump')
        input_handler.bind('shift', 'run')
        input_handler.bind('left mouse down', 'attack')

    def update(self):      
        self.movement()
        self.cameraFollow()
      
    def input(self, key):
        if key == 'run':
            self.speed = self.speed * 2
            self.isRunning = True
        
        if key == 'run up':
            self.speed = self.speed / 2
            self.isRunning = False
        
        if key == 'jump':
            if self.isAttaking: return
            self.isJumping = True
            self.loopAnim('jump')
            invoke(self.jump, delay=0.1)
            invoke(self.stopJump, delay=0.7)
            
        if key == 'attack':
            self.attack()
                
        self.animation(key)

    def movement(self):
        if self.isAttaking: return
        
        self.player.move((0, 0, 0), True)
                
        if held_keys['forward'] or held_keys['backward'] or held_keys['left'] or held_keys['right']:
            self.isWalking = True
            self.player.move((0, 0, self.speed), True)
        else:
            self.isWalking = False
        
        if held_keys['backward']:
            if (self.lastDir == 'left'):
                self.player.rotate(-self.rotation_speed)
            if (self.lastDir == 'right'):
                self.player.rotate(self.rotation_speed)
                
        if held_keys['left']:
            self.player.rotate(-self.rotation_speed)
            self.lastDir = 'left'
        
        if held_keys['right']:
            self.player.rotate(self.rotation_speed)
            self.lastDir = 'right'
            
    def jump(self):
        self.player.jump()
        
    def stopJump(self):
        self.isJumping = False
        if self.isWalking and not self.isRunning:
            self.loopAnim('walk')
        elif self.isRunning:
            self.loopAnim('run')
        else:
            self.loopAnim('idle')
    
    def attack(self):
        attackList = ['attack1', 'attack2', 'attack3', 'attack4']        
        if not self.isJumping and not self.isAttaking:
            self.isAttaking = True
            self.player.move((0, 0, 0), True)
            currentAttack = random.choice(attackList)
            self.loopAnim(currentAttack)
            invoke(self.stopAttack, delay=2.1)
    
    def stopAttack(self):
        self.isAttaking = False
        self.movement()
        self.animation(None)
    
    def animation(self, key):
        if held_keys['forward'] or held_keys['backward'] or held_keys['left'] or held_keys['right']:
            if self.isRunning:
                if not self.player_actor.getAnimControl('run').isPlaying() and not self.isJumping and not self.isAttaking:
                    self.loopAnim('run')
            else:
                if (not self.player_actor.getAnimControl('walk').isPlaying() and not self.isJumping and not self.isAttaking):
                    self.loopAnim('walk')   
        else:
            if not self.isJumping and not self.isAttaking:
                self.loopAnim('idle')
                self.player_actor.disableBlend()
            
    def loopAnim(self, name):        
        # for anim in self.player_actor_anims:
        self.player_actor.stop()        
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
