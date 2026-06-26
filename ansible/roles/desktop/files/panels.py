import os, re

appletsrc = os.path.expanduser("~/.config/plasma-org.kde.plasma.desktop-appletsrc")
plasmashellrc = os.path.expanduser("~/.config/plasmashellrc")

with open(appletsrc) as f:
    lines = f.readlines()

# Keep header (non-Containment lines) + screen mapping
header = [l for l in lines if not l.startswith('[Containments]')]
screendump = [l for l in lines if l.startswith('[ScreenMapping]')]

# Top panel: empty
toppanel = """\
[Containments][1]
activityId=
formfactor=2
immutability=2
lastScreen=0
location=3
plugin=org.kde.panel
wallpaperplugin=org.kde.image

[Containments][1][General]
AppletOrder=

"""

# Bottom panel: kickoff + icontasks(pinned) + spacer + systemtray
panel = """\
[Containments][2]
activityId=
formfactor=2
immutability=2
lastScreen=0
location=4
plugin=org.kde.panel
wallpaperplugin=org.kde.image

[Containments][2][Applets][3]
immutability=2
plugin=org.kde.plasma.kicker

[Containments][2][Applets][3][Configuration]
popupWidth=600

[Containments][2][Applets][5]
immutability=2
plugin=org.kde.plasma.icontasks

[Containments][2][Applets][5][Configuration][General]
iconSize=32
launchers=preferred://browser,applications:org.kde.dolphin.desktop,applications:org.kde.konsole.desktop,applications:systemsettings.desktop
groupingStrategy=1
showOnlyPinned=false

[Containments][2][Applets][6]
immutability=2
plugin=org.kde.plasma.panelspacer

[Containments][2][Applets][6][Configuration][General]
expanding=true

[Containments][2][Applets][7]
immutability=2
plugin=org.kde.plasma.digitalclock

[Containments][2][Applets][7][Configuration][General]
compactMode=true
showDate=true
showSeconds=false
use24hFormat=true

[Containments][2][Applets][9]
immutability=2
plugin=org.kde.plasma.systemtray

[Containments][2][Applets][9][Applets][10]
immutability=2
plugin=org.kde.plasma.vault

[Containments][2][Applets][9][Applets][11]
immutability=2
plugin=org.kde.kscreen

[Containments][2][Applets][9][Applets][12]
immutability=2
plugin=org.kde.plasma.cameraindicator

[Containments][2][Applets][9][Applets][13]
immutability=2
plugin=org.kde.plasma.clipboard

[Containments][2][Applets][9][Applets][14]
immutability=2
plugin=org.kde.plasma.devicenotifier

[Containments][2][Applets][9][Applets][15]
immutability=2
plugin=org.kde.plasma.keyboardindicator

[Containments][2][Applets][9][Applets][16]
immutability=2
plugin=org.kde.plasma.keyboardlayout

[Containments][2][Applets][9][Applets][17]
immutability=2
plugin=org.kde.plasma.manage-inputmethod

[Containments][2][Applets][9][Applets][18]
immutability=2
plugin=org.kde.plasma.networkmanagement

[Containments][2][Applets][9][Applets][19]
immutability=2
plugin=org.kde.plasma.notifications

[Containments][2][Applets][9][Applets][20]
immutability=2
plugin=org.kde.plasma.printmanager

[Containments][2][Applets][9][Applets][21]
immutability=2
plugin=org.kde.plasma.volume

[Containments][2][Applets][9][Applets][21][Configuration][General]
migrated=true

[Containments][2][Applets][9][Applets][22]
immutability=2
plugin=org.kde.plasma.weather

[Containments][2][Applets][9][Applets][23]
immutability=2
plugin=org.kde.plasma.brightness

[Containments][2][Applets][9][Applets][24]
immutability=2
plugin=org.kde.plasma.battery

[Containments][2][Applets][9][Applets][25]
immutability=2
plugin=org.kde.plasma.bluetooth

[Containments][2][Applets][9][General]
AppletOrder=10;11;12;13;14;15;16;17;18;25;19;20;21;22;23;24
extraItems=org.kde.plasma.vault,org.kde.kscreen,org.kde.plasma.battery,org.kde.plasma.bluetooth,org.kde.plasma.brightness,org.kde.plasma.cameraindicator,org.kde.plasma.clipboard,org.kde.plasma.devicenotifier,org.kde.plasma.keyboardindicator,org.kde.plasma.keyboardlayout,org.kde.plasma.manage-inputmethod,org.kde.plasma.mediacontroller,org.kde.plasma.networkmanagement,org.kde.plasma.notifications,org.kde.plasma.printmanager,org.kde.plasma.volume,org.kde.plasma.weather
knownItems=org.kde.plasma.vault,org.kde.kscreen,org.kde.plasma.battery,org.kde.plasma.bluetooth,org.kde.plasma.brightness,org.kde.plasma.cameraindicator,org.kde.plasma.clipboard,org.kde.plasma.devicenotifier,org.kde.plasma.keyboardindicator,org.kde.plasma.keyboardlayout,org.kde.plasma.manage-inputmethod,org.kde.plasma.mediacontroller,org.kde.plasma.networkmanagement,org.kde.plasma.notifications,org.kde.plasma.printmanager,org.kde.plasma.volume,org.kde.plasma.weather

[Containments][2][General]
AppletOrder=3;5;6;7;9

"""

with open(appletsrc, 'w') as f:
    f.writelines(header)
    f.write('\n')
    f.write(toppanel)
    f.write('\n')
    f.write(panel)
    f.write(''.join(screendump))

view = """\
[PlasmaViews][Panel 1]
floating=0
opacity=1
shell=org.kde.plasma.desktop

[PlasmaViews][Panel 1][Defaults]
thickness=32

[PlasmaViews][Panel 2]
floating=1
opacity=1
shell=org.kde.plasma.desktop

[PlasmaViews][Panel 2][Defaults]
thickness=44

"""
try:
    with open(plasmashellrc) as f:
        old = f.read()
    m = re.search(r'(\[Updates\].*)', old, re.DOTALL)
    if m:
        view += '\n' + m.group(1)
except FileNotFoundError:
    pass

with open(plasmashellrc, 'w') as f:
    f.write(view)
