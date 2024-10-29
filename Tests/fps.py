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

        # Posiciona a entidade no chão, se ela começar dentro do terreno
        self.initialize_position()

    def initialize_position(self):
        if self.gravity:
            ray = raycast(self.entity.world_position + (0, self.entity.height, 0), self.entity.down, 
                          traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                self.entity.y = ray.world_point.y

    def apply_gravity(self):
        if self.gravity:
            ray = raycast(self.entity.world_position + (0, self.entity.height, 0), self.entity.down, 
                          traverse_target=self.traverse_target, ignore=self.ignore_list)

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


class FirstPersonController(Entity):
    def __init__(self, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=0.008, rotation_z=45)
        super().__init__()
        self.speed = 5
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)
        self.mouse_sensitivity = Vec2(40, 40)

        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 90
        mouse.locked = True

        self.physics = PhysicsComponent(entity=self)
        self.traverse_target = scene
        self.ignore_list = [self]

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 90)

        direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
        ).normalized()

        feet_ray = raycast(self.position + Vec3(0, 0.5, 0), direction, traverse_target=self.traverse_target, 
                           ignore=self.ignore_list, distance=0.5, debug=False)
        head_ray = raycast(self.position + Vec3(0, self.height - 0.1, 0), direction, traverse_target=self.traverse_target, 
                           ignore=self.ignore_list, distance=0.5, debug=False)

        if not feet_ray.hit and not head_ray.hit:
            move_amount = direction * time.dt * self.speed

            for axis, direction in zip([Vec3(1, 0, 0), Vec3(-1, 0, 0), Vec3(0, 0, 1), Vec3(0, 0, -1)], [0, 0, 2, 2]):
                ray = raycast(self.position + Vec3(0, 1, 0), axis, distance=0.5, traverse_target=self.traverse_target, 
                              ignore=self.ignore_list)
                if ray.hit:
                    move_amount[direction] = min(move_amount[direction], 0) if axis[direction] > 0 else max(move_amount[direction], 0)

            self.position += move_amount

        self.physics.apply_gravity()

    def input(self, key):
        if key == 'space':
            self.physics.jump()


if __name__ == '__main__':
    from ursina.prefabs.first_person_controller import FirstPersonController
    window.vsync = False
    app = Ursina(borderless=False)
    ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)

    player = FirstPersonController(y=2, origin_y=-.5)
    player.gun = None

    gun = Button(parent=scene, model='cube', color=color.blue, origin_y=-.5, position=(3,0,3), collider='box', scale=(.2,.2,1))
    def get_gun():
        gun.parent = camera
        gun.position = Vec3(.5,0,.5)
        player.gun = gun
    gun.on_click = get_gun

    gun_2 = duplicate(gun, z=7, x=8)
    slope = Entity(model='cube', collider='box', position=(0,0,8), scale=6, rotation=(45,0,0), texture='brick', texture_scale=(8,8))
    slope = Entity(model='cube', collider='box', position=(5,0,10), scale=6, rotation=(80,0,0), texture='brick', texture_scale=(8,8))

    hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
    hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)

    def input(key):
        if key == 'left mouse down' and player.gun:
            gun.blink(color.orange)
            bullet = Entity(parent=gun, model='cube', scale=.1, color=color.black)
            bullet.world_parent = scene
            bullet.animate_position(bullet.position + (bullet.forward * 50), curve=curve.linear, duration=1)
            destroy(bullet, delay=1)

    app.run()
