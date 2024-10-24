from ursina import *
import pybullet as p
import pybullet_data
import math

class Player(Entity):
    def __init__(self, physics_client):
        super().__init__(
            model='cube',
            color=color.orange,
            position=(0, 2, 0)  # Inicialmente acima do chão
        )
        self.speed = 5
        self.jump_height = 5
        self.physics_client = physics_client

        # Criação do corpo rígido (rigid body) no PyBullet
        self.player_collider = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5], physicsClientId=self.physics_client)
        self.player_body = p.createMultiBody(
            baseMass=1,  # Massa do corpo, define se será afetado por física
            baseCollisionShapeIndex=self.player_collider,
            basePosition=self.position,
            physicsClientId=self.physics_client
        )
        p.changeDynamics(self.player_body, -1, lateralFriction=1)

    def update(self):
        # Sincroniza o movimento e rotação do PyBullet com a Ursina
        pos, orn = p.getBasePositionAndOrientation(self.player_body, physicsClientId=self.physics_client)
        self.position = Vec3(pos)  # Atualiza a posição do player na Ursina

        # Converter o quaternion para ângulos de Euler
        euler = p.getEulerFromQuaternion(orn)
        self.rotation = Vec3(math.degrees(euler[0]), math.degrees(euler[1]), math.degrees(euler[2]))  # Atualiza a rotação do player

        # Movimentação básica com W, A, S, D
        if held_keys['w']:
            p.applyExternalForce(self.player_body, -1, (0, 0, -self.speed), (0, 0, 0), p.WORLD_FRAME, physicsClientId=self.physics_client)
        if held_keys['s']:
            p.applyExternalForce(self.player_body, -1, (0, 0, self.speed), (0, 0, 0), p.WORLD_FRAME, physicsClientId=self.physics_client)
        if held_keys['a']:
            p.applyExternalForce(self.player_body, -1, (-self.speed, 0, 0), (0, 0, 0), p.WORLD_FRAME, physicsClientId=self.physics_client)
        if held_keys['d']:
            p.applyExternalForce(self.player_body, -1, (self.speed, 0, 0), (0, 0, 0), p.WORLD_FRAME, physicsClientId=self.physics_client)

        # Pular (aplica força para cima)
        if held_keys['space']:
            p.applyExternalForce(self.player_body, -1, (0, self.jump_height, 0), (0, 0, 0), p.WORLD_FRAME, physicsClientId=self.physics_client)

def update():
    p.stepSimulation(physics_client)

app = Ursina(borderless=False)

# Inicialização do mundo de física no PyBullet
physics_client = p.connect(p.DIRECT)  # Alternativamente, use p.GUI para uma visualização
p.setGravity(0, -9.81, 0, physicsClientId=physics_client)
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # Caminho para modelos padrão do PyBullet

# Criação do chão
ground_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=physics_client)
ground_body = p.createMultiBody(0, ground_shape, physicsClientId=physics_client)  # Massa 0 significa que é estático

# Criar o chão visual na Ursina
ground = Entity(model='plane', scale=(10, 1, 10), color=color.green)

# Instanciar o player
player = Player(physics_client)

# Chamar a simulação do PyBullet a cada frame
app.run()
