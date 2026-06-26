# Atomik Full-Nordic Roadmap — Sprint Operativi

Roadmap per l'ecosistema desktop **Full-Nordic**: KDE Plasma 6 + GNOME 47+ con tuning estremo delle prestazioni.
Tutti i parametri di configurazione vivono in `group_vars/all.yml`; i playbook sono puri esecutori.

---

## Sprint 0: Asset & Palette Unification

**Obiettivo:** Definire la palette Nordic vincolante per TUTTI i componenti ed eliminare derive cromatiche.

| Attività | File | Dettagli |
|---|---|---|
| Definire palette rigida | `docs/NORDIC_PALETTE.md` | 16 colori esadecimali (nord0–nord15) + 4 tonalità frost + aurora |
| Verificare coerenza icone | Audit `Tela-circle-nord-dark` | Sovrascrivere eventuali icone fuori palette con template SVG custom |
| Campionare Nordic-kDE repo | `extra/kde/install_nordic_kde.py` | Estrarre i colori esatti usati da Aurorae e aggiornare palette |
| Generare wallpaper unificato | `files/wallpaper/` | Wallpaper gradient SVG/Fluid nord + variante solida notte |
| Audit asset esistenti | Tutti i file `.svg`, `.svgz` | Convertire a palette esatta |

**Nordic Palette Canonica:**
```
nord0  #2e3440  (nero polar notte)
nord1  #3b4252  (grigio scuro)
nord2  #434c5e  (grigio medio)
nord3  #4c566a  (grigio chiaro)
nord4  #d8dee9  (bianco neve)
nord5  #e5e9f0  (bianco tempesta)
nord6  #eceff4  (bianco puro)
nord7  #8fbcbb  (frost 1 - verde acqua)
nord8  #88c0d0  (frost 2 - azzurro ghiaccio)
nord9  #81a1c1  (frost 3 - blu ghiaccio)
nord10 #5e81ac  (frost 4 - blu scuro)
nord11 #bf616a  (aurora rosso)
nord12 #d08770  (aurora arancio)
nord13 #ebcb8b  (aurora giallo)
nord14 #a3be8c  (aurora verde)
nord15 #b48ead  (aurora viola)
```

---

## Sprint 1: KDE Foundation — Look-and-Feel Fix

**Obiettivo:** Correggere le derive nel pacchetto `com.atomik.desktop` e allineare tema, icone, cursori, decorazioni.

| Attività | File | Azione |
|---|---|---|
| Fix `contents/defaults` | `roles/desktop/files/look-and-feel/com.atomik.desktop/contents/defaults` | Impostare `Tela-circle-nord-dark`, `Nordic-cursors`, Aurorae Nordic |
| Fix decorazioni finestre | `group_vars/all.yml` → `atomik_kde_theme` | Aggiungere `window_deco=Nordic`, `BorderSize=Tiny` |
| Fix gestione Doppio Look-and-Feel | `roles/desktop/tasks/kde.yml` | Eliminare la sotto-directory `look-and-feel/` duplicata |
| Integrare Kvantum | `group_vars/all.yml` | `widgetStyle=Kvantum`, deploy tema Kvantum Nordic |
| Applicare Nordic-cursors in Ansible | `roles/desktop/tasks/kde.yml` | `kwriteconfig6 --file kdeglobals --group Icons --key cursorTheme Nordic-cursors` |
| Configurare trasparenza KWin | `group_vars/all.yml` → `atomik_kde_settings` | `kwinrc/Compositing/Backend=OpenGL`, blur discreto per pannelli |
| Pannelli: opacità e sfumatura | `files/panel-background.svg` | Renderizzare con opacità 0.25 e gradienti frost |
| Disattivare effetti superflui | `group_vars/all.yml` | `kwinrc/Effect-*` disabilitati, solo blur + slide |

### Fix specifico per `contents/defaults`:
```
[kdeglobals][Icons]
Theme=Tela-circle-nord-dark

[kcminputrc][Mouse]
cursorTheme=Nordic-cursors

[kwinrc][org.kde.kdecoration2]
library=org.kde.kwin.aurorae
theme=__aurorae__svg__Nordic
BorderSize=Tiny
CustomButtonPositions=true
LeftButtons=
RightButtons=M,S,C
```

### Nuove variabili `group_vars/all.yml`:
```yaml
atomik_kde_theme:
  kinoite:
    theme: Nordic
    colorscheme: Nordic
    font: Cantarell 11
    monospace_font: Noto Sans Mono 11
    icon_theme: Tela-circle-nord-dark
    cursor_theme: Nordic-cursors
    window_deco: __aurorae__svg__Nordic
    border_size: Tiny
    widget_style: Kvantum
```

---

## Sprint 2: KDE Full-Nordic Polish

**Obiettivo:** Perfezionare Konsole, SDDM, splash screen, notifiche, suoni.

| Attività | File | Azione |
|---|---|---|
| Deploy profilo Konsole Nordic | `roles/desktop/tasks/kde.yml` | Aggiungere task per scrivere `Nordic.colorscheme` + `Nordic.profile` |
| Tema SDDM Nordic | `roles/desktop/tasks/kde.yml` | Installare `Nordic-kDE` SDDM theme, configurare `/etc/sddm.conf` |
| Disabilitare splash screen | Già fatto | `ksplashrc` Engine=none, Theme=none |
| Tema notifiche | `group_vars/all.yml` | `knotifyrc` con Nordic palette |
| Suoni di sistema disabilitati | `group_vars/all.yml` | `kdeglobals/ Sounds/Enabled=false` |
| Applicare Nordic a GTK via KDE | `roles/desktop/tasks/kde.yml` | `kde-gtk-config` → GTK theme=Nordic |
| Lock screen coerente | `group_vars/all.yml` | Tema lockscreen = Nordic, wallpaper matching |
| Menu applicazioni stile macOS | `roles/desktop/files/panel-background.svg` | Applicare sfumatura nord ai pannelli |

---

## Sprint 3: GNOME Foundation — Full-Nordic GTK3/4 + Shell

**Obiettivo:** Portare la parità visiva KDE → GNOME con tema GTK, Shell, GDM.

| Attività | File | Azione |
|---|---|---|
| GTK3/4 theme Nordic | `roles/desktop/tasks/gnome.yml` | Già presente, migliorare copia asset |
| Shell theme via user-theme | `roles/desktop/tasks/gnome.yml` | Aggiungere `gnome-shell` asset copia + gsettings |
| GDM theme | `roles/desktop/tasks/gnome.yml` | Impostare Nordic come tema GDM via `gsettings set org.gnome.login-screen` |
| Icone Tela-circle-nord-dark | `group_vars/all.yml` → `atomik_gnome_dconf` | Già presente, OK |
| Cursori Nordic-cursors | `group_vars/all.yml` | Già presente |
| Font Cantarell + Noto Mono | `group_vars/all.yml` | OK |
| GNOME Terminal profilo Nordic | `roles/desktop/tasks/gnome.yml` | Task per creare profilo `Nordic` con palette |
| Button layout M,S,C destra | `roles/desktop/tasks/gnome.yml` | Già presente, OK |
| Disabilitare animazioni | `group_vars/all.yml` | Già presente, OK |
| Dash-to-Dock tuning | `roles/desktop/tasks/gnome.yml` | Aggiungere: opacity 0.85, pressure-threshold, intellihide |

### Nuove gsettings per GNOME:
```yaml
atomik_gnome_dconf:
  - path: /org/gnome/desktop/interface/enable-animations
    value: "false"
  - path: /org/gnome/desktop/interface/icon-theme
    value: "'Tela-circle-nord-dark'"
  - path: /org/gnome/desktop/interface/cursor-theme
    value: "'Nordic-cursors'"
  - path: /org/gnome/desktop/interface/gtk-theme
    value: "'Nordic'"
  - path: /org/gnome/desktop/interface/font-name
    value: "'Cantarell 11'"
  - path: /org/gnome/desktop/interface/document-font-name
    value: "'Cantarell 11'"
  - path: /org/gnome/desktop/interface/monospace-font-name
    value: "'Noto Sans Mono 11'"
  - path: /org/gnome/desktop/wm/preferences/theme
    value: "'Nordic'"
  - path: /org/gnome/desktop/wm/preferences/button-layout
    value: "':minimize,maximize,close'"
  - path: /org/gnome/shell/extensions/user-theme/name
    value: "'Nordic'"
```

---

## Sprint 4: GNOME Full-Nordic Polish

**Obiettivo:** Estensioni, GDM, Terminale, suoni, Dconf completo.

| Attività | File | Azione |
|---|---|---|
| Dash-to-Dock configurazione | `roles/desktop/tasks/gnome.yml` | Dock BOTTOM, extend-height=false, icon-size=64, pressure-threshold, intellihide |
| GNOME Terminal profilo | `roles/desktop/tasks/gnome.yml` | `dconf write /org/gnome/terminal/legacy/profiles:` con palette Nordic |
| Disabilitare tracker/miner | `group_vars/all.yml` → nuovo `atomik_gnome_dconf` | `tracker disable`, `privacy/disable-external=true` |
| GDM tema | `roles/desktop/tasks/gnome.yml` | Copiare Nordic in `/usr/share/gnome-shell/` + gdm settings |
| Disabilitare suoni evento | `group_vars/all.yml` | `sound/event-sounds=false` |
| Schermata di blocco | `group_vars/all.yml` | Wallpaper Nordic + orologio 24h |
| Night Light | `group_vars/all.yml` | `night-light-enabled=true`, temp 3800K |
| Estensioni consigliate | `group_vars/all.yml` → `atomik_flatpak_verified` | Dash-to-Dock, User-Themes, GSConnect (opzionale) |
| Accent color | `group_vars/all.yml` | `accent-color='blue'` → nord8 |

---

## Sprint 5: Cross-DE Consistency

**Obiettivo:** Garanzia di coerenza visiva assoluta tra KDE e GNOME.

| Attività | Dettagli |
|---|---|
| Audit palette incrociato | Confrontare ogni elemento visivo KDE ↔ GNOME, tabella di corrispondenza |
| Wallpaper unico | Stesso wallpaper per SDDM/GDM/KDE/GNOME |
| Icone | Stessa Tela-circle-nord-dark su entrambi |
| Cursori | Nordic-cursors su entrambi (con fallback Adwaita) |
| Font | Cantarell 11 UI + Noto Sans Mono 11 terminale |
| Finestre | Button M,S,C destra, bordi 0px, ombre coerenti |
| Pannelli/Dock | Opacità 0.25 con sfumatura frost, autohide |
| Terminale | Palette nord identica (Konsole ↔ GNOME Terminal) |
| Suoni | Disabilitati su entrambi |
| Animazioni | Disabilitate su entrambi (massima reattività) |

---

## Sprint 6: Extreme Kernel Tuning

**Obiettivo:** Configurazione kernel più aggressiva possibile per desktop a bassa latenza.

| Attività | Parametro | Valore |
|---|---|---|
| GRUB: mitigazioni CPU off | `mitigations=off` | Disabilita mitigazioni spettro per ~5-15% performance |
| GRUB: nowatchdog | `nowatchdog` | Disabilita NMI watchdog (già in tuned) |
| GRUB: nohz_full | `nohz_full=2-{n-1}` | Tickless sui core non-boot (riduce interruzioni) |
| GRUB: rcu_nocbs | `rcu_nocbs=2-{n-1}` | RCU callback offloading |
| GRUB: processor.max_cstate=1 | C-states minimi | Riduce latenza wake-up |
| GRUB: intel_idle.max_cstate=0 | Idle disabilitato | Massima reattività (tradeoff energia) |
| GRUB: skew_tick=1 | `skew_tick=1` | Evita thundering herd timer |
| sysctl: sched_autogroup | già 0 | Disabilitato |
| sysctl: preempt | FULL (RT) | `CONFIG_PREEMPT_FULL` (se supportato) |
| sysctl: perf_cpu_time_max_percent=1 | Riduce overhead profiling | Già predisposto |

### Nuovo task GRUB: `roles/security/tasks/grub.yml`
```yaml
- name: Deploy GRUB tuning
  ansible.builtin.copy:
    content: |
      GRUB_CMDLINE_LINUX="$GRUB_CMDLINE_LINUX mitigations=off nowatchdog nohz_full=2-{{ ansible_processor_cores - 1 }} rcu_nocbs=2-{{ ansible_processor_cores - 1 }} processor.max_cstate=1 intel_idle.max_cstate=0 skew_tick=1"
    dest: /etc/default/grub.d/99-atomik-performance.cfg
    owner: root
    group: root
    mode: "0644"
  notify: Rebuild grub
```

---

## Sprint 7: Memory & Storage Warp

**Obiettivo:** Spingere RAM, ZRAM e I/O al limite massimo.

| Attività | File | Modifica |
|---|---|---|
| ZRAM: zram-size = ram | `group_vars/all.yml` | `zram-size = ram` (da `ram / 2`) — più spazio compresso |
| ZRAM: algorithm = zstd | OK | Già zstd |
| THP defrag = never | `group_vars/all.yml` | `defer` → `never` (evita stall) |
| VM dirty_ratio = 5 | OK | Già 5 |
| VM dirty_background = 2 | `group_vars/all.yml` | 5 → 2 (più aggressivo) |
| VM swappiness = 5 | `group_vars/all.yml` | 10 → 5 (solo swap compresso) |
| VM watermark_scale = 150 | `sysctl_dynamic.conf.j2` | 125 → 150 (più memoria libera) |
| min_free_kbytes = 1.5% RAM | `sysctl_dynamic.conf.j2` | 2% → 1.5% |
| IO: kyber per NVMe | OK | Già kyber |
| IO: BFQ per SATA | OK | Già BFQ |
| IO: add nr_requests=2048 | `group_vars/all.yml` → `atomik_io_udev_rules` | `queue/nr_requests=2048` |
| IO: add read_ahead_kb=4096 | `group_vars/all.yml` → `atomik_io_udev_rules` | `queue/read_ahead_kb=4096` |
| NOATIME su tutte le partizioni | `roles/security/tasks/io.yml` | Già fatto |
| Disabilitare swap file | `group_vars/all.yml` | Opzionale: solo ZRAM è sufficiente |

### Nuovo udev rules avanzato:
```
ACTION=="add|change", KERNEL=="nvme[0-9]*", ATTR{queue/scheduler}="kyber", ATTR{queue/nr_requests}="2048", ATTR{queue/read_ahead_kb}="4096"
ACTION=="add|change", KERNEL=="sd[a-z]|mmcblk[0-9]*", ATTR{queue/scheduler}="bfq", ATTR{queue/nr_requests}="2048", ATTR{queue/read_ahead_kb}="4096"
```

---

## Sprint 8: GPU & Rendering Latency

**Obiettivo:** Minima latenza di rendering possibile su Wayland.

| Attività | Configurazione |
|---|---|
| KWin: Backend=OpenGL | Già fatto |
| KWin: blur = false (KDE) | Già fatto |
| KWin: OpenGLIsUnsafe=true | Già fatto (wayland native) |
| KWin: MaxFps=144/240 | `group_vars/all.yml`: `kwinrc/Compositing/MaxFps=144` |
| GNOME: disabilitare blur | Già animazioni=false |
| Mutter: tuning sperimentale | `mutter experimental-features=['scale-monitor-framebuffer']` (se supportato) |
| Disabilitare VSync (se GSync/FreeSync) | `kwinrc/Compositing/VSync=none` |
| GPU scheduler: RT priority | Già fatto (desktop_scheduler) |
| Intel: enable_psr=0 (evita flicker) | `i915.enable_psr=0` in GRUB |
| AMD: amdgpu.sched_jobs=1024 | GRUB parametro |
| NVIDIA: nvidia.NVreg_EnableGpuFirmware=0 | GRUB parametro |
| Wayland: ridurre buffer count | `KWIN_DRM_BUFFER_COUNT=2` |

---

## Sprint 9: Network & Audio Latency

**Obiettivo:** Latenza di rete e audio minima per applicazioni real-time.

| Attività | File | Valore |
|---|---|---|
| Network: net.core.rmem_max | `group_vars/all.yml` → `atomik_sysctl` | 16777216 |
| Network: net.core.wmem_max | `group_vars/all.yml` | 16777216 |
| Network: net.ipv4.tcp_congestion_control=bbr | `group_vars/all.yml` | bbr (se modulo caricato) |
| Network: net.core.default_qdisc=fq | `group_vars/all.yml` | fq (fair queue) |
| Network: disable IPv6 | Opzionale | Se non serve, `disable_ipv6=1` |
| Audio: RT priority per PipeWire | `roles/security/tasks/oomd.yml` | Aggiungere a `atomik_oomd_protected_services` |
| Audio: ALSA buffer size=64 | `group_vars/all.yml` → tuned.conf | 128 → 64 |
| Audio: disabilitare power-save | `/etc/modprobe.d/alsa-power.conf` | `options snd_hda_intel power_save=0` |
| Bluetooth: disabilitare (se non usato) | `group_vars/all.yml` | `atomik_rpm_remove` + systemd mask |
| WiFi power-save off | `roles/security/tasks/network.yml` | `iw dev wlan0 set power_save off` |

---

## Sprint 10: Service Minimization & Bloat Removal

**Obiettivo:** Disabilitare ogni demone/servizio non indispensabile.

| Servizio | Azione | Note |
|---|---|---|
| abrtd / abrt-journal-core | mask | Crash reporting non necessario |
| packagekit | mask | Immutabile, rpm-ostree gestisce |
| fwupd | mask | Update firmware (se non serve) |
| cups / cups-browsed | mask | Se nessuna stampante |
| bluetooth | mask | Se nessun BT |
| NetworkManager-wait-online | mask | Ritarda boot |
| gssproxy / rpcbind | mask | Se no NFS |
| pmlogger / pmie | mask | Se no Performance Co-Pilot |
| racoon / ipsec | mask | Se no VPN |
| fedora-policy | mask | Su Atomic |
| systemd-resolved | mask | Se si usa NetworkManager |
| upower | mask | Se desktop fisso |
| geoclue | mask | Servizio posizione |
| ModemManager | mask | Se no modem cellulare |
| colord | mask | Se no profili colore |
| accounts-daemon | mask | Su Atomic non serve |

### Nuovo task: `roles/security/tasks/mask_services.yml`
```yaml
- name: Mask non-essential services
  ansible.builtin.systemd:
    name: "{{ item }}"
    state: masked
    enabled: false
    masked: true
  loop: "{{ atomik_masked_services }}"
```

---

## Sprint 11: Integration & Stress Testing

**Obiettivo:** Verificare che ogni modifica sia applicata correttamente senza regressioni.

| Attività | Comando / Script |
|---|---|
| Verifica sysctl | `sysctl -a | grep atomik` |
| Verifica ZRAM | `zramctl`, `swapon --show` |
| Verifica OOMD | `systemctl status systemd-oomd` |
| Verifica tuned | `tuned-adm active`, `tuned-adm verify` |
| Verifica scheduler | `chrt -p $(pidof kwin_wayland)` → RR |
| Verifica IO scheduler | `cat /sys/block/nvme0n1/queue/scheduler` |
| Verifica THP | `cat /sys/kernel/mm/transparent_hugepage/enabled` |
| Verifica temi KDE | `kreadconfig6 --file kdeglobals --group General --key ColorScheme` |
| Verifica temi GNOME | `gsettings get org.gnome.desktop.interface gtk-theme` |
| Stress test memoria | `stress-ng --vm 2 --vm-bytes 80% -t 30` |
| Latenza | `cyclictest` (se rt-tools installato) |
| Benchmark I/O | `fio --randwrite --ioengine=libaio --size=1G` |
| verifica YAML lint | `yamllint ansible/` |

---

## Sprint 12: Documentation & Release

**Obiettivo:** Documentare ogni parametro e rilasciare la versione Full-Nordic.

| Attività | File |
|---|---|
| Tabella parametri tuning | `docs/TUNING.md` — ogni parametro spiegato |
| Guida temi Full-Nordic | `docs/THEMING.md` — palette, font, icone |
| Esempi make target | `Makefile` + `README.md` |
| Changelog v2.0 | `CHANGELOG.md` |
| Video dimostrativo | Opzionale |

---

## Cronologia Sprint

| Sprint | Durata | Dipende da |
|---|---|---|
| 0 — Asset & Palette | 1g | — |
| 1 — KDE Foundation | 2g | Sprint 0 |
| 2 — KDE Polish | 2g | Sprint 1 |
| 3 — GNOME Foundation | 2g | Sprint 0 |
| 4 — GNOME Polish | 2g | Sprint 3 |
| 5 — Cross-DE Consistency | 1g | Sprint 2,4 |
| 6 — Extreme Kernel | 2g | — |
| 7 — Memory & Storage | 1g | Sprint 6 |
| 8 — GPU & Rendering | 1g | Sprint 6 |
| 9 — Network & Audio | 1g | Sprint 6 |
| 10 — Service Minimization | 1g | — |
| 11 — Integration Testing | 2g | Sprint 5,10 |
| 12 — Documentation | 2g | Sprint 11 |

**Totale: ≈ 20 giorni lavorativi**
