from ursina import *

class PhysicsEntity(Entity):
    def __init__(self, mass=1, pushable=False, **kwargs):
        super().__init__(**kwargs)
        self.gravity = 1
        self.velocity_y = 0
        self.jump_height = 0.2
        self.walk_speed = 2
        self.run_speed = 4
        self.rotation_speed = 100
        self.pushable = pushable  # Atributo para determinar se a entidade pode ser empurrada
        self.mass = mass  # Massa do objeto

    def update_physics(self):
        self.apply_gravity()
        self.check_ground_collision()

    def apply_gravity(self):
        self.velocity_y -= self.gravity * time.dt / 2
        self.y += self.velocity_y

    def check_ground_collision(self):
        ray = raycast(self.world_position, self.down, ignore=[self], distance=0.6)
        if ray.hit:
            self.velocity_y = 0
            self.y = ray.world_point.y + 0.5

    def move(self, direction):
        speed = self.run_speed if held_keys['shift'] else self.walk_speed
        
        # Ajustar a velocidade se estiver empurrando um objeto
        if self.is_pushing():
            speed *= (1 - (self.current_pushable.mass / 10))  # Reduzir a velocidade baseada na massa

        movement_direction = direction * speed * time.dt

        # Checar colisões em múltiplas direções
        if not self.check_collisions(movement_direction):
            self.position += movement_direction

            # Tentar empurrar objetos colididos
            self.push_objects(movement_direction)

    def move_forward(self):
        self.move(self.forward)

    def move_backward(self):
        self.move(-self.forward)

    def jump(self):
        if self.is_on_ground():  # Verificar se a entidade está no chão
            self.velocity_y = self.jump_height

    def check_collisions(self, movement_direction):
        # Verificando colisões para cada direção
        for offset in [Vec3(0.5, 0, 0), Vec3(-0.5, 0, 0), Vec3(0, 0, 0.5), Vec3(0, 0, -0.5)]:
            ray = raycast(self.position + offset, movement_direction, ignore=[self], distance=movement_direction.length() + 0.6)
            if ray.hit:
                # Ajustar a posição para evitar que entre no objeto
                self.position -= movement_direction * (movement_direction.length() + ray.distance)
                return True
        return False

    def push_objects(self, movement_direction):
        # Verificar se há objetos que podem ser empurrados
        ray = raycast(self.position + self.forward * 0.5, self.forward, ignore=[self], distance=0.7)
        if ray.hit and hasattr(ray.entity, 'pushable') and ray.entity.pushable:
            self.current_pushable = ray.entity  # Armazenar o objeto atual que está sendo empurrado
            
            # Calcular a direção de empurrão com base no movimento do player
            push_direction = movement_direction.normalized()
            # Suavizar o movimento de empurrar, mantendo a posição Y do objeto
            ray.entity.position += Vec3(push_direction.x, 0, push_direction.z) * time.dt * (self.run_speed * 2 / ray.entity.mass)  # Não alterar a posição Y
            
            # Ajustar a posição do player para evitar que entre no objeto
            if push_direction.length() > 0:
                overlap_distance = (self.current_pushable.scale_x / 2) + (self.scale_x / 2)
                if distance(self.position, ray.entity.position) < overlap_distance:  # Usando a função distance correta
                    self.position -= push_direction * (overlap_distance - distance(self.position, ray.entity.position))

            # Empurrar objetos próximos
            self.check_nearby_pushable_objects(ray.entity)

        else:
            self.current_pushable = None  # Resetar se não houver objeto sendo empurrado

    def check_nearby_pushable_objects(self, pushed_object):
        # Verifica se há objetos próximos que também podem ser empurrados
        nearby_objects = [obj for obj in self.get_pushable_objects() if obj != pushed_object]

        for obj in nearby_objects:
            if distance(pushed_object.position, obj.position) < 1.0:  # Ajuste a distância conforme necessário
                # Calcular a direção para empurrar o objeto
                direction_to_obj = (obj.position - pushed_object.position).normalized()
                overlap_distance = (pushed_object.scale_x / 2) + (obj.scale_x / 2)

                # Ajustar a posição do objeto empurrado
                if distance(pushed_object.position, obj.position) < overlap_distance:
                    obj.position += direction_to_obj * (overlap_distance - distance(pushed_object.position, obj.position))

    def get_pushable_objects(self):
        # Retorna uma lista de todos os objetos empurráveis na cena
        return [entity for entity in scene.entities if hasattr(entity, 'pushable') and entity.pushable]

    def is_on_ground(self):
        ray = raycast(self.world_position, self.down, ignore=[self], distance=0.6)
        return ray.hit

    def is_pushing(self):
        return hasattr(self, 'current_pushable') and self.current_pushable is not None

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