from ursina import *
from ursina import EditorCamera

class Car(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'  # Substitua pelo seu modelo 3D de carro
        self.texture = 'white_cube'
        self.scale = (1.5, 0.5, 3)  # Um formato simplificado para o carro
        self.speed = 0
        self.max_speed = 20
        self.acceleration = 10
        self.friction = 1
        self.turn_speed = 60
        self.wheel_angle = 0
        self.velocity = Vec3(0, 0, 0)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        # Controles do jogador
        self.handle_input()
        # Atualização da física simples do carro
        self.apply_friction()
        self.move_car()

    def handle_input(self):
        # Acelerar (frente e ré)
        if held_keys['w']:
            self.speed += self.acceleration * time.dt
        elif held_keys['s']:
            self.speed -= self.acceleration * time.dt

        # Limitar a velocidade máxima
        self.speed = clamp(self.speed, -self.max_speed, self.max_speed)

        # Girar o carro
        if held_keys['a']:
            self.wheel_angle -= (self.turn_speed / 2) * (time.dt * 8)
        elif held_keys['d']:
            self.wheel_angle += (self.turn_speed / 2) * (time.dt * 8)
        else:
            self.wheel_angle = lerp(self.wheel_angle, 0, time.dt * 12)  # Volta ao centro

        # Aplicar rotação à medida que o carro se move
        if self.speed != 0:
            self.rotation_y += self.wheel_angle * time.dt * (self.speed / self.max_speed)

    def apply_friction(self):
        # Aplicar fricção para reduzir a velocidade gradualmente quando não acelerar
        if not held_keys['w'] and not held_keys['s']:
            self.speed = lerp(self.speed, 0, self.friction * time.dt)

    def move_car(self):
        # Mover o carro na direção que ele está virado
        forward = Vec3(0, 0, 1)
        self.velocity = self.forward * self.speed * time.dt
        self.position += self.velocity

class Game(Ursina):
    def __init__(self):
        super().__init__(borderless=False)
        self.car = Car(position=(0, 0, 0))
        self.ground = Entity(model='plane', texture='grass', scale=(100, 1, 100))
        EditorCamera()

if __name__ == '__main__':
    game = Game()
    game.run()
