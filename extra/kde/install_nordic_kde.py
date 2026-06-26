#!/usr/bin/env python3
"""Clone and install Nordic, Nordic-kDE, and Tela-circle themes from source."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOME = Path.home()
LOCAL_SHARE = HOME / ".local/share"
SCRIPT_DIR = Path(__file__).resolve().parent


def run(*args, check=True, **kwargs):
    return subprocess.run(args, check=check, **kwargs)


def git_clone(url, dest):
    if dest.exists():
        shutil.rmtree(dest)
    run("git", "clone", "--depth", "1", url, str(dest))


def main():
    tmp = tempfile.mkdtemp()
    tmpdir = Path(tmp)
    try:
        git_clone("https://github.com/EliverLara/Nordic.git", tmpdir / "Nordic")
        git_clone("https://github.com/EliverLara/Nordic-kDE.git", tmpdir / "Nordic-kDE")
        git_clone("https://github.com/vinceliuice/Tela-circle-icon-theme.git", tmpdir / "Tela-circle")

        desktop_theme = LOCAL_SHARE / "plasma" / "desktoptheme" / "Nordic"
        shutil.rmtree(desktop_theme, ignore_errors=True)
        shutil.copytree(tmpdir / "Nordic-kDE", desktop_theme)

        plasmarc = desktop_theme / "plasmarc"
        plasmarc.write_text("""[Wallpaper]
defaultWallpaperTheme=Next
defaultFileSuffix=.png
defaultWidth=1920
defaultHeight=1080
[AdaptiveTransparency]
enabled=true
""")

        lf_src = tmpdir / "Nordic" / "kde" / "plasma" / "look-and-feel" / "Nordic"
        lf_dst = LOCAL_SHARE / "plasma" / "look-and-feel" / "Nordic"
        shutil.rmtree(lf_dst, ignore_errors=True)
        if lf_src.exists():
            shutil.copytree(lf_src, lf_dst)

        colors_dir = LOCAL_SHARE / "color-schemes"
        colors_dir.mkdir(parents=True, exist_ok=True)
        for f in (tmpdir / "Nordic" / "kde" / "colorschemes").glob("*.colors"):
            shutil.copy2(f, colors_dir)

        aurorae_src = tmpdir / "Nordic" / "kde" / "aurorae" / "Nordic"
        aurorae_dst = LOCAL_SHARE / "aurorae" / "themes" / "Nordic"
        shutil.rmtree(aurorae_dst, ignore_errors=True)
        if aurorae_src.exists():
            shutil.copytree(aurorae_src, aurorae_dst)

        konsole_dir = LOCAL_SHARE / "konsole"
        konsole_dir.mkdir(parents=True, exist_ok=True)
        konsole_src = tmpdir / "Nordic" / "kde" / "konsole" / "Nordic.colorscheme"
        if konsole_src.exists():
            shutil.copy2(konsole_src, konsole_dir)

        kvantum_src = tmpdir / "Nordic" / "kde" / "kvantum" / "Nordic"
        kvantum_dst = LOCAL_SHARE / "Kvantum" / "Nordic"
        shutil.rmtree(kvantum_dst, ignore_errors=True)
        if kvantum_src.exists():
            shutil.copytree(kvantum_src, kvantum_dst)

        icons_dir = LOCAL_SHARE / "icons"
        icons_dir.mkdir(parents=True, exist_ok=True)
        tela_src = tmpdir / "Tela-circle"
        for variant in ["Tela-circle", "Tela-circle-nord"]:
            src = tela_src / variant
            dst = icons_dir / variant
            shutil.rmtree(dst, ignore_errors=True)
            if src.exists():
                shutil.copytree(src, dst)

        run("plasma-apply-desktoptheme", "Nordic", check=False)
        run("plasma-apply-colorscheme", "Nordic", check=False)

        apply_py = SCRIPT_DIR / "apply_kde.py"
        if apply_py.exists():
            run(sys.executable, str(apply_py))

        profile = konsole_dir / "Nordic.profile"
        profile.write_text("""[Appearance]
ColorScheme=Nordic
Font=Noto Sans Mono,11
[General]
Name=Nordic
Parent=FALLBACK/
""")

        js = ""
        for js_file in ["topbar.js", "dock.js"]:
            fp = SCRIPT_DIR / js_file
            if fp.exists():
                js += fp.read_text() + "\n"

        if js.strip():
            subprocess.run(
                ["busctl", "--user", "call", "org.kde.plasmashell", "/PlasmaShell",
                 "org.kde.PlasmaShell", "evaluateScript", "s", js],
                check=False,
            )

        print("Nordic KDE installed from source.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
