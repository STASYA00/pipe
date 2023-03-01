import bpy

from clo_material import CloMaterial
from config import MaterialConfig
from material_manager import MaterialManager


class CloMaterialFactory:
    def __init__(self) -> None:
        pass

    def __call__(self, material) -> CloMaterial:
        return CloMaterial(material.name)


class CloMaterialManager:
    def __init__(self) -> None:
        self._factory = CloMaterialFactory()
        self._materials = []
        self._content = []

    @property
    def content(self):
        return [x for x in self._content]

    def _clean(self):
        MaterialManager.run()

    def _load(self):
        self._materials = [x for x in bpy.data.materials if MaterialConfig().code in x.name]

    def _populate(self):
        for mat in self._materials:
            self._content.append(self._factory(mat))

    def run(self):
        self._clean()
        self._load()
        print(self._materials)
        self._populate()
