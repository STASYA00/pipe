import bpy

class Importer:
    def __init__(self, value):
        self.value = value

    def run(self):
        return self._run()

    def _run(self):
        bpy.ops.import_scene.gltf(filepath=self.value)
        return