#!/usr/bin/env python3
"""Revert KDE Plasma to Breeze defaults."""

import shutil
import subprocess
import sys
import time
from pathlib import Path

HOME = Path.home()
LOCAL_SHARE = HOME / ".local/share"

KWRITE = shutil.which("kwriteconfig6") or shutil.which("kwriteconfig5")


def run(*args, check=True, **kwargs):
    return subprocess.run(args, check=check, **kwargs)


def kwrite(file, group, key, value):
    if not KWRITE:
        return
    run(KWRITE, "--file", str(file), "--group", group, "--key", key, str(value),
        capture_output=True, check=False)


def main():
    run("systemctl", "--user", "stop", "plasma-plasmashell", check=False)
    run("killall", "-9", "plasmashell", check=False)
    time.sleep(1)

    bg = LOCAL_SHARE / "plasma" / "desktoptheme" / "Nordic" / "widgets" / "panel-background.svgz"
    bg.unlink(missing_ok=True)

    lf_dir = LOCAL_SHARE / "look-and-feel" / "com.atomik.desktop"
    shutil.rmtree(lf_dir, ignore_errors=True)

    kwrite("kdeglobals", "General", "ColorScheme", "Breeze")
    kwrite("kdeglobals", "KDE", "widgetStyle", "Breeze")
    kwrite("kdeglobals", "KDE", "LookAndFeelPackage", "org.kde.breeze.desktop")
    kwrite("kdeglobals", "Icons", "Theme", "breeze")
    kwrite("kdeplasmarc", "Theme", "name", "Breeze")

    cache = HOME / ".cache"
    for p in cache.glob("plasma*"):
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)

    run("systemctl", "--user", "start", "plasma-plasmashell")
    time.sleep(4)

    script = """
    var ps = panels();
    for (var i = ps.length - 1; i >= 0; i--) {
        var p = ps[i];
        if (p.location === 'top') {
            p.remove();
        } else {
            p.hiding = 'none';
            p.lengthMode = 'fill';
            p.alignment = 'center';
            p.offset = 0;
            p.floating = false;
            p.immutability = 0;
        }
    }
    """
    run("busctl", "--user", "call", "org.kde.plasmashell", "/PlasmaShell",
        "org.kde.PlasmaShell", "evaluateScript", "s", script, check=False)

    run("qdbus6", "org.kde.KWin", "/KWin", "reconfigure", check=False)
    print("Reverted to Breeze. Top panel removed.")


if __name__ == "__main__":
    main()
