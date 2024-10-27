from ursina import *

class SlowParent(Entity):
    def __init__(self, parent_entity, lag=0.1, **kwargs):
        super().__init__(**kwargs)
        self.parent_entity = parent_entity
        self.lag = lag
        self.target_position = self.parent_entity.position

    def update(self):
        self.target_position = lerp(self.target_position, self.parent_entity.position, self.lag)
        self.position = self.target_position

if __name__ == '__main__':
    app = Ursina()

    # Criar o objeto que a câmera vai seguir
    player = Entity(model='cube', color=color.red, scale=(2, 2, 2))

    # Definir a câmera como uma instância de SlowParent
    camera_entity = SlowParent(parent_entity=player, lag=0.1)
    camera_entity.add_script(SmoothFollow(target=player, offset=(0, 5, -10), speed=4))

    def update():
        # Movimentar o player com as teclas W, A, S, D
        if held_keys['w']:
            player.y += time.dt * 5
        if held_keys['s']:
            player.y -= time.dt * 5
        if held_keys['a']:
            player.x -= time.dt * 5
        if held_keys['d']:
            player.x += time.dt * 5

    app.run()
