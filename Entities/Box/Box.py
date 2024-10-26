from ursina import *
from Core.Physic import PhysicsEntity

class Box(PhysicsEntity):
    def __init__(self, mass, pushable=True):
        super().__init__(
            model='cube',
            color=color.blue,
            collider='box',
            position=(2, 0.5, 0),
            pushable=pushable,  # Definindo que este objeto pode ser empurrado
            mass=mass  # Definindo a massa do objeto
        )
        
    def update(self):
      self.update_physics()
