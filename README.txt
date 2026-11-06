# Wizard's Lair

A text-based adventure game written in Python. You wake up in your own home,
now warped by a rival wizard's magic, and must explore the house, collect
seven enchanted items, and confront the wizard in the Parlor before he
confronts you.

*Originally built as a class project; rebuilt here with an object-oriented
design, save/load support, and a test suite.*

## Features

- **Object-oriented design** — `Room`, `Item`, `Player`, and `Game` classes
  cleanly separate the world data, player state, and game logic.
- **Save & load** — progress is saved to `savegame.json` and can be resumed
  on the next run.
- **Extra commands** — `map` (see which rooms you've explored),
  `inventory`/`i`, `look`, and `help`, in addition to `go` and `get`.
- **Safer input handling** — invalid commands, directions, and item names
  are handled gracefully instead of crashing.
- **Confirmation before a fatal mistake** — walking toward the Parlor
  without all 7 items warns you and asks if you're sure.
- **Colorized output** via `colorama` (falls back to plain text if it isn't
  installed).
- **Unit tested** — 14 tests covering movement, inventory, win/lose
  conditions, and save/load, using `pytest`.

## Running it

```bash
pip install -r requirements.txt
python main.py
```

## Running the tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Project structure

```
wizards-lair/
├── main.py              # entry point, console I/O, colored output
├── game/
│   ├── entities.py       # Item, Room, Player classes
│   ├── world.py          # the map: rooms, exits, item placement
│   └── engine.py         # Game class: command parsing & state transitions
├── test/
│   └── test_engine.py    # pytest suite for the game engine
└── requirements.txt
```

The engine (`game/engine.py`) is deliberately decoupled from `input()`/
`print()` — `Game.execute_command()` takes a string and returns a string,
which is what makes it straightforward to unit test and would make it easy
to swap in a different front end (e.g. a web UI) later without touching the
game logic.

## Possible next steps

- A web front end (Flask/HTML) reusing the same `Game` engine
- Randomized item/room placement for replay-ability
- A simple scoring system based on turns taken
