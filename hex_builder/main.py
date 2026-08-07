import random

# Core game data used to generate random hexes and challenges.
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

# The three primary stats that can be affected by hazards and curses.
HAZARD_STATS = ["strength", "dexterity", "willpower"]

# Possible hazards that can appear in a hex.
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

# Possible curses that can appear in a hex.
CURSES = [
    "ice mist",
    "shifting pits",
    "illusory paths",
    "heralds of doom",
    "dark woods",
    "ominuous chimes",
    "deafining birds",
    "hallucinogenic spores",
    "confounding caverns",
    "eternal night",
    "ghostly shadows",
    "strange constellations",
]

def roll_stat() -> int:
    """Generate a single character stat using 3d6."""
    # Roll three six-sided dice and sum the result.
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
    # Use the supplied name, or fall back to a default if it is blank.
    return {
        "name": name.strip() or "Player",
        "hp": roll_hp(),
        "stats": generate_stats(),
    }


def print_character_status(character: dict[str, object]) -> None:
    """Print the current character status including HP and main stats."""
    # Show the full character sheet in a readable block.
    print("\nCurrent player status")
    print("---------------------")
    print(f"Name: {character['name']}")
    print(f"HP: {character['hp']}")
    for stat_name, stat_value in character["stats"].items():
        print(f"{stat_name.capitalize()}: {stat_value}")


def prompt_for_choice(prompt: str, character: dict[str, object]) -> str:
    """Prompt the player for a command, with 's' showing the character status."""
    while True:
        choice = input(prompt).strip().lower()
        if choice == "s":
            print_character_status(character)
            continue
        return choice


def random_hex_type() -> str:
    """Select a random hex type from the available terrain options."""
    # Choose one of the terrain categories defined at the top of the file.
    return random.choice(HEX_TYPES)


def random_landmark_for_type(hex_type: str) -> tuple[int, str]:
    """Roll a d20 on the landmark table and return the corresponding landmark."""
    # Pick a random landmark from the matching terrain list.
    if hex_type not in LANDMARKS:
        raise ValueError(f"Unknown hex type: {hex_type}")
    row = random.randint(1, len(LANDMARKS[hex_type]))
    return row, LANDMARKS[hex_type][row - 1]


def random_hazard() -> str:
    """Pick a random hazard from the hazard table."""
    return random.choice(HAZARDS)


def random_curse() -> str:
    """Pick a random curse from the curse table."""
    return random.choice(CURSES)


def random_challenge_stat() -> str:
    """Pick a single random stat for the challenge."""
    return random.choice(HAZARD_STATS)


def random_obstacle() -> tuple[str, str]:
    """Choose either a hazard or a curse and return its kind and name."""
    # A random decision determines whether the hex contains a hazard or a curse.
    if random.choice([True, False]):
        return "hazard", random_hazard()
    return "curse", random_curse()

HEX_DIRECTIONS: dict[str, tuple[str, tuple[int, int]]] = {
    "1": ("north", (0, -1)),
    "2": ("northeast", (1, -1)),
    "3": ("southeast", (1, 0)),
    "4": ("south", (0, 1)),
    "5": ("southwest", (-1, 1)),
    "6": ("northwest", (-1, 0)),
}


def roll_d20() -> int:
    """Roll a d20 for challenge resolution."""
    return random.randint(1, 20)


def resolve_challenge(
    character: dict[str, object], chosen_stat: str, kind: str = "hazard"
) -> tuple[bool, int, int, int, int]:
    # Resolve the challenge by comparing the roll to the chosen stat.
    """Resolve a challenge by rolling under the chosen stat.

    Hazards deal damage on failure; curses do not.
    Returns (success, roll, damage, soaked, remaining).
    """
    stat_value = int(character["stats"][chosen_stat])
    roll = roll_d20()
    if roll <= stat_value:
        return True, roll, 0, 0, 0

    if kind == "curse":
        return False, roll, 0, 0, 0

    damage = random.randint(1, 6)
    soaked = min(character["hp"], damage)
    character["hp"] -= soaked
    remaining = damage - soaked
    if remaining > 0:
        character["stats"][chosen_stat] = max(0, stat_value - remaining)
    return False, roll, damage, soaked, remaining


def generate_hex_entry() -> dict[str, str]:
    """Generate a single hex entry with landmark, obstacle kind, and stat."""
    # Build the data for one hex so the main loop can describe it clearly.
    hex_type = random_hex_type()
    _, landmark = random_landmark_for_type(hex_type)
    kind, obstacle = random_obstacle()
    stat = random_challenge_stat()
    return {
        "hex_type": hex_type,
        "landmark": landmark,
        "kind": kind,
        "obstacle": obstacle,
        "stat": stat,
    }


def choose_direction(character: dict[str, object]) -> tuple[str, tuple[int, int]] | None:
    """Ask the player to choose a direction for the next hex."""
    # Show the available movement options and validate the player's choice.
    print("\nChoose a direction to move into the next hex:")
    for number, (name, _) in HEX_DIRECTIONS.items():
        print(f"  {number} - {name}")

    while True:
        choice = prompt_for_choice("Direction [1-6/s/q]: ", character)
        if choice == "q":
            return None
        if choice in HEX_DIRECTIONS:
            return HEX_DIRECTIONS[choice]
        print("Invalid choice. Please enter a number from 1 to 6, or q to quit.")


def hex_key(position: tuple[int, int]) -> str:
    """Return a consistent key for a hex position."""
    # Store positions in a simple coordinate format for easy lookup.
    return f"{position[0]},{position[1]}"


if __name__ == "__main__":
    # Start the game by creating the player character and setting up the journey state.
    player_name = input("Enter your character name: ").strip()
    character = create_character(player_name)

    print("\nCharacter Sheet")
    print("--------------")
    print(f"Name: {character['name']}")
    print(f"HP: {character['hp']}")
    for stat_name, stat_value in character["stats"].items():
        print(f"{stat_name.capitalize()}: {stat_value}")

    print("\nYour journey begins. Choose a direction to move into the next hex, or type 'q' to quit.")
    hex_number = 0
    watch_count = 0
    position = (0, 0)
    visited_positions: set[tuple[int, int]] = {position}
    hex_map: dict[str, dict[str, str]] = {}
    print(f"Starting position: {position}")
    print(f"Visited hexes: {len(visited_positions)}")

    # Main gameplay loop: move through hexes, resolve challenges, and rest when required.
    while True:
        # Ask the player which direction to move next.
        direction_choice = choose_direction(character)
        if direction_choice is None:
            print("\nJourney ended.")
            break

        # Calculate the next position based on the selected direction.
        direction_name, delta = direction_choice
        next_position = (position[0] + delta[0], position[1] + delta[1])
        next_key = hex_key(next_position)
        if next_key in hex_map:
            entry = hex_map[next_key]
            revisited = True
        else:
            entry = generate_hex_entry()
            hex_map[next_key] = entry
            revisited = False

        print(f"\nAhead of you is a hex to the {direction_name} at {next_position}.")
        print(f"hex type: {entry['hex_type']}")
        print(f"landmark: {entry['landmark']}")
        print(f"{entry['kind'].capitalize()}: {entry['obstacle']}")
        print(f"stat for this challenge: {entry['stat']}")
        print(f"Current HP: {character['hp']}")
        if revisited:
            # Let the player know they have encountered this hex before.
            print(f"This is a previously visited hex. The same {entry['kind']} remains.")

        # Ask whether the player wants to enter and challenge this hex.
        while True:
            challenge_choice = prompt_for_choice("Do you wish to challenge this hex? (y/n/s/q) ", character)
            if challenge_choice == "y":
                position = next_position
                visited_positions.add(position)
                hex_number += 1
                watch_count += 1
                print(f"\nHex {hex_number} at {position}")
                print(f"Moved {direction_name} into this hex.")
                print(f"Visited hexes: {len(visited_positions)}")
                break
            if challenge_choice == "n":
                print("You retreat to the previous hex.")
                break
            if challenge_choice == "q":
                print("\nJourney ended.")
                direction_choice = None
                break
            print("Please answer 'y', 'n', or 'q'.")

        if challenge_choice == "n":
            continue
        if challenge_choice == "q":
            break

        # Resolve the challenge and describe the outcome.
        success, roll, damage, soaked, remaining = resolve_challenge(character, entry["stat"], entry["kind"])
        print(f"You rolled {roll} against {entry['stat']}.")
        if success:
            print("Success! You move on with no problem.")
        else:
            if entry["kind"] == "hazard":
                print(f"Failure. Damage rolled: {damage}.")
                print(f"HP soaked: {soaked}.")
                print(f"{remaining} damage carries over to {entry['stat']}.")
            else:
                print("Failure. The curse has taken hold.")
            if entry["kind"] == "curse":
                curse_outcome = random.choice(["drift", "double_watch"])
                if curse_outcome == "drift":
                    drift_direction = random.choice(list(HEX_DIRECTIONS.values()))
                    drift_name, drift_delta = drift_direction
                    position = (position[0] + drift_delta[0], position[1] + drift_delta[1])
                    visited_positions.add(position)
                    hex_number += 1
                    watch_count += 1
                    print(f"The curse has taken hold. You get lost and drift {drift_name} to a random hex at {position}, and lose an entire watch.")
                    print(f"Visited hexes: {len(visited_positions)}")
                else:
                    watch_count += 1
                    print("The curse has taken hold. You lose a watch and this hex takes two watches to move through.")
                    if watch_count >= 3:
                        print("You have passed the rest threshold without resting.")
                        watch_count -= 3
                        lost_stat = random.choice(HAZARD_STATS)
                        lost_amount = random.randint(1, 6)
                        character["stats"][lost_stat] = max(0, character["stats"][lost_stat] - lost_amount)
                        print(f"You suffer {lost_amount} loss to {lost_stat} because you did not rest.")
                        print(f"Current {lost_stat}: {character['stats'][lost_stat]}")
                        if any(value <= 0 for value in character["stats"].values()):
                            print("\nOne of your stats has dropped to 0. You are dead.")
                            print("Game over.")
                            break
        print(f"Current {entry['stat']}: {character['stats'][entry['stat']]}")
        print(f"Current HP: {character['hp']}")

        # Check whether the character has died from a stat loss.
        if any(value <= 0 for value in character["stats"].values()):
            print("\nOne of your stats has dropped to 0. You are dead.")
            print("Game over.")
            break

        # If enough watches have passed, offer the player a chance to rest.
        if watch_count >= 3:
            watch_count = 0
            print("\nYou have completed three watches.")
            print_character_status(character)
            while True:
                rest_choice = prompt_for_choice(
                    "Rest for the night and reset HP, or keep going and suffer 1d6 damage to a random stat? (y/n/s/q) ",
                    character,
                )
                if rest_choice == "y":
                    character["hp"] = roll_hp()
                    print(f"You rest and recover HP to {character['hp']}.")
                    break
                if rest_choice == "n":
                    lost_stat = random.choice(HAZARD_STATS)
                    lost_amount = random.randint(1, 6)
                    character["stats"][lost_stat] = max(0, character["stats"][lost_stat] - lost_amount)
                    print(f"You keep going and suffer {lost_amount} loss to {lost_stat}.")
                    print(f"Current {lost_stat}: {character['stats'][lost_stat]}")
                    if any(value <= 0 for value in character["stats"].values()):
                        print("\nOne of your stats has dropped to 0. You are dead.")
                        print("Game over.")
                        direction_choice = None
                    break
                if rest_choice == "q":
                    print("\nJourney ended.")
                    direction_choice = None
                    break
                print("Please answer 'y', 'n', or 'q'.")
            if direction_choice is None:
                break
