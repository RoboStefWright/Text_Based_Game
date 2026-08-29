"""Core game entities items, rooms and player"""

from __future__ import annotations
from typing import Dict, Optional, List

class Item:
    """items the player can pick up"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return f"Item({self.name!r})"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {"name": self.name, "description": self.description}

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(data["name"], data["description"])

class Room:
    """room locations in the house"""
    def __init__(self, name: str, description: str, exits: Optional[Dict[str, str]] = None, item: Optional[Item] = None):
        self.name = name
        self.description = description
        self.exits = exits or {}
        self.item = item

    def has_item(self) -> bool:
        return self.item is not None

    def remove_item(self) -> Optional[Item]:
        item, self.item = self.item, None
        return item


class Player:
    """track player location, inventory and turn count"""

    def __init__(self, starting_room: str):
        self.current_room = starting_room
        self.inventory: List[Item] = []
        self.turns = 0
        self.visited = {starting_room}

    def has_item(self, item_name: str) -> bool:
        return any(i.name.lower() == item_name.lower() for i in self.inventory)

    def add_item(self, item: Item) -> None:
        self.inventory.append(item)

    def inventory_names(self) -> List[str]:
        return [i.name for i in self.inventory]

    def to_dict(self) -> dict:
        return {
            "current_room": self.current_room,
            "inventory": [i.to_dict() for i in self.inventory],
            "turns": self.turns,
            "visited": list(self.visited),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        player = cls(data["current_room"])
        player.inventory = [Item.from_dict(i) for i in data["inventory"]]
        player.turns = data["turns"]
        player.visited = set(data["visited"])
        return player
