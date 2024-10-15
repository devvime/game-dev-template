### Installing dependencies

```bash
pip install ursina
```
### Directory structure

```
/my_game
│
├── /assets
│   ├── /models          # 3D Models (formato .obj, .gltf, etc)
│   ├── /textures        # Textures images
│   ├── /audio           # Sond files
│
├── /scenes              # Game scenes, each in a separate file
│   ├── main_menu.py
│   ├── game_scene.py
│   ├── settings_scene.py
│
├── /entities            # Game object classes
│   ├── player.py
│   ├── enemy.py
│   ├── environment.py
│
├── /config              # Configuration files
│   ├── settings.json
│
├── game.py              # Main game file
└── utils.py             # Utilities and auxiliary functions
```

### 1. **Main game file (game.py)**

This file will load the initial scene and manage transitions between scenes.

```python
from ursina import Ursina, window
from scenes.main_menu import MainMenu
from scenes.game_scene import GameScene
from scenes.settings_scene import SettingsScene

class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.title = 'Meu Jogo'
        window.borderless = False
        
        self.current_scene = None
        self.load_scene(MainMenu(self))
        
    def load_scene(self, scene_class):
        if self.current_scene:
            self.current_scene.disable()
        self.current_scene = scene_class
        self.current_scene.enable()

    def switch_scene(self, scene_name):
        scenes = {
            'menu': MainMenu,
            'game': GameScene,
            'settings': SettingsScene,
        }
        self.load_scene(scenes[scene_name](self))

if __name__ == '__main__':
    game = Game()
    game.run()
```

### 2. **Scenes (scenes/main_menu.py)**

Each scene will be a separate class, inheriting from `Entity`, which controls the scene's objects and events.

```python
from ursina import Entity, Text, Button
from utils import load_settings

class MainMenu(Entity):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.title = Text(text="Meu Jogo", scale=2, position=(0, 0.4))

        self.play_button = Button(text="Play", position=(0, 0.1), scale=(0.2, 0.1))
        self.play_button.on_click = self.start_game

        self.settings_button = Button(text="Settings", position=(0, -0.1), scale=(0.2, 0.1))
        self.settings_button.on_click = self.go_to_settings

        self.quit_button = Button(text="Quit", position=(0, -0.3), scale=(0.2, 0.1))
        self.quit_button.on_click = self.quit_game

    def start_game(self):
        self.game.switch_scene('game')

    def go_to_settings(self):
        self.game.switch_scene('settings')

    def quit_game(self):
        exit()
```

### 3. **Game Entities (entities/player.py)**

Objects such as the player and enemies must be encapsulated in specific classes.

```python
from ursina import Entity, Vec3

class Player(Entity):
    def __init__(self, position=Vec3(0, 0, 0)):
        super().__init__(
            model='assets/models/player.obj',
            texture='assets/textures/player_texture.png',
            position=position
        )
        self.speed = 5

    def update(self):
        self.move()

    def move(self):
        if held_keys['w']:
            self.position += Vec3(0, 0, self.speed * time.dt)
        # Outros controles...
```

### 4. **Settings (config/settings.json)**

Use JSON files to store settings like volume, difficulty, etc.

```json
{
  "volume": 0.5,
  "resolution": [1280, 720],
  "fullscreen": false
}
```

### 5. **Utility Functions (utils.py)**

Create helper functions to load data, apply settings, etc.

```python
import json

def load_settings():
    with open('config/settings.json', 'r') as f:
        return json.load(f)

def save_settings(settings):
    with open('config/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)
```

### Good Practices

1. **Modularity**: Separate each scene and entity into different files.
2. **Good naming practices**: Use clear names for classes, methods and variables.
3. **Use Configuration Files**: As JSON files, to facilitate game adjustments without changing the code.
4. **Keep the code clean**: avoid code repetition and organize resources into methods and classes.