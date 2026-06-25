#!/usr/bin/env bash
set -euo pipefail

echo "Installing non-system Flatpak applications..."

flatpak remote-add --if-not-exists flathub "https://dl.flathub.org/repo/flathub.flatpakrepo" 2>/dev/null || true

APPS=(
    com.discordapp.Discord
    com.slack.Slack
    com.jetbrains.IntelliJ-IDEA-Ultimate
    com.jetbrains.PyCharm-Professional
    com.jetbrains.GoLand
    com.jetbrains.WebStorm
    com.google.AndroidStudio
)

for app in "${APPS[@]}"; do
    echo "  Installing $app..."
    flatpak install -y flathub "$app" 2>/dev/null || true
done

echo "Applying Flatpak overrides..."
flatpak override --user --reset com.discordapp.Discord 2>/dev/null || true
flatpak override --user com.discordapp.Discord \
    --share=ipc \
    --socket=fallback-x11 \
    --socket=wayland \
    --socket=pulseaudio \
    --device=dri \
    --talk-name=org.kde.StatusNotifierWatcher \
    --env=GTK_USE_PORTAL=1

for ide in \
    com.jetbrains.IntelliJ-IDEA-Ultimate \
    com.jetbrains.PyCharm-Professional \
    com.jetbrains.GoLand \
    com.jetbrains.WebStorm \
    com.google.AndroidStudio; do
    flatpak override --user --reset "$ide" 2>/dev/null || true
    flatpak override --user "$ide" --filesystem=host --talk-name=org.freedesktop.Flatpak
done

echo "Done."
