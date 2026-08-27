# android_adbkit/adb.py
import re
import subprocess





class AdbHandle(str):
    def version(self):
        try:
            out = subprocess.check_output([str(self), "--version"], stderr=subprocess.DEVNULL)
            return out.decode("utf-8").strip()
        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
            raise RuntimeError(f"[android_adbkit] failed to run adb --version: {e}")

    def revision(self):
        text = self.version()
        match = re.search(r"^Version\s+(\d+\.\d+\.\d+)", text, re.MULTILINE)

        return match.group(1) if match else None