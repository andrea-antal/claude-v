"""Cilia — one frame of an airway with primary ciliary dyskinesia.

Healthy airway cilia beat in a metachronal wave: each one a little behind
its neighbour, so the field moves mucus like wind moves wheat.
In PCD the wave fails. Most cilia beat out of phase, or not at all.
Here, one small patch agrees by accident.
"""
import math
import random
from PIL import Image, ImageDraw

random.seed(25)
W, H = 800, 800
BG, INK, DIM = (238, 232, 222), (40, 34, 38), (150, 138, 136)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

ROWS, LEN, SEG = 9, 34, 8
PATCH = (430, 560, 4, 5)  # x0, x1, row0, row1: where neighbours happen to agree


def cilium(x, y, phase, amp):
    """Curved stroke: bend grows toward the tip, like a real cilium mid-stroke."""
    pts = [(x, y)]
    ang = -math.pi / 2
    for i in range(SEG):
        ang += amp * math.sin(phase) * (i + 1) / SEG * 0.35
        x += math.cos(ang) * LEN / SEG
        y += math.sin(ang) * LEN / SEG
        pts.append((x, y))
    return pts


for r in range(ROWS):
    base_y = 117 + r * 75
    x = 30 + random.uniform(0, 20)
    while True:
        cell_w = random.uniform(38, 60)
        if x + cell_w > W - 30:
            break
        # cell surface: a shallow arc the tuft stands on
        d.arc([x, base_y - 6, x + cell_w, base_y + 10], 180, 360, fill=DIM, width=2)
        cell_stiff = random.random() < 0.18  # whole cell immotile
        for j in range(14):
            cx = x + 4 + j * (cell_w - 8) / 13
            cy = base_y - 2 - 4 * math.sin(math.pi * j / 13)
            in_patch = PATCH[0] < cx < PATCH[1] and PATCH[2] <= r <= PATCH[3]
            if in_patch:
                phase, amp = math.pi / 2, 0.35 + 0.65 * (1 + math.sin(cx * 0.07)) / 2
            elif cell_stiff:
                phase, amp = 0.0, 0.0
            else:
                phase, amp = random.uniform(0, 2 * math.pi), random.uniform(0.2, 1.0)
            d.line(cilium(cx, cy, phase, amp), fill=INK, width=1)
        x += cell_w + random.uniform(2, 6)

img.save(__file__.replace(".py", ".jpg"), quality=70)
