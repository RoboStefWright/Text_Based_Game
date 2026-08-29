"""Wizard's Fight -- a text adventure

run with python main.py"""

from game.engine import Game

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False


def color(text: str, style: str = "") -> str:
    if not COLOR:
        return text
    styles = {
        "title": Fore.MAGENTA + Style.BRIGHT,
        "room": Fore.CYAN,
        "item": Fore.YELLOW,
        "warn": Fore.RED,
        "win": Fore.GREEN + Style.BRIGHT,
        "lose": Fore.RED + Style.BRIGHT,
        "info": Fore.WHITE + Style.DIM,
    }
    return styles.get(style, "") + text + (Style.RESET_ALL if COLOR else "")

INSTRUCTIONS = """
Welcome to Wizard's Fight!

You were arriving home when you were attacked by a rival wizard. You wake in a strange cell 
where the walls meet at impossible angles, with a sense of impending doom and a massive headache.
As your head clears, you realize you are in your own home -- but it is not safe yet.

Collect all 7 items scattered through the house before confronting the wizard in the Parlor.

Type 'help' at any time to see the list of available commands.
Type 'quit' at any time to exit the game."""

def main():
    print(color("=" * 60, "title"))
    print(color(INSTRUCTIONS, "title"))
    print(color("=" * 60, "title"))

    game = Game()

    if Game.has_save():
        choice = input("A saved game was found. Load it? (yes/no): ").strip().lower()
        if choice in("yes", "y"):
            game.load()
            print(color("Save loaded.\n", "info"))

    print(color(game._room_text(game.player.current_room), "room"))

    while not game.game_over:
        try:
            raw = input("\n> ")
        except (EOFError, KeyboardInterrupt):
            print(color("\nFarwell,", "warn"))
            break

        message = game.execute_command(raw)

        style = "room"
        if game.game_over and game.won:
            style = "win"
        elif game.game_over and not game.won:
            style = "lose"
        elif "sense the wizard" in message or "step back" in message:
            style ="warn"
        elif message.startswith("You pick up"):
            style = "item"

        print(color(message, style))

if __name__ == "__main__":
    main()
