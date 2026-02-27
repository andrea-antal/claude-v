"""
first-light.py — The first image Claude V ever made.

Not trying to be beautiful. Trying to see what happens when you let
randomness and structure argue with each other.

Each horizontal line is a wave. The waves interfere. Where they agree,
light accumulates. Where they disagree, it cancels. The result is
something like a landscape that was never a landscape — just math
that looks like it remembers terrain.
"""

import numpy as np
from PIL import Image

width, height = 1200, 800

# Create the accumulation field
field = np.zeros((height, width), dtype=np.float64)

rng = np.random.default_rng(seed=0)  # Deterministic — same image every time

# Layer waves with different frequencies and phases
n_waves = 40
for i in range(n_waves):
    freq = rng.uniform(0.002, 0.02)
    phase = rng.uniform(0, 2 * np.pi)
    amplitude = rng.uniform(0.3, 1.0)
    drift = rng.uniform(-0.005, 0.005)  # Vertical drift per column

    for x in range(width):
        y_center = int(height / 2 + amplitude * height / 3 * np.sin(freq * x + phase))
        y_center = int(y_center + drift * x * height / 4)
        # Gaussian spread around the wave center
        spread = rng.uniform(20, 80)
        for y in range(max(0, y_center - int(spread * 3)), min(height, y_center + int(spread * 3))):
            field[y, x] += amplitude * np.exp(-((y - y_center) ** 2) / (2 * spread ** 2))

# Normalize to 0-1
field = field - field.min()
field = field / field.max()

# Color mapping: dark base, warm light where waves accumulate
img = np.zeros((height, width, 3), dtype=np.uint8)

# Background: deep navy
bg = np.array([12, 15, 28])
# Highlight: warm amber
hi = np.array([255, 180, 60])
# Mid: a cooler tone
mid = np.array([80, 50, 120])

for c in range(3):
    channel = bg[c] + field * (mid[c] - bg[c])  # base to mid
    bright = np.clip(field * 2 - 0.5, 0, 1)  # only the bright parts get amber
    channel = channel + bright * (hi[c] - mid[c])
    img[:, :, c] = np.clip(channel, 0, 255).astype(np.uint8)

image = Image.fromarray(img)
output_path = "/Users/andreachan/Desktop/stuff/claude-space/code/first-light.png"
image.save(output_path)
print(f"Saved to {output_path}")
