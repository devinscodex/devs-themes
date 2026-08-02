# themes-custom

Central source of truth for Devin's custom theme families. Each real
consumer — **Slate** (`slate/theme_data/`), **Runestone**
(`.obsidian/snippets/*.css`), **webUI** (`cairn/webui/index.html`), and
hand-tuned **Alacritty** terminal themes (`dotfiles/config/alacritty/
themes/`) — pulls its own **copy** from here and is free to tweak/
fine-tune it independently; this repo is canonical, not hard-linked to
consumers.

`sync_all.py <family>` is the real one-command propagation path (see
Format below) for Slate/webUI/Runestone-bonepaper; Alacritty's terminal
themes need actual per-theme ANSI-palette design on top of the base 8
keys, so those stay hand-built, not auto-synced.

## Roster (4 families, light + dark each = 8 variants)

Order: Slate is always top/default. The other three sort alphabetically
(Bonepaper, Flexoki, Martin) — Devin's explicit ordering rule, 2026-07-31.
Note this is this REPO's own listing convention, not necessarily a given
consumer's live UI order -- webUI's swatch grid moved Slate to 2nd
2026-08-02 (Martin, Slate, Flexoki, Bonepaper), a display preference for
that one app, not a change to this repo's own roster rule.

- **Slate** (top/default) — Runestone's `slate.css` house theme. Light
  stone (`bg`/`button_bg` #d0cbbf/#c1bcad, unchanged since original).
  Dark retired its real official Solarized Osaka neutrals (#001a1d)
  2026-08-01 for a real Bluish/"Cobalt Dark" blue-grey instead (`bg`
  #2c3640, `button_bg` #414f5a) — Devin: "as gray as bluish, dark
  slate," after Cobalt was retired as its own family. The old Osaka
  values live on as a new standalone `runestone/.obsidian/snippets/
  solarized-osaka.css` (dark half) so they weren't lost, just moved.
- **Bonepaper** — aged tankōbon paper/sumi ink (light) + true-black night-rain
  with sampled sage-mint glow (dark). Real numpy-sampled values, not picked
  by eye. Briefly renamed "Ossuary" 2026-07-31, reverted same day ("leave
  bonepaper") once the 4th family below took "Martin" instead of
  "Graphpaper" — no more "-paper" collision to avoid. MIT License, (c) 2026
  Devin Dwight (@devinscodex).
- **Flexoki** — Steph Ango's real published palette (stephango.com/flexoki).
  Accent (`select_bg`/`highlight_bg`) swapped from his blue to his own
  real teal (#24837B light / #3AA99F dark) 2026-07-31, "like osaka teal."
  `bg`/`button_bg` no longer stock spec either as of 2026-08-02 — chased
  through Selenized Light's cream, then Devin's own Parchment-CSS cream,
  before landing on `#fdf6dc`/`#eee2c9` (a straight midpoint between
  Parchment's cream and Flexoki's own real `#fffcf0`, "happy medium").
- **Martin** — real Martin Energy Group brand colors, pulled from
  martinenergygroup.com's live Elementor global palette. Long same-day
  rename history (2026-07-31): MEG -> Anthracite (company-neutral, once
  this repo started spanning multiple apps) -> Gridpaper (merged with a
  separately-parked white/green graph-paper plan) -> Graphpaper (same-day
  refinement) -> **Martin** (Devin's final call — explicit override of his
  own earlier stated "Martin Construction" collision concern, flagged and
  confirmed twice anyway: "just Martin," "clean, elegant"). Values
  unchanged through every rename.

Full provenance/history for every value lives in the original source files —
`slate/theme.py`, `runestone/.obsidian/snippets/bonepaper.css`, and
`cairn/webui/index.html` — this repo harvests the real hex values, it
doesn't re-derive or re-justify them.

**Retired:** a 5th family, **Cobalt** (Bluish dark + Selenized Light
light, two genuinely different real source themes combined into one
family), existed 2026-08-01 then was retired the same day — its dark
half's blue-grey character folded into Slate Dark, its light half's
cream folded into Flexoki Light (see those bullets above). No
`cobalt.json` in `palettes/` anymore; if you see a reference to it
anywhere else, that's stale.

## Format

`palettes/<family>.json` — `{"light": {...}, "dark": {...}}`, one flat dict of
named hex values per variant. Consuming code (Python dict, CSS custom
properties, whatever) maps these onto its own token names.

`palettes/<family>.toml` — the same data, generated. **JSON stays
canonical, never hand-edit the `.toml` files** — run `python3
export_toml.py` after any JSON change to regenerate them. Added
2026-07-31 (Devin likes Alacritty's own `.toml`-config-points-to-
`.toml`-theme-files pattern) as an alternate format for consumers that
want it, e.g. terminal-emulator theme files. Note: these `.toml` mirrors
are the flat 8-key base palette only, NOT a full 16-color terminal ANSI
palette (red/yellow/blue/magenta/cyan aren't part of this repo's data at
all) — building a real Alacritty color scheme from one of these families
still needs actual per-theme color design; see
`dotfiles/config/alacritty/themes/{slate,bonepaper,flexoki,martin}_{dark,light}.toml`
for all 8 built so far (Slate's dark uses a real Bluish-blended ANSI
palette, the others build out from each family's own base colors).

`sync_all.py <family> [--dry-run]` propagates one family's JSON into
Slate (`slate/pull_themes.sh`) and webUI (regex-patches the 4 keys that
actually vary: fg/muted_fg/select_bg/highlight_bg) always; Runestone only
for Bonepaper so far (`--dry-run` prints what would change without
writing). Everything else — Runestone's Slate/Flexoki/Martin CSS, all
Alacritty `.toml` files — is still hand-edited to match after a JSON
change; the script says so itself when it hits one of those.
