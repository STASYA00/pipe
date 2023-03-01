class ConfigMeta(type):
    """
    Singleton metaclass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RenderConfig(metaclass=ConfigMeta):
    def __init__(self):
        self.samples = 200
        self.engine = "CYCLES"
        self.image_size = 600
        self.output_folder = "C:/Users/STFED/_A/Products/POC_pipeline/assets/out"
        self.device = "GPU"
        self.color_mode = "RGBA"
        self.img_format = "PNG"
        
    def get_properties(self):
        """
        Function that gets the render properties to set in the scene.
        """
        return


class MaterialConfig(metaclass=ConfigMeta):
    def __init__(self):
        self.name = "Generic"
        self.section = "\\Material\\"
        self.filepath = "C:/Users/00sta/source/repos/pipe/assets/Material_Cube_01.blend"
        
        self.color_node = "Mix"
        self.mapping_node = "Mapping"
        self.code = "MLK"
    
