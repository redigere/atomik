#!/usr/bin/env python3
"""Install non-system Flatpak applications and apply overrides."""

import subprocess
import sys


def run(*args, check=False, **kwargs):
    return subprocess.run(args, check=check, **kwargs)


APPS = [
    "com.discordapp.Discord",
    "com.slack.Slack",
    "com.jetbrains.IntelliJ-IDEA-Ultimate",
    "com.jetbrains.PyCharm-Professional",
    "com.jetbrains.GoLand",
    "com.jetbrains.WebStorm",
    "com.google.AndroidStudio",
]

IDE_OVERRIDES = [
    "com.jetbrains.IntelliJ-IDEA-Ultimate",
    "com.jetbrains.PyCharm-Professional",
    "com.jetbrains.GoLand",
    "com.jetbrains.WebStorm",
    "com.google.AndroidStudio",
]


def main():
    print("Installing non-system Flatpak applications...")

    run(
        "flatpak", "remote-add", "--if-not-exists", "flathub",
        "https://dl.flathub.org/repo/flathub.flatpakrepo",
        check=False,
    )

    for app in APPS:
        print(f"  Installing {app}...")
        run("flatpak", "install", "-y", "flathub", app, check=False)

    print("Applying Flatpak overrides...")
    run("flatpak", "override", "--user", "--reset", "com.discordapp.Discord", check=False)
    run(
        "flatpak", "override", "--user", "com.discordapp.Discord",
        "--share=ipc",
        "--socket=fallback-x11",
        "--socket=wayland",
        "--socket=pulseaudio",
        "--device=dri",
        "--talk-name=org.kde.StatusNotifierWatcher",
        "--env=GTK_USE_PORTAL=1",
        check=False,
    )

    for ide in IDE_OVERRIDES:
        run("flatpak", "override", "--user", "--reset", ide, check=False)
        run(
            "flatpak", "override", "--user", ide,
            "--filesystem=host",
            "--talk-name=org.freedesktop.Flatpak",
            check=False,
        )

    print("Done.")


if __name__ == "__main__":
    main()
