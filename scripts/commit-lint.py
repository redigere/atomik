#!/usr/bin/env python3
"""Validate commit messages for formatting rules."""

import logging
import subprocess
import sys

logging.basicConfig(level=logging.WARNING, format="%(message)s")
log = logging.getLogger("commit-lint")

FORBIDDEN = set("→←✕✗✘▶►▸▹▷")


def get_commits(base_sha):
    result = subprocess.run(
        ["git", "rev-list", f"{base_sha}..HEAD"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.splitlines()


def get_commit_info(sha):
    subj = subprocess.run(
        ["git", "log", "-1", "--format=%s", sha],
        capture_output=True, text=True,
    ).stdout.strip()
    body = subprocess.run(
        ["git", "log", "-1", "--format=%B", sha],
        capture_output=True, text=True,
    ).stdout
    return subj, body


def main():
    base_sha = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
    failed = False

    for sha in get_commits(base_sha):
        subj, body = get_commit_info(sha)

        if len(subj) > 80:
            log.error("FAIL: %s subject exceeds 80 chars: %s", sha[:8], subj)
            failed = True

        if FORBIDDEN.intersection(subj):
            log.error("FAIL: %s forbidden symbols: %s", sha[:8], subj)
            failed = True

        if "Signed-off-by:" not in body:
            log.error("FAIL: %s missing Signed-off-by: %s", sha[:8], subj)
            failed = True

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
