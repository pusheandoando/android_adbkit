# android_adbkit/__init__.py
import os

from android_adbkit.adb import AdbHandle
from android_adbkit.core.installer import install_platform_tools
from android_adbkit.core.platform_detect import detect_os, detect_arch
from android_adbkit.core.paths import default_storage_path, adb_binary_path





def get_adb(download_path: str = None, auto_update: bool = True, version: str = None):
    os_name = detect_os()
    arch_name = detect_arch()

    storage_path = download_path if download_path else default_storage_path(os_name)
    binary_path = adb_binary_path(storage_path, os_name)
    
    if os.path.exists(binary_path) and version is None and not auto_update:
        return AdbHandle(binary_path)

    result_path = install_platform_tools(
        storage_path = storage_path,
        os_name = os_name,
        arch_name = arch_name,
        version = version,
        auto_update = auto_update,
    )

    if result_path is None:
        return None

    return AdbHandle(result_path)