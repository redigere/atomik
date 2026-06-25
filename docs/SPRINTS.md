# Atomik Sprint Plan

This document tracks the Atomik configuration sprints. All configuration is Ansible-based.

## Sprint: Ansible Scaffold

Playbook layout, role structure, Makefile, inventory, host vars.

## Sprint: Repositories + Packages

RPM-ostree layers, Flatpak overrides, JetBrains Toolbox.

## Sprint: Security

Sysctl, limits, sudo, firewall, OOMD, zram, swap, IO scheduler, thermald, tuned.

## Sprint: Desktop (KDE/GNOME)

Theme (Nordic), color scheme, icons, window decorations, panels (topbar + dock), Konsole, animations off, wallet off, App Nap service.

## Sprint: DevTools

Fish shell, oh-my-fish + bobthefish (nord), nvm, pnpm, Rust, SDKMAN, opencode, IDE terminal config (flatpak-spawn --host).

## Sprint: Cleanup + Docs

Remove old Python/Rust references, document Ansible workflow, verify all `make apply-*` targets.
