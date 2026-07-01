#!/usr/bin/env python3
"""Apply KDE Plasma panels, theme, and Nordic configuration."""

import gzip
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("kde")

SCRIPT_DIR = Path(__file__).resolve().parent
HOME = Path.home()
CONFIG = HOME / ".config"
LOCAL_SHARE = HOME / ".local/share"
LF_DIR = LOCAL_SHARE / "look-and-feel" / "com.atomik.desktop"

KWRITE = shutil.which("kwriteconfig6") or shutil.which("kwriteconfig5")


def run(*args, check=True, **kwargs):
    return subprocess.run(args, check=check, **kwargs)


def kwrite(file, group, key, value):
    if not KWRITE:
        return
    run(KWRITE, "--file", str(file), "--group", group, "--key", key, str(value),
        capture_output=True, check=False)


def stop_plasma():
    run("systemctl", "--user", "stop", "plasma-plasmashell", check=False)
    run("killall", "-9", "plasmashell", check=False)
    time.sleep(1)


def start_plasma():
    run("systemctl", "--user", "start", "plasma-plasmashell")
    time.sleep(4)


def deploy_panel_background():
    dest = LOCAL_SHARE / "plasma" / "desktoptheme" / "Nordic" / "widgets"
    dest.mkdir(parents=True, exist_ok=True)
    svg = SCRIPT_DIR / "panel-background.svg"
    if svg.exists():
        with open(svg, "rb") as f_in, gzip.open(dest / "panel-background.svgz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def deploy_look_and_feel():
    LF_DIR.mkdir(parents=True, exist_ok=True)
    src_lf = SCRIPT_DIR / "look-and-feel" / "com.atomik.desktop"
    if src_lf.exists():
        for item in src_lf.rglob("*"):
            if item.is_file():
                rel = item.relative_to(src_lf)
                dest = LF_DIR / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)


def run_panels_script():
    panels_py = SCRIPT_DIR / "panels.py"
    if panels_py.exists():
        run(sys.executable, str(panels_py), check=False)
        cache = HOME / ".cache"
        for p in cache.glob("plasma*"):
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)


def lock_panels_via_dbus():
    script = """
    var ps = panels();
    for (var i = 0; i < ps.length; i++) {
        var p = ps[i];
        p.lengthMode = 'fill';
        p.alignment = 'center';
        p.offset = 0;
        p.hiding = 'none';
        p.immutability = 2;
    }
    """
    run("busctl", "--user", "call", "org.kde.plasmashell", "/PlasmaShell",
        "org.kde.PlasmaShell", "evaluateScript", "s", script, check=False)


def apply_theme_settings():
    kwrite("kdeglobals", "General", "theme", "Nordic")
    kwrite("kdeglobals", "General", "ColorScheme", "Nordic")
    kwrite("kdeglobals", "General", "font", "Cantarell 11")
    kwrite("kdeglobals", "General", "fixed", "Noto Sans Mono 11")
    kwrite("kdeglobals", "Icons", "IconTheme", "Tela-circle-nord-dark")
    kwrite("kdeglobals", "Icons", "cursorTheme", "Nordic-cursors")
    kwrite("kdeglobals", "KDE", "LookAndFeelPackage", "com.atomik.desktop")
    kwrite("kdeglobals", "KDE", "DefaultDarkLookAndFeel", "com.atomik.desktop")
    kwrite("kdeglobals", "KDE", "widgetStyle", "Kvantum")
    kwrite("kdeglobals", "General", "TerminalApplication", "konsole")
    kwrite(CONFIG / "kwinrc", "org.kde.kdecoration2", "library", "org.kde.kwin.aurorae")
    kwrite(CONFIG / "kwinrc", "org.kde.kdecoration2", "theme", "__aurorae__svg__Nordic")
    kwrite(CONFIG / "kwinrc", "org.kde.kdecoration2", "BorderSize", "Tiny")
    kwrite(CONFIG / "kwinrc", "org.kde.kdecoration2", "CustomButtonPositions", "true")
    kwrite(CONFIG / "kwinrc", "org.kde.kdecoration2", "LeftButtons", "")
    kwrite(CONFIG / "kwinrc", "org.kde.kdecoration2", "RightButtons", "M,S,C")
    kwrite(CONFIG / "kwinrc", "Windows", "TitlebarDoubleClickCommand", "Maximize")
    kwrite(CONFIG / "kwinrc", "Compositing", "OpenGLIsUnsafe", "false")
    kwrite(CONFIG / "kwinrc", "Compositing", "Backend", "OpenGL")
    kwrite(CONFIG / "kwinrc", "Compositing", "MaxFps", "144")
    kwrite(CONFIG / "kwinrc", "Compositing", "VSync", "none")
    kwrite(CONFIG / "kcminputrc", "LibInput", "NaturalScroll", "true")
    kwrite(CONFIG / "breezerc", "Common", "ColorScheme", "Nordic")
    kwrite("kdeglobals", "General", "EmojiFont", "Noto Color Emoji")
    kwrite("ksplashrc", "KSplash", "Engine", "none")
    kwrite("ksplashrc", "KSplash", "Theme", "none")
    kwrite("konsolerc", "Desktop Entry", "DefaultProfile", "Nordic.profile")
    kwrite("kdeglobals", "KDE", "AnimationDurationFactor", "0")


def deploy_konsole_theme():
    konsole_dir = LOCAL_SHARE / "konsole"
    konsole_dir.mkdir(parents=True, exist_ok=True)

    colorscheme = konsole_dir / "Nordic.colorscheme"
    if not colorscheme.exists():
        colorscheme.write_text("""[Background]
Color=46,52,64
[BackgroundFaint]
Color=46,52,64
[BackgroundIntense]
Color=46,52,64
[Foreground]
Color=216,222,233
[ForegroundFaint]
Color=216,222,233
[ForegroundIntense]
Color=216,222,233
[General]
Description=Nordic
Opacity=0.95
Wallpaper=
[Color0]
Color=59,66,82
[Color0Faint]
Color=59,66,82
[Color0Intense]
Color=76,86,106
[Color1]
Color=191,97,106
[Color1Faint]
Color=191,97,106
[Color1Intense]
Color=191,97,106
[Color2]
Color=163,190,140
[Color2Faint]
Color=163,190,140
[Color2Intense]
Color=163,190,140
[Color3]
Color=235,203,139
[Color3Faint]
Color=235,203,139
[Color3Intense]
Color=235,203,139
[Color4]
Color=129,161,193
[Color4Faint]
Color=129,161,193
[Color4Intense]
Color=129,161,193
[Color5]
Color=180,142,173
[Color5Faint]
Color=180,142,173
[Color5Intense]
Color=180,142,173
[Color6]
Color=136,192,208
[Color6Faint]
Color=136,192,208
[Color6Intense]
Color=136,192,208
[Color7]
Color=229,229,229
[Color7Faint]
Color=229,229,229
[Color7Intense]
Color=255,255,255
""")

    profile = konsole_dir / "Nordic.profile"
    if not profile.exists():
        profile.write_text("""[Appearance]
ColorScheme=Nordic
Font=Noto Sans Mono,11
[General]
Name=Nordic
Parent=FALLBACK/
TerminalCenter=false
TerminalRows=40
TerminalColumns=120
[Scrolling]
HistoryMode=2
HistorySize=10000
[TerminalFeatures]
BlinkingCursorEnabled=false
""")


def reconfigure_kwin():
    run("qdbus6", "org.kde.KWin", "/KWin", "reconfigure", check=False)


def is_kde():
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if "kde" in desktop or "plasma" in desktop:
        return True
    session = os.environ.get("DESKTOP_SESSION", "").lower()
    if "kde" in session or "plasma" in session:
        return True
    return shutil.which("plasmashell") is not None


def main():
    if not is_kde():
        log.info("skipping: not running on KDE Plasma")
        return
    stop_plasma()
    deploy_panel_background()
    run_panels_script()
    deploy_look_and_feel()
    start_plasma()
    lock_panels_via_dbus()
    apply_theme_settings()
    deploy_konsole_theme()
    reconfigure_kwin()
    log.info("done")


if __name__ == "__main__":
    main()
