#!/usr/bin/env bash
# Apply GNOME macOS-like configuration — refined
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

bash "$SCRIPT_DIR/theme.sh"

# Interface
gsettings set org.gnome.desktop.interface font-name 'Cantarell 11' 2>/dev/null || true
gsettings set org.gnome.desktop.interface document-font-name 'Cantarell 11' 2>/dev/null || true
gsettings set org.gnome.desktop.interface monospace-font-name 'Noto Sans Mono 11' 2>/dev/null || true
gsettings set org.gnome.desktop.interface enable-animations false 2>/dev/null || true
gsettings set org.gnome.desktop.interface show-battery-percentage true 2>/dev/null || true
gsettings set org.gnome.desktop.interface clock-show-weekday true 2>/dev/null || true
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark' 2>/dev/null || true

# Window manager
gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close' 2>/dev/null || true
gsettings set org.gnome.desktop.wm.preferences mouse-button-modifier '<Super>' 2>/dev/null || true

# Privacy
gsettings set org.gnome.desktop.privacy send-technical-reports false 2>/dev/null || true
gsettings set org.gnome.desktop.privacy report-technical-problems false 2>/dev/null || true
gsettings set org.gnome.desktop.privacy hide-identity true 2>/dev/null || true
gsettings set org.gnome.desktop.privacy old-power-menu true 2>/dev/null || true
gsettings set org.gnome.desktop.privacy show-full-name-in-top-bar false 2>/dev/null || true

# Peripherals
gsettings set org.gnome.desktop.peripherals.touchpad natural-scroll true 2>/dev/null || true
gsettings set org.gnome.desktop.peripherals.touchpad tap-to-click true 2>/dev/null || true

# Dash to Dock (macOS-style bottom dock)
gsettings set org.gnome.shell.extensions.dash-to-dock dock-position BOTTOM 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock dash-max-icon-size 48 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock extend-height false 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock show-trash false 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock show-mounts false 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock show-show-apps-button true 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock autohide-in-fullscreen true 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock intellihide false 2>/dev/null || true
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize' 2>/dev/null || true

# Workspace
gsettings set org.gnome.desktop.wm.preferences num-workspaces 4 2>/dev/null || true
gsettings set org.gnome.mutter dynamic-workspaces false 2>/dev/null || true
gsettings set org.gnome.mutter edge-tiling true 2>/dev/null || true

# Night light
gsettings set org.gnome.settings-daemon.plugins.color night-light-enabled true 2>/dev/null || true
gsettings set org.gnome.settings-daemon.plugins.color night-light-temperature 3800 2>/dev/null || true

# Media keys
gsettings set org.gnome.settings-daemon.plugins.media-keys max-screencast-length 30 2>/dev/null || true

# File manager
gsettings set org.gnome.nautilus.preferences show-directory-item-counts 'never' 2>/dev/null || true
gsettings set org.gnome.nautilus.preferences default-folder-viewer 'list-view' 2>/dev/null || true
gsettings set org.gnome.nautilus.list-view default-zoom-level 'small' 2>/dev/null || true

# Search
gsettings set org.gnome.desktop.search-providers disable-external true 2>/dev/null || true

echo "GNOME config applied."
