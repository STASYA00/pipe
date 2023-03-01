import bpy

from config import MaterialConfig
from material_manager import MaterialManager

class CloMaterial:
    def __init__(self, name):
        self.name = name
        self._color = None
        self._scale = []
        self._mat = self._load()

    @property
    def color(self):
        return [x for x in self._color]
    
    @property
    def scale(self):
        return [x for x in self._scale]
    
    def delete(self):
        MaterialManager.delete_material(self._mat)
        
    def _load(self):
        m = [x for x in bpy.data.materials if self.name in x.name]
        if len(m) > 0:
            m = m[0]
            self._mat = m
            self._get_color()
            self._get_scale()
            return m
        
    def _get_color(self):
        _node = [x for x in self._mat.node_tree.nodes if MaterialConfig().color_node==x.name]
        if len(_node)>0:
            _node = _node[0]
            self._color = [x for x in _node.inputs[7].default_value] # RGBA

    def _get_scale(self):
        _node = [x for x in self._mat.node_tree.nodes if MaterialConfig().mapping_node==x.name]
        if len(_node)>0:
            _node = _node[0]
            self._scale = [x for x in _node.inputs[3].default_value] # XYZ