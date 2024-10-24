from ursina import *

class Scene(Entity):
    def __init__(self):
        super().__init__()
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)
        
    def update(self):
        pass

    def enable(self):
        for element in self.elements:
            element.enabled = True
        self.enabled = True

    def disable(self):
        for element in self.elements:
            element.enabled = False
        self.enabled = False
