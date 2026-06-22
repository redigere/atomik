const ps = panels();
if (ps.length > 0) {
    const p = ps[0];
    p.location = 'left';
    p.lengthMode = 'fill';
    p.alignment = 'center';
    p.floating = true;
    const ws = p.widgets();
    for (let i = 0; i < ws.length; ++i) {
        ws[i].remove();
    }
    let w = p.addWidget('org.kde.plasma.kickerdash');
    w.currentConfigGroup = ['General'];
    w.writeConfig('icon', 'start-here-kde');
    p.addWidget('org.kde.plasma.icontasks');
    w = p.addWidget('org.kde.plasma.panelspacer');
    w.currentConfigGroup = ['General'];
    w.writeConfig('expanding', false);
    w.writeConfig('length', 16);
    p.addWidget('org.kde.plasma.systemtray');
    p.addWidget('org.kde.plasma.digitalclock');
}
