#include "stdafx.h"

#include "BlenderController.h"
#include "utils.h"

std::string ASSET_FOLDER = "asséts/";
std::string SRC_FOLDER = "src/py/src/";
std::string SCENE = "assets/Blender_Scene/scene.blend";
std::string PY_EXEC = "main.py";

bool BlenderController::run(std::string asset, std::string material) {
	std::string scene;
	std::string code;
	getScene(scene);
	getCode(code);
	auto exec = command + " " + scene + " " + "--python " + code + " -- --garment " + asset + " --material " + material;
	system(exec.c_str());
	return true;
}

bool BlenderController::getScene(std::string& root) {

	Utils::GetRootPath(root);
	root = Utils::AddToPath(root, SCENE);
	return true;
}

bool BlenderController::getCode(std::string &root) {

	Utils::GetRootPath(root);
	root = Utils::AddToPath(root, SRC_FOLDER);
	root = Utils::AddToPath(root, PY_EXEC);
	return true;

}