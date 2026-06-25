var p = new Panel()
p.alignment = 'center'
p.lengthMode = 'fit'
p.floating = true
p.location = 'bottom'
p.addWidget('org.kde.plasma.kickerdash')
var t = p.addWidget('org.kde.plasma.icontasks')
t.currentConfigGroup = ['General']
t.writeConfig('iconSize', 96)
p.writeConfig('thickness', 128)
p.writeConfig('offset', 48)
