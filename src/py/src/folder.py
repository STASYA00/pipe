import bpy
from bpy_extras.io_utils import ImportHelper 

class DialogWindow(bpy.types.Operator):

    bl_idname = "open.browser"
    bl_label = "Somelabel"

    def execute(self, context):
        print("filepath=", self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event): # See comments at end  [1]        
        context.window_manager.fileselect_add(self)  
        #Open browser, take reference to 'self' read the path to selected 
        #file, put path in predetermined data structure self.filepath
        return {'RUNNING_MODAL'}  
