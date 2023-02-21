#include "stdafx.h"

#include "ExportPlugin.h"

#include "CLOAPIInterface.h"

#include <string>
#include <fstream>
#include <map>

#if defined(__APPLE__)
#include <unistd.h>
#include <pwd.h>
#endif



using namespace std;
using namespace CLOAPI;

static std::string base64_encode(const std::string& in) {

	std::string out;

	int val = 0, valb = -6;
	for (unsigned char c : in) {
		val = (val << 8) + c;
		valb += 8;
		while (valb >= 0) {
			out.push_back("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[(val >> valb) & 0x3F]);
			valb -= 6;
		}
	}
	if (valb > -6) out.push_back("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[((val << 8) >> (valb + 8)) & 0x3F]);
	while (out.size() % 4) out.push_back('=');
	return out;
}

string getHomePath()
{
	string homePath = "C:/";

#if defined(__APPLE__)
	const char* homeDir = getenv("HOME");

	if (homeDir == nullptr)
	{
		struct passwd* pwd = getpwuid(getuid());
		if (pwd)
			homeDir = pwd->pw_dir;
	}

	if (homeDir)
	{
		homePath = homeDir;
		homePath = homePath + "/";
	}
	else
	{
		homePath = "/usr/local/";
	}
#endif

	return homePath;
}

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
		string baseFolder = getHomePath() + "Zpac/";
		exportedFilePathList = EXPORT_API->ExportOBJ(baseFolder + "test.obj", options); // returns only a file path for a zipped file including OBJ, MTL, and image files.

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
	string baseFolder = getHomePath() + "export_gltf/";
	exportedFilePathList = EXPORT_API->ExportGLTF(baseFolder + "test.gltf", options, false); // returns only a file path for a zipped file including GLTF and BIN files.

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

	string baseFolder = getHomePath() + "Zpac/";
	UTILITY_API->DisplayMessageBox(baseFolder);
	string filePath = "C:/Users/STFED/_A/Products/POC_pipeline/assets/test.zprj"; //must assign correct file path

	Marvelous::ImportZPRJOption option;
	IMPORT_API->ImportZprj(filePath, option);
}

void ImportFile_Sample()
{
	if (!IMPORT_API)
		return;

	string baseFolder = getHomePath() + "Zpac/";
	string filePath = baseFolder + "test.zprj"; //must assign correct file path

	IMPORT_API->ImportFile(filePath);
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
	options.bSaveInZip = false;
	options.scale = 0.001f; // same as gltf scale

	// the other options are given as default. please refer to ImportExportOption class in ExportAPI.h

	vector<string> exportedFilePathList;
	string baseFolder = getHomePath() + "export_glb/";
	exportedFilePathList = EXPORT_API->ExportGLB("C:/Users/STFED/_A/Products/POC_pipeline/assets/test.glb", options); // returns only a file path for GLB file 

	for (auto& path : exportedFilePathList)
	{
		if (UTILITY_API)
			UTILITY_API->DisplayMessageBox(path);
	}
	system("blender");
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
	string baseFolder = getHomePath() + "export_fbx/";
	exportedFilePathList = EXPORT_API->ExportFBX(baseFolder + "test.fbx", options);

	for (const auto& path : exportedFilePathList)
	{
		if (UTILITY_API)
			UTILITY_API->DisplayMessageBox(path);
	}
}



extern CLO_PLUGIN_SPECIFIER void DoFunction()
{
	ImportZprj_Sample();
	ExportGLB_Sample();
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
