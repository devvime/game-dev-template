# Game dev template for Ursina Engine

### Installing dependencies

```bash
pip install -r requirements.txt
```

### Directory structure

```
/my_game
│
├── /Assets
│   ├── /Models          # 3D Models (formato .obj, .gltf, etc)
│   ├── /Textures        # Textures images
│   ├── /Audio           # Sond files
│
├── /Core                # Game scenes classes
│   ├── Scene.py
│   ├── SceneData.py
│   ├── SceneManager.py
│
├── /Entities            # Game object classes
│   ├── Player.py
│   ├── Enemy.py
│   ├── Environment.py
│
├── /Scenes              # Game scenes, each in a separate file
│   ├── Menu.py
│   ├── Game.py
│
├── /Config              # Configuration files
│   ├── Settings.json
│
├── main.py              # Main game file
```

### Default Scene

```python
from ursina import *
from ursina.shaders import lit_with_shadows_shader
from Core.Scene import Scene

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        
        self.environment()
        
        self.player = Entity(model='cube', texture='white_cube', position=(0, 10, 0), shader=lit_with_shadows_shader)
        self.ground = Entity(model='plane', scale=(10, 1, 10), texture='white_cube', collider='box', shader=lit_with_shadows_shader)
        
        # Add elements to the scene element list
        self.addElements()
        
    def addElements(self):
        self.add_element([self.editorCamera, self.sky, self.light, self.player, self.ground])
        
    def update(self):
        pass
        
    def environment(self):
        self.editorCamera = EditorCamera()
        self.sky = Sky()        
        
        self.light = DirectionalLight(shadows=True)
        self.light.look_at(Vec3(1,-1,1))

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")
```

Add all scene elements using the self.add_element() parameter