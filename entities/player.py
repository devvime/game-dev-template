from ursina import Entity, Vec3

class Player(Entity):
    def __init__(self, position=Vec3(0, 0, 0)):
        super().__init__(
            model='assets/models/player.obj',
            texture='assets/textures/player_texture.png',
            position=position
        )
        self.speed = 5

    def update(self):
        self.move()

    def move(self):
        if held_keys['w']:
            self.position += Vec3(0, 0, self.speed * time.dt)
        # Outros controles...
