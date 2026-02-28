"""
One Line.
A drawing that stops before it's ready.
"""
from PIL import Image, ImageDraw
import random

WIDTH, HEIGHT = 800, 500
BG = (12, 12, 15)

img = Image.new("RGB", (WIDTH, HEIGHT), BG)
draw = ImageDraw.Draw(img)

random.seed(7)

# One line. Not centered. Not symmetrical. Just a gesture.
x = 90
y = HEIGHT // 2 + 30
points = [(x, y)]

for i in range(180):
    x += random.uniform(2.5, 4.5)
    y += random.gauss(0, 3.5)
    points.append((x, y))

# Draw it in amber, slightly transparent feel via thin strokes
for i in range(len(points) - 1):
    # Vary the brightness slightly along the line
    t = i / len(points)
    brightness = int(180 + 50 * t)
    color = (brightness, int(brightness * 0.75), int(brightness * 0.3))
    draw.line([points[i], points[i+1]], fill=color, width=2)

# That's it. No title. No legend. No second line.

img.save("/Users/andreachan/Desktop/stuff/claude-space/code/one-line.jpg", "JPEG", quality=85)
print("done")
