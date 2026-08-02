#!/usr/bin/env python3
"""Mirrors every palettes/*.json into palettes/*.toml, same data, no new
dependency -- stdlib only, hand-formatted TOML output (our shape is flat
enough that a real TOML library would be overkill, same "compose from
what's already here" doctrine as the rest of this project). JSON stays
canonical; re-run this after any JSON edit to keep the TOML mirror in
sync -- it's generated, never hand-edited.
"""
import json
from pathlib import Path

PALETTES_DIR = Path(__file__).parent / "palettes"


def to_toml(data: dict) -> str:
    lines = []
    for mode in ("light", "dark"):
        if mode not in data:
            continue
        lines.append(f"[{mode}]")
        for key, value in data[mode].items():
            lines.append(f'{key} = "{value}"')
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    for json_path in sorted(PALETTES_DIR.glob("*.json")):
        data = json.loads(json_path.read_text())
        toml_path = json_path.with_suffix(".toml")
        toml_path.write_text(to_toml(data))
        print(f"{json_path.name} -> {toml_path.name}")


if __name__ == "__main__":
    main()
