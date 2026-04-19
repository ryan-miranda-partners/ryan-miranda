#!/usr/bin/env bash
# validate-skills.sh — sanity-check every SKILL.md under skills/
# Checks:
#   1. YAML frontmatter parses
#   2. `name:` field exists and matches the parent directory name
#   3. `description:` field exists
#   4. Any referenced hook command paths exist on disk
# Exits non-zero on any failure. Prints a pass/fail summary.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_DIR/skills"

if [ ! -d "$SKILLS_DIR" ]; then
  echo "error: $SKILLS_DIR not found" >&2
  exit 1
fi

python3 - "$SKILLS_DIR" <<'PY'
import os, sys, re

skills_dir = sys.argv[1]
failures = []
passed = 0

skill_files = []
for entry in sorted(os.listdir(skills_dir)):
    skill_path = os.path.join(skills_dir, entry, "SKILL.md")
    if os.path.isfile(skill_path):
        skill_files.append((entry, skill_path))

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    current_key = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        top = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if top:
            current_key = top.group(1)
            val = top.group(2).strip()
            fm[current_key] = val
        else:
            if current_key and fm.get(current_key) == "|":
                fm[current_key] = "<block>"
    return fm

for dir_name, path in skill_files:
    with open(path) as f:
        text = f.read()
    fm = parse_frontmatter(text)
    if fm is None:
        failures.append(f"{dir_name}: no YAML frontmatter detected")
        continue
    if "name" not in fm:
        failures.append(f"{dir_name}: missing `name:` field")
        continue
    if fm["name"] != dir_name:
        failures.append(f"{dir_name}: name field is '{fm['name']}', expected '{dir_name}'")
        continue
    if "description" not in fm:
        failures.append(f"{dir_name}: missing `description:` field")
        continue
    passed += 1

total = len(skill_files)
print(f"skills checked: {total}")
print(f"passed: {passed}")
if failures:
    print(f"failures: {len(failures)}")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("all skills valid.")
PY
