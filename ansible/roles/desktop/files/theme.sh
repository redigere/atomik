#!/usr/bin/env bash
set -euo pipefail

# Window decorations (Nordic theme, buttons on right)
kwriteconfig6 --file "$HOME/.config/kwinrc" --group "org.kde.kdecoration2" --key "library" "org.kde.kwin.aurorae"
kwriteconfig6 --file "$HOME/.config/kwinrc" --group "org.kde.kdecoration2" --key "theme" "__aurorae__svg__Nordic"

# Title bar buttons: minimize, maximize, close on the right
kwriteconfig6 --file "$HOME/.config/kwinrc" --group "org.kde.kdecoration2" --key "BorderSize" "Tiny"
kwriteconfig6 --file "$HOME/.config/kwinrc" --group "org.kde.kdecoration2" --key "CustomButtonPositions" "true"
kwriteconfig6 --file "$HOME/.config/kwinrc" --group "org.kde.kdecoration2" --key "LeftButtons" ""
kwriteconfig6 --file "$HOME/.config/kwinrc" --group "org.kde.kdecoration2" --key "RightButtons" "M,S,C"

# Window behavior
kwriteconfig6 --file "$HOME/.config/kwinrc" --group "Windows" --key "TitlebarDoubleClickCommand" "Maximize"

# Compositor settings
kwriteconfig6 --file "$HOME/.config/kwinrc" --group "Compositing" --key "OpenGLIsUnsafe" "false"
kwriteconfig6 --file "$HOME/.config/kwinrc" --group "Compositing" --key "Backend" "OpenGL"

# Mouse/touchpad
kwriteconfig6 --file "$HOME/.config/kcminputrc" --group "LibInput" --key "NaturalScroll" "true"

# Color scheme, icons, global theme
kwriteconfig6 --file kdeglobals --group "General" --key "ColorScheme" "Nordic"
kwriteconfig6 --file kdeglobals --group "Icons" --key "Theme" "Tela-circle-nord-dark"
kwriteconfig6 --file kdeglobals --group "KDE" --key "widgetStyle" "Breeze"
kwriteconfig6 --file kdeglobals --group "KDE" --key "LookAndFeelPackage" "com.atomik.desktop"
kwriteconfig6 --file kdeglobals --group "KDE" --key "DefaultDarkLookAndFeel" "com.atomik.desktop"

# Breeze style
kwriteconfig6 --file "$HOME/.config/breezerc" --group "Common" --key "ColorScheme" "Nordic"

# Fonts
kwriteconfig6 --file kdeglobals --group "General" --key "font" "Noto Sans,11,-1,5,50,0,0,0,0,0"
kwriteconfig6 --file kdeglobals --group "General" --key "fixed" "Noto Sans Mono,11,-1,5,50,0,0,0,0,0"
kwriteconfig6 --file kdeglobals --group "General" --key "smallestReadableFont" "Noto Sans,9,-1,5,50,0,0,0,0,0"

# Noto Color Emoji for emoji
kwriteconfig6 --file kdeglobals --group "General" --key "EmojiFont" "Noto Color Emoji"

qdbus6 org.kde.KWin /KWin reconfigure 2>/dev/null || true
