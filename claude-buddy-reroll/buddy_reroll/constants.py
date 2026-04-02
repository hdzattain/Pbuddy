"""Claude /buddy pet reroll constants."""

# Salt for deterministic hashing
SALT = 'friend-2026-401'

# Species (18 types)
SPECIES = (
    'duck', 'goose', 'blob', 'cat', 'dragon', 'octopus',
    'owl', 'penguin', 'turtle', 'snail', 'ghost', 'axolotl',
    'capybara', 'cactus', 'robot', 'rabbit', 'mushroom', 'chonk'
)

# Rarities with weights (must sum to 100)
RARITY_WEIGHTS = (
    ('common', 60),
    ('uncommon', 25),
    ('rare', 10),
    ('epic', 4),
    ('legendary', 1),
)

RARITIES = tuple(r[0] for r in RARITY_WEIGHTS)

# Rarity floor values for stats
RARITY_FLOORS = {
    'common': 5,
    'uncommon': 15,
    'rare': 25,
    'epic': 35,
    'legendary': 50,
}

# Eyes (6 types)
EYES = ('·', '✦', '×', '◉', '@', '°')

# Hats (8 types)
HATS = ('none', 'crown', 'tophat', 'propeller', 'halo', 'wizard', 'beanie', 'tinyduck')

# Stat names
STATS = ('DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK')

# Shiny probability (1%)
SHINY_CHANCE = 0.01

# FNV-1a 32-bit constants
FNV_OFFSET_BASIS = 2166136261
FNV_PRIME = 16777619
FNV_MOD = 2 ** 32
