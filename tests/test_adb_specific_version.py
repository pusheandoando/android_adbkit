# tests/test_adb_specific_version.py
from android_adbkit import get_adb





if __name__ == '__main__':
    try:
        adb = get_adb(version="35.0.2")
        
        print("\n")
        print(f"ADB path: {adb}")

        if adb:
            print(f"ADB version: {adb.version()}")
    except Exception as error_log:
        print("[TEST Error]")
        print(error_log)