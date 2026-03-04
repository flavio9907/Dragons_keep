"""
inventory.py — Player & Inventory System
Person 3's module: defines the player, all items, and inventory management.
"""

# ---------------------------------------------------------------------------
# ITEM DATA
# ---------------------------------------------------------------------------

ITEMS = {
    "health_potion": {
        "name": "Health Potion",
        "description": "A glowing red vial. Restores 40 HP.",
        "type": "consumable",
        "effect": {"hp": 40},
        "value": 15,
    },
    "rusty_sword": {
        "name": "Rusty Sword",
        "description": "An old blade, still sharp enough. +5 Attack.",
        "type": "weapon",
        "effect": {"attack": 5},
        "value": 20,
    },
    "magic_scroll": {
        "name": "Magic Scroll",
        "description": "Crackles with energy. One-use: deals 30 damage to any enemy.",
        "type": "consumable",
        "effect": {"enemy_damage": 30},
        "value": 40,
    },
    "gold_coin": {
        "name": "Gold Coin",
        "description": "Shiny and valuable.",
        "type": "currency",
        "effect": {"gold": 5},
        "value": 5,
    },
    "iron_shield": {
        "name": "Iron Shield",
        "description": "A sturdy shield. +4 Defense.",
        "type": "armor",
        "effect": {"defense": 4},
        "value": 30,
        },
    "steel_sword": {
        "name": "Steel Sword",
        "description": "A well-forged blade, still sharp. +10 Attack.",
        "type": "weapon",
        "effect": {"attack": 10},
        "value": 45,
    },
    "chainmail": {
        "name": "Chainmail Armor",
        "description": "Interlocked steel rings. Heavy but protective. +8 Defense.",
        "type": "armor",
        "effect": {"defense": 5},
        "value": 50,
    },
}


# ---------------------------------------------------------------------------
# PLAYER FUNCTIONS
# ---------------------------------------------------------------------------

def create_player(name: str) -> dict:
    """
    Create and return a new player dictionary with default starting stats.

    Parameters:
        name (str): The player's chosen name.

    Returns:
        dict: A dictionary containing all player stats and an empty inventory.
    """
    return {
        "name": name,
        "hp": 100,
        "max_hp": 100,
        "attack": 10,
        "defense": 5,
        "level": 1,
        "xp": 0,
        "gold": 0,
        "inventory": [],
        "equipped_weapon": None,
        "equipped_armor": None,
    }


def show_stats(player: dict) -> None:
    """
    Display the player's current stats in a formatted summary.

    Parameters:
        player (dict): The player's stats dictionary.

    Returns:
        None
    """
    print(f"\n{'='*50}")
    print(f"  🧙 {player['name']}   |   Level {player['level']}")
    print(f"{'='*50}")
    print(f"  ❤️  HP:      {player['hp']} / {player['max_hp']}")
    print(f"  ⚔️  Attack:  {player['attack']}")
    print(f"  🛡️  Defense: {player['defense']}")
    print(f"  ✨ XP:      {player['xp']}")
    print(f"  💰 Gold:    {player['gold']}")
    print(f"  🎒 Items:   {', '.join(player['inventory']) if player['inventory'] else 'empty'}")
    print(f"{'='*50}\n")


def pick_up(player: dict, item_name: str) -> dict:
    """
    Add an item to the player's inventory, applying instant effects for
    currency-type items (like gold coins).

    Parameters:
        player (dict): The player's stats dictionary.
        item_name (str): The key of the item in the ITEMS dictionary.

    Returns:
        dict: The updated player dictionary.
    """
    item = ITEMS.get(item_name)

    if not item:
        print(f"  ❌ Unknown item: '{item_name}'")
        return player

    # Gold coins are auto-collected, not stored in inventory
    if item["type"] == "currency":
        gold_amount = item["effect"].get("gold", 0)
        player["gold"] += gold_amount
        print(f"  💰 You picked up {item['name']} (+{gold_amount} gold)!")
        return player

    player["inventory"].append(item_name)
    print(f"  🎒 You picked up: {item['name']} — {item['description']}")
    return player


def use_item(player: dict, item_name: str) -> dict:
    """
    Use a consumable item from the player's inventory, applying its effect.

    Parameters:
        player (dict): The player's stats dictionary.
        item_name (str): The key of the item to use.

    Returns:
        dict: The updated player dictionary.
    """
    try:
        if item_name not in player["inventory"]:
            print(f"  ❌ You don't have '{item_name}' in your inventory.")
            return player

        item = ITEMS.get(item_name)
        if not item:
            print(f"  ❌ Item data not found for '{item_name}'.")
            return player

        if item["type"] != "consumable":
            print(f"  ❌ {item['name']} cannot be used directly. Try equipping it instead.")
            return player

        effect = item["effect"]

        # Healing effect
        if "hp" in effect:
            heal_amount = effect["hp"]
            old_hp = player["hp"]
            player["hp"] = min(player["max_hp"], player["hp"] + heal_amount)
            actual_heal = player["hp"] - old_hp
            print(f"  💊 You used {item['name']} and restored {actual_heal} HP!")

        # Scroll: enemy_damage is handled in combat.py
        elif "enemy_damage" in effect:
            print(f"  📜 You unleash the {item['name']}! (deals {effect['enemy_damage']} damage to enemy)")
            # Return the damage value via a temporary player key for combat.py to read
            player["_scroll_damage"] = effect["enemy_damage"]

        player["inventory"].remove(item_name)
        return player

    except Exception as e:
        print(f"  ⚠️  Could not use item: {e}")
        return player


def equip_item(player: dict, item_name: str) -> dict:
    """
    Equip a weapon or armor item, boosting player stats.
    Unequips any previously equipped item of the same type.

    Parameters:
        player (dict): The player's stats dictionary.
        item_name (str): The key of the item to equip.

    Returns:
        dict: The updated player dictionary.
    """
    try:
        if item_name not in player["inventory"]:
            print(f"  ❌ You don't have '{item_name}' in your inventory.")
            return player

        item = ITEMS.get(item_name)
        if not item:
            print(f"  ❌ Item data not found.")
            return player

        if item["type"] == "weapon":
            # Unequip old weapon first
            if player["equipped_weapon"]:
                old = ITEMS[player["equipped_weapon"]]
                player["attack"] -= old["effect"].get("attack", 0)
                print(f"  🔄 Unequipped: {old['name']}")

            player["attack"] += item["effect"].get("attack", 0)
            player["equipped_weapon"] = item_name
            player["inventory"].remove(item_name)
            print(f"  ⚔️  Equipped: {item['name']} (+{item['effect'].get('attack',0)} Attack)")

        elif item["type"] == "armor":
            if player["equipped_armor"]:
                old = ITEMS[player["equipped_armor"]]
                player["defense"] -= old["effect"].get("defense", 0)
                print(f"  🔄 Unequipped: {old['name']}")

            player["defense"] += item["effect"].get("defense", 0)
            player["equipped_armor"] = item_name
            player["inventory"].remove(item_name)
            print(f"  🛡️  Equipped: {item['name']} (+{item['effect'].get('defense',0)} Defense)")

        else:
            print(f"  ❌ {item['name']} cannot be equipped.")

    except Exception as e:
        print(f"  ⚠️  Could not equip item: {e}")

    return player


def drop_item(player: dict, item_name: str) -> dict:
    """
    Remove an item from the player's inventory without using it.

    Parameters:
        player (dict): The player's stats dictionary.
        item_name (str): The key of the item to drop.

    Returns:
        dict: The updated player dictionary.
    """
    if item_name in player["inventory"]:
        player["inventory"].remove(item_name)
        item = ITEMS.get(item_name, {})
        print(f"  🗑️  You dropped: {item.get('name', item_name)}")
    else:
        print(f"  ❌ '{item_name}' is not in your inventory.")

    return player


def show_inventory(player: dict) -> None:
    """
    Print a detailed list of every item currently in the player's inventory.

    Parameters:
        player (dict): The player's stats dictionary.

    Returns:
        None
    """
    print("\n  🎒 Inventory:")
    if not player["inventory"]:
        print("     (empty)")
        return

    for item_name in player["inventory"]:
        item = ITEMS.get(item_name, {})
        print(f"     - {item.get('name', item_name)}: {item.get('description', '?')}")
    print()

SHOP_INVENTORY = {
    "health_potion": 15,
    "iron_shield": 30,
    "rusty_sword": 20,
    "magic_scroll": 40,
}

def visit_shop(player: dict) -> dict:
    """
    Opens an interactive shop where the player can spend gold on items.

    Parameters:
        player (dict): The player's stats dictionary.

    Returns:
        dict: The updated player dictionary.
    """
    print(f"\n{'='*50}")
    print("  🏪 MERCHANT'S SHOP")
    print(f"  Your gold: 💰 {player['gold']}")
    print(f"{'='*50}")

    for item_key, price in SHOP_INVENTORY.items():
        item = ITEMS.get(item_key, {})
        print(f"  {item.get('name', item_key):<20} {price} gold  —  {item.get('description', '')}")

    print("\n  Type an item name to buy it, or 'leave' to exit.")

    while True:
        try:
            choice = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "leave":
            print("  🚶 You leave the shop.")
            break

        if choice not in SHOP_INVENTORY:
            print("  ❌ That item isn't available. Check your spelling!")
            continue

        price = SHOP_INVENTORY[choice]
        if player["gold"] < price:
            print(f"  ❌ Not enough gold! You need {price} but only have {player['gold']}.")
            continue

        player["gold"] -= price
        player["inventory"].append(choice)
        item_name = ITEMS[choice]["name"]
        print(f"  ✅ You bought {item_name}! Remaining gold: {player['gold']}")

    return player