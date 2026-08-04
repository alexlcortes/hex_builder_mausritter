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

# Store generated numbered hex entries here.
generated_hex_types: list[str] = []


def random_hex_type() -> str:
    """Select a random hex type from the available terrain options."""
    return random.choice(HEX_TYPES)


def random_landmark_for_type(hex_type: str) -> tuple[int, str]:
    """Roll a d20 on the landmark table and return the corresponding landmark."""
    if hex_type not in LANDMARKS:
        raise ValueError(f"Unknown hex type: {hex_type}")
    row = random.randint(1, len(LANDMARKS[hex_type]))
    return row, LANDMARKS[hex_type][row - 1]


def generate_hex_map(count: int = 1) -> list[str]:
    """Generate a numbered list of hex entries with landmarks from the table."""
    entries = []
    for index in range(count):
        hex_type = random_hex_type()
        _, landmark = random_landmark_for_type(hex_type)
        combined = f"{hex_type}, {landmark}"
        generated_hex_types.append(combined)
        entries.append(f"{index + 1}: {combined}")
    return entries


if __name__ == "__main__":
    hex_map = generate_hex_map()
    print("Generated hex map:")
    for entry in hex_map:
        print(entry)
    print("Stored hex types:", generated_hex_types)
