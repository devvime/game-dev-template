from ursina import *

class Scene(Entity):
    def __init__(self):
        super().__init__()
        self.elements = []

    def add_element(self, elements = []):
        for element in elements:
            self.elements.append(element)
        
    def update(self):
        pass
    
    def input(self, key):
        pass

    def enable(self):
        for element in self.elements:
            element.enabled = True
        self.enabled = True

    def disable(self):
        for element in self.elements:
            element.enabled = False
        self.enabled = False
