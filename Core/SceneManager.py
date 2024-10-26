from Core.SceneData import sceneData

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        sceneData[name] = scene
        sceneData[name].disable()

    def switch_to(self, name):
        for key, value in sceneData.items():
            sceneData[key].disable()
            
        if self.current_scene:
            self.current_scene.disable()
        
        self.current_scene = sceneData[name]
        self.current_scene.enable()
        
    def update(self):
        if self.current_scene:
            self.current_scene.update()
            
    def input(self, key):
        if self.current_scene:
            self.current_scene.input(key)
