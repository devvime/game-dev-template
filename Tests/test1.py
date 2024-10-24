from ursina import *
import pybullet as p
import pybullet_data
import math

# Definir a variável global para o cliente de física
physics_client = None

class PhysicsEntity(Entity):
    def __init__(self, model='cube', position=(0, 0, 0), mass=1, collision_shape='box', **kwargs):
        super().__init__(model=model, position=position, **kwargs)
        
        global physics_client
        if physics_client is None:
            physics_client = p.connect(p.DIRECT)
            p.setGravity(0, -200, 0, physicsClientId=physics_client)
            p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # Adicionar uma cápsula de colisão baseada na escala do objeto
        if collision_shape == 'capsule':
            radius = self.scale_x / 2  # Raio com base na largura do modelo
            height = self.scale_y - 2 * radius  # Altura do corpo, excluindo as extremidades arredondadas
            self.collision_shape = p.createCollisionShape(p.GEOM_CAPSULE, radius=radius, height=height, physicsClientId=physics_client)
        else:
            self.collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[self.scale_x / 2, self.scale_y / 2, self.scale_z / 2], physicsClientId=physics_client)

        # Criar corpo rígido
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
        
        euler = p.getEulerFromQuaternion(orn)
        self.rotation = Vec3(0, math.degrees(euler[1]), 0)  # Somente rotação no eixo Y

    def apply_force(self, force, position=None):
        p.applyExternalForce(self.body, -1, force, position if position else (0, 0, 0), p.WORLD_FRAME, physicsClientId=physics_client)

    def set_velocity(self, velocity):
        p.resetBaseVelocity(self.body, linearVelocity=velocity, physicsClientId=physics_client)

    def get_velocity(self):
        vel, _ = p.getBaseVelocity(self.body, physicsClientId=physics_client)
        return Vec3(vel)

class Player(PhysicsEntity):
    def __init__(self):
        super().__init__(model='cube', position=(0, 2, 0), mass=1, color=color.orange, scale=(1, 2, 1), collision_shape='capsule')
        self.speed = 15
        self.jump_height = 15
        self.grounded = False

    def update(self):
        super().update()

        # Checar se o player está no chão
        contact_points = p.getContactPoints(self.body, physicsClientId=physics_client)
        self.grounded = len(contact_points) > 0

        movement = Vec3(0, 0, 0)

        # Mover o player lateralmente com as teclas 'A' e 'D'
        if held_keys['a']:
            movement -= self.right * self.speed  # Mover para a esquerda
        if held_keys['d']:
            movement += self.right * self.speed  # Mover para a direita
        
        # Mover o player para frente e para trás com base na orientação
        if held_keys['w']:
            movement += self.forward * self.speed
        if held_keys['s']:
            movement -= self.forward * self.speed
        
        # Obter a velocidade atual para manter o movimento suave
        current_velocity = self.get_velocity()

        # Aplicar a nova velocidade
        self.set_velocity((movement.x, current_velocity.y, movement.z))

        # Saltar
        if self.grounded and held_keys['space']:
            self.set_velocity((movement.x, self.jump_height, movement.z))

def update():
    p.stepSimulation(physics_client)

app = Ursina(borderless=False)

ground = PhysicsEntity(model='plane', scale=(10, 1, 10), position=(0, 0, 0), texture='grass', mass=0)

player = Player()

EditorCamera()

app.run()
