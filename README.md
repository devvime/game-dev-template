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
from Core.Scene import Scene

from Entities.Player.Player import Player
from Entities.Box.Box import Box

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        
        self.environment()
        
        self.player = Player()
        
        self.ground = Entity(
            model='plane', 
            scale=(30,1,30), 
            color=color.yellow.tint(-.2), 
            texture='white_cube', 
            texture_scale=(30,30), 
            collider='box'
        )
        
        self.obstacle = Box(mass=1)
        self.obstacle.position = (2, 5, 5)
        
        self.obstacle2 = Box(mass=5, pushable=True)
        self.obstacle2.position = (4, 10, 3)
        
        self.obstacle3 = Entity(model='cube', scale=(1, 1, 1), color=color.red, position=(6, 0.5, 0), collider='box')
        
        # Add elements to the scene element list
        self.addElements()
        
    def addElements(self):
        self.add_element(
            [
                self.editorCamera, 
                self.sky, 
                self.light, 
                self.player, 
                self.ground, 
                self.obstacle, 
                self.obstacle2, 
                self.obstacle3
            ]
        )
        
    def update(self):
        pass
    
    def input(self, key):
        pass
        
    def environment(self):
        self.editorCamera = EditorCamera()
        self.sky = Sky()        
        
        camera.position = (0, 5, -10)
        camera.rotation_x = -90
        camera.fov = 120
        
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