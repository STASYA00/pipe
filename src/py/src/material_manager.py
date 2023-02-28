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
