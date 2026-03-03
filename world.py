"""
world.py — World & Navigation System
Person 1's module: defines all rooms, map layout, and movement logic.
"""

# ---------------------------------------------------------------------------
# WORLD DATA
# ---------------------------------------------------------------------------

ROOMS = {
    "entrance": {
        "name": "Castle Entrance",
        "description": (
            "You stand at the crumbling gates of an ancient castle. "
            "Torches flicker along mossy stone walls. A cold wind howls from the north."
        ),
        "exits": {"north": "hallway", "east": "courtyard"},
        "items": ["rusty_sword"],
        "enemy": None,
    },
    "hallway": {
        "name": "Dark Hallway",
        "description": (
            "A long corridor stretches before you. Portraits of forgotten kings "
            "stare down with empty eyes. You hear growling to the north."
        ),
        "exits": {"south": "entrance", "north": "throne_room", "east": "library"},
        "items": ["health_potion"],
        "enemy": "goblin",
    },
    "courtyard": {
        "name": "Overgrown Courtyard",
        "description": (
            "Cracked stone tiles are overtaken by wild vines. A dried-up fountain "
            "sits in the center. Something rustles in the bushes."
        ),
        "exits": {"west": "entrance", "north": "library"},
        "items": ["gold_coin", "gold_coin"],
        "enemy": "wolf",
    },
    "library": {
        "name": "Ancient Library",
        "description": (
            "Towering bookshelves line every wall. Most books have rotted away, "
            "but a faint magical glow emanates from one tome on the floor."
        ),
        "exits": {"west": "hallway", "south": "courtyard", "north": "throne_room"},
        "items": ["magic_scroll"],
        "enemy": None,
    },
    "throne_room": {
        "name": "The Throne Room",
        "description": (
            "A massive chamber with a cracked throne at its center. "
            "Bones litter the floor. On the throne sits the Dragon King — "
            "he was expecting you."
        ),
        "exits": {"south": "hallway"},
        "items": [],
        "enemy": "dragon_king",
    },
}


# ---------------------------------------------------------------------------
# NAVIGATION FUNCTIONS
# ---------------------------------------------------------------------------

def get_room(room_id: str) -> dict:
    """
    Retrieve room data by its ID.

    Parameters:
        room_id (str): The key of the room in the ROOMS dictionary.

    Returns:
        dict: The room data dictionary, or an empty dict if not found.
    """
    return ROOMS.get(room_id, {})


def describe_room(room_id: str) -> None:
    """
    Print the name, description, visible exits, and visible items of a room.

    Parameters:
        room_id (str): The key of the room to describe.

    Returns:
        None
    """
    room = get_room(room_id)
    if not room:
        print("You are nowhere. The void stares back.")
        return

    print(f"\n{'='*50}")
    print(f"  📍 {room['name']}")
    print(f"{'='*50}")
    print(f"{room['description']}\n")

    exits = room.get("exits", {})
    if exits:
        print(f"  Exits: {', '.join(exits.keys())}")
    else:
        print("  Exits: none")

    items = room.get("items", [])
    if items:
        print(f"  Items on the ground: {', '.join(items)}")

    if room.get("enemy"):
        print(f"  ⚠️  You sense a presence: [{room['enemy'].replace('_', ' ').title()}]")
    print()


def move(current_room_id: str, direction: str) -> str:
    """
    Attempt to move the player in a given direction from the current room.

    Parameters:
        current_room_id (str): The player's current room ID.
        direction (str): The direction the player wants to move (e.g. 'north').

    Returns:
        str: The new room ID if the move is valid, or the current room ID if not.
    """
    try:
        direction = direction.strip().lower()
        room = get_room(current_room_id)

        if not room:
            raise ValueError("Current room does not exist.")

        exits = room.get("exits", {})

        if direction not in exits:
            valid = ', '.join(exits.keys()) if exits else "none"
            print(f"  ❌ You can't go '{direction}' from here. Valid exits: {valid}")
            return current_room_id

        new_room_id = exits[direction]
        print(f"  ➡️  You head {direction}...")
        return new_room_id

    except ValueError as e:
        print(f"  ⚠️  Navigation error: {e}")
        return current_room_id


def pick_up_item(room_id: str, item_name: str) -> bool:
    """
    Remove an item from a room (called when a player picks it up).

    Parameters:
        room_id (str): The room the item is in.
        item_name (str): The name of the item to remove.

    Returns:
        bool: True if item was found and removed, False otherwise.
    """
    room = ROOMS.get(room_id, {})
    items = room.get("items", [])

    if item_name in items:
        items.remove(item_name)
        return True

    print(f"  ❌ '{item_name}' is not in this room.")
    return False


def clear_enemy(room_id: str) -> None:
    """
    Remove the enemy from a room after it has been defeated.

    Parameters:
        room_id (str): The room whose enemy should be cleared.

    Returns:
        None
    """
    if room_id in ROOMS:
        ROOMS[room_id]["enemy"] = None
