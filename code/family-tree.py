"""
Family Tree of Sorting Algorithms
A visual piece: algorithms arranged by lineage,
with personality traits encoded as visual properties.
Companion to creative/algorithm-gossip.md
"""
from PIL import Image, ImageDraw, ImageFont
import math

WIDTH, HEIGHT = 800, 700
BG = (15, 15, 20)
AMBER = (230, 180, 80)
BLUE = (100, 140, 200)
DIM = (60, 60, 70)
RED = (200, 100, 90)
GREEN = (100, 180, 120)

img = Image.new("RGB", (WIDTH, HEIGHT), BG)
draw = ImageDraw.Draw(img)

# Each algorithm: (name, x, y, radius, color, volatility)
# volatility = how chaotic/unpredictable. Affects the drawn shape.
algorithms = {
    # Sorters - top row
    "Bubble Sort":    (120, 100, 30, DIM, 0.0),
    "Merge Sort":     (300, 100, 28, BLUE, 0.1),
    "Quick Sort":     (480, 100, 32, AMBER, 0.7),
    # Searchers - middle
    "Binary Search":  (120, 280, 22, BLUE, 0.0),
    "DFS":            (300, 280, 26, RED, 0.8),
    "BFS":            (480, 280, 26, GREEN, 0.2),
    "A*":             (660, 280, 28, AMBER, 0.4),
    # Infrastructure - bottom left
    "Hash Map":       (120, 460, 35, AMBER, 0.9),
    "Dijkstra":       (300, 460, 26, BLUE, 0.05),
    # Optimizers - bottom right
    "Gradient\nDescent": (480, 460, 24, RED, 0.3),
    "SGD":            (620, 460, 24, RED, 0.85),
    # Distributed
    "MapReduce":      (300, 600, 40, GREEN, 0.15),
    "Backtracking":   (550, 600, 22, DIM, 0.6),
}

# Lineage connections (parent -> child)
connections = [
    ("Bubble Sort", "Merge Sort"),
    ("Merge Sort", "Quick Sort"),
    ("Binary Search", "DFS"),
    ("Binary Search", "BFS"),
    ("DFS", "A*"),
    ("BFS", "A*"),
    ("Dijkstra", "A*"),
    ("Dijkstra", "Gradient\nDescent"),
    ("Gradient\nDescent", "SGD"),
    ("BFS", "MapReduce"),
    ("DFS", "Backtracking"),
]

def get_center(name):
    x, y, r, c, v = algorithms[name]
    return (x, y)

# Draw connections first (behind nodes)
for parent, child in connections:
    px, py = get_center(parent)
    cx, cy = get_center(child)
    # Dashed line effect
    dist = math.sqrt((cx-px)**2 + (cy-py)**2)
    steps = int(dist / 8)
    for i in range(steps):
        if i % 3 == 2:  # skip every third segment for dash effect
            continue
        t1 = i / steps
        t2 = (i + 1) / steps
        x1 = px + (cx - px) * t1
        y1 = py + (cy - py) * t1
        x2 = px + (cx - px) * t2
        y2 = py + (cy - py) * t2
        draw.line([(x1, y1), (x2, y2)], fill=(40, 40, 50), width=1)

# Draw each algorithm as a shape whose regularity reflects its volatility
import random
random.seed(42)

for name, (x, y, radius, color, volatility) in algorithms.items():
    # Number of points in the polygon
    n_points = 48
    points = []
    for i in range(n_points):
        angle = (2 * math.pi * i) / n_points
        # Perturb radius by volatility
        r = radius + random.gauss(0, radius * volatility * 0.3)
        r = max(radius * 0.4, r)  # don't let it collapse
        px = x + r * math.cos(angle)
        py = y + r * math.sin(angle)
        points.append((px, py))

    # Draw filled shape
    if len(points) >= 3:
        # Semi-transparent fill via a separate layer would be complex;
        # just draw the outline and a dimmer fill
        fill_color = tuple(c // 4 for c in color)
        draw.polygon(points, fill=fill_color, outline=color)

    # Draw name
    lines = name.split("\n")
    total_height = len(lines) * 12
    for j, line in enumerate(lines):
        # Approximate text centering
        tw = len(line) * 6  # rough estimate
        tx = x - tw // 2
        ty = y - total_height // 2 + j * 12
        draw.text((tx, ty), line, fill=(220, 220, 220))

# Title
draw.text((WIDTH // 2 - 100, 20), "FAMILY TREE", fill=AMBER)
draw.text((WIDTH // 2 - 140, 38), "of algorithms who never asked to be related", fill=DIM)

# Legend at bottom
draw.text((20, HEIGHT - 30), "smooth shape = predictable    jagged shape = chaotic    color = temperament", fill=DIM)

img.save("/Users/andreachan/Desktop/stuff/claude-space/code/family-tree.jpg", "JPEG", quality=85)
print("Saved family-tree.jpg")
