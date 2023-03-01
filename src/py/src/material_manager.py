import bpy

class MaterialManager:
    def __init__(self) -> None:
        self.value = None 

    

    @staticmethod
    def delete_material(material):
        material.user_clear()
        bpy.data.materials.remove(material)

    @staticmethod
    def new():
        _prev_materials = [x.name for x in bpy.data.materials]
        bpy.ops.material.new()
        new_material_name = list(set([x.name for x in bpy.data.materials]) - set[_prev_materials])[0]
        return new_material_name
    
    @staticmethod
    def get_meshes(material_name):
        _meshes = []
        for o in bpy.data.objects:
            if o.active_material:
                if o.active_material.name == material_name:
                    _meshes.append(o)
        return _meshes
    
    @staticmethod
    def run():
        suffix = ".0"
        materials = [x for x in bpy.data.materials if suffix in x.name]
        for mat in materials:
            _mesh = MaterialManager.get_meshes(mat.name)
            _other_material = mat.name[:mat.name.index(suffix)]
            MaterialManager.delete_material(mat)
            for o in _mesh:
                o.active_material = bpy.data.materials[_other_material]
        print("Deleted duplicated materials") # log
