#!/usr/bin/env bash
set -euo pipefail

# Nordic-cursors: skip if not available (upstream repo removed)
CURSOR_DIR="$HOME/.icons/Nordic-cursors"
if [ ! -d "$CURSOR_DIR" ]; then
  echo "Warning: Nordic-cursors not found. Install manually or use another cursor theme."
fi

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
kwriteconfig6 --file kdeglobals --group "Icons" --key "cursorTheme" "Nordic-cursors"
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

# Konsole profile: set up Nordic color scheme
mkdir -p "$HOME/.local/share/konsole"
if [ ! -f "$HOME/.local/share/konsole/Nordic.colorscheme" ]; then
  cat > "$HOME/.local/share/konsole/Nordic.colorscheme" << 'EOF'
[Background]
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
EOF
fi

# Konsole profile: use Nordic colors + Fish shell
kwriteconfig6 --file "$HOME/.local/share/konsole/konsolerc" --group "Desktop Entry" --key "DefaultProfile" "Nordic.profile"
mkdir -p "$HOME/.local/share/konsole"
if [ ! -f "$HOME/.local/share/konsole/Nordic.profile" ]; then
  cat > "$HOME/.local/share/konsole/Nordic.profile" << 'EOF'
[Appearance]
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
EOF
fi

qdbus6 org.kde.KWin /KWin reconfigure 2>/dev/null || true

echo "Nordic KDE theme applied."
