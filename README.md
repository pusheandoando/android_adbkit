# Android ADB Kit (android_adbkit)
Automated ADB (Android Platform-Tools) downloader and manager. Handles downloading, caching, and version-matching of the official Android platform-tools package so you can skip manual Android Studio setup and PATH configuration.





## Supported Platforms
| Platform | Status |
|---|---|
| Windows | Supported |
| Linux | Supported |
| macOS | Supported |

## Supported Architectures
| Architecture | Status |
|---|---|
| x86_64 / amd64 | Supported |
| arm64 / aarch64 | Supported |

## Installation
```bash
pip3 install --upgrade git+https://github.com/pusheandoando/android_adbkit.git
```





## Usage
```python
from android_adbkit import get_adb

adb = get_adb()

print(adb)
# ~/.android_adbkit/platform-tools/adb
```

```python
import subprocess
from android_adbkit import get_adb

adb = get_adb()

subprocess.run([adb, "devices"])
```

### Checking the installed version
```python
adb = get_adb()

print(adb.version())
```

### Auto-updating to the latest version
```python
adb = get_adb(auto_update=True)
```

### Requesting a specific version
```python
adb = get_adb(version="35.0.2")
```

### Custom download path
```python
adb = get_adb(
    download_path = "/custom/path",
    auto_update = True
)
```





### Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `download_path` | `str` | `None` | Custom storage path |
| `version` | `str` | `None` | Specific platform-tools version to install (e.g. `"35.0.2"`) |
| `auto_update` | `bool` | `True` | Re-download platform-tools when a newer version is available |

Returns an `AdbHandle` (a string subclass pointing to the adb binary path), or `None` on failure.





## Storage
Platform-tools are stored under:
```
~/.android_adbkit/
    platform-tools/
        adb
        fastboot
        ...
```

On Windows:
```
%LOCALAPPDATA%\android_adbkit\
    platform-tools\
        adb.exe
        fastboot.exe
        ...