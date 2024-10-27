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

    # Criar o objeto pai
    parent_entity = Entity(model='cube', color=color.red, scale=(2, 2, 2))

    # Criar o objeto filho com o script de SlowParent
    slow_parent_entity = SlowParent(parent_entity, lag=0.1, model='cube', color=color.blue, scale=(1, 1, 1), position=(0, 2, 0))

    def update():
        # Movimentar o objeto pai com as teclas W, A, S, D
        if held_keys['w']:
            parent_entity.y += time.dt * 5
        if held_keys['s']:
            parent_entity.y -= time.dt * 5
        if held_keys['a']:
            parent_entity.x -= time.dt * 5
        if held_keys['d']:
            parent_entity.x += time.dt * 5

    app.run()
