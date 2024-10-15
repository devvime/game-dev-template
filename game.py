from ursina import Ursina, window
from scenes.main_menu import MainMenu
from scenes.game_scene import GameScene
from scenes.settings_scene import SettingsScene

class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.title = 'My Game'
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
