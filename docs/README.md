# Atomik

Atomik is an Ansible-based declarative configuration for Fedora Atomic desktops (Silverblue, Kinoite, Cosmic Atomic). It adapts to the detected desktop environment at runtime.

## Requirements

4 GB RAM minimum. The system must already be running Fedora Silverblue, Kinoite, or Cosmic Atomic.

## Usage

```bash
make apply         # Apply full configuration
make apply-repos   # Configure repositories
make apply-packages  # Install/remove packages
make apply-security  # Apply security hardening
make apply-desktop   # Configure desktop settings
make apply-devtools  # Set up development tools
```

## Security

Firewalld, audit rules, hardened kernel parameters, SSH key-only auth, resource limits.

## Memory Management

ZRAM compressed swap, systemd-oomd with desktop-tuned thresholds, no earlyoom.

## Directory Layout

```
ansible/          # Ansible playbooks + roles
extra/kde/        # KDE theme scripts and Python tools
extra/kde/install_nordic_kde.py  # Nordic KDE theme installer
extra/kde/apply_kde.py           # Apply KDE panels and theme
```

## Reset

Revert the system to baseline: uninstall custom packages, remove repositories, delete wallpapers, reset desktop settings.
