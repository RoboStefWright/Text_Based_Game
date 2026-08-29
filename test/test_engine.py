import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from game.engine import Game
from game.world import TOTAL_ITEMS_NEEDED


@pytest.fixture
def game():
    return Game()


def test_starting_state(game):
    assert game.player.current_room == "Dungeon Cell"
    assert game.player.inventory == []
    assert not game.game_over


def test_valid_move(game):
    game.execute_command("go West")
    assert game.player.current_room == "Basement"


def test_invalid_direction_does_not_move(game):
    game.execute_command("go North")  # no North exit from Dungeon Cell
    assert game.player.current_room == "Dungeon Cell"


def test_unknown_direction_word(game):
    msg = game.execute_command("go Up")
    assert "isn't a direction" in msg
    assert game.player.current_room == "Dungeon Cell"


def test_get_item_adds_to_inventory(game):
    game.execute_command("go West")  # -> Basement, has Keys
    msg = game.execute_command("get Keys")
    assert "pick up the Keys" in msg
    assert game.player.has_item("Keys")


def test_get_wrong_item_name_fails(game):
    game.execute_command("go West")  # -> Basement, has Keys
    msg = game.execute_command("get Amulet")
    assert "no 'Amulet' here" in msg
    assert not game.player.has_item("Amulet")


def test_get_item_when_room_empty(game):
    game.execute_command("go West")  # Basement
    game.execute_command("get Keys")  # room now empty
    msg = game.execute_command("get Keys")
    assert "nothing here" in msg


def test_item_removed_from_room_after_pickup(game):
    game.execute_command("go West")
    game.execute_command("get Keys")
    assert not game.rooms["Basement"].has_item()


def _collect_all_items(game):
    """Walks the player through the house and picks up all 7 items."""
    path = [
        ("go West", "Keys"),        # Dungeon Cell -> Basement
        ("go West", "Amulet"),      # Basement -> Cellar
        ("go East", None),          # Cellar -> Basement
        ("go North", "Staff"),      # Basement -> Grand Hall
        ("go East", "Cloak"),       # Grand Hall -> Sitting Room
        ("go North", "Book"),       # Sitting Room -> Library
        ("go South", None),         # Library -> Sitting Room
        ("go West", None),          # Sitting Room -> Grand Hall
        ("go West", "Dusty Cupcake"),  # Grand Hall -> Dining Room
        ("go North", "Strange Potion"),  # Dining Room -> Kitchen
    ]
    for move, item in path:
        game.execute_command(move)
        if item:
            game.execute_command(f"get {item}")


def test_full_playthrough_win(game):
    _collect_all_items(game)
    assert len(game.player.inventory) == TOTAL_ITEMS_NEEDED
    game.execute_command("go East")  # Kitchen -> Entryway
    game.execute_command("go East")  # Entryway -> Parlor
    assert game.game_over
    assert game.won


def test_entering_parlor_underprepared_requires_confirmation(game):
    game.execute_command("go West")   # Basement
    game.execute_command("go North")  # Grand Hall
    game.execute_command("go North")  # Entryway
    msg = game.execute_command("go East")  # -> Parlor, but 0 items
    assert "Enter anyway" in msg
    assert not game.game_over
    assert game.player.current_room == "Entryway"


def test_declining_parlor_entry_stays_put(game):
    game.execute_command("go West")
    game.execute_command("go North")
    game.execute_command("go North")
    game.execute_command("go East")  # triggers confirmation
    game.execute_command("no")
    assert not game.game_over
    assert game.player.current_room == "Entryway"


def test_confirming_parlor_entry_underprepared_loses(game):
    game.execute_command("go West")
    game.execute_command("go North")
    game.execute_command("go North")
    game.execute_command("go East")  # triggers confirmation
    game.execute_command("yes")
    assert game.game_over
    assert not game.won


def test_save_and_load_roundtrip(game, tmp_path, monkeypatch):
    import game.engine as engine_module
    save_file = tmp_path / "save.json"
    monkeypatch.setattr(engine_module, "SAVE_PATH", str(save_file))

    game.execute_command("go West")
    game.execute_command("get Keys")
    game.save()

    new_game = Game()
    new_game.load()
    assert new_game.player.current_room == "Basement"
    assert new_game.player.has_item("Keys")
    assert not new_game.rooms["Basement"].has_item()


def test_exit_command_ends_game(game):
    game.execute_command("exit")
    assert game.game_over
