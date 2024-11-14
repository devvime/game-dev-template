from ursina import *
from direct.actor.Actor import Actor
from panda3d.core import *
import random

from Core.Physic.character_controller import CharacterController

class PlayerCharacter(Entity):
    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        
        self.bindKeys()
        
        self.player_entity = Entity()
        self.player = CharacterController(world, self.player_entity, radius=0.5, height=2.7)
        
        self.player_actor = Actor("../Assets/Models/Player/player.glb")
        self.player_actor.reparentTo(scene)
        
        self.player_actor_anims = ['idle', 'walk', 'run', 'jump', 'attack1', 'attack2', 'attack3', 'attack4', 'hit', 'death']
             
        self.speed = 1.8
        self.player.jump_speed = 6
        self.rotation_speed = 210
        self.lastDir = ''
        self.isWalking = False
        self.isRunning = False
        self.isJumping = False
        self.isAttaking = False
        self.isDead = False
        self.isArmed = False
        self.life = 100
        self.cameraPosition = Vec3(0, 0.4, -0.6)
        
        self.playerBat = self.player_actor.find("**/Bat")
        # self.playerBat.hide()
        
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
        self.parentActor()
      
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
            invoke(self.jump, delay=0.1)
            
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
        self.loopAnim('jump')
        invoke(self.stopJump, delay=0.7)
        
    def stopJump(self):
        self.isJumping = False
        if self.isWalking and not self.isRunning:
            self.loopAnim('walk')
        elif self.isRunning:
            self.loopAnim('run')
        else:
            self.loopAnim('idle')
    
    def attack(self):
        attackList = [
            { 'name': 'attack1', 'time': 1.9, 'playRate': 1.5 }, 
            { 'name': 'attack2', 'time': 1.7, 'playRate': 1.5 }, 
            { 'name': 'attack3', 'time': 2, 'playRate': 1.5 }, 
            { 'name': 'attack4', 'time': 1.6, 'playRate': 1.5 }
        ]
        camera.animate_position(Vec3(0.3, 0.5, -0.8), duration=1, curve=curve.in_sine)
        if not self.isJumping and not self.isAttaking:
            self.isAttaking = True
            self.player.move((0, 0, 0), True)
            currentAttack = random.choice(attackList)
            self.loopAnim(currentAttack['name'], currentAttack['playRate'])
            invoke(self.stopAttack, delay=currentAttack['time'])
    
    def stopAttack(self):
        self.isAttaking = False
        self.movement()
        self.animation(None)
        invoke(self.cameraAnimationReturn, delay=0.5)
        
    def cameraAnimationReturn(self):
        camera.animate_position(self.cameraPosition, duration=2, curve=curve.out_sine)
    
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
            
    def loopAnim(self, name, playRate = 1):
        self.player_actor.stop()
        self.player_actor.setPlayRate(playRate, name)
        self.player_actor.loop(name)
            
    def cameraFollowConfig(self):
        camera.position = self.cameraPosition
        
        self.playerPivot = Entity(model='sphere', scale=3)
        self.playerPivot.visible_self = False
        
        self.lag = 0.2
        self.camera_target_position = Vec3(self.player.np.getPos())
      
    def cameraFollow(self):
        camera.rotation_x = 10
        camera.fov = 120
        camera.parent = self.playerPivot
        
        self.camera_target_position = Vec3(lerp(self.camera_target_position, Vec3(self.player.np.getPos()), self.lag))
        self.playerPivot.position = self.camera_target_position      
        self.playerPivot.rotation_y = - Vec3(self.player.np.getHpr()).x
        
    def parentActor(self):
        playerPos = self.player.np.getPos()
        playerRot = self.player.np.getHpr()
        self.player_actor.setPos(playerPos.x, playerPos.y - 0.89, playerPos.z)
        self.player_actor.setHpr(playerRot.x - 180, playerRot.y, playerRot.z)