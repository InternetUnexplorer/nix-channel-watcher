#! /usr/bin/env python3

from os import listdir, path
from subprocess import run
from typing import Dict, Tuple
from urllib.request import urlopen

CHANNELS_FILENAME = "channels.txt"
HOOK_DIR_SUFFIX = ".hooks"


def load_channels(filename: str) -> Dict[str, Tuple[str, str]]:
    channels = {}
    with open(filename, "r") as file:
        for line in file:
            name, url, rev = line.split()
            channels[name.strip()] = (url.strip(), rev.strip())
    return channels


def save_channels(channels: Dict[str, Tuple[str, str]], filename: str) -> None:
    with open(filename, "w") as file:
        for name, (url, rev) in channels.items():
            print(f"{name} {url} {rev}", file=file)


def get_channel_rev(channel_url: str) -> str:
    with urlopen(f"{channel_url}/git-revision") as file:
        return file.read().decode().strip()


def run_hooks(name: str, url: str, old_rev: str, new_rev: str) -> None:
    hook_dir = name + HOOK_DIR_SUFFIX
    for hook in listdir(hook_dir):
        print(f"-> running '{hook}'...")
        run([path.join(hook_dir, hook), name, old_rev, new_rev], check=True)


if __name__ == "__main__":
    channels = load_channels(CHANNELS_FILENAME)

    for name, (url, rev) in channels.items():
        new_rev = get_channel_rev(url)
        if rev == new_rev:
            continue
        print(f"channel updated: {name}: {rev} -> {new_rev}")
        run_hooks(name, url, rev, new_rev)
        channels[name] = (url, new_rev)

    save_channels(channels, CHANNELS_FILENAME)
