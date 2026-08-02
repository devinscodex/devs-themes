# devs-themes

Central repo for my custom themes. Each app pulls its own ##copy** from here and is free to fine-tune it independently; this repo is canonical, not hard-linked to my apps.

`sync_all.py <family>` is the real one-command propagation path (see
Format below) for Slate/webUI/Runestone-bonepaper; Alacritty's terminal
themes need actual per-theme ANSI-palette design on top of the base 8
keys, so those stay hand-built, not auto-synced.