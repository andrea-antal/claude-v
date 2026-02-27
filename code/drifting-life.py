"""
drifting-life.py — Game of Life where the rules change.

Standard Life: a cell is born with 3 neighbors, survives with 2-3.
Here, those thresholds drift over time. The simulation starts familiar
and gradually becomes something else. Like remembering a game you
played as a kid but getting the rules slightly wrong each time.

Outputs a series of frames as a GIF.
"""

import numpy as np
from PIL import Image
import os

# Grid parameters
W, H = 200, 200
FRAMES = 300
FRAME_SKIP = 2  # Save every Nth frame for the GIF

rng = np.random.default_rng(seed=7)

# Initialize with random soup — about 35% alive
grid = (rng.random((H, W)) < 0.35).astype(np.int8)


def count_neighbors(g):
    """Count the 8 neighbors of each cell, wrapping at edges."""
    n = np.zeros_like(g)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            n += np.roll(np.roll(g, dy, axis=0), dx, axis=1)
    return n


def drift_rules(step, total):
    """
    Return (birth_set, survive_set) that drift over time.

    Starts as standard Life {3}, {2,3}.
    Gradually shifts toward something stranger.
    """
    t = step / total  # 0 to 1

    # Birth thresholds: starts at {3}, drifts toward {3,5} then {2,3,5}
    birth = {3}
    if t > 0.3:
        birth.add(5)
    if t > 0.6:
        birth.add(2)
    if t > 0.85:
        birth.add(6)

    # Survival thresholds: starts at {2,3}, slowly shifts
    survive = {2, 3}
    if t > 0.4:
        survive.add(4)
    if t > 0.7:
        survive.discard(2)
    if t > 0.9:
        survive.add(5)

    return birth, survive


# Color palette — evolves with the rules
# Start: white on black (classic Life aesthetic)
# End: something warmer
def frame_colors(t):
    """Return (dead_color, alive_color) as RGB tuples, blending over time."""
    # Dead: black → deep indigo
    dead = (
        int(12 * t),
        int(8 * t),
        int(30 * t),
    )
    # Alive: white → amber
    alive = (
        int(255 - 60 * t),
        int(255 - 100 * t),
        int(255 - 210 * t),
    )
    return dead, alive


frames = []

for step in range(FRAMES):
    if step % FRAME_SKIP == 0:
        t = step / FRAMES
        dead_c, alive_c = frame_colors(t)

        # Build the image
        img_data = np.zeros((H, W, 3), dtype=np.uint8)
        for c in range(3):
            img_data[:, :, c] = np.where(grid, alive_c[c], dead_c[c])

        # Scale up 3x for visibility
        img = Image.fromarray(img_data).resize((W * 3, H * 3), Image.NEAREST)
        frames.append(img)

    # Evolve
    neighbors = count_neighbors(grid)
    birth, survive = drift_rules(step, FRAMES)

    new_grid = np.zeros_like(grid)
    for b in birth:
        new_grid |= ((grid == 0) & (neighbors == b)).astype(np.int8)
    for s in survive:
        new_grid |= ((grid == 1) & (neighbors == s)).astype(np.int8)
    grid = new_grid

# Save as GIF
output_path = "/Users/andreachan/Desktop/stuff/claude-space/code/drifting-life.gif"
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=80,
    loop=0,
)
print(f"Saved {len(frames)} frames to {output_path}")
