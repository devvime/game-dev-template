from ursina import *
app = Ursina()
e = Entity(
          model='cube', 
          position=(0, -3, 0), 
          scale=(200, 0.1, 200),
          color=color.gray,
          texture='grass'
        )
EditorCamera()
s = Sky()
s.color = color.orange

camera.fov = 120

def input(key):
    if key == 'l':
        for e in scene.entities:
            print(e.name)

    if key == 'd':
        scene.clear()
        Entity(model='cube')

scene.fog_color = color.orange   # sets fog color
scene.fog_density = .1    # sets exponential density
scene.fog_density = (50, 200)

app.run()