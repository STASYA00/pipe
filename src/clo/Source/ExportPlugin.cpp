#include "stdafx.h"


#include "ExportPlugin.h"

#include "CLOAPIInterface.h"

#include <string>
#include <fstream>
#include <map>

#include "BlenderController.h"
#include "utils.h"

#if defined(__APPLE__)
#include <unistd.h>
#include <pwd.h>
#endif



using namespace std;
using namespace CLOAPI;


void ExportOBJ_Sample()
{
	if (!EXPORT_API)
		return;

	Marvelous::ImportExportOption options;
	options.bExportAvatar = false;
	options.bExportGarment = true;
	options.bSaveInZip = true;
	// the other options are given as default. please refer to ImportExportOption class in ExportAPI.h

	vector<string> exportedFilePathList;
	if (options.bSaveInZip)
	{
		std::string root;
		Utils::GetRootPath(root);
		root = Utils::AddToPath(root, "assets");
		root = Utils::AddToPath(root, "test.obj");
		exportedFilePathList = EXPORT_API->ExportOBJ(root, options); // returns only a file path for a zipped file including OBJ, MTL, and image files.

		// exportedFilePathList[0] -> a zip file

	}
	else
	{
		exportedFilePathList = EXPORT_API->ExportOBJ(options); // returns OBJ and MTL files. In addition, MTL files for colorways will be created as well.

		// exportedFilePathList[0] -> OBJ
		// exportedFilePathList[1] -> MTL for the current colorway
		// exportedFilePathList[2] -> MTL for the first colorway
		// exportedFilePathList[3] -> MTL for the second colorway
		// ...
		// exportedFilePathList[exportedFilePathList.size()-1]-> MTL for the last colorway
	}

	for (auto& path : exportedFilePathList)
	{
		if (UTILITY_API)
			UTILITY_API->DisplayMessageBox(path);
	}

}

void ExportGLTF_Sample()
{
	if (!EXPORT_API)
		return;

	Marvelous::ImportExportOption options;
	options.bExportAvatar = false;
	options.bExportGarment = true;
	options.bSaveInZip = true;
	options.scale = 0.001f; // gltf scale

	// the other options are given as default. please refer to ImportExportOption class in ExportAPI.h

	vector<string> exportedFilePathList;
	std::string root;
	Utils::GetRootPath(root);
	root = Utils::AddToPath(root, "assets");
	root = Utils::AddToPath(root, "test.gltf");
	exportedFilePathList = EXPORT_API->ExportGLTF(root, options, false); // returns only a file path for a zipped file including GLTF and BIN files.

	for (auto& path : exportedFilePathList)
	{
		if (UTILITY_API)
			UTILITY_API->DisplayMessageBox(path);
	}
}

void ImportZprj_Sample()
{

	if (!IMPORT_API)
		return;

	std::string root;
	Utils::GetRootPath(root);
	root = Utils::AddToPath(root, "assets");
	root = Utils::AddToPath(root, "test.zprj");
	UTILITY_API->DisplayMessageBox(root);

	Marvelous::ImportZPRJOption option;
	IMPORT_API->ImportZprj(root, option);
}

void ImportFile_Sample()
{
	if (!IMPORT_API)
		return;
	std::string root;
	Utils::GetRootPath(root);
	root = Utils::AddToPath(root, "assets");
	root = Utils::AddToPath(root, "test.zprj");

	IMPORT_API->ImportFile(root);
}

void GetMajorVersion_Test()
{
	if (!UTILITY_API)
		return;

	unsigned int majorVer = UTILITY_API->GetMajorVersion();

	string msg = "Major Version of CLO : " + to_string(majorVer);
	UTILITY_API->DisplayMessageBox(msg);
}

void GetMinorVersion_Test()
{
	if (!UTILITY_API)
		return;

	unsigned int minorVer = UTILITY_API->GetMinorVersion();

	string msg = "Minor Version of CLO : " + to_string(minorVer);
	UTILITY_API->DisplayMessageBox(msg);
}

void GetPatchVersion_Test()
{
	if (!UTILITY_API)
		return;

	unsigned int patchVer = UTILITY_API->GetPatchVersion();

	string msg = "Patch Version of CLO : " + to_string(patchVer);
	UTILITY_API->DisplayMessageBox(msg);
}

void ExportGLB_Sample()
{
	if (!EXPORT_API)
		return;

	Marvelous::ImportExportOption options;
	options.bExportAvatar = false;
	options.bExportGarment = true;
	options.bThin = false;
	options.bSingleObject = false;
	options.bMetaData = true;

	options.bSaveInZip = false;
	options.scale = 0.001f; // same as gltf scale

	// the other options are given as default. please refer to ImportExportOption class in ExportAPI.h

	vector<string> exportedFilePathList;
	string baseFolder = ""; // +"export_fbx/";
	Utils::GetRootPath(baseFolder);
	baseFolder = Utils::AddToPath(baseFolder, "assets");

	auto asset = Utils::AddToPath(baseFolder, "test.glb");

	exportedFilePathList = EXPORT_API->ExportGLB(asset, options);

	for (auto& path : exportedFilePathList)
	{
		if (UTILITY_API)
			UTILITY_API->DisplayMessageBox(path);
	}
	//system("blender");
}

void main() {

	std::string material;
	Utils::OpenFileDialog(material);
	material = Utils::GetParentPath(material);
	std::string baseFolder = ""; // +"export_fbx/";
	Utils::GetRootPath(baseFolder);
	baseFolder = Utils::AddToPath(baseFolder, "assets");

	auto asset = Utils::AddToPath(baseFolder, "test.glb");
	//ImportZprj_Sample();
	ExportGLB_Sample();
	auto b = BlenderController();
	b.run(asset, material);
}

void ExportFBX_Test()
{
	if (!EXPORT_API)
		return;

	Marvelous::ImportExportOption options;
	options.bExportAvatar = true;
	options.bExportGarment = true;
	// the other options are given as default. please refer to ImportExportOption class in ExportAPI.h

	vector<string> exportedFilePathList;
	string baseFolder = ""; // +"export_fbx/";
	Utils::GetRootPath(baseFolder);
	Utils::AddToPath(baseFolder, "assets");

	exportedFilePathList = EXPORT_API->ExportFBX(baseFolder + "test.fbx", options);

	for (const auto& path : exportedFilePathList)
	{
		if (UTILITY_API)
			UTILITY_API->DisplayMessageBox(path);
	}
}



extern CLO_PLUGIN_SPECIFIER void DoFunction()
{
	main();
}

extern CLO_PLUGIN_SPECIFIER void DoFunctionAfterLoadingCLOFile(const char* fileExtenstion)
{
	if (UTILITY_API != nullptr)
		UTILITY_API->DisplayMessageBox("DoFunctionAferLoadingProject starts... for file type -  " + string(fileExtenstion));
}

extern CLO_PLUGIN_SPECIFIER const char* GetActionName()
{
	const char* actionName = "POC__";
	return actionName;
}

extern CLO_PLUGIN_SPECIFIER const char* GetObjectNameTreeToAddAction()
{
	const char* objetNameTree = "menu_Setting / menuPlug_In";

	return objetNameTree;
}

extern CLO_PLUGIN_SPECIFIER int GetPositionIndexToAddAction()
{
	return 1; // 0: Above, 1: below (default = 0)
}
