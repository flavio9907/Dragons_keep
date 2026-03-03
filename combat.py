"""
combat.py — Combat System
Person 2's module: defines all enemies, combat logic, and reward handling.
"""

import random
from inventory import use_item, show_inventory, ITEMS

# ---------------------------------------------------------------------------
# ENEMY DATA
# ---------------------------------------------------------------------------

ENEMIES = {
    "goblin": {
        "name": "Goblin",
        "hp": 30,
        "max_hp": 30,
        "attack": 6,
        "defense": 2,
        "xp_reward": 20,
        "gold_reward": 10,
        "description": "A small, vicious creature with a rusty blade.",
    },
    "wolf": {
        "name": "Shadow Wolf",
        "hp": 45,
        "max_hp": 45,
        "attack": 10,
        "defense": 3,
        "xp_reward": 35,
        "gold_reward": 5,
        "description": "A massive black wolf with glowing red eyes.",
    },
    "dragon_king": {
        "name": "Dragon King",
        "hp": 120,
        "max_hp": 120,
        "attack": 22,
        "defense": 10,
        "xp_reward": 200,
        "gold_reward": 100,
        "min_damage": 12,
        "description": "An ancient dragon sitting on a crumbling throne. Final boss.",
    },
    "skeleton": {
        "name": "Skeleton Soldier",
        "hp": 35,
        "max_hp": 35,
        "attack": 8,
        "defense": 4,
        "xp_reward": 25,
        "gold_reward": 8,
        "description": "A rattling skeleton in rusty armour, sword raised.",
    },
    "giant_spider": {
        "name": "Giant Spider",
        "hp": 50,
        "max_hp": 50,
        "attack": 12,
        "defense": 3,
        "xp_reward": 40,
        "gold_reward": 12,
        "description": "A massive black spider, fangs dripping with venom.",
    },
    "troll": {
        "name": "Cave Troll",
        "hp": 70,
        "max_hp": 70,
        "attack": 16,
        "defense": 6,
        "xp_reward": 60,
        "gold_reward": 20,
        "description": "A hulking troll that regenerates health each turn.",
    },
    "wraith": {
        "name": "Wraith",
        "hp": 55,
        "max_hp": 55,
        "attack": 14,
        "defense": 2,
        "xp_reward": 50,
        "gold_reward": 15,
        "description": "A ghostly figure that phases in and out of reality.",
    },
}


# ---------------------------------------------------------------------------
# COMBAT FUNCTIONS
# ---------------------------------------------------------------------------

def get_enemy(enemy_id: str) -> dict:
    """
    Return a fresh copy of an enemy by ID (so HP resets each encounter).

    Parameters:
        enemy_id (str): The key of the enemy in the ENEMIES dictionary.

    Returns:
        dict: A copy of the enemy's stats, or an empty dict if not found.
    """
    enemy_data = ENEMIES.get(enemy_id)
    if enemy_data:
        return enemy_data.copy()
    return {}


def calculate_damage(attacker_attack: int, defender_defense: int, min_damage: int = 1) -> int:
    """
    Calculate damage dealt after applying defense, with a small random variance.

    Parameters:
        attacker_attack (int): The attacker's attack stat.
        defender_defense (int): The defender's defense stat.
        min_damage (int): The minimum damage that can be dealt (default 1).

    Returns:
        int: The final damage value (minimum min_damage).
    """
    base_damage = attacker_attack - defender_defense
    variance = random.randint(-2, 3)
    return max(min_damage, base_damage + variance)


def player_attack(player: dict, enemy: dict) -> dict:
    """
    Execute the player's attack on an enemy.

    Parameters:
        player (dict): The player's stats dictionary.
        enemy (dict): The current enemy's stats dictionary (modified in place).

    Returns:
        dict: The updated enemy dictionary.
    """
    # Check for critical hit (10% chance)
    is_critical = random.random() < 0.10
    attack_power = player["attack"] * 2 if is_critical else player["attack"]

    damage = calculate_damage(attack_power, enemy["defense"])
    enemy["hp"] = max(0, enemy["hp"] - damage)

    if is_critical:
        print(f"  💥 CRITICAL HIT! You strike the {enemy['name']} for {damage} damage!")
    else:
        print(f"  ⚔️  You attack the {enemy['name']} for {damage} damage!")
    print(f"     {enemy['name']} HP: {enemy['hp']}/{enemy['max_hp']}")

    return enemy


def enemy_attack(enemy: dict, player: dict) -> dict:
    """
    Execute the enemy's attack on the player.

    Parameters:
        enemy (dict): The enemy's stats dictionary.
        player (dict): The player's stats dictionary (modified in place).

    Returns:
        dict: The updated player dictionary.
    """
    # Enemy has a 20% chance to miss
    if random.random() < 0.20:
        print(f"  🌀 The {enemy['name']} swings wildly and misses!")
        return player

    min_dmg = enemy.get("min_damage", 1)
    damage = calculate_damage(enemy["attack"], player["defense"], min_dmg)
    player["hp"] = max(0, player["hp"] - damage)

    print(f"  🩸 The {enemy['name']} hits you for {damage} damage!")
    print(f"     Your HP: {player['hp']}/{player['max_hp']}")

    return player


def award_rewards(player: dict, enemy: dict) -> dict:
    """
    Grant XP and gold to the player after defeating an enemy.
    Also checks if the player levels up.

    Parameters:
        player (dict): The player's stats dictionary.
        enemy (dict): The defeated enemy's stats dictionary.

    Returns:
        dict: The updated player dictionary.
    """
    xp_gained = enemy.get("xp_reward", 0)
    gold_gained = enemy.get("gold_reward", 0)

    player["xp"] += xp_gained
    player["gold"] += gold_gained

    print(f"\n  🏆 Victory! You defeated the {enemy['name']}!")
    print(f"     +{xp_gained} XP  |  +{gold_gained} Gold")

    # Level up every 50 XP
    xp_threshold = player["level"] * 50
    if player["xp"] >= xp_threshold:
        player = level_up(player)

    return player


def level_up(player: dict) -> dict:
    """
    Increase the player's level and improve their stats.

    Parameters:
        player (dict): The player's stats dictionary.

    Returns:
        dict: The updated player dictionary with improved stats.
    """
    player["level"] += 1
    player["max_hp"] += 15
    player["hp"] = player["max_hp"]   # Full heal on level up
    player["attack"] += 3
    player["defense"] += 2

    print(f"\n  ✨ LEVEL UP! You are now Level {player['level']}!")
    print(f"     Max HP ↑ | Attack ↑ | Defense ↑ | Full HP restored!")

    return player


def run_combat(player: dict, enemy_id: str) -> tuple:
    """
    Run a full turn-based combat loop between the player and an enemy.

    Parameters:
        player (dict): The player's stats dictionary.
        enemy_id (str): The ID of the enemy to fight.

    Returns:
        tuple: (player dict, won: bool)
            - player: updated player stats after combat
            - won: True if player won, False if player died
    """
    enemy = get_enemy(enemy_id)
    if not enemy:
        print("  ⚠️  No enemy found with that ID.")
        return player, False

    print(f"\n{'='*50}")
    print(f"  ⚔️  COMBAT: {enemy['name']} appears!")
    print(f"  {enemy['description']}")
    print(f"  Enemy HP: {enemy['hp']}  |  Attack: {enemy['attack']}  |  Defense: {enemy['defense']}")
    print(f"{'='*50}\n")

    while player["hp"] > 0 and enemy["hp"] > 0:
        print(f"  Your HP: {player['hp']}/{player['max_hp']}  |  {enemy['name']} HP: {enemy['hp']}/{enemy['max_hp']}")
        print("  Actions: [1] Attack  [2] Use Item  [3] Run")

        try:
            choice = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            choice = "3"

        if choice == "1":
            enemy = player_attack(player, enemy)
            if enemy["hp"] > 0:
                player = enemy_attack(enemy, player)

        elif choice == "2":
            show_inventory(player)
            item_choice = input("  Use which item? > ").strip().lower()
            if item_choice not in player["inventory"]:
                print(f"  ❌ You don't have '{item_choice}' in your inventory.")
            else:
                item_data = ITEMS.get(item_choice, {})
                item_type = item_data.get("type", "")
                if item_type in ("weapon", "armor"):
                    print(f"  ❌ You can't use equipment in combat! Equip weapons and armor before a fight.")
                else:
                    player = use_item(player, item_choice)
                    if "_scroll_damage" in player:
                        damage = player.pop("_scroll_damage")
                        enemy["hp"] = max(0, enemy["hp"] - damage)
                        print(f"  📜 The scroll blasts the {enemy['name']} for {damage} damage!")
                    # Enemy only counter-attacks if still alive
                    if enemy["hp"] > 0:
                        player = enemy_attack(enemy, player)

        elif choice == "3":
            escape_chance = random.random()
            if escape_chance > 0.4:
                print("  🏃 You successfully flee!")
                return player, False
            else:
                print("  ❌ You couldn't escape!")
                player = enemy_attack(enemy, player)

        else:
            print("  ❌ Invalid choice. Enter 1, 2, or 3.")

        print()

    if player["hp"] <= 0:
        print("\n  💀 You have been defeated...")
        return player, False

    player = award_rewards(player, enemy)
    return player, True