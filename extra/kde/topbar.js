var existing = panels()
for (var i = existing.length - 1; i >= 0; i--)
    existing[i].remove()
var p = new Panel()
p.alignment = 'center'
p.lengthMode = 'fill'
p.floating = false
p.location = 'top'
p.addWidget('org.kde.plasma.notifications')
var s1 = p.addWidget('org.kde.plasma.panelspacer')
s1.currentConfigGroup = ['General']
s1.writeConfig('expanding', 'true')
p.addWidget('org.kde.plasma.datetime')
var s2 = p.addWidget('org.kde.plasma.panelspacer')
s2.currentConfigGroup = ['General']
s2.writeConfig('expanding', 'true')
p.addWidget('org.kde.plasma.systemtray')
