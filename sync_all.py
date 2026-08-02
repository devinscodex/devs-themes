#!/usr/bin/env python3
"""Propagates one family's palettes/<family>.json into every real
consumer -- Slate, Runestone, webUI -- in one command. Built 2026-07-31
after a night of manually hand-editing the same 3 files for every color
tweak; extended same day (Devin: "color syncs should now happen across
Slate/Runestone and now WebUI") to call Slate's own pull_themes.sh too,
so this is genuinely the one command instead of "run this, then also
remember to run that other script." Not a symlink (the consumers are
different file FORMATS -- Python dict loaded from JSON, an Obsidian CSS
snippet, inline HTML CSS -- you can't symlink part of a differently-
shaped file), but gets the same "one edit, one command" convenience
where the target structure is known and stable.

Usage:
    python3 sync_all.py bonepaper
    python3 sync_all.py bonepaper --dry-run
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WEBUI_HTML = REPO_ROOT / "cairn" / "webui" / "index.html"

# family -> Runestone CSS snippet path, or None if no CSS counterpart
# exists (e.g. Martin/MEG has never had a Runestone theme file).
RUNESTONE_CSS = {
    "bonepaper": REPO_ROOT / "runestone" / ".obsidian" / "snippets" / "bonepaper.css",
    "slate": REPO_ROOT / "runestone" / ".obsidian" / "snippets" / "slate.css",
}


def load_palette(family: str) -> dict:
    path = Path(__file__).parent / "palettes" / f"{family}.json"
    return json.loads(path.read_text())


def patch_webui(family: str, palette: dict, dry_run: bool) -> int:
    """Rewrites --ink/--ink-soft/--moss/--moss-solid inside the
    [data-theme="family-mode"] block. Only touches the 4 keys that
    actually vary per Devin's live tweaks tonight (fg/muted_fg/
    select_bg/highlight_bg) -- bg/bg-2/bg-3/line/card/sidebar are
    structural and rarely change, left alone so a family-wide re-sync
    doesn't accidentally revert an intentional structural edit."""
    if not WEBUI_HTML.exists():
        print(f"  webui: {WEBUI_HTML} not found, skipped")
        return 0
    text = WEBUI_HTML.read_text()
    changes = 0
    for mode in ("light", "dark"):
        if mode not in palette:
            continue
        p = palette[mode]
        rgb = tuple(int(p["select_bg"][i:i+2], 16) for i in (1, 3, 5))
        block_re = re.compile(
            r'(\[data-theme="' + family + '-' + mode + r'"\]\{.*?)'
            r'--ink: #[0-9a-fA-F]{6}; --ink-soft: #[0-9a-fA-F]{6};(.*?)'
            r'--moss: \d+, \d+, \d+; --moss-solid: #[0-9a-fA-F]{6};',
            re.DOTALL,
        )
        new_text, n = block_re.subn(
            lambda m: (
                m.group(1)
                + f'--ink: {p["fg"]}; --ink-soft: {p["muted_fg"]};'
                + m.group(2)
                + f'--moss: {rgb[0]}, {rgb[1]}, {rgb[2]}; --moss-solid: {p["select_bg"]};'
            ),
            text,
        )
        if n == 0:
            print(f"  webui: no [data-theme=\"{family}-{mode}\"] block found, skipped")
            continue
        text = new_text
        changes += n
    if changes and not dry_run:
        WEBUI_HTML.write_text(text)
    print(f"  webui: {changes} block(s) {'would be ' if dry_run else ''}updated")
    return changes


def patch_runestone_bonepaper(palette: dict, dry_run: bool) -> int:
    """Bonepaper-specific: --bp-glow is the dark-mode accent RGB triple
    (propagates to selection/active-line/callouts/etc via var()), plus
    two hardcoded --code-string/--code-value hex literals. Light mode's
    --bp-jade is a separate, rarely-touched accent -- not synced here,
    edit by hand if that one ever needs to move."""
    path = RUNESTONE_CSS["bonepaper"]
    if not path.exists():
        print(f"  runestone: {path} not found, skipped")
        return 0
    text = path.read_text()
    dark = palette.get("dark", {})
    if not dark:
        return 0
    hexval = dark["select_bg"]
    rgb = tuple(int(hexval[i:i+2], 16) for i in (1, 3, 5))
    new_text, n1 = re.subn(
        r"--bp-glow: \d+, \d+, \d+;",
        f"--bp-glow: {rgb[0]}, {rgb[1]}, {rgb[2]};",
        text,
    )
    new_text, n2 = re.subn(r"--code-string: #[0-9a-fA-F]{6};", f"--code-string: {hexval};", new_text)
    new_text, n3 = re.subn(r"--code-value: #[0-9a-fA-F]{6};", f"--code-value: {hexval};", new_text)
    changed = n1 + n2 + n3
    if changed and not dry_run:
        path.write_text(new_text)
    print(f"  runestone: {changed} value(s) {'would be ' if dry_run else ''}updated")
    return changed


def sync_slate(dry_run: bool) -> None:
    """Calls Slate's own pull_themes.sh -- that script already does the
    real work (copies every palettes/*.json into slate/theme_data/,
    theme.py loads them at runtime, nothing to regex-patch). Runs for
    ALL families every time since pull_themes.sh isn't family-scoped --
    cheap, idempotent, matches what it already does when run by hand."""
    script = REPO_ROOT / "slate" / "pull_themes.sh"
    if not script.exists():
        print(f"  slate: {script} not found, skipped")
        return
    if dry_run:
        print(f"  slate: would run {script}")
        return
    result = subprocess.run(["sh", str(script)], capture_output=True, text=True)
    print(f"  slate: {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"  slate: FAILED -- {result.stderr.strip()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("family", choices=["bonepaper", "flexoki", "martin", "slate"])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    palette = load_palette(args.family)
    print(f"Syncing {args.family} -> Slate, Runestone, webUI")
    sync_slate(args.dry_run)
    patch_webui(args.family, palette, args.dry_run)
    if args.family == "bonepaper":
        patch_runestone_bonepaper(palette, args.dry_run)
    elif args.family in RUNESTONE_CSS:
        print(f"  runestone: {args.family}.css sync not built yet (only bonepaper's structure is handled) -- edit by hand")
    else:
        print(f"  runestone: no CSS counterpart for {args.family}")


if __name__ == "__main__":
    main()
