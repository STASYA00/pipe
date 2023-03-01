import bpy

from importer import Importer
from material import Material
from clo_material_manager import CloMaterialManager
from renderer import Renderer
from transformer import Transformer, TRANSFORMATIONS

class Pipeline:
    def __init__(self, value):
        self.name = ""
        self.value = value

    def run(self):
        return self._run()

    def _run(self):
        return 
    
class MaterialPipeline(Pipeline):
    def __init__(self, value=None):
        Pipeline.__init__(self, value)
        self._transformer = Transformer()

    def _run(self):
        
        manager = CloMaterialManager()
        manager.run()
        for clo_material in manager.content:
            new_material = Material()
            new_material.material.name = clo_material.name
            self._transformer(new_material.material, clo_material.color, TRANSFORMATIONS.COLOR)
            self._transformer(new_material.material, clo_material.scale, TRANSFORMATIONS.SCALE)
            print("MATERIAL: {}".format(clo_material.name))
            print("Meshes: {}".format(len(clo_material.mesh)))
            for o in clo_material.mesh: #apply new material to mesh
                o.active_material = new_material.material
            
            clo_material.delete()

class MvpPipeline(Pipeline):
    def __init__(self, value):
        Pipeline.__init__(self, value)
        self.importer = Importer(self.value)
        self.renderer = Renderer()

    def _run(self):
        self.importer.run()
        manager = CloMaterialManager()
        manager.run()
        pipe = MaterialPipeline()
        pipe.run()
        #MaterialManager.run()
        Material()
        #self.renderer.render(self.value[:-4])
