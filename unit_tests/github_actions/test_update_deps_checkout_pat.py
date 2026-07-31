#!/usr/bin/env python3
"""Regression test: update-lockfile checkout must use PAT to push branch."""

import re
import sys


def main():
    with open(".github/workflows/_update_dependencies.yml") as f:
        content = f.read()

    # Isolate the update-lockfile job (it precedes create-pr)
    update_job = content.split("  create-pr:")[0]

    match = re.search(
        r"- name: Checkout repo\s+uses: actions/checkout@[^\n]+\s+with:\s+ref: \$\{\{ env\.TARGET_BRANCH \}\}(?:\s+token: \$\{\{ secrets\.PAT \}\})?",
        update_job,
        re.DOTALL,
    )
    if not match:
        print("Could not locate update-lockfile checkout step")
        sys.exit(1)

    block = match.group(0)
    if "token: ${{ secrets.PAT }}" not in block:
        print("BUG: update-lockfile checkout must authenticate with PAT to push the bump branch")
        sys.exit(1)

    print("OK")


