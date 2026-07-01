#!/usr/bin/env python3
"""Validate that atomik_masked_services does not conflict with critical services."""

import sys
import yaml

CRITICAL = ["NetworkManager", "bluetooth", "systemd-resolved", "sshd", "gdm", "sddm", "upower"]


def main() -> int:
    with open("ansible/group_vars/all.yml") as f:
        cfg = yaml.safe_load(f)

    masked = cfg.get("atomik_masked_services", [])
    conflicts = [s for s in masked if s in CRITICAL or s.rsplit(".", 1)[0] in CRITICAL]

    if conflicts:
        print(f"CRITICAL: Masked services conflict with critical list: {conflicts}")
        return 1

    print(f"Masked services OK: {len(masked)} services, no critical conflicts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
