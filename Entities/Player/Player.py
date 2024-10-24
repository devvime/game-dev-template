from ursina import *

class Player(Entity):
    def __init__(self):
        super().__init__(
            model='cube',    
            color=color.orange,
            collider='box',  
            position=(0, 0.5, 0),  # Levantar o player pela metade da altura do cubo (0.5)
        )
        self.speed = 5
        self.rotation_speed = 100
        self.velocity_y = 0
        self.jump_height = 0.2
        self.gravity = 1

    def update(self):
        # Rotacionar o player com as teclas 'A' e 'D'
        if held_keys['a']:
          if held_keys['s']:
            self.rotation_y += self.rotation_speed * time.dt
          else:
            self.rotation_y -= self.rotation_speed * time.dt
        if held_keys['d']:
          if held_keys['s']:
            self.rotation_y -= self.rotation_speed * time.dt
          else:
            self.rotation_y += self.rotation_speed * time.dt

        # Mover o player na direção em que ele está virado (baseado na rotação)
        forward_direction = self.forward * self.speed * time.dt
        if held_keys['w']:
            self.position += forward_direction
        if held_keys['s']:
            self.position -= forward_direction

        # Aplicar gravidade
        self.velocity_y -= self.gravity * time.dt
        self.y += self.velocity_y
        if self.intersects().hit:
            self.velocity_y = 0
            self.y = 0.5  # Ajustar a posição para garantir que o player fique totalmente acima do chão

        # Saltar
        if held_keys['space'] and self.y <= 0.5:
            self.velocity_y = self.jump_height