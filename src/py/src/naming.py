import os

from config import RenderConfig, ConfigMeta, MaterialConfig

class NamingProtocol(metaclass=ConfigMeta):
    
    def get_filename(self, fname) -> str:
        # return "{}/{}.png".format(RenderConfig().output_folder, fname) 
        return "{}.png".format(fname) 

    def get_material(self, category, suffix):
        folder = NamingProtocol.get_material_folder(category)
        name = [x for x in os.listdir( "{}/{}/image_maps".format(MaterialConfig().asset_path, folder)) if suffix in x][0]
        return "{}/{}/image_maps/{}".format(MaterialConfig().asset_path, folder, name)  # type/category/image

    @staticmethod
    def get_material_folder(mat):
        _folders = [x for x in os.listdir(MaterialConfig().asset_path) if x.startswith(mat)]
        assert len(_folders) > 0, "Material {} not in {}".format(mat, MaterialConfig().asset_path)
        return _folders[0]
