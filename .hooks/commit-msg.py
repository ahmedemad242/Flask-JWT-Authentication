#!/usr/bin/env python

import re
import json
import sys


def main():
    msg = sys.argv[1]
    msg = open(".git/COMMIT_EDITMSG")
    msg = msg.read()
    f = None
    try:
        f = open("./.hooks/commit-msg.config.json")
        config = json.load(f)
    except ValueError as e:
        print(e)
        sys.exit(1)
    finally:
        f.close()

    # Construct regex to the following rules
    # 1. Optional "revert:" tag before commit msg
    # 2. A tag from the config followed by a semi colon and a whitespace
    # 3. A commit-msg within a min and max length
    regexp = r"^(revert: )?("
    for type in config["types"]:
        regexp += f"{type}|"
    regexp = (
        regexp[0:-1] + f"): .{{{config['length']['min']},{config['length']['max']}}}$"
    )

    if re.match(regexp, msg) is None:
        print("Something went wrong with the commit msg")
        print("Make sure it adheres to the conventions in the manual")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
