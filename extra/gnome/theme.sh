#!/usr/bin/env bash
# Install and apply Nordic theme (GNOME) — refined
set -euo pipefail

REPO_URL="https://github.com/EliverLara/Nordic.git"
THEME_DIR="$HOME/.themes/Nordic"
ICON_DIR="$HOME/.icons"
CURSOR_DIR="$ICON_DIR/Nordic-cursors"
NORDIC_CURSORS_URL="https://github.com/EliverLara/Nordic/releases/download/v2.2.0/Nordic-cursors.tar.xz"

install_theme() {
  if [ ! -d "$THEME_DIR" ]; then
    echo "Cloning Nordic theme from $REPO_URL ..."
    TMPDIR=$(mktemp -d)
    trap 'rm -rf "$TMPDIR"' EXIT
    git clone --depth 1 --single-branch "$REPO_URL" "$TMPDIR/Nordic"
    mkdir -p "$HOME/.themes"
    for dir in gtk-3.0 gtk-4.0 gnome-shell metacity-1 assets; do
      if [ -d "$TMPDIR/Nordic/$dir" ]; then
        cp -r "$TMPDIR/Nordic/$dir" "$THEME_DIR/"
      fi
    done
    if [ -f "$TMPDIR/Nordic/index.theme" ]; then
      cp "$TMPDIR/Nordic/index.theme" "$THEME_DIR/"
    fi
    echo "Nordic theme installed."
  else
    echo "Nordic theme already present."
  fi

  if [ ! -d "$CURSOR_DIR" ]; then
    echo "Installing Nordic-cursors..."
    mkdir -p "$ICON_DIR"
    TMPDIR2=$(mktemp -d)
    curl -fsSL "$NORDIC_CURSORS_URL" | tar -xJ -C "$TMPDIR2"
    cp -r "$TMPDIR2/Nordic-cursors" "$ICON_DIR/"
    rm -rf "$TMPDIR2"
    echo "Nordic-cursors installed."
  fi
}

apply_theme() {
  gsettings set org.gnome.desktop.interface gtk-theme "Nordic" 2>/dev/null || true
  gsettings set org.gnome.desktop.wm.preferences theme "Nordic" 2>/dev/null || true
  gsettings set org.gnome.shell.extensions.user-theme name "Nordic" 2>/dev/null || true
  gsettings set org.gnome.desktop.interface icon-theme "Tela-circle-nord-dark" 2>/dev/null || true
  gsettings set org.gnome.desktop.interface cursor-theme "Nordic-cursors" 2>/dev/null || true
  gsettings set org.gnome.desktop.interface font-name 'Cantarell 11' 2>/dev/null || true
  gsettings set org.gnome.desktop.interface document-font-name 'Cantarell 11' 2>/dev/null || true
  gsettings set org.gnome.desktop.interface monospace-font-name 'Noto Sans Mono 11' 2>/dev/null || true
  gsettings set org.gnome.desktop.interface enable-animations false 2>/dev/null || true
  gsettings set org.gnome.desktop.interface show-battery-percentage true 2>/dev/null || true
  gsettings set org.gnome.desktop.interface clock-show-weekday true 2>/dev/null || true
  gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close' 2>/dev/null || true
  gsettings set org.gnome.desktop.wm.preferences mouse-button-modifier '<Super>' 2>/dev/null || true
  gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark' 2>/dev/null || true
}

install_theme
apply_theme
echo "Nordic GNOME theme applied."
