#pragma once
#include <string>

class BlenderController {
public:
	BlenderController() {}
public:
	bool run(std::string asset, std::string material);

private:
	bool getScene(std::string& f);
	bool getCode(std::string& f);

public:
	std::string command = "blender";
	std::string command_bgr = "blender -b assets/Blender_Scene/scene.blend --python py_plugin/src/main.py -- --garment ";
};