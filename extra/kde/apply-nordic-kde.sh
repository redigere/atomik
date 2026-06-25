#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

git clone --depth 1 https://github.com/EliverLara/Nordic.git "$TMPDIR/Nordic"
git clone --depth 1 https://github.com/EliverLara/Nordic-kDE.git "$TMPDIR/Nordic-kDE"
git clone --depth 1 https://github.com/vinceliuice/Tela-circle-icon-theme.git "$TMPDIR/Tela-circle"

mkdir -p "$HOME/.local/share/plasma/desktoptheme/Nordic"
cp -r "$TMPDIR/Nordic-kDE/"* "$HOME/.local/share/plasma/desktoptheme/Nordic/"
cat > "$HOME/.local/share/plasma/desktoptheme/Nordic/plasmarc" << 'PLASMARC'
[Wallpaper]
defaultWallpaperTheme=Next
defaultFileSuffix=.png
defaultWidth=1920
defaultHeight=1080
[AdaptiveTransparency]
enabled=true
PLASMARC
cp -r "$TMPDIR/Nordic/kde/plasma/look-and-feel/Nordic" "$HOME/.local/share/plasma/look-and-feel/"
mkdir -p "$HOME/.local/share/color-schemes"
cp "$TMPDIR/Nordic/kde/colorschemes/"*.colors "$HOME/.local/share/color-schemes/"
mkdir -p "$HOME/.local/share/aurorae/themes"
cp -r "$TMPDIR/Nordic/kde/aurorae/Nordic" "$HOME/.local/share/aurorae/themes/"
mkdir -p "$HOME/.local/share/konsole"
cp "$TMPDIR/Nordic/kde/konsole/Nordic.colorscheme" "$HOME/.local/share/konsole/"
mkdir -p "$HOME/.local/share/Kvantum"
cp -r "$TMPDIR/Nordic/kde/kvantum/Nordic" "$HOME/.local/share/Kvantum/" 2>/dev/null || true
cd "$TMPDIR/Tela-circle" && bash install.sh nord 2>/dev/null

plasma-apply-desktoptheme Nordic 2>/dev/null
plasma-apply-colorscheme Nordic 2>/dev/null

bash "$SCRIPT_DIR/extra/kde/theme.sh"

mkdir -p "$HOME/.local/share/konsole"
cat > "$HOME/.local/share/konsole/Nordic.profile" << 'PROFILE'
[Appearance]
ColorScheme=Nordic
Font=Noto Sans Mono,11
[General]
Name=Nordic
Parent=FALLBACK/
PROFILE

JS=$(cat "$SCRIPT_DIR/extra/kde/topbar.js")
JS="$JS"$'\n'"$(cat "$SCRIPT_DIR/extra/kde/dock.js")"
busctl --user call org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell evaluateScript s "$JS"
sleep 2

python3 << 'PYEOF'
cfg = "/var/home/alessio.attilio/.config/plasma-org.kde.plasma.desktop-appletsrc"
with open(cfg, 'r') as f:
    lines = f.readlines()

dock_keys = {'thickness=128', 'offset=48'}
dock_start = None
for i, line in enumerate(lines):
    if line.rstrip().startswith('[Containments][') and ']' in line and 'Applets' not in line and 'General' not in line:
        for j in range(i+1, min(i+10, len(lines))):
            if lines[j].startswith('location=4'):
                dock_start = i
                break

if dock_start is not None:
    sec_end = len(lines)
    for j in range(dock_start+1, len(lines)):
        if lines[j].startswith('[') and 'Applets' not in lines[j]:
            sec_end = j
            break

    keys_in_sec = set()
    for j in range(dock_start+1, sec_end):
        stripped = lines[j].strip()
        if '=' in stripped and not stripped.startswith('['):
            k = stripped.split('=', 1)[0]
            keys_in_sec.add(k)

    insert_at = dock_start + 1
    for k in sorted(dock_keys):
        k_name = k.split('=', 1)[0]
        if k_name not in keys_in_sec:
            lines.insert(insert_at, k + '\n')
            insert_at += 1
        else:
            for j in range(dock_start+1, sec_end):
                if lines[j].strip().startswith(k_name + '='):
                    lines[j] = k + '\n'
                    break

    with open(cfg, 'w') as f:
        f.writelines(lines)

PYEOF
