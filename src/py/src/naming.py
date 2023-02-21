from config import RenderConfig, ConfigMeta

class NamingProtocol(metaclass=ConfigMeta):
    
    def get_filename(self, fname) -> str:
        # return "{}/{}.png".format(RenderConfig().output_folder, fname) 
        return "{}.png".format(fname) 

    def get_material(self, category, name):
        return "{}/{}".format(category, name)  # type/category/image