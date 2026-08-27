# tests/test_adb_subprocess_commands.py
import subprocess

from android_adbkit import get_adb





def run_command(adb, args, label):
    print('\n')
    print(f"[ {label} ]")
    print(f" - Command: adb {' '.join(args)}")

    try:
        result = subprocess.run(
            [adb, *args],
            capture_output = True,
            text = True,
            timeout = 30,
        )

        if result.stdout.strip():
            print(f" - stdout:\n{result.stdout.strip()}")

        if result.stderr.strip():
            print(f" - stderr:\n{result.stderr.strip()}")

        print(f" - Return code: {result.returncode}")

    except subprocess.TimeoutExpired:
        print(" [!!] Command timed out.")
    except Exception as error_log:
        print(f" [!!] Command failed: {error_log}")





if __name__ == '__main__':
    adb = get_adb(auto_update=True)

    if adb is None:
        print("[TEST Error]")
        print("adb could not be resolved, aborting subprocess tests.")
    else:
        print("\n")
        print(f"ADB path: {adb}")
        print(f"ADB version (via AdbHandle): {adb.version()}")

        run_command(adb, ["--version"], "Version check")
        run_command(adb, ["start-server"], "Start server")
        run_command(adb, ["devices"], "List devices")
        run_command(adb, ["devices", "-l"], "List devices (verbose)")
        run_command(adb, ["help"], "Help output")
        run_command(adb, ["kill-server"], "Kill server")