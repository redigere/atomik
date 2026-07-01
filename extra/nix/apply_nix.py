#!/usr/bin/env python3
"""Setup Nix user-level package manager and install applications."""

import os
import subprocess
import sys
import shutil
from pathlib import Path

USER = os.environ.get("USER", os.path.basename(os.path.expanduser("~")))
HOME = Path(f"/var/home/{USER}")
NIX_STORE = HOME / ".nix" / "store"
NIX_CHROOT = HOME / ".nix-user-chroot" / "bin" / "nix-user-chroot"
NIX_ROOT = HOME / ".nix"
NIX_HELPER = HOME / ".local" / "bin" / "nix"
NIX_CONF = HOME / ".config" / "nix" / "nix.conf"
NIX_FISH = HOME / ".config" / "fish" / "conf.d" / "nix.fish"

NIX_CHROOT_URL = "https://github.com/nix-community/nix-user-chroot/releases/download/2.1.1/nix-user-chroot-bin-2.1.1-x86_64-unknown-linux-musl"
NIX_INSTALLER_URL = "https://nixos.org/nix/install"

NIX_PACKAGES = [
    "discord",
    "easyeffects",
    "obs-studio",
    "slack",
    "vlc",
]


def run(*args, check=False, **kwargs):
    return subprocess.run(args, check=check, **kwargs)


def nix_cmd(*args):
    return [
        str(NIX_CHROOT), str(NIX_ROOT),
        str(HOME / ".nix-profile" / "bin" / "nix"),
        *args,
    ]


def setup_nix_user_chroot():
    if NIX_CHROOT.exists():
        return

    print("Installing nix-user-chroot...")
    NIX_CHROOT.parent.mkdir(parents=True, exist_ok=True)
    run("curl", "-sL", NIX_CHROOT_URL, "-o", str(NIX_CHROOT), check=True)
    NIX_CHROOT.chmod(0o755)


def setup_nix():
    if NIX_STORE.exists():
        return

    print("Installing Nix...")
    NIX_ROOT.mkdir(parents=True, exist_ok=True)

    NIX_HELPER.parent.mkdir(parents=True, exist_ok=True)
    NIX_HELPER.write_text(
        f"#!/bin/sh\n"
        f'export HOME="/home/{USER}"\n'
        f'exec /home/{USER}/.nix-user-chroot/bin/nix-user-chroot '
        f'/home/{USER}/.nix /home/{USER}/.nix-profile/bin/nix "$@"\n'
    )
    NIX_HELPER.chmod(0o755)

    installer = Path("/tmp/nix-install.sh")
    run("curl", "-sL", NIX_INSTALLER_URL, "-o", str(installer), check=True)
    installer.chmod(0o755)

    run(
        str(NIX_CHROOT), str(NIX_ROOT),
        "sh", str(installer), "--no-daemon", "--yes",
        check=True,
    )
    installer.unlink(missing_ok=True)


def configure_nix():
    print("Configuring Nix...")
    NIX_CONF.parent.mkdir(parents=True, exist_ok=True)
    NIX_CONF.write_text("experimental-features = nix-command flakes\n")

    NIX_FISH.parent.mkdir(parents=True, exist_ok=True)
    NIX_FISH.write_text(
        f"if test -f /home/{USER}/.nix-profile/etc/profile.d/nix.fish\n"
        f"    source /home/{USER}/.nix-profile/etc/profile.d/nix.fish\n"
        f"end\n"
    )


def add_channels():
    print("Adding Nix channels...")
    result = run(
        *nix_cmd("channel", "--list"),
        capture_output=True, text=True,
    )
    if "nixpkgs" not in result.stdout:
        run(*nix_cmd("channel", "--add", "https://nixos.org/channels/nixpkgs-unstable", "nixpkgs"), check=True)
    run(*nix_cmd("channel", "--update"), check=True)


def get_installed_packages():
    result = run(
        *nix_cmd("profile", "list"),
        capture_output=True, text=True,
    )
    packages = []
    for line in result.stdout.splitlines():
        if line.startswith("Name:"):
            name = line.split()[-1]
            packages.append(name)
    return packages


def install_packages():
    installed = get_installed_packages()
    print(f"Installed packages: {installed}")

    for pkg in NIX_PACKAGES:
        if pkg in installed:
            print(f"  {pkg} already installed, skipping")
            continue
        print(f"  Installing {pkg}...")
        run(*nix_cmd("profile", "add", f"nixpkgs#{pkg}"), check=False)


def main():
    print("Setting up Nix user-level package manager...")
    setup_nix_user_chroot()
    setup_nix()
    configure_nix()
    add_channels()
    install_packages()
    print("Done.")


if __name__ == "__main__":
    main()
