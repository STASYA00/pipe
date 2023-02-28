import bpy
# import numpy as np
# import os

from blender_utils import get_fromnode_links, get_nodes_link, get_tonode_links
from config import MaterialConfig
    
class Material:
    def __init__(self) -> None:
        
        self._config = MaterialConfig()

        self.filepath  = self._config.filepath + self._config.section + self._config.name
        self.dir = self._config.filepath + self._config.section

        self._material = self._create()

    def _get_default(self):
        _mat = [x for x in bpy.data.materials if x.name==self._config.name]
        if len(_mat)>0:
            return _mat[0]

    def _create(self):
        new_material = self._copy()
        if (not new_material):
            new_material = self._import()
        return new_material

    def _copy(self)->bool:
        _mat = self._get_default()
        if _mat:
            return _mat.copy()
    
    def _import(self):
        bpy.ops.wm.append(
            filepath=self.filepath, 
            filename=self._config.name,
            directory=self.dir)
        return self._get_default()

# class Material:
#     def __init__(self, part):
#         self._nodes = self._get_node()
#         self.active_values = []
        
#     def activate(self):
#         pass

#     def make(self, category="random", value=True):
#         return self._make(category, value)

#     def _get_node(self):
#         """
#         Function that gets the customizable node from the part's active material tree.
#         """
#         m = [x.material for x in self.part.mesh.material_slots if x.material][0]
#         return [x for x in m.node_tree.nodes if self._get_nodename() in x.name]

#     def _get_nodename(self):
#         return "Image Texture"  # "RGB"

#     def _make(self, category, value=True):
#         self._reset()
#         if value:
#             self.activate()
#             self.active_values = self._produce_textures(category)
#             self._update_nodes(self.active_values)
#         return self.active_values

#     def _produce_textures(self, category=None):
#         return []

#     def _reset(self):
#         self.active_values = []

#     def _split_nodes(self, material):
#         print("Material {} in object {} should not be split.".format(
#             self.part.mesh.active_material, self.part.name))
#         raise KeyboardInterrupt
    
#     def _update_nodes(self, materials):
#         pass


# class SubstanceMaterial(Material):
#     def __init__(self, part):
#         Material.__init__(self, part)
#         self.mapdict = SubstanceDictionary()

#     def activate(self):
#         _current_material = self.part.mesh.active_material.name
#         try:
#             if not self._suffix in _current_material:
#                 self.part.mesh.active_material = bpy.data.materials[
#                     _current_material + "_" + self._suffix]
                    
#         except KeyError:
#             print("Could not activate material {} as NFT".format(_current_material))
#             pass

#     def _get_links(self):
#         """
#         Function that gets the main node from the part's active material tree.
#         """
#         m = [x.material for x in self.part.mesh.material_slots if x.material][0]
#         return [x for x in m.node_tree.links]

#     def _produce_textures(self, category):
#         self.active_values.append(category)
#         _result = self.factory.produce_substance(category)
#         return _result

#     def _check_link(self, link):
#         for key, value in self.mapdict.content.items():
#             if link.to_node.name.lower() == key.lower():
#                 for v in value:
#                     if link.to_socket.name.lower() == v[0].lower():
#                         return v[1]

#     def _update_nodes(self, materials):
#         _result = materials
#         self._nodes = self._get_node()
#         for n in self._nodes:
#             mapname = None
#             links = get_fromnode_links(n, self._get_links())
#             for link in links:
#                 mapname = self._check_link(link)
                
#                 if mapname:
#                     if mapname.lower() != "print".lower(): 
#                         texture = [x for x in _result if mapname.lower() in x.name.lower()]
                        
#                         if texture:
#                             texture = texture[0]
#                             n.image = texture.content


# class SubstanceDictionary:
#     def __init__(self) -> None:
#         # node_name : (socket_name, string in imagefile)
#         self.content = {"Mix": [("Color1", "BaseColor"), 
#                                 ("Color2", "print")],
#                         'Hue Saturation Value': [("Color", "BaseColor")],
#                         "Principled BSDF": [("Base Color", "BaseColor"),
#                                             ("Alpha", "Alpha"),
#                                             ("Metallic", "Metallic"),
#                                             ("Roughness", "Roughness")],
#                         "Displacement": [("Height", "Displacement")],
#                         "Normal map": [("Color", "Normal")],
#                        }



