# android_adbkit/core/repository.py
import requests
import xml.etree.ElementTree as ElementTree





_REPOSITORY_URL = "https://dl.google.com/android/repository/repository2-3.xml"
_LATEST_DOWNLOAD_URL = "https://dl.google.com/android/repository/platform-tools-latest-{host_os}.zip"

_HOST_OS_MAP = {
    "windows": "windows",
    "linux": "linux",
    "macos": "macosx",
}

_LATEST_URL_OS_MAP = {
    "windows": "windows",
    "linux": "linux",
    "macos": "darwin",
}





def resolve_host_os(os_name):
    host_os = _HOST_OS_MAP.get(os_name)
    
    if not host_os:
        raise RuntimeError(f"[android_adbkit] unsupported platform for repository lookup: '{os_name}'.")
    
    return host_os


def resolve_latest_download_url(os_name):
    latest_os = _LATEST_URL_OS_MAP.get(os_name)
    
    if not latest_os:
        raise RuntimeError(f"[android_adbkit] unsupported platform for latest download: '{os_name}'.")
    
    return _LATEST_DOWNLOAD_URL.format(host_os=latest_os)


def resolve_specific_version_url(os_name, version):
    host_os = resolve_host_os(os_name)

    response = requests.get(_REPOSITORY_URL, timeout=15)
    response.raise_for_status()

    root = ElementTree.fromstring(response.content)

    for remote_package in root.findall("remotePackage"):
        if remote_package.get("path") != "platform-tools":
            continue

        revision = remote_package.find("revision")
        if revision is None:
            continue

        major = revision.findtext("major", default="0")
        minor = revision.findtext("minor", default="0")
        micro = revision.findtext("micro", default="0")
        package_version = f"{major}.{minor}.{micro}"

        if package_version != version:
            continue

        archives = remote_package.find("archives")
        if archives is None:
            continue

        for archive in archives.findall("archive"):
            archive_host_os = archive.findtext("host-os")
            if archive_host_os != host_os:
                continue

            complete = archive.find("complete")
            if complete is None:
                continue

            relative_url = complete.findtext("url")
            if not relative_url:
                continue

            return package_version, f"https://dl.google.com/android/repository/{relative_url}"

    raise RuntimeError(f"[android_adbkit] version '{version}' not found in the platform-tools repository for '{os_name}'.")