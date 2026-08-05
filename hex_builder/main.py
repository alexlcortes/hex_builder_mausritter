import random

HEX_TYPES = [
    "countryside",
    "countryside",
    "forest",
    "forest",
    "river",
    "human town",
]

LANDMARKS = {
    "countryside": [
        "anthill",
        "lightning split beech",
        "bone-white tree",
        "cow skeleton",
        "field of flowers",
        "field of wheat",
        "hedge row",
        "hidden cave",
        "huge flat rock",
        "lily-lined pond",
        "massive fallen tree",
        "old craggy oak",
        "old farm house",
        "quiet dirt road",
        "rabbit warren",
        "sparrow nest",
        "stand of pine trees",
        "steep hill",
        "stone wall",
        "tangle of fig roots",
    ],
    "forest": [
        "abandoned shack",
        "bright clearing",
        "cascading waterfalls",
        "cliff face",
        "fresh spring cold",
        "dense underbrush",
        "face in ancient oak",
        "fox hole",
        "grove of ferns",
        "hollow tree stump",
        "huge pine tree",
        "human walking track",
        "meandering brook",
        "overgrown ruins",
        "ring of stones",
        "rocky outcropping",
        "sunken hollow",
        "tangle of roots",
        "termite-riddled tree",
        "human made clearing",
    ],
    "river": [
        "canal lock",
        "converging tributaries",
        "draping willow",
        "eroded riverbank",
        "fallen tree crossing",
        "high tree crossing",
        "huge boulder",
        "huge concrete dam",
        "isolated island",
        "muddy flats",
        "rocky rapids",
        "row of dead trees",
        "silty dam",
        "stepping-stones",
        "stone bridge",
        "stony shallows",
        "submerged trash",
        "sunken barge",
        "twisted roots",
        "wooden bridge",
    ],
    "human town": [
        "abandoned car",
        "apartment balcony",
        "blackberry hedge",
        "busy road",
        "drainpipe outlet",
        "dumped furniture",
        "greenhouse",
        "mouse ruins",
        "newly built house",
        "overgrown garden bed",
        "pigeon nest",
        "rocky riverbed",
        "shopping trolley",
        "stagnant pond",
        "steel bridge",
        "trash-filled skip",
        "underground car park",
        "woodshed",
        "tree-lined footpath",
        "pile of trash",
    ],
}

HAZARD_STATS = ["strength", "dexterity", "willpower"]

HAZARDS = [
    "choking woodland",
    "stinging leaves",
    "forgotten traps",
    "razor rocks",
    "carrion birds",
    "salt bog",
    "barbed gorge",
    "sticky weeds",
    "steam holes",
    "raging rapids",
    "toxic air",
    "spiked walls",
]

def roll_stat() -> int:
    """Generate a single character stat using 3d6."""
    return sum(random.randint(1, 6) for _ in range(3))


def roll_hp() -> int:
    """Generate a character HP value using 1d6."""
    return random.randint(1, 6)


def generate_stats() -> dict[str, int]:
    """Generate the character's strength, dexterity, and willpower."""
    return {
        "strength": roll_stat(),
        "dexterity": roll_stat(),
        "willpower": roll_stat(),
    }


def create_character(name: str) -> dict[str, object]:
    """Create a player character sheet with a name, stats, and HP."""
    return {
        "name": name.strip() or "Player",
        "hp": roll_hp(),
        "stats": generate_stats(),
    }


def random_hex_type() -> str:
    """Select a random hex type from the available terrain options."""
    return random.choice(HEX_TYPES)


def random_landmark_for_type(hex_type: str) -> tuple[int, str]:
    """Roll a d20 on the landmark table and return the corresponding landmark."""
    if hex_type not in LANDMARKS:
        raise ValueError(f"Unknown hex type: {hex_type}")
    row = random.randint(1, len(LANDMARKS[hex_type]))
    return row, LANDMARKS[hex_type][row - 1]


def random_hazard() -> str:
    """Pick a random hazard from the hazard table."""
    return random.choice(HAZARDS)


def random_hazard_stat() -> str:
    """Pick a single random stat for the hazard."""
    return random.choice(HAZARD_STATS)


def roll_d20() -> int:
    """Roll a d20 for hazard resolution."""
    return random.randint(1, 20)


def resolve_hazard(character: dict[str, object], chosen_stat: str) -> tuple[bool, int, int, int, int]:
    """Resolve a hazard by rolling under the chosen stat.

    Returns (success, roll, damage, soaked, remaining).
    """
    stat_value = int(character["stats"][chosen_stat])
    roll = roll_d20()
    if roll <= stat_value:
        return True, roll, 0, 0, 0

    damage = random.randint(1, 6)
    soaked = min(character["hp"], damage)
    character["hp"] -= soaked
    remaining = damage - soaked
    if remaining > 0:
        character["stats"][chosen_stat] = max(0, stat_value - remaining)
    return False, roll, damage, soaked, remaining


def generate_hex_entry() -> dict[str, str]:
    """Generate a single hex entry with landmark, hazard, and stat."""
    hex_type = random_hex_type()
    _, landmark = random_landmark_for_type(hex_type)
    hazard = random_hazard()
    stat = random_hazard_stat()
    return {
        "hex_type": hex_type,
        "landmark": landmark,
        "hazard": hazard,
        "stat": stat,
    }


if __name__ == "__main__":
    player_name = input("Enter your character name: ").strip()
    character = create_character(player_name)

    print("\nCharacter Sheet")
    print("--------------")
    print(f"Name: {character['name']}")
    print(f"HP: {character['hp']}")
    for stat_name, stat_value in character["stats"].items():
        print(f"{stat_name.capitalize()}: {stat_value}")

    print("\nYour journey begins. Press Enter to explore the next hex, or type 'q' to quit.")
    hex_number = 0
    watch_count = 0
    while True:
        user_input = input("Continue? [Enter/q] ").strip().lower()
        if user_input == "q":
            print("\nJourney ended.")
            break

        hex_number += 1
        watch_count += 1
        entry = generate_hex_entry()

        print(f"\nHex {hex_number}")
        print(f"hex type: {entry['hex_type']}")
        print(f"watch: {watch_count}")
        print(f"landmark: {entry['landmark']}")
        print(f"hazard: {entry['hazard']}")
        print(f"stat for this hazard: {entry['stat']}")
        print(f"Current HP: {character['hp']}")

        success, roll, damage, soaked, remaining = resolve_hazard(character, entry["stat"])
        print(f"You rolled {roll} against {entry['stat']}.")
        if success:
            print("Success! You move on with no problem.")
        else:
            print(f"Failure. Damage rolled: {damage}.")
            print(f"HP soaked: {soaked}.")
            print(f"{remaining} damage carries over to {entry['stat']}.")
        print(f"Current {entry['stat']}: {character['stats'][entry['stat']]}")
        print(f"Current HP: {character['hp']}")

        if any(value <= 0 for value in character["stats"].values()):
            print("\nOne of your stats has dropped to 0. You are dead.")
            print("Game over.")
            break

        if watch_count >= 3:
            watch_count = 0
            print("\nYou have completed three watches.")
            while True:
                rest_choice = input("Rest for the night and reset HP? (yes/no) ").strip().lower()
                if rest_choice in {"yes", "y"}:
                    character["hp"] = roll_hp()
                    print(f"You rest and recover HP to {character['hp']}.")
                    break
                if rest_choice in {"no", "n"}:
                    lost_stat = random.choice(HAZARD_STATS)
                    lost_amount = random.randint(1, 6)
                    character["stats"][lost_stat] = max(0, character["stats"][lost_stat] - lost_amount)
                    print(f"You keep going and suffer {lost_amount} loss to {lost_stat}.")
                    print(f"Current {lost_stat}: {character['stats'][lost_stat]}")
                    if any(value <= 0 for value in character["stats"].values()):
                        print("\nOne of your stats has dropped to 0. You are dead.")
                        print("Game over.")
                        user_input = "q"
                    break
                print("Please answer 'yes' or 'no'.")
            if user_input == "q":
                break
