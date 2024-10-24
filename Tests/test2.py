from ursina import *
import pybullet as p
import pybullet_data
import math

# Definir a variável global para o cliente de física
physics_client = None

class PhysicsEntity(Entity):
    def __init__(self, model='cube', position=(0, 0, 0), mass=1, **kwargs):
        super().__init__(model=model, position=position, **kwargs)
        
        global physics_client  # Acessar a variável global
        # Inicializar o cliente de física do PyBullet
        if physics_client is None:
            physics_client = p.connect(p.DIRECT)
            p.setGravity(0, -100, 0, physicsClientId=physics_client)
            p.setAdditionalSearchPath(pybullet_data.getDataPath())
        
        # Criar a forma de colisão e o corpo rígido
        self.collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5], physicsClientId=physics_client)
        self.body = p.createMultiBody(
            baseMass=mass,
            baseCollisionShapeIndex=self.collision_shape,
            basePosition=position,
            physicsClientId=physics_client
        )

    def update(self):
        # Sincroniza a posição e rotação com o PyBullet
        pos, orn = p.getBasePositionAndOrientation(self.body, physicsClientId=physics_client)
        self.position = Vec3(pos)
        
        # Converter o quaternion para ângulos de Euler
        euler = p.getEulerFromQuaternion(orn)
        self.rotation = Vec3(math.degrees(euler[0]), math.degrees(euler[1]), math.degrees(euler[2]))

    def apply_force(self, force, position=None):
        p.applyExternalForce(self.body, -1, force, position if position else (0, 0, 0), p.WORLD_FRAME, physicsClientId=physics_client)

class Player(PhysicsEntity):
    def __init__(self):
        super().__init__(model='cube', position=(0, 2, 0), mass=1, color=color.orange)
        self.speed = 5
        self.jump_height = 5

    def update(self):
        super().update()  # Chama a atualização da classe base
        
        # Movimentação básica com W, A, S, D
        if held_keys['w']:
            self.apply_force((0, 0, -self.speed))
        if held_keys['s']:
            self.apply_force((0, 0, self.speed))
        if held_keys['a']:
            self.apply_force((-self.speed, 0, 0))
        if held_keys['d']:
            self.apply_force((self.speed, 0, 0))
        
        # Pular
        if held_keys['space']:
            self.apply_force((0, self.jump_height, 0))

def update():
    p.stepSimulation(physics_client)  # Agora pode acessar a variável global

app = Ursina(borderless=False)

# Criar o chão visual na Ursina
ground = PhysicsEntity(model='plane', scale=(10, 1, 10), position=(0, 0, 0), texture='grass', collider='box', mass=0)

# Instanciar o player
player = Player()

EditorCamera()

# Chamar a simulação do PyBullet a cada frame
app.run()
