#!/usr/bin/env python3
"""
bad character scanner for benchmark codebase
finds em dashes en dashes smart quotes emojis invisible chars and other non ascii anomalies
"""

import os
import sys
import glob
import unicodedata

# hey everyone this file is our in house bad character scanner
# we built this tool to comb through the entire repository and catch any pesky characters
# things like em dashes en dashes curly smart quotes emojis zero width spaces or weird unicode bits
# that might cause parsing hiccups on different operating systems or terminal encodings
# the scanner honours clean ascii standards while keeping intentional box characters like progress bars intact
# we use this script to analyse all python files markdown documentation and data files in one go
#
# the two functions below handle the core detection and fixing logic
# scan_file opens up a single file and inspects every character one by one
# it flags any em dashes emojis or hidden control characters and reports their exact line and column
# fix_file takes those findings and replaces em dashes with standard hyphens or commas
# swaps curly quotes for straight ascii quotes and strips out unwanted zero width artefacts
# so the whole codebase stays tidy clean and predictable across linux mac and windows

ALLOWED_NON_ASCII = {"█", "░", "★", "☆"}

REPLACEMENTS = {
    "\u2014": " - ",
    "\u2013": "-",
    "\u201c": '"',
    "\u201d": '"',
    "\u2018": "'",
    "\u2019": "'",
    "\u2022": "-",
    "\u2191": "",
    "\u2193": "",
    "\u2122": "",
    "\u00ae": "",
    "\u00a7": "Section ",
    "\u200b": "",
    "\ufeff": ""
}


def scan_file(filepath):
    issues = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            for col_num, ch in enumerate(line, 1):
                # allow ascii and progress bar blocks
                if ch in ALLOWED_NON_ASCII:
                    continue
                code = ord(ch)
                if code > 127:
                    # allow standard accented letters in prediction text files
                    if filepath.endswith(".txt") and unicodedata.category(ch).startswith("L"):
                        continue
                    char_name = unicodedata.name(ch, "UNKNOWN")
                    issues.append({
                        "file": filepath,
                        "line": line_num,
                        "col": col_num,
                        "char": ch,
                        "name": char_name,
                        "codepoint": f"U+{ord(ch):04X}"
                    })
    return issues


def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    new_content = content
    replaced_count = 0
    for bad_char, good_char in REPLACEMENTS.items():
        if bad_char in new_content:
            count = new_content.count(bad_char)
            new_content = new_content.replace(bad_char, good_char)
            replaced_count += count

    if replaced_count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
    return replaced_count


# now these next helper functions pull together the whole scanning workflow
# find_repository_files rounds up all the relevant source code markdown and json documents
# run_scanner loops through every file in our catalogue and prints a friendly summary
# and main handles any command line flags like checking whether the user wants to automatically fix issues
# it gives us a clear conversational report right in the terminal showing if the codebase is good to go

def find_repository_files():
    patterns = ["**/*.py", "**/*.md", "**/*.json", "**/*.txt"]
    all_files = []
    skip_dirs = {".venv", ".git", "__pycache__", "node_modules", "pillars-of-gec"}
    for pat in patterns:
        for f in glob.glob(pat, recursive=True):
            parts = f.replace("\\", "/").split("/")
            if not any(part in skip_dirs or part.startswith(".") for part in parts):
                all_files.append(f)
    return sorted(list(set(all_files)))


def run_scanner(fix_mode=False):
    files = find_repository_files()
    total_issues = 0
    fixed_count = 0

    print("=" * 80)
    print("BAD CHARACTER SCANNER - CODEBASE AUDIT")
    print("=" * 80)

    for filepath in files:
        if fix_mode:
            reps = fix_file(filepath)
            fixed_count += reps

        issues = scan_file(filepath)
        if issues:
            total_issues += len(issues)
            print(f"[{filepath}] found {len(issues)} character anomalies:")
            for issue in issues[:10]:
                print(f"  line {issue['line']} col {issue['col']}: '{issue['char']}' ({issue['name']} {issue['codepoint']})")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")
        else:
            print(f"[{filepath}] clean")

    print("-" * 80)
    if fix_mode:
        print(f"audit complete - fixed {fixed_count} characters across files")
    print(f"audit complete - remaining non ascii characters: {total_issues}")
    print("=" * 80)
    return total_issues


def main():
    fix_mode = "--fix" in sys.argv
    remaining = run_scanner(fix_mode=fix_mode)
    if remaining > 0 and not fix_mode:
        print("hint run with --fix to automatically replace em dashes curly quotes and other anomalies")
    sys.exit(0 if remaining == 0 else 1)


if __name__ == "__main__":
    main()
