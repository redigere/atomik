#!/usr/bin/env bash
set -euo pipefail

echo "Reverting KDE to Breeze defaults..."

systemctl --user stop plasma-plasmashell 2>/dev/null || true
killall -9 plasmashell 2>/dev/null || true
sleep 1

# Remove custom panel background
rm -f ~/.local/share/plasma/desktoptheme/Nordic/widgets/panel-background.svgz

# Remove custom look-and-feel
rm -rf ~/.local/share/look-and-feel/com.atomik.desktop

# Reset theme to Breeze
kwriteconfig6 --file kdeglobals --group "General" --key "ColorScheme" "Breeze"
kwriteconfig6 --file kdeglobals --group "KDE" --key "widgetStyle" "Breeze"
kwriteconfig6 --file kdeglobals --group "KDE" --key "LookAndFeelPackage" "org.kde.breeze.desktop"
kwriteconfig6 --file kdeglobals --group "Icons" --key "Theme" "breeze"
kwriteconfig6 --file kdeplasmarc --group "Theme" --key "name" "Breeze"

# Clear plasma cache
rm -rf ~/.cache/plasma*

systemctl --user start plasma-plasmashell
sleep 4

# Remove top panel and reset bottom panel to defaults
busctl --user call org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell evaluateScript s "
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
"

qdbus6 org.kde.KWin /KWin reconfigure 2>/dev/null || true

echo "Reverted to Breeze. Top panel removed."
