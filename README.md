# Python Adventure Hex Builder

A small Python app for generating one or more random hex terrain types and matching landmark entries for Mausritter-style game sessions.
Added some randomize hex travel rules and character stats to actually simulate a hex crawl.

## Features

- Randomly selects a hex type from:
  - `countryside`
  - `forest`
  - `river`
  - `human town`
- Rolls a 1-in-20 landmark table for the selected terrain type
- Prints the result as `hex type, landmark`
- Stores the generated result as one combined string

## Usage

From the repository root:

```bash
python hex_builder/main.py
```

The main script currently generates a single hex and landmark pair by default.

## Repository Contents

- `hex_builder/main.py` — main app logic
- `.gitignore` — tracks only `hex_builder` and repository metadata
- `README.md` — project overview and usage
- `LICENSE` — open source license
