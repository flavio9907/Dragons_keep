"""
world.py — World & Navigation System
Flavio's module: defines all rooms, map layout, and movement logic.
"""

ROOMS = {
    "entrance": {
        "name": "Castle Entrance",
        "description": (
            "You stand at the crumbling gates of an ancient castle. "
            "Torches flicker along mossy stone walls. A cold wind howls from the north."
        ),
        "exits": {"north": "hallway", "east": "courtyard", "west": "market", "south": "forest_path"},
        "items": ["rusty_sword"],
        "enemy": None,
    },
    "market": {
        "name": "Wandering Merchant",
        "description": (
            "A hooded merchant sits beside a lantern, goods spread on a tattered cloth. "
            "'Buy something, will you?' he rasps."
        ),
        "exits": {"east": "entrance"},
        "items": [],
        "enemy": None,
    },
    "forest_path": {
        "name": "Forest Path",
        "description": (
            "A narrow trail winds through gnarled trees. Shadows move between "
            "the branches. Something watches you from the darkness."
        ),
        "exits": {"north": "entrance", "south": "deep_forest", "east": "swamp"},
        "items": ["health_potion"],
        "enemy": "goblin",
    },
    "deep_forest": {
        "name": "Deep Forest",
        "description": (
            "The trees grow dense here, blocking out the sky. Strange sounds echo "
            "all around. A faint glimmer on the ground catches your eye."
        ),
        "exits": {"north": "forest_path", "west": "abandoned_camp"},
        "items": ["gold_coin", "gold_coin"],
        "enemy": "wolf",
    },
    "abandoned_camp": {
        "name": "Abandoned Camp",
        "description": (
            "The remains of a campfire still smolder. Scattered supplies suggest "
            "someone left in a hurry. A rusted chest sits in the corner."
        ),
        "exits": {"east": "deep_forest"},
        "items": ["gold_coin", "gold_coin", "iron_shield"],
        "enemy": None,
    },
    "swamp": {
        "name": "Murky Swamp",
        "description": (
            "Thick fog clings to the ground. The air smells of rot. "
            "Every step sinks slightly into the mud. You hear splashing nearby."
        ),
        "exits": {"west": "forest_path", "north": "courtyard", "south": "swamp_depths"},
        "items": [],
        "enemy": "goblin",
    },
    "swamp_depths": {
        "name": "Swamp Depths",
        "description": (
            "The swamp grows darker and more treacherous. Twisted roots rise from "
            "the water like grasping hands. A troll lurks in the murk ahead."
        ),
        "exits": {"north": "swamp"},
        "items": ["health_potion", "magic_scroll"],
        "enemy": "troll",
    },
    "hallway": {
        "name": "Dark Hallway",
        "description": (
            "A long corridor stretches before you. Portraits of forgotten kings "
            "stare down with empty eyes. You hear growling to the north."
        ),
        "exits": {"south": "entrance", "north": "throne_room", "east": "library", "west": "barracks"},
        "items": [],
        "enemy": "goblin",
    },
    "barracks": {
        "name": "Old Barracks",
        "description": (
            "Rows of rotting bunk beds line the walls. Rusted armour hangs from "
            "stands. A skeleton soldier stirs as you enter."
        ),
        "exits": {"east": "hallway", "north": "armory"},
        "items": ["steel_sword"],
        "enemy": "skeleton",
    },
    "armory": {
        "name": "Castle Armory",
        "description": (
            "Weapon racks line every wall — most are empty, but a few useful "
            "pieces remain. A guard wolf circles the room protectively."
        ),
        "exits": {"south": "barracks"},
        "items": ["iron_shield", "chainmail", "gold_coin"],
        "enemy": "wolf",
    },
    "courtyard": {
        "name": "Overgrown Courtyard",
        "description": (
            "Cracked stone tiles are overtaken by wild vines. A dried-up fountain "
            "sits in the center. Something rustles in the bushes."
        ),
        "exits": {"west": "entrance", "north": "library", "south": "swamp", "east": "garden"},
        "items": [],
        "enemy": "wolf",
    },
    "garden": {
        "name": "Poisoned Garden",
        "description": (
            "What was once a beautiful garden is now overrun with dark thorned plants. "
            "Black flowers bloom in eerie silence. A giant spider descends from above."
        ),
        "exits": {"west": "courtyard"},
        "items": [],
        "enemy": "giant_spider",
    },
    "library": {
        "name": "Ancient Library",
        "description": (
            "Towering bookshelves line every wall. Most books have rotted away, "
            "but a faint magical glow emanates from one tome on the floor."
        ),
        "exits": {"west": "hallway", "south": "courtyard", "north": "study", "east": "chapel"},
        "items": ["magic_scroll"],
        "enemy": None,
    },
    "chapel": {
        "name": "Desecrated Chapel",
        "description": (
            "Broken pews and shattered stained glass litter the floor. "
            "An altar at the front glows faintly. A wraith drifts toward you."
        ),
        "exits": {"west": "library"},
        "items": ["health_potion", "gold_coin", "gold_coin", "gold_coin", "gold_coin"],
        "enemy": "wraith",
    },
    "study": {
        "name": "The Wizard's Study",
        "description": (
            "Beakers and scrolls cover every surface. A large crystal ball "
            "pulses with dim light. Bookshelves have been ransacked."
        ),
        "exits": {"south": "library", "north": "tower_stairs"},
        "items": ["magic_scroll"],
        "enemy": "skeleton",
    },
    "tower_stairs": {
        "name": "Tower Staircase",
        "description": (
            "A spiraling stone staircase winds upward into darkness. "
            "The air grows colder with every step. You can hear a deep rumble above."
        ),
        "exits": {"south": "study", "up": "throne_room"},
        "items": ["health_potion", "gold_coin"],
        "enemy": "troll",
    },
    "throne_room": {
        "name": "The Throne Room",
        "description": (
            "A massive chamber with a cracked throne at its center. "
            "Bones litter the floor. On the throne sits Bogdan the Dragon King — "
            "he was expecting you."
        ),
        "exits": {"south": "hallway"},
        "items": ["gold_coin", "gold_coin", "gold_coin", "gold_coin", "gold_coin"],
        "enemy": "dragon_king",
    },
}


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
        direction (str): The direction the player wants to move.

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
    Remove an item from a room when a player picks it up.

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
