from core.scene_data import scene_data

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        scene_data[name] = scene
        scene_data[name].pause()
        scene_data[name].disable()

    def switch_to(self, name):
        for key, value in scene_data.items():
            scene_data[key].pause()
            scene_data[key].disable()
            
        if self.current_scene:
            self.current_scene.pause()
            self.current_scene.disable()
        
        self.current_scene = scene_data[name]
        self.current_scene.enable()
        self.current_scene.resume()
        
    def update(self):
        if self.current_scene:
            self.current_scene.update()
            
    def input(self, key):
        if self.current_scene:
            self.current_scene.input(key)
