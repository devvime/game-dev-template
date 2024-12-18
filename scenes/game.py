from ursina import *
from ursina.shaders.screenspace_shaders.pixelation_shader import pixelation_shader

from core.physic import Debugger, BoxCollider, MeshCollider
from panda3d.bullet import BulletWorld

from core.scene import Scene

from entities.player.player_character import PlayerCharacter

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
            position=(0, -0.5, 0), 
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
            self.player.player_entity,
            self.player.player_actor,
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
        self.sky = Sky(texture='sky_sunset')
        
        self.light = DirectionalLight(shadows=True)
        self.light.look_at(Vec3(1,-1,1))
        
        # camera.shader = Shader(
        #     fragment='''
        #     #version 150

        #     uniform sampler2D tex;
        #     in vec2 window_size;
        #     in vec2 uv;
        #     out vec4 color;


        #     void main() {
        #         float Pixels = 1600.0;
        #         float dx = 2.0 * (1.0 / Pixels);
        #         float dy = 4.0 * (1.0 / Pixels);
        #         vec2 new_uv = vec2(dx * floor(uv.x / dx), dy * floor(uv.y / dy));
        #         color = texture(tex, new_uv);
        #     }
        #     ''')

    def enable(self):
        super().enable()

    def disable(self):
        super().disable()