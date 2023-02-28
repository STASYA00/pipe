import bpy

from importer import Importer
from material_manager import MaterialManager
from renderer import Renderer

class Pipeline:
    def __init__(self, value):
        self.name = ""
        self.value = value

    def run(self):
        return self._run()

    def _run(self):
        return 

class MvpPipeline(Pipeline):
    def __init__(self, value):
        Pipeline.__init__(self, value)
        self.importer = Importer(self.value)
        self.renderer = Renderer()

    def _run(self):
        self.importer.run()
        MaterialManager.run()
        self.renderer.render(self.value[:-4])
