import bpy

from importer import Importer
from material import Material
from clo_material_manager import CloMaterialManager
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
        manager = CloMaterialManager()
        manager.run()
        print([ x.scale for x in manager.content])
        print([ x.color for x in manager.content])
        #MaterialManager.run()
        #Material()
        #self.renderer.render(self.value[:-4])
