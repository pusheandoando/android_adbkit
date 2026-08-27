# android_adbkit/core/installer.py
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ElementTree

import requests

from android_adbkit.core import repository
from android_adbkit.core.downloader import download_file
from android_adbkit.core.archive_extract import extract_zip
from android_adbkit.core.paths import platform_tools_dir, adb_binary_path





def _get_installed_version(binary_path):
    try:
        out = subprocess.check_output([binary_path, "--version"], stderr=subprocess.DEVNULL)
        text = out.decode("utf-8").strip()
        match = re.search(r"^Version\s+(\d+\.\d+\.\d+)", text, re.MULTILINE)
        
        if match:
            return match.group(1)
        
        return None
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None


def _get_latest_available_version(os_name):
    host_os = repository.resolve_host_os(os_name)

    response = requests.get(repository._REPOSITORY_URL, timeout=15)
    response.raise_for_status()
    
    root = ElementTree.fromstring(response.content)

    for remote_package in root.findall("remotePackage"):
        if remote_package.get("path") != "platform-tools":
            continue

        archives = remote_package.find("archives")
        if archives is None:
            continue

        for archive in archives.findall("archive"):
            if archive.findtext("host-os") != host_os:
                continue

            revision = remote_package.find("revision")
            if revision is None:
                continue

            major = revision.findtext("major", default="0")
            minor = revision.findtext("minor", default="0")
            micro = revision.findtext("micro", default="0")
            
            return f"{major}.{minor}.{micro}"

    return None


def _make_binary_executable(binary_path, os_name):
    if os_name != "windows":
        os.chmod(binary_path, 0o755)


def install_platform_tools(storage_path, os_name, arch_name, version=None, auto_update=True):
    tools_dir = platform_tools_dir(storage_path)
    binary_path = adb_binary_path(storage_path, os_name)

    print('\n')
    print(f"[ Android Platform-Tools ({os_name}, {arch_name}) ]")

    if os.path.exists(binary_path):
        installed_version = _get_installed_version(binary_path)

        if version:
            if installed_version == version:
                print(f" - Requested version {version} already installed, nothing to do.")
                return binary_path
        elif installed_version and not auto_update:
            print(f" - Platform-tools already installed (version {installed_version}), auto_update=False.")
            return binary_path
        elif installed_version:
            latest_version = _get_latest_available_version(os_name)
            
            if latest_version and installed_version == latest_version:
                print(f" - Platform-tools already up to date (version {installed_version}).")
                return binary_path

            print('\n')
            print("( Version mismatch detected )")
            print(f" - Installed version: {installed_version}")
            print(f" - Latest version:    {latest_version}")

        print(" - Removing outdated installation...")
        shutil.rmtree(tools_dir, ignore_errors=True)

    os.makedirs(storage_path, exist_ok=True)

    try:
        if version:
            print(f" - Resolving download URL for version {version}...")
            resolved_version, download_url = repository.resolve_specific_version_url(os_name, version)
        else:
            print(" - Resolving latest platform-tools download URL...")
            resolved_version = _get_latest_available_version(os_name)
            download_url = repository.resolve_latest_download_url(os_name)
        print(f" - Resolved version: {resolved_version}")
    except (RuntimeError, requests.RequestException) as e:
        print(f" [!!] {e}")
        return None

    zip_path = os.path.join(storage_path, "platform-tools.zip")

    try:
        print(f" - Downloading from: {download_url}")
        download_file(download_url, zip_path)
    except requests.RequestException as e:
        print(f" [!!] Download failed: {e}")
        return None

    print(" - Extracting...")
    extract_zip(zip_path, storage_path)
    os.remove(zip_path)

    if not os.path.exists(binary_path):
        print(f" [!!] Extraction completed but binary was not found at: {binary_path}")
        return None

    _make_binary_executable(binary_path, os_name)

    print(f" - ADB installed at: {binary_path}")
    
    return binary_path