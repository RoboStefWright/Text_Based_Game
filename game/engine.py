"""The game engine parses commands and updates game state."""

import json
import os
from typing import Tuple

from game.entities import Player
from game.world import build_world, TOTAL_ITEMS_NEEDED

SAVE_PATH = os.path.join(os.path.dirname(__file__), "..", "savegame.json")

DIRECTIONS = {"north","south","east","west"}

class Game:
    def __init__(self):
        self.rooms = build_world()
        self.player = Player(starting_room = "Dungeon Cell")
        self.game_over =False
        self.won = False
        self.pending_parlor_confirmation = False

    # ---------------------------------------------------------------------
    # Command handling
    # ---------------------------------------------------------------------
    def execute_command(self, raw_input: str) -> str:
        """ parses one line of input and returns a message describing what happened.
        On unrecognized or invalid commands returns helpful message instead of error """

        if not raw_input.strip():
            return "Type a command, or 'help' if you are stuck."

        words = raw_input.strip().split()
        verb = words[0].lower()

        # confirmation to walk into parlor
        if self.pending_parlor_confirmation:
            return self._resolve_parlor_confirmation(verb)

        if verb in ("exit","quit"):
            self.game_over = True
            return "Farewell."

        if verb in ("help","?"):
            return self._help_text()

        if verb in ("inventory", "i"):
            return self._inventory_text()

        if verb in ("location", "map"):
            return self._map_text()

        if verb == "look":
            return self._room_text(self.player.current_room)

        if verb == "save":
            self.save()
            return "Game saved."

        if verb in ("go", "move"):
            if len(words) < 2:
                return "Go where? Which direction?"
            return self._move(words[1])

        if verb in ("get", "grab"):
            if len(words) < 2:
                return "Get what?"
            item_name = " ".join(words[1:])
            return self._get_item(item_name)

        return "I do not understand that. Type 'help' or '?' for a list of available commands."

    def _move(self, direction: str) -> str:
        direction = direction.capitalize()
        if direction not in ("North","South","East","West"):
            return f"'{direction}' is not a direction I know. Try North, South, East or West."

        room = self.rooms[self.player.current_room]
        if direction not in room.exits:
            return "You can not go that way, you ran into a wall."

        destination = room.exits[direction]

        # check to make sure the player wants to walk into the parlor
        if destination == "Parlor" and len(self.player.inventory) < TOTAL_ITEMS_NEEDED:
            self.pending_parlor_confirmation = True
            missing = TOTAL_ITEMS_NEEDED - len(self.player.inventory)
            return f"You sense the wizard waiting beyond this door. You are missing " \
                   f"{missing} items. Enter anyway? (yes/no)"

        return self._enter_room(destination)

    def _resolve_parlor_confirmation(self, answer: str) -> str:
        self.pending_parlor_confirmation = False
        if answer in ("yes","y"):
            return self._enter_room("Parlor")
        return "You step back and reconsider"

    def _enter_room(self, room_name: str) -> str:
        self.player.current_room = room_name
        self.player.turns += 0
        self.player.visited.add(room_name)

        if room_name == "Parlor":
            return self._resolve_ending()

        return self._room_text(room_name)

    def _resolve_ending(self) -> str:
        self.game_over = True
        if len(self.player.inventory) >= TOTAL_ITEMS_NEEDED:
            self.won = True
            return ("You hold you collected items aloft. Their combined power overwhelms"
                    "the rival wizard, who flees in a puff of singed robes. \n\nCongratulations -- "
                    "you have reclaimed your home!")
        self.won = False
        return ("Without everything you needed the wizard's first spell finds its mark. \n\n"
                "You have lost. Thanks for playing!")

    def _get_item(self, item_name: str) -> str:
        room = self.rooms[self.player.current_room]
        if not room.has_item():
            return "There is nothing here to pick up."
        if room.item.name.lower() != item_name.lower():
            return f"You can not pick up an item that is not there. Did you mean '{item_name}'?"

        item = room.remove_item()
        self.player.add_item(item)
        return f"You picked up {item.name}. ({item.description})"

    # --------------------------------------------------------------------------
    # Text helpers
    # --------------------------------------------------------------------------
    def _room_text(self, room_name: str) -> str:
        room = self.rooms[room_name]
        lines = [f"-- {room.name} --", room.description]
        if room.has_item():
            lines.append(f"You see a {room.item.name}")
        exits = ", ".join(sorted(room.exits.keys()))
        lines.append(f"Exits: {exits}" if exits else "There are no exits from here.")
        return "\n".join(lines)

    def _inventory_text(self) -> str:
        if not self.player.inventory:
            return "You are not carrying anything."
        items = ", ".join(self.player.inventory_names())
        return f"Carrying ({len(self.player.inventory)}/{TOTAL_ITEMS_NEEDED}): {items}"

    def _map_text(self) -> str:
        lines = ["Rooms you have explored:"]
        for name in self.rooms:
            marker = "X" if name in self.player.visited else " "
            here = " <- You are here" if name == self.player.current_room else ""
            lines.append (f"    [{marker}] {name}{here}")
        return "\n".join(lines)

    def _help_text(self) -> str:
        return ("Commands:\n"
                " go/move <direction>   move North, South, East or West\n"
                " get/grab <item>       pick up an item in the current room\n"
                " inventory/i           show what you are carrying\n"
                " look                  redescribe the current room\n"
                " location/map          show which rooms you have visited\n"
                " save                  save your progress\n"
                " help/?                show this message\n"
                " exit/quit             leave the game\n")

    # ------------------------------------------------------------------------
    # Save/load
    # ------------------------------------------------------------------------

    def save(self) -> None:
        data = {
            "player": self.player.to_dict(),
            "collected_items": [i.name for i in self.player.inventory],
        }
        with open(SAVE_PATH, "w") as f:
            json.dump(data, f, indent=2)

    def load(self) -> bool:
        if not os.path.exists(SAVE_PATH):
            return False
        with open(SAVE_PATH) as f:
            data = json.load(f)
        self.player = Player.from_dict(data["player"])
        # make picked up items removed from world so they can not be picked up again
        for room in self.rooms.values():
            if room.has_item() and room.item.name in data["collected_items"]:
                room.remove_item()
        return True

    @staticmethod
    def has_save() -> bool:
        return os.path.exists(SAVE_PATH)