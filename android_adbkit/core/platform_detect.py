# android_adbkit/core/platform_detect.py
import platform





_ARCH_ALIASES = {
    "x86_64": "x86_64",
    "amd64": "x86_64",
    "aarch64": "arm64",
    "arm64": "arm64",
}





def detect_os():
    system = platform.system().lower()

    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    else:
        raise RuntimeError(f"[android_adbkit] unsupported operating system: '{system}'.")


def detect_arch():
    machine = platform.machine().lower()
    arch = _ARCH_ALIASES.get(machine)

    if not arch:
        raise RuntimeError(f"[android_adbkit] unsupported architecture: '{machine}'.")

    return arch