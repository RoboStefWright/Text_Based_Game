# Wizard's Lair 🧙

A Python text-based adventure game where a rival wizard has transformed your home into a dangerous maze. Explore the rooms, collect seven enchanted items, and prepare for a final confrontation in the Parlor.

Originally developed as a class project, this version was rebuilt with an object-oriented design, persistent save/load functionality, and automated tests.

## Features

- **Object-oriented architecture:** Separate `Room`, `Item`, `Player`, and `Game` classes organize the game world, player state, and game logic.
- **Exploration:** Navigate interconnected rooms, discover items, and track previously visited locations.
- **Inventory management:** Collect and review the seven items needed to win.
- **Save and load:** Save progress to a JSON file and resume a previous game.
- **Command handling:** Supports movement, item collection, inventory, map, help, save, and exit commands.
- **Input handling:** Responds to invalid commands and directions without terminating the game.
- **Game-state logic:** Includes win/loss conditions and a confirmation prompt before entering the final room without all required items.
- **Optional colored output:** Uses Colorama when installed, with plain-text output as a fallback.

## Technologies

- Python
- Object-oriented programming
- JSON
- Pytest
- Colorama

## Getting Started

### Requirements

Python 3.9 or later is recommended.

Install the dependencies:

```bash
python -m pip install colorama pytest
```

### Run the game

From the repository directory:

```bash
python main.py
```

If a saved game exists, the game will offer the option to load it.

### Run the tests

```bash
python -m pytest test/ -v
```

## Available Commands

| Command | Description |
|---|---|
| `go <direction>` | Move north, south, east, or west |
| `get <item>` | Pick up an item in the current room |
| `inventory` or `i` | View collected items |
| `look` | Review the current room |
| `map` or `location` | View explored rooms |
| `save` | Save current progress |
| `help` or `?` | Display available commands |
| `quit` or `exit` | Leave the game |

## Project Structure

```text
Text_Based_Game/
├── main.py
├── game/
│   ├── engine.py
│   ├── entities.py
│   └── world.py
├── test/
│   └── test_engine.py
├── requirements.txt
└── README.md
```

## Design Highlights

One of the main design decisions was separating the game engine from console input and output.

`Game.execute_command()` accepts a command string and returns a response string rather than directly reading from the keyboard or printing to the console. This makes the game logic easier to test independently and leaves room for a different interface in the future.

The game also uses JSON serialization to preserve player location, inventory, and exploration progress between sessions.

## Future Improvements

- Add a graphical or web-based interface while reusing the game engine.
- Introduce randomized room or item placement for replayability.
- Add a scoring system based on turns or exploration.

