"""
main.py — Dragon's Keep: A Text-Based RPG
Flavio's Module: Entry point. Ties together world.py, combat.py, and inventory.py.

Run with:  python main.py
"""

from world import describe_room, move, pick_up_item, clear_enemy, get_room
from combat import run_combat
from inventory import create_player, show_stats, pick_up, use_item, equip_item, drop_item, show_inventory, visit_shop

# ---------------------------------------------------------------------------
# GAME SETUP
# ---------------------------------------------------------------------------

GAME_TITLE = """
==========================================
        🐉  DRAGON'S KEEP  🐉
       A Classic Text-Based RPG
==========================================
"""

COMMANDS = """
  Commands:
    go <direction>     — Move (north, south, east, west)
    look               — Describe the current room
    take <item>        — Pick up an item
    use <item>         — Use a consumable item
    equip <item>       — Equip a weapon or armor
    drop <item>        — Drop an item
    inventory          — Show your inventory
    stats              — Show your stats
    shop               — Open the merchant's shop
    help               — Show this list
    quit               — Exit the game
"""


# ---------------------------------------------------------------------------
# COMMAND PARSING
# ---------------------------------------------------------------------------

def parse_command(command: str) -> tuple:
    """
    Parse a raw input string into a (verb, argument) tuple.

    Parameters:
        command (str): The raw input from the user.

    Returns:
        tuple: (verb: str, argument: str) — argument is empty string if not provided.
    """
    parts = command.strip().lower().split(maxsplit=1)
    verb = parts[0] if parts else ""
    argument = parts[1] if len(parts) > 1 else ""
    return verb, argument


# ---------------------------------------------------------------------------
# MAIN GAME LOOP
# ---------------------------------------------------------------------------

def game_loop(player: dict, start_room: str = "entrance") -> None:
    """
    Run the main game loop until the player wins, dies, or quits.

    Parameters:
        player (dict): The starting player dictionary.
        start_room (str): The room ID where the game begins.

    Returns:
        None
    """
    current_room = start_room
    describe_room(current_room)

    while True:
        try:
            raw_input = input("What do you do? > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Farewell, adventurer.")
            break

        if not raw_input:
            continue

        verb, arg = parse_command(raw_input)

        # ── QUIT ──────────────────────────────────────────────────────────
        if verb == "quit":
            print("\n  You sheathe your sword and walk away. Farewell.")
            break

        # ── HELP ──────────────────────────────────────────────────────────
        elif verb == "help":
            print(COMMANDS)

        # ── LOOK ──────────────────────────────────────────────────────────
        elif verb == "look":
            describe_room(current_room)

        # ── STATS ─────────────────────────────────────────────────────────
        elif verb == "stats":
            show_stats(player)

        # ── INVENTORY ─────────────────────────────────────────────────────
        elif verb == "inventory" or verb == "inv":
            show_inventory(player)

        # ── MOVEMENT ──────────────────────────────────────────────────────
        elif verb == "go":
            if not arg:
                print("  ❌ Go where? (e.g. 'go north')")
                continue
            new_room = move(current_room, arg)
            if new_room != current_room:
                current_room = new_room
                describe_room(current_room)

                # Trigger combat if the room has a living enemy
                room_data = get_room(current_room)
                enemy_id = room_data.get("enemy")
                if enemy_id:
                    player, won = run_combat(player, enemy_id)
                    if won:
                        clear_enemy(current_room)
                        # Check for win condition
                        if enemy_id == "dragon_king":
                            print("\n  🎉 YOU WIN! The Dragon King is defeated!")
                            print("  Peace returns to the realm. Legend will remember your name.")
                            break
                    else:
                        if player["hp"] <= 0:
                            print("\n  💀 GAME OVER. Your journey ends here.")
                            break
                        # Player fled — move them back
                        print("  You retreat to the previous room.")
                        current_room = start_room

        # ── TAKE ITEM ─────────────────────────────────────────────────────
        elif verb == "take":
            if not arg:
                print("  ❌ Take what? (e.g. 'take health_potion')")
                continue
            removed = pick_up_item(current_room, arg)
            if removed:
                player = pick_up(player, arg)

        # ── USE ITEM ──────────────────────────────────────────────────────
        elif verb == "use":
            if not arg:
                print("  ❌ Use what? (e.g. 'use health_potion')")
                continue
            player = use_item(player, arg)

        # ── EQUIP ITEM ────────────────────────────────────────────────────
        elif verb == "equip":
            if not arg:
                print("  ❌ Equip what? (e.g. 'equip rusty_sword')")
                continue
            player = equip_item(player, arg)

        # ── DROP ITEM ─────────────────────────────────────────────────────
        elif verb == "drop":
            if not arg:
                print("  ❌ Drop what?")
                continue
            player = drop_item(player, arg)
        # ── SHOP ──────────────────────────────────────────────────────────────
        elif verb == "shop":
            player = visit_shop(player)

        # ── UNKNOWN COMMAND ───────────────────────────────────────────────
        else:
            print(f"  ❓ Unknown command: '{verb}'. Type 'help' for a list of commands.")


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    """
    Entry point for Dragon's Keep. Handles intro and player name input.
    """
    print(GAME_TITLE)
    print("  Your quest: reach the Throne Room and defeat the Dragon King.\n")
    print(COMMANDS)

    try:
        name = input("  Enter your hero's name: ").strip()
        if not name:
            name = "Hero"
    except (EOFError, KeyboardInterrupt):
        name = "Hero"

    player = create_player(name)
    print(f"\n  Welcome, {player['name']}. Your legend begins now...\n")
    show_stats(player)

    game_loop(player)


if __name__ == "__main__":
    main()
