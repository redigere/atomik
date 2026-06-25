#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LF_DIR="$HOME/.local/share/look-and-feel/com.atomik.desktop"

systemctl --user stop plasma-plasmashell 2>/dev/null || true
killall -9 plasmashell 2>/dev/null || true
sleep 1

# Deploy panel background SVG (gradient fade, no hard edges)
mkdir -p ~/.local/share/plasma/desktoptheme/Nordic/widgets
gzip -c "$SCRIPT_DIR/panel-background.svg" > ~/.local/share/plasma/desktoptheme/Nordic/widgets/panel-background.svgz 2>/dev/null || true

# Write panel config
python3 "$SCRIPT_DIR/panels.py"
rm -rf ~/.cache/plasma*

# Install custom look-and-feel
mkdir -p "$LF_DIR/contents"
cp "$SCRIPT_DIR/look-and-feel/com.atomik.desktop/metadata.json" "$LF_DIR/"
cp "$SCRIPT_DIR/look-and-feel/com.atomik.desktop/contents/defaults" "$LF_DIR/contents/"

systemctl --user start plasma-plasmashell
sleep 4

# Lock runtime properties (alignment, centering, autohide)
busctl --user call org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell evaluateScript s "
var ps = panels();
for (var i = 0; i < ps.length; i++) {
    if (ps[i].location == 'bottom') {
        var p = ps[i];
p.lengthMode = 'fill';
        p.alignment = 'center';
        p.offset = 0;
        p.hiding = 'none';
        p.immutability = 2;
    }
}
"

bash "$SCRIPT_DIR/theme.sh"
