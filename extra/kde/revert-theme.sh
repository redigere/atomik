#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Reverting to original KDE theme..."

# Stop plasmashell
systemctl --user stop plasma-plasmashell 2>/dev/null || true
killall -9 plasmashell 2>/dev/null || true
sleep 1

# Remove custom panel background
rm -f ~/.local/share/plasma/desktoptheme/Nordic/widgets/panel-background.svgz

# Remove custom look-and-feel
rm -rf ~/.local/share/look-and-feel/com.atomik.desktop

# Clear plasma cache
rm -rf ~/.cache/plasma*

# Restart plasmashell with default config
systemctl --user start plasma-plasmashell
sleep 4

# Reset panel properties to defaults
busctl --user call org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell evaluateScript s "
var ps = panels();
for (var i = 0; i < ps.length; i++) {
    var p = ps[i];
    p.hiding = 'none';
    p.lengthMode = 'fill';
    p.alignment = 'center';
    p.offset = 0;
    p.floating = false;
    p.immutability = 0;
}
"

echo "Theme reverted to defaults."
