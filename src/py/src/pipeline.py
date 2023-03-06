import bpy

from importer import Importer
from material import Material
from material_nodes import NODES, TextureMapping
from clo_material_manager import CloMaterialManager
from renderer import Renderer
from transformer import Transformer

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
            clo_material.delete()
            new_material.material.name = clo_material.name
            
            self._transformer(new_material.material, clo_material.color, NODES.MIX)
            self._transformer(new_material.material, clo_material.scale, NODES.MAPPING)
            for node in NODES:
                if TextureMapping().is_texture(node):
                    self._transformer(new_material.material, clo_material.name[:6], node)
            
            for o in clo_material.mesh: #apply new material to mesh
                o.active_material = new_material.material
            
            

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
        self.renderer.render(self.value[:-4])
