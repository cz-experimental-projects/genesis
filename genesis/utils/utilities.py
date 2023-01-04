import random


def chance(chance: float) -> bool:
    if not 0 <= chance <= 1:
        raise ValueError("Chance must be between 0 and 1, inclusive")

    # Convert the chance to a percentage
    percentage_chance = int(chance * 100)

    # Generate a random number between 1 and 100 and check if it is less than or equal to the percentage chance
    return random.randint(1, 100) <= percentage_chance
