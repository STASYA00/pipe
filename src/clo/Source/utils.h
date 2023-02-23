#pragma once
#include <string>
#include <fstream>
#include <Windows.h>
//#include <atlstr.h> // Used for converting side string to string (in open file-dialog)
//#include <ShObjIdl.h> // Used for open file dialog
#include <filesystem>

#include <string>
#include <shlobj.h>
#include <iostream>
#include <sstream>

//#include "nlohmann/json.hpp"


namespace Utils {

	const std::string logFilePath = "c:/temp/log_pipePoc.txt";
	EXTERN_C IMAGE_DOS_HEADER __ImageBase;
	


	static void wtof(std::string msg)
	{
		std::ofstream f;

		f.open(logFilePath, std::ios::app);
		//f << GetCurrentTime() << ": " << msg << std::endl;
		f << msg << std::endl;
		f.close();
	}

	static void err(std::string msg) {
		std::string s = "ERROR " + msg;
		wtof(s);
	}

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

	static std::string GetParentPath(std::string pathIn, int levels = 1) {
		auto ind = 0;
		auto start = 0;
		for (int i = 0; i < levels; i++) {
			ind = pathIn.find_last_of("\\");
			pathIn = pathIn.substr(start, ind);
		}

		return pathIn;
	}
	
	static bool GetPluginPath(std::string& pathOut) {
		char path[MAX_PATH];
		HMODULE hm = NULL;

		if (GetModuleFileNameA(hm, path, sizeof(path)) == 0)
		{
			int ret = GetLastError();
			err(std::string("GetModuleFileName failed, error = {}", ret));
			return false;
		}

		LPTSTR  strDLLPath1 = new TCHAR[_MAX_PATH];
		::GetModuleFileName((HINSTANCE)&__ImageBase, strDLLPath1, _MAX_PATH);

		auto ws = (std::wstring)strDLLPath1;
		std::string str(ws.begin(), ws.end());
		pathOut = str;

		return true;
	}

	static bool GetRootPath(std::string& pathOut) {
		GetPluginPath(pathOut);
		pathOut = GetParentPath(pathOut, 5); //7

		return true;
	}

	
	/*static std::string GetParentPath(std::string pathIn, int levels = 1) {

		std::filesystem::path path = pathIn;
		for (int i = 0; i < levels; i++) {
			path = path.parent_path();
		}

		return path.string();
	}*/

	static std::string AddToPath(std::string pathIn, std::string add) {
		
		pathIn = pathIn + "/" + add;

		return pathIn;
	}

	static bool OpenFileDialog(std::string& path)
	{
		bool ok = false;

		auto hr = CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE);

		if (SUCCEEDED(hr))
		{
			IFileOpenDialog* fileDialog;
			hr = CoCreateInstance(CLSID_FileOpenDialog, nullptr,
				CLSCTX_ALL, IID_IFileOpenDialog,
				reinterpret_cast<void**>(&fileDialog));
			COMDLG_FILTERSPEC rgSpec[] =
			{
				{ L"hatch", L"*.jpg;*.jpeg;*png;*.tif;*.tiff;*.TIF;*.TIFF;*.psd;*.PSD;*.ai;*.AI;*.pdf;*.PDF;"},
				{ L"jpg", L"*.jpg;*.jpeg"},
				{ L"png", L"*.png"},
				{ L"tif", L"*.tif;*.tiff;*.TIF;*.TIFF"},
				{ L"psd", L"*.psd;*.PSD"},
				{ L"ai", L"*.ai;*.AI"},
				{ L"pdf", L"*.pdf;*.PDF"},
				//{ L"folder", L"*(?!=.*)"},  // regex for folder but doesnt allow to select a folder :(
			};
			fileDialog->SetFileTypes(7, rgSpec);
			if (SUCCEEDED(hr))
			{
				hr = fileDialog->Show(nullptr);

				if (SUCCEEDED(hr))
				{
					IShellItem* item;
					hr = fileDialog->GetResult(&item);
					if (SUCCEEDED(hr))
					{
						PWSTR filePath;
						hr = item->GetDisplayName(SIGDN_FILESYSPATH, &filePath);
						if (SUCCEEDED(hr))
						{
							char res[1024];
							auto ret = WideCharToMultiByte(CP_ACP, 0, filePath, -1, res, 1024, nullptr, nullptr);

							// WideCharToMultiByte returns 0 if it conversion fails
							if (ret > 0)
							{
								ok = true;
								path = std::string(res);
							}

							CoTaskMemFree(filePath);
						}
						item->Release();
					}
				}
				fileDialog->Release();
			}
			CoUninitialize();
		}

		return ok;
	}
}