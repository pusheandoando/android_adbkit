# android_adbkit/core/paths.py
import os





_STORAGE_DIR_NAME = "android_adbkit"





def default_storage_path(os_name):
    if os_name == "windows":
        local_app_data = os.environ.get("LOCALAPPDATA")
        
        if local_app_data:
            return os.path.join(local_app_data, _STORAGE_DIR_NAME)
        
        return os.path.join(os.path.expanduser("~"), _STORAGE_DIR_NAME)

    return os.path.join(os.path.expanduser("~"), f".{_STORAGE_DIR_NAME}")


def platform_tools_dir(storage_path):
    return os.path.join(storage_path, "platform-tools")


def adb_binary_path(storage_path, os_name):
    binary_name = "adb.exe" if os_name == "windows" else "adb"
    
    return os.path.join(platform_tools_dir(storage_path), binary_name)