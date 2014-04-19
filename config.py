import math

# IN_THE_MATRIX: Set to True for a grainy, ascii cube.
IN_THE_MATRIX = True

# DEFAULT_FOV: Default angular field of view if no other is given.
DEFAULT_FOV = 2.0 * math.pi / 3.0

# DEFAULT_CHAR: Character to use for pixels (if not IN_THE_MATRIX).
DEFAULT_CHAR = ' '

# STEPS_PER_TURN: Number of animation frames per cube transformation.
STEPS_PER_TURN = 8
#STEPS_PER_TURN = 5

SCRAMBLE_LEN = 80

TILE_SIZE = 1.0

#GAP_SIZE = 0.35
GAP_SIZE = 0.20
