# Game dev template for Ursina Engine

### Installing dependencies

```bash
pip install ursina
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

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.player = Entity(model='cube', color=color.azure, position=(0, 1, 0))
        self.ground = Entity(model='plane', scale=(10, 1, 10), texture='white_cube', collider='box')
        
        # Add elements to the scene element list
        self.add_element(self.player)
        self.add_element(self.ground)

    def enable(self):
        super().enable()
        print("Game Scene enabled!")

    def disable(self):
        super().disable()
        print("Game Scene disabled!")
```

Add all scene elements using the self.add_element() parameter