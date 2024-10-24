from ursina import *
from Core.SceneManager import SceneManager

from Scenes.Menu import MenuScene
from Scenes.Game import GameScene

app = Ursina(
    title='My Game',
    borderless=False,
    fullscreen=False,
    vsync=False,
    development_mode=True,
    show_ursina_splash=True
)

scene_manager = SceneManager()

menu_scene = MenuScene()
game_scene = GameScene()

scene_manager.add_scene('menu', menu_scene)
scene_manager.add_scene('game', game_scene)

scene_manager.switch_to('menu')

def input(key):
    if key == '1':
        scene_manager.switch_to('menu')
    elif key == '2':
        scene_manager.switch_to('game')

app.run()

