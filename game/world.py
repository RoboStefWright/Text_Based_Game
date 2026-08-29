"""defines the house, its rooms, exits, descriptions, and items"""
from game.entities import Room, Item

TOTAL_ITEMS_NEEDED = 7

def build_world() -> dict:
    """builds fresh dict or rooms so new game does not share with previous games"""

    rooms = {
        "Dungeon Cell": Room(
            "Dungeon Cell",
            "Cold stone walls meet at angles that don't feel quite right. "
            "A single door leads west.",
            exits={"West": "Basement"},
        ),
        "Basement": Room(
            "Basement",
            "Dust and old cobwebs. Somehow, this is unmistakably your house.",
            exits={"East": "Dungeon Cell", "West": "Cellar", "North": "Grand Hall"},
            item=Item("Keys", "A heavy iron ring of keys, warm to the touch."),
        ),
        "Cellar": Room(
            "Cellar",
            "Shelves of forgotten jars line the walls.",
            exits={"East": "Basement"},
            item=Item("Amulet", "A tarnished amulet that hums faintly with magic."),
        ),
        "Grand Hall": Room(
            "Grand Hall",
            "A once-grand hall, now cracked and dim. Passages lead in every direction.",
            exits={"South": "Basement", "East": "Sitting Room",
                   "West": "Dining Room", "North": "Entryway"},
            item=Item("Staff", "A gnarled wooden staff that crackles with static."),
        ),
        "Sitting Room": Room(
            "Sitting Room",
            "An overturned armchair sits beside a cold fireplace.",
            exits={"North": "Library", "West": "Grand Hall"},
            item=Item("Cloak", "A midnight-blue cloak, still warm as if worn recently."),
        ),
        "Library": Room(
            "Library",
            "Towering shelves, most of the books scattered across the floor.",
            exits={"South": "Sitting Room"},
            item=Item("Book", "A leather-bound book titled 'Wards & Counterwards'."),
        ),
        "Dining Room": Room(
            "Dining Room",
            "A long table set for a dinner that never happened.",
            exits={"East": "Grand Hall", "North": "Kitchen"},
            item=Item("Dusty Cupcake", "A suspiciously well-preserved cupcake."),
        ),
        "Kitchen": Room(
            "Kitchen",
            "Pots hang undisturbed. Something bubbles on the stove, untended.",
            exits={"South": "Dining Room", "East": "Entryway"},
            item=Item("Strange Potion", "A vial of liquid that shifts color when you're not looking directly at it."),
        ),
        "Entryway": Room(
            "Entryway",
            "Your front door. It feels like a lifetime since you last used it normally.",
            exits={"West": "Kitchen", "South": "Grand Hall", "East": "Parlor"},
        ),
        "Parlor": Room(
            "Parlor",
            "The rival wizard stands waiting, exactly where you last saw the sofa.",
            exits={"West": "Entryway"},
        ),
    }
    return rooms