import argparse
import bpy
import os
import sys
import textwrap


file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from argarse_blender import ArgumentParserForBlender
from folder import DialogWindow
from pipeline import MvpPipeline
from texture import Texture

################################################################################

if __name__ == '__main__':
	if '--' in sys.argv:
		argv = sys.argv[sys.argv.index('--') + 1:]
		parser = ArgumentParserForBlender(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description=textwrap.dedent('''\
			USAGE: blender -b assets/Blender_Scene/scene.blend --python src/main.py -- --garment assets/garment.glb --material assets/Textures

	        ------------------------------------------------------------------------
	
	        This is an algorithm that imports a file into the given scene and renders 
            it.
	
	        ------------------------------------------------------------------------
	
	        -garment        file containing 3D mesh to be inserted in the scene and
                            rendered, string
	
	        ------------------------------------------------------------------------
	
	        '''), epilog=textwrap.dedent('''\
	        The algorithm will be updated.
	        '''))

		parser.add_argument('--garment', type=str, help='path to the mesh file with '
		                                            '.obj or .glb or .gltf extension'
                                                    ', str')
		parser.add_argument('--material', type=str, help='path to the material folder'
                                                    ', str')

	############################################################################

	try:
		args = parser.parse_args()


	except SystemExit as e:
		print(repr(e))

	############################################################################

	# def menu_func_import(self, context):
	# 	self.layout.operator(
	# 		DialogWindow.bl_idname)

	# def register():
	# 	bpy.utils.register_class(DialogWindow)
	# 	#bpy.types.INFO_MT_file_import.append(menu_func_import)

	# def unregister():
	# 	bpy.utils.unregister_class(DialogWindow)
	# 	#bpy.types.INFO_MT_file_import.remove(menu_func_import)
		
	# register()
	# print("register class")
	# r = bpy.ops.open.browser('INVOKE_DEFAULT')
	# print("open file browser")
	# print(r)
	# print("\n")
	# bpy.utils.unregister_class(DialogWindow)

	print(argv)
	GARMENT = argv[1]
	MATERIAL = argv[3]
	print("\nMATERIAL:\n", MATERIAL)
	t = Texture(MATERIAL, "Image_9.png")
	print(t.content)
	p = MvpPipeline(GARMENT)
	p.run()