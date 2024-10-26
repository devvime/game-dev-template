from ursina import *
from Core.Physic import PhysicsEntity

class Player(PhysicsEntity):
    def __init__(self):
        super().__init__(
            model='cube',
            color=color.orange,
            collider='box',
            position=(0, 1, 0)
        )

    def update(self):
        self.update_physics()
        self.rotate_player()
        self.handle_movement()

    def rotate_player(self):
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

    def handle_movement(self):
        if held_keys['w']:
            self.move_forward()
        if held_keys['s']:
            self.move_backward()
        if held_keys['space']:
            self.jump()
