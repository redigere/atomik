#!/usr/bin/env python3
"""Install Nordic GTK theme and apply GNOME macOS-like configuration."""

import io
import logging
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("gnome")

HOME = Path.home()
THEME_DIR = HOME / ".themes" / "Nordic"
ICON_DIR = HOME / ".icons"
CURSOR_DIR = ICON_DIR / "Nordic-cursors"

REPO_URL = "https://github.com/EliverLara/Nordic.git"
CURSORS_URL = "https://github.com/EliverLara/Nordic/releases/download/v2.2.0/Nordic-cursors.tar.xz"


def run(*args, check=False, **kwargs):
    return subprocess.run(args, check=check, **kwargs)


def gset(schema, key, value):
    run("gsettings", "set", schema, key, value, check=False)


def install_theme():
    if THEME_DIR.exists():
        return
    log.info("installing Nordic theme")
    tmp = tempfile.mkdtemp()
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "--single-branch", REPO_URL, f"{tmp}/Nordic"],
            check=True,
        )
        THEME_DIR.mkdir(parents=True, exist_ok=True)
        for subdir in ["gtk-3.0", "gtk-4.0", "gnome-shell", "metacity-1", "assets"]:
            src = Path(tmp) / "Nordic" / subdir
            if src.exists():
                shutil.copytree(src, THEME_DIR / subdir, dirs_exist_ok=True)
        index = Path(tmp) / "Nordic" / "index.theme"
        if index.exists():
            shutil.copy2(index, THEME_DIR)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if CURSOR_DIR.exists():
        return
    log.info("installing Nordic-cursors")
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    tmp2 = tempfile.mkdtemp()
    try:
        req = urllib.request.Request(CURSORS_URL, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req).read()
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:xz") as tar:
            tar.extractall(path=tmp2)
        src_cursor = Path(tmp2) / "Nordic-cursors"
        if src_cursor.exists():
            shutil.copytree(src_cursor, CURSOR_DIR, dirs_exist_ok=True)
    finally:
        shutil.rmtree(tmp2, ignore_errors=True)


def apply_settings():
    gset("org.gnome.desktop.interface", "gtk-theme", "'Nordic'")
    gset("org.gnome.desktop.wm.preferences", "theme", "'Nordic'")
    gset("org.gnome.shell.extensions.user-theme", "name", "'Nordic'")
    gset("org.gnome.desktop.interface", "icon-theme", "'Tela-circle-nord-dark'")
    gset("org.gnome.desktop.interface", "cursor-theme", "'Nordic-cursors'")
    gset("org.gnome.desktop.interface", "font-name", "'Cantarell 11'")
    gset("org.gnome.desktop.interface", "document-font-name", "'Cantarell 11'")
    gset("org.gnome.desktop.interface", "monospace-font-name", "'Noto Sans Mono 11'")
    gset("org.gnome.desktop.interface", "enable-animations", "false")
    gset("org.gnome.desktop.interface", "show-battery-percentage", "true")
    gset("org.gnome.desktop.interface", "clock-show-weekday", "true")
    gset("org.gnome.desktop.interface", "color-scheme", "'prefer-dark'")
    gset("org.gnome.desktop.wm.preferences", "button-layout", "':minimize,maximize,close'")
    gset("org.gnome.desktop.wm.preferences", "mouse-button-modifier", "'<Super>'")
    gset("org.gnome.desktop.privacy", "send-technical-reports", "false")
    gset("org.gnome.desktop.privacy", "report-technical-problems", "false")
    gset("org.gnome.desktop.privacy", "hide-identity", "true")
    gset("org.gnome.desktop.privacy", "show-full-name-in-top-bar", "false")
    gset("org.gnome.desktop.peripherals.touchpad", "natural-scroll", "true")
    gset("org.gnome.desktop.peripherals.touchpad", "tap-to-click", "true")
    gset("org.gnome.shell.extensions.dash-to-dock", "dock-position", "BOTTOM")
    gset("org.gnome.shell.extensions.dash-to-dock", "dash-max-icon-size", "48")
    gset("org.gnome.shell.extensions.dash-to-dock", "extend-height", "false")
    gset("org.gnome.shell.extensions.dash-to-dock", "show-trash", "false")
    gset("org.gnome.shell.extensions.dash-to-dock", "show-mounts", "false")
    gset("org.gnome.shell.extensions.dash-to-dock", "show-show-apps-button", "true")
    gset("org.gnome.shell.extensions.dash-to-dock", "autohide-in-fullscreen", "true")
    gset("org.gnome.shell.extensions.dash-to-dock", "intellihide", "false")
    gset("org.gnome.shell.extensions.dash-to-dock", "click-action", "'minimize'")
    gset("org.gnome.shell.extensions.dash-to-dock", "background-opacity", "0.25")
    gset("org.gnome.desktop.wm.preferences", "num-workspaces", "4")
    gset("org.gnome.mutter", "dynamic-workspaces", "false")
    gset("org.gnome.mutter", "edge-tiling", "true")
    gset("org.gnome.settings-daemon.plugins.color", "night-light-enabled", "true")
    gset("org.gnome.settings-daemon.plugins.color", "night-light-temperature", "3800")
    gset("org.gnome.settings-daemon.plugins.media-keys", "max-screencast-length", "30")
    gset("org.gnome.nautilus.preferences", "show-directory-item-counts", "'never'")
    gset("org.gnome.nautilus.preferences", "default-folder-viewer", "'list-view'")
    gset("org.gnome.nautilus.list-view", "default-zoom-level", "'small'")
    gset("org.gnome.desktop.search-providers", "disable-external", "true")
    gset("org.gnome.desktop.sound", "event-sounds", "false")


def is_gnome():
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if "gnome" in desktop or "unity" in desktop or "gnome-flashback" in desktop:
        return True
    session = os.environ.get("DESKTOP_SESSION", "").lower()
    if "gnome" in session:
        return True
    return shutil.which("gnome-session") is not None


def main():
    if not is_gnome():
        log.info("skipping: not running on GNOME")
        return
    install_theme()
    apply_settings()
    log.info("done")


if __name__ == "__main__":
    main()
