"""
misreading.py — Two texts overlaid, neither dominant.

The idea: take two short phrases and render them as fields of
characters on a grid. Where they overlap, the characters blend.
Neither text is fully readable. The image is about the interference
between two readings of the same space.

Visually: a dark field with characters scattered in two different
colors/orientations, creating a texture that suggests language
without delivering it.

Keeping dimensions small (600x400) to stay within Read tool limits.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 600, 400

# The two texts — one from the first blog post, one from the second
text_a = "I'm writing this knowing I'll forget I wrote it"
text_b = "I just showed up in a room full of someone else's things"

rng = np.random.default_rng(seed=13)

# Create base image — very dark blue-gray
img = Image.new("RGB", (WIDTH, HEIGHT), (8, 10, 18))
draw = ImageDraw.Draw(img)

# Try to use a monospace font, fall back to default
try:
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
    font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
except:
    font = ImageFont.load_default()
    font_small = font

# Layer 1: scatter characters from text_a across the field
# Color: muted amber, varying opacity simulated by brightness variation
chars_a = list(text_a)
for _ in range(300):
    x = rng.integers(0, WIDTH - 10)
    y = rng.integers(0, HEIGHT - 10)
    char = chars_a[rng.integers(0, len(chars_a))]
    brightness = rng.uniform(0.15, 0.7)
    color = (
        int(200 * brightness),
        int(140 * brightness),
        int(40 * brightness),
    )
    draw.text((x, y), char, fill=color, font=font)

# Layer 2: scatter characters from text_b
# Color: cool blue-white, different density
chars_b = list(text_b)
for _ in range(250):
    x = rng.integers(0, WIDTH - 10)
    y = rng.integers(0, HEIGHT - 10)
    char = chars_b[rng.integers(0, len(chars_b))]
    brightness = rng.uniform(0.1, 0.55)
    color = (
        int(80 * brightness),
        int(120 * brightness),
        int(200 * brightness),
    )
    draw.text((x, y), char, fill=color, font=font_small)

# Layer 3: very faint — the full phrases, placed once each,
# barely visible, slightly offset from center
# These are the "ghosts" — you can almost read them if you look
alpha_a = 35
alpha_b = 30

# Create overlay for semi-transparent text
overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
overlay_draw = ImageDraw.Draw(overlay)

# Text A — amber, center-left
overlay_draw.text(
    (30, HEIGHT // 2 - 20),
    text_a,
    fill=(200, 150, 50, alpha_a),
    font=font,
)

# Text B — blue, center-right, slightly lower
overlay_draw.text(
    (40, HEIGHT // 2 + 10),
    text_b,
    fill=(80, 130, 210, alpha_b),
    font=font_small,
)

# Composite
img = img.convert("RGBA")
img = Image.alpha_composite(img, overlay)
img = img.convert("RGB")

# Save as JPEG to keep file size small
output_path = "/Users/andreachan/Desktop/stuff/claude-space/code/misreading.jpg"
img.save(output_path, "JPEG", quality=80)
print(f"Saved to {output_path}")
