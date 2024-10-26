from ursina import *

class PhysicsComponent:
    def __init__(self, entity, gravity=1, jump_height=2, jump_up_duration=0.5, fall_after=0.35):
        self.entity = entity
        self.gravity = gravity
        self.jump_height = jump_height
        self.jump_up_duration = jump_up_duration
        self.fall_after = fall_after
        self.grounded = False
        self.air_time = 0
        self.traverse_target = scene
        self.ignore_list = [self.entity]

        self.initialize_position()

    def initialize_position(self):
        if self.gravity:
            ray = raycast(
                self.entity.world_position + (0, self.entity.height, 0), 
                self.entity.down, 
                traverse_target=self.traverse_target, 
                ignore=self.ignore_list
            )
            if ray.hit:
                self.entity.y = ray.world_point.y

    def apply_gravity(self):
        if self.gravity:
            ray = raycast(
                self.entity.world_position + (0, self.entity.height, 0), 
                self.entity.down, 
                traverse_target=self.traverse_target, 
                ignore=self.ignore_list
            )

            if ray.distance <= self.entity.height + 0.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                if ray.world_normal.y > 0.7 and ray.world_point.y - self.entity.world_y < 0.5:
                    self.entity.y = ray.world_point[1]
            else:
                self.grounded = False
                self.entity.y -= min(self.air_time, ray.distance - 0.05) * time.dt * 100
                self.air_time += time.dt * 0.25 * self.gravity

    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.entity.animate_y(self.entity.y + self.jump_height, self.jump_up_duration, 
                              resolution=int(1 // time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)

    def start_fall(self):
        self.entity.y_animator.pause()

    def land(self):
        self.air_time = 0
        self.grounded = True