import bpy
import os

from config import RenderConfig
from blender_utils import *
from naming import NamingProtocol

class Renderer:
    """
    Class that manages the scene rendering.
    """
    def __init__(self):
        self.config = RenderConfig()
        
        bpy.types.ImageFormatSettings.color_mode = self.config.color_mode
        self._scene_name = bpy.data.scenes[-1].name
        self._set_gpu()
        self.scene = bpy.data.scenes[self._scene_name]
        self._set_scene()
        
    def render(self, filename:str='new_mask_test'):
        """
        Function that performs all the rendering steps: normal render, segmentation
        mask.
        :param filename: name of the file, str
        :return:
        """
        deselect_all()
        self._render(filename)

    def _set_scene(self):
        self.scene.render.engine = self.config.engine
        self.scene.cycles.device = self.config.device
        self.scene.render.use_persistent_data = True
        
        self.scene.render.resolution_percentage = 100
        self.scene.render.resolution_x = self.config.image_size
        self.scene.render.resolution_y = self.config.image_size
        self.scene.cycles.samples = self.config.samples


    def _set_gpu(self):
         pref = bpy.context.preferences.addons["cycles"].preferences
         pref.get_devices()
         gpu_dev = [x for x in pref.devices if x.type=="CUDA"][0]
         pref.compute_device_type = gpu_dev.type
         gpu_dev.use = True

    def _set_img_settings(self):
        image_settings = bpy.context.scene.render.image_settings
        image_settings.file_format = self.config.img_format
        image_settings.color_depth = '8'
        image_settings.color_mode = self.config.color_mode

        
    def _render(self, filename):
        """
        Function that renders the scene.
        :return:
        """
        self._set_img_settings()
        self._set_scene()
        
        bpy.ops.render.render()
        
        print(f"output folder: {self.config.output_folder}")
        # if not self.config.output_folder in os.listdir():
        #     print("current:")
        #     print(os.listdir())
        #     os.mkdir(self.config.output_folder)
        
        try:
            bpy.data.images["Render Result"].save_render(
                NamingProtocol().get_filename(filename))
            print(f"Image saved as {NamingProtocol().get_filename(filename)}")
        except RuntimeError as e:
            print(repr(e))
            print("Could not save the render {}".format(filename))
            pass