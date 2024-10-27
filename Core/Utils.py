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
        
class FollowCharacterCamera:
    def __init__(self, parent_entity, offset=Vec3(0, 4, -5), lag=0.02, **kwargs):
        self.parent_entity = parent_entity
        self.offset = offset
        self.lag = lag
        self.target_position = Vec3(self.parent_entity.np.getPos() + self.offset)

    def update(self):
        self.target_position = Vec3(lerp(self.target_position, Vec3(self.parent_entity.np.getPos() + self.offset), self.lag))
        camera.position = self.target_position