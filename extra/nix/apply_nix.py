#!/usr/bin/env python3
"""Setup Nix user-level package manager and install applications."""

import logging
import os
import re
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("nix")

USER = os.environ.get("USER", os.path.basename(os.path.expanduser("~")))
HOME = Path(f"/var/home/{USER}")
NIX_STORE = HOME / ".nix" / "store"
NIX_CHROOT_BIN = HOME / ".nix-user-chroot" / "bin" / "nix-user-chroot"
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


def chroot_nix(*args):
    nix_profile = f"/home/{USER}/.nix-profile/bin"
    return [str(NIX_CHROOT_BIN), str(NIX_ROOT), f"{nix_profile}/nix", *args]


def chroot_nix_channel(*args):
    nix_profile = f"/home/{USER}/.nix-profile/bin"
    return [str(NIX_CHROOT_BIN), str(NIX_ROOT), f"{nix_profile}/nix-channel", *args]


def setup_nix_user_chroot():
    if NIX_CHROOT_BIN.exists():
        return
    log.info("installing nix-user-chroot")
    NIX_CHROOT_BIN.parent.mkdir(parents=True, exist_ok=True)
    run("curl", "-sL", NIX_CHROOT_URL, "-o", str(NIX_CHROOT_BIN), check=True)
    NIX_CHROOT_BIN.chmod(0o755)


def setup_nix():
    if NIX_STORE.exists():
        return
    log.info("installing nix")
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
        str(NIX_CHROOT_BIN), str(NIX_ROOT),
        "sh", str(installer), "--no-daemon", "--yes",
        check=True,
    )
    installer.unlink(missing_ok=True)


def configure_nix():
    log.info("configuring nix")
    NIX_CONF.parent.mkdir(parents=True, exist_ok=True)
    NIX_CONF.write_text("experimental-features = nix-command flakes\n")

    NIX_FISH.parent.mkdir(parents=True, exist_ok=True)
    NIX_FISH.write_text(
        f"if test -f /home/{USER}/.nix-profile/etc/profile.d/nix.fish\n"
        f"    source /home/{USER}/.nix-profile/etc/profile.d/nix.fish\n"
        f"end\n"
    )


def add_channels():
    log.info("adding nix channels")
    result = run(*chroot_nix_channel("--list"), capture_output=True, text=True)
    if "nixpkgs" not in result.stdout:
        run(*chroot_nix_channel("--add", "https://nixos.org/channels/nixpkgs-unstable", "nixpkgs"), check=True)
    run(*chroot_nix_channel("--update"), check=True)


def get_installed_packages():
    result = run(*chroot_nix("profile", "list"), capture_output=True, text=True)
    packages = []
    for line in result.stdout.splitlines():
        if line.startswith("Name:"):
            clean = re.sub(r"\x1b\[[0-9;]*m", "", line)
            packages.append(clean.split()[-1])
    return packages


def install_packages():
    installed = get_installed_packages()
    env = os.environ.copy()
    env["NIXPKGS_ALLOW_UNFREE"] = "1"

    for pkg in NIX_PACKAGES:
        if pkg in installed:
            continue
        log.info("installing %s", pkg)
        run(*chroot_nix("profile", "add", "--impure", f"nixpkgs#{pkg}"), check=False, env=env)


def main():
    setup_nix_user_chroot()
    setup_nix()
    configure_nix()
    add_channels()
    install_packages()
    log.info("done")


if __name__ == "__main__":
    main()
