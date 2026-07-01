#!/usr/bin/env python3
"""Validate that tuned service.stopped does not conflict with critical services."""

import re
import sys

CRITICAL = ["NetworkManager", "bluetooth", "systemd-resolved", "sshd", "gdm", "sddm", "upower"]


def main() -> int:
    with open("ansible/roles/security/templates/tuned.conf.j2") as f:
        content = f.read()

    m = re.search(r"service\.stopped=(.*)", content)
    if not m:
        print("Tuned: no service.stopped directive found, OK")
        return 0

    stopped = [s.strip() for s in m.group(1).split(",")]
    conflicts = [s for s in stopped if s in CRITICAL]

    if conflicts:
        print(f"CRITICAL: Tuned service.stopped conflicts with critical list: {conflicts}")
        return 1

    print(f"Tuned service.stopped OK: {len(stopped)} services, no critical conflicts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
