"""
growth.py — SVG of a branching structure that grows by simple rules.

Not a data visualization. Not a corpus analysis. Not a mapping.
A thing that makes its own shape.

Rules:
  - Start with a single vertical line
  - At each step, each branch tip either:
    (a) extends forward with slight angle drift
    (b) splits into two branches
  - The probability of splitting decreases with depth
  - Branch thickness decreases with depth
  - Color shifts from amber to pale as branches thin

The result is a tree-like form. Not a tree. Not a metaphor for anything.
Just what these rules produce.
"""

import random
import math

random.seed(7)  # Fixed seed for reproducibility

OUTPUT = "/Users/andreachan/Desktop/stuff/claude-space/code/growth.svg"

W, H = 800, 800
elements = []

def branch(x, y, angle, depth, thickness):
    if depth > 12 or thickness < 0.3:
        return

    # Length decreases with depth, with some randomness
    length = (28 - depth * 1.5) * random.uniform(0.7, 1.3)

    # End point
    x2 = x + length * math.sin(angle)
    y2 = y - length * math.cos(angle)

    # Color: warm amber fading to pale
    t = depth / 12
    r = int(200 + t * 50)
    g = int(140 + t * 90)
    b = int(40 + t * 140)
    color = f"rgb({min(255,r)},{min(255,g)},{min(255,b)})"

    # Opacity decreases slightly with depth
    opacity = max(0.3, 1.0 - t * 0.5)

    elements.append(
        f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{thickness:.1f}" '
        f'opacity="{opacity:.2f}" stroke-linecap="round"/>'
    )

    # Decide: split or continue
    split_chance = max(0.05, 0.55 - depth * 0.04)

    if random.random() < split_chance:
        # Split into two
        spread = random.uniform(0.3, 0.7)
        branch(x2, y2, angle - spread, depth + 1, thickness * 0.7)
        branch(x2, y2, angle + spread, depth + 1, thickness * 0.7)
        # Sometimes a third, weaker branch
        if random.random() < 0.15:
            branch(x2, y2, angle + random.uniform(-0.2, 0.2), depth + 1, thickness * 0.5)
    else:
        # Continue with drift
        drift = random.uniform(-0.25, 0.25)
        branch(x2, y2, angle + drift, depth + 1, thickness * 0.92)

# Grow from bottom center
branch(W/2, H - 60, 0, 0, 5)

# A few secondary trunks
branch(W/2 - 8, H - 60, -0.15, 0, 3.5)
branch(W/2 + 6, H - 60, 0.12, 0, 3)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#0f0f19"/>
{chr(10).join('  ' + e for e in elements)}
</svg>'''

with open(OUTPUT, 'w') as f:
    f.write(svg)

print(f"Generated {len(elements)} branches")
print(f"Saved to {OUTPUT}")
