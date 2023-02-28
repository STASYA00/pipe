import bpy

class MaterialManager:
    def __init__(self) -> None:
        self.value = None 

    @staticmethod
    def run():
        materials = [x for x in bpy.data.materials if ".0" in x.name]
        for mat in materials:
            mat.user_clear()
            bpy.data.materials.remove(mat)
        print("Deleted duplicated materials") # log

    @staticmethod
    def new():
        _prev_materials = [x.name for x in bpy.data.materials]
        bpy.ops.material.new()
        new_material_name = list(set([x.name for x in bpy.data.materials]) - set[_prev_materials])[0]
        return new_material_name
