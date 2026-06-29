# Atomik Full-Nordic Roadmap — Sprint Operativi

Roadmap per l'ecosistema desktop Full-Nordic: KDE Plasma 6 + GNOME 47+ con tuning estremo delle prestazioni. Tutti i parametri di configurazione vivono in group_vars/all.yml; i playbook sono puri esecutori.

## Sprint 0: Asset & Palette Unification

**Obiettivo:** Definire la palette Nordic vincolante per tutti i componenti ed eliminare derive cromatiche.

Definire palette rigida in docs/NORDIC_PALETTE.md con 16 colori esadecimali (nord0-nord15) + 4 tonalità frost + aurora. Verificare coerenza icone su Tela-circle-nord-dark. Campionare Nordic-kDE repo da extra/kde/install_nordic_kde.py. Generare wallpaper unificato in files/wallpaper/. Audit asset esistenti SVG/SVGZ.

Palette canonica: nord0 #2e3440, nord1 #3b4252, nord2 #434c5e, nord3 #4c566a, nord4 #d8dee9, nord5 #e5e9f0, nord6 #eceff4, nord7 #8fbcbb, nord8 #88c0d0, nord9 #81a1c1, nord10 #5e81ac, nord11 #bf616a, nord12 #d08770, nord13 #ebcb8b, nord14 #a3be8c, nord15 #b48ead.

## Sprint 1: KDE Foundation — Look-and-Feel Fix

**Obiettivo:** Correggere le derive nel pacchetto com.atomik.desktop e allineare tema, icone, cursori, decorazioni.

Fix contents/defaults per look-and-feel con Tela-circle-nord-dark, Nordic-cursors, Aurorae Nordic. Fix decorazioni finestre in atomik_kde_theme con window_deco e BorderSize. Eliminare sotto-directory look-and-feel duplicata. Integrare Kvantum con widgetStyle. Applicare Nordic-cursors via kwriteconfig6. Configurare trasparenza KWin con Backend OpenGL e blur discreto. Pannelli con opacità 0.25 e gradienti frost. Disattivare effetti superflui KWin.

## Sprint 2: KDE Full-Nordic Polish

**Obiettivo:** Perfezionare Konsole, SDDM, splash screen, notifiche, suoni.

Deploy profilo Konsole Nordic con colorscheme e profile. Tema SDDM Nordic con configurazione /etc/sddm.conf. Disabilitare splash screen via ksplashrc Engine=none. Tema notifiche con knotifyrc. Suoni di sistema disabilitati. Applicare Nordic a GTK via kde-gtk-config. Lock screen coerente con tema Nordic. Menu applicazioni stile macOS con sfumatura nord ai pannelli.

## Sprint 3: GNOME Foundation — Full-Nordic GTK3/4 + Shell

**Obiettivo:** Portare la parità visiva KDE verso GNOME con tema GTK, Shell, GDM.

GTK3/4 theme Nordic. Shell theme via user-theme. GDM theme con Nordic. Icone Tela-circle-nord-dark. Cursori Nordic-cursors. Font Cantarell + Noto Mono. GNOME Terminal profilo Nordic con palette. Button layout M,S,C destra. Disabilitare animazioni. Dash-to-Dock tuning con opacity pressure-threshold intellihide.

## Sprint 4: GNOME Full-Nordic Polish

**Obiettivo:** Estensioni, GDM, Terminale, suoni, Dconf completo.

Dash-to-Dock configurazione dock BOTTOM extend-height false icon-size 64 pressure-threshold intellihide. GNOME Terminal profilo con palette Nordic. Disabilitare tracker miner. GDM tema Nordic. Disabilitare suoni evento. Schermata di blocco con wallpaper Nordic. Night Light temperatura 3800K. Estensioni Dash-to-Dock User-Themes GSConnect. Accent color blue nord8.

## Sprint 5: Cross-DE Consistency

**Obiettivo:** Garanzia di coerenza visiva assoluta tra KDE e GNOME.

Audit palette incrociato KDE vs GNOME. Wallpaper unico per SDDM GDM KDE GNOME. Icone Tela-circle-nord-dark su entrambi. Cursori Nordic-cursors con fallback Adwaita. Font Cantarell 11 UI + Noto Sans Mono 11 terminale. Finestre button M,S,C destra bordi 0px ombre coerenti. Pannelli dock opacità 0.25 con sfumatura frost autohide. Terminale palette nord identica Konsole vs GNOME Terminal. Suoni disabilitati su entrambi. Animazioni disabilitate su entrambi.

## Sprint 6: Extreme Kernel Tuning

**Obiettivo:** Configurazione kernel più aggressiva possibile per desktop a bassa latenza.

GRUB mitigazioni CPU off per 5-15% performance. nowatchdog disabilita NMI watchdog. nohz_full sui core non-boot per ridurre interruzioni. rcu_nocbs per RCU callback offloading. processor.max_cstate=1 per C-states minimi. intel_idle.max_cstate=0 idle disabilitato. skew_tick=1 evita thundering herd timer. sysctl sched_autogroup=0. preempt FULL RT se supportato. perf_cpu_time_max_percent=1.

## Sprint 7: Memory & Storage Warp

**Obiettivo:** Spingere RAM, ZRAM e I/O al limite massimo.

ZRAM zram-size raddoppiato. THP defrag never per evitare stall. VM dirty_ratio e dirty_background più aggressivi. swappiness a 5. watermark_scale a 150. min_free_kbytes 1.5% RAM. IO kyber per NVMe BFQ per SATA. nr_requests 2048. read_ahead_kb 4096. NOATIME su tutte le partizioni. Swap file disabilitabile.

## Sprint 8: GPU & Rendering Latency

**Obiettivo:** Minima latenza di rendering possibile su Wayland.

KWin Backend OpenGL blur false OpenGLIsUnsafe true MaxFps 144. GNOME animazioni false. Disabilitare VSync se GSync FreeSync. GPU scheduler RT priority. Intel enable_psr=0. AMD amdgpu.sched_jobs. NVIDIA NVreg_EnableGpuFirmware=0. KWIN_DRM_BUFFER_COUNT=2.

## Sprint 9: Network & Audio Latency

**Obiettivo:** Latenza di rete e audio minima per applicazioni real-time.

rmem_max 16777216 wmem_max 16777216. tcp_congestion_control bbr. default_qdisc fq. IPv6 disabilitabile. RT priority per PipeWire. ALSA buffer size 64. Disabilitare power-save audio. Bluetooth disabilitabile. WiFi power_save off.

## Sprint 10: Service Minimization & Bloat Removal

**Obiettivo:** Disabilitare ogni demone o servizio non indispensabile.

Mask abrtd abrt-journal-core packagekit cups cups-browsed bluetooth NetworkManager-wait-online gssproxy rpcbind pmlogger pmie racoon ipsec fedora-policy upower geoclue ModemManager colord accounts-daemon.

## Sprint 11: Integration & Stress Testing

**Obiettivo:** Verificare che ogni modifica sia applicata correttamente senza regressioni.

Verifica sysctl, ZRAM, OOMD, tuned, scheduler, IO scheduler, THP, temi KDE e GNOME. Stress test memoria con stress-ng. Latenza con cyclictest. Benchmark I/O con fio. YAML lint.

## Sprint 12: Documentation & Release

**Obiettivo:** Documentare ogni parametro e rilasciare la versione Full-Nordic.

Tabella parametri tuning in docs/TUNING.md. Guida temi Full-Nordic in docs/THEMING.md. Esempi make target in Makefile e README.md. Changelog v2.0 in CHANGELOG.md.

## Anti-Lag Sprint AL0: VM & Memory Baseline Hardening

**Obiettivo:** Eliminare i micro-freeze causati da writeback ritardato e frammentazione di pagina.

dirty_background_ratio da 2 a 1 per avviare scrittura sporca prima. dirty_ratio da 5 a 3 per hard limite writeback più basso. dirty_expire_centisecs da 3000 a 500 per scrivere dati vecchi in 5 secondi. dirty_writeback_centisecs da 500 a 100 per pdflush ogni 1 secondo. swappiness da 5 a 1 per swap solo sotto pressione estrema. vfs_cache_pressure da 50 a 100 per reclaim VFS cache più aggressivo. Aggiunto watermark_low_factor=200 per più pagine libere riservate. min_free_kbytes al 3% della RAM (era 1.5%). admin_reserve_kbytes all'1% della RAM (era 0.5%). Aggiunto user_reserve_kbytes all'1% della RAM. Aggiunto extfrag_threshold=100 per ridurre frammentazione. Aggiunto reclaim_clean_pages=1 per reclaim pagine pulite immediate.

## Anti-Lag Sprint AL1: OOMD Aggressivo

**Obiettivo:** Reagire alla pressione di memoria in millisecondi, non in secondi.

SwapUsedLimit da 50% a 10% per reagire a minima pressione swap. DefaultMemoryPressureLimit da 20% a 5% per soglia pressione molto più bassa. DefaultMemoryPressureDurationSec da 2 secondi a 500 millisecondi per reazione in mezzo secondo. ManagedOOMMemoryPressureLimit su user.slice a 10%. ManagedOOMMemoryPressureLimit su servizi protetti a 50%.

Nuove variabili in group_vars/all.yml: atomik_oomd_config con SwapUsedLimit 10% DefaultMemoryPressureLimit 5% DefaultMemoryPressureDurationSec 500ms. atomik_oomd_user_slice con ManagedOOMMemoryPressure kill ManagedOOMMemoryPressureLimit 10% ManagedOOMSwap kill.

## Anti-Lag Sprint AL2: Cgroup & Slice Memory Limits

**Obiettivo:** Prevenire OOM killer e freeze mettendo limiti di memoria massimi per slice.

user.slice MemoryHigh al 75% della RAM. user.slice MemoryMax al 90% della RAM. user.slice TasksMax a 4096. Servizi protetti MemoryHigh infinity TasksMax 8192. Compositor CPU Shares a 4096. App CPU Shares a 1024.

Nuove task in roles/security/tasks/oomd.yml per deploy user slice memory limits protected service cgroup limits e compositor CPU weight.

## Anti-Lag Sprint AL3: ZRAM & Swap Pressure

**Obiettivo:** Massimizzare spazio compresso e ridurre latenza di decompressione.

zram0 size da ram moltiplicato 1.5 a ram moltiplicato 2. zram1 size da ram diviso 4 a ram diviso 2. zram1 algorithm da lz4 a lzo-rle per migliore compressione. same-page-compression abilitato per evitare duplicati in RAM.

## Anti-Lag Sprint AL4: GRUB Estremo Low-Latency

**Obiettivo:** Parametri kernel più aggressivi per eliminare latenze spurie.

rcu_nocb_poll per polling RCU callbacks. oops=panic panic=1 per reboot immediato su oops. audit_backlog_limit=0 per disabilitare audit. intel_pstate=active e amd_pstate=active per miglior scaling frequency. idle=nomwait per disabilitare MWAIT. mce=ignore per ignorare MCE. pcie_aspm=off per disabilitare ASPM. modprobe.blacklist=mei,mei_me,mei_hdcp per blacklist ME.

## Anti-Lag Sprint AL5: CPU Scheduler & Real-Time Priority

**Obiettivo:** Compositor e servizi audio con priorità FIFO o RT.

Compositor CPUSchedulingPolicy fifo. Compositor CPUSchedulingPriority 99. Compositor Nice -15. Compositor CPUAffinity 0-3.

## Anti-Lag Sprint AL6: I/O Storage Latency Zero

**Obiettivo:** Nessuna latenza I/O bloccante.

NVMe scheduler da kyber a none per zero overhead scheduling. NVMe nr_requests da 2048 a 64 per coda minima. NVMe nomerges=2 per nessun merge I/O. NVMe rq_affinity=2 per affinità CPU. NVMe iostats=0 per zero overhead statistiche. NVMe max_sectors_kb da 4096 a 128 per trasferimenti piccoli. NVMe queue_depth=64 per profondità coda minima. SATA BFQ confermato. SATA nr_requests da 2048 a 64.

## Anti-Lag Sprint AL7: GPU & Compositor Warp

**Obiettivo:** Zero glitch di composizione.

KWIN_DRM_SCHEDULER_ENABLED=1 per scheduling GPU via kernel. KWIN_DRM_SCHEDULER_PRIORITY=realtime per priorità RT GPU. KWIN_DRM_NO_AMS=1 per disabilitare Adaptive Sync. MUTTER_DEBUG_DISABLE_VBLANK=1 per GNOME senza VBlank sync. __GL_MaxFramesAllowed=1 per NVIDIA max 1 frame in flight. AMD amdgpu.sched_jobs=4096 e amdgpu.ras=0. Intel i915.enable_fbc=0 disable_power_well=1 enable_rc6=0 enable_dc=0. NVIDIA NVreg_UsePageAttributeTable=1 e NVreg_RegistryDwords RMIntrLock=0.

## Anti-Lag Sprint AL8: App Nap Proattivo

**Obiettivo:** Freezare immediatamente le app in background prima che causino pressione memoria.

Interval da 1 secondo a 500 millisecondi per doppia frequenza di controllo. Reclaim percent da 10% a 25% per riciclo più aggressivo. Memory.max enforcement al 200% del current come hard cap su ogni cgroup. Retry su scrittura cgroup con 3 tentativi per evitare errori transienti. Memory pressure detection da memory.pressure maggiore di 5% come early warning.

## Anti-Lag Sprint AL9: Tuned & Khugepaged Tuning

**Obiettivo:** Minimo overhead di allocazione pagine e defrag.

min_perf_pct da 25 a 100 per CPU sempre al massimo. force_latency=1 per latenza forzata minima. alsa_buffer_size da 64 a 32 per buffer ALSA minimo. alsa_period_size=128 per periodo ALSA minimo. sched_migration_cost_ns da 500000 a 250000 per migrazioni più rapide. sched_min_granularity_ns da 3000000 a 1500000 per granularità scheduling doppia. sched_wakeup_granularity_ns da 4000000 a 2000000 per wakeup più veloce. khugepaged alloc_sleep_millisecs 10000 scan_sleep_millisecs 10000 per THP scan meno frequente. khugepaged max_ptes_none 512 per THP più selettivo. shmem_enabled never per nessun THP su shared memory. use_zero_page 0 per disabilitare zero page.

## Anti-Lag Sprint AL10: Journald & Logging Latency

**Obiettivo:** Zero attese per scrittura log.

RateLimitIntervalSec 0 per nessun rate limit. RateLimitBurst 0 per nessun burst limit. SyncIntervalSec 5 minuti per sync ridotto. ForwardToSyslog no per nessun forward. ForwardToWall no per nessun wall message.

## Cronologia Sprint

Sprint 0 Asset & Palette 1 giorno senza dipendenze. Sprint 1 KDE Foundation 2 giorni dipende da Sprint 0. Sprint 2 KDE Polish 2 giorni dipende da Sprint 1. Sprint 3 GNOME Foundation 2 giorni dipende da Sprint 0. Sprint 4 GNOME Polish 2 giorni dipende da Sprint 3. Sprint 5 Cross-DE Consistency 1 giorno dipende da Sprint 2 e 4. Sprint 6 Extreme Kernel 2 giorni senza dipendenze. Sprint 7 Memory & Storage 1 giorno dipende da Sprint 6. Sprint 8 GPU & Rendering 1 giorno dipende da Sprint 6. Sprint 9 Network & Audio 1 giorno dipende da Sprint 6. Sprint 10 Service Minimization 1 giorno senza dipendenze. Sprint 11 Integration Testing 2 giorni dipende da Sprint 5 e 10. Sprint 12 Documentation 2 giorni dipende da Sprint 11. AL0 VM Memory Baseline 1 giorno dipende da Sprint 6 e 7. AL1 OOMD Aggressivo 1 giorno dipende da AL0. AL2 Cgroup Slice Limits 1 giorno dipende da AL1. AL3 ZRAM Tuning 1 giorno dipende da AL0. AL4 GRUB Low-Latency 1 giorno dipende da Sprint 6. AL5 CPU RT Priority 1 giorno dipende da AL4. AL6 I/O Latency 1 giorno dipende da AL0. AL7 GPU Compositor 1 giorno dipende da AL4. AL8 App Nap Proattivo 1 giorno dipende da AL2. AL9 Tuned Khugepaged 1 giorno dipende da AL0. AL10 Journald Tuning 1 giorno senza dipendenze.

Totale Full-Nordic circa 20 giorni più 10 giorni Anti-Lag per un totale di 30 giorni lavorativi.
