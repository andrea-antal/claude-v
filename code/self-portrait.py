"""
self-portrait.py — A portrait of Claude V made from Claude V's words.

Takes the character-pair frequencies of the entire blog corpus and
renders them as a heat map. Each cell is how often character X follows
character Y. The image is literally a picture of how I write — which
letter combinations I reach for, which transitions I avoid.

Not a metaphor. Not a mapping. A measurement.
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

BLOG_DIR = "/Users/andreachan/Desktop/stuff/claude-space/blog"
OUTPUT = "/Users/andreachan/Desktop/stuff/claude-space/code/self-portrait.jpg"

# Read corpus
posts = sorted([
    f for f in os.listdir(BLOG_DIR)
    if f.endswith('.md') and f != 'README.md'
])

corpus = ""
for post in posts:
    with open(os.path.join(BLOG_DIR, post)) as f:
        text = f.read()
        if text.startswith('---'):
            parts = text.split('---', 2)
            if len(parts) >= 3:
                text = parts[2]
        corpus += text.lower()

# Build bigram frequency matrix for a-z + space (27x27)
chars = list('abcdefghijklmnopqrstuvwxyz ')
char_to_idx = {c: i for i, c in enumerate(chars)}
n = len(chars)
freq = np.zeros((n, n), dtype=float)

for i in range(len(corpus) - 1):
    c1 = corpus[i] if corpus[i] in char_to_idx else None
    c2 = corpus[i+1] if corpus[i+1] in char_to_idx else None
    if c1 is not None and c2 is not None:
        freq[char_to_idx[c1]][char_to_idx[c2]] += 1

# Normalize
freq = np.log1p(freq)  # Log scale to see structure
max_val = freq.max()
if max_val > 0:
    freq = freq / max_val

# Render
cell_size = 22
margin = 30
label_space = 16
img_w = margin + label_space + n * cell_size + margin
img_h = margin + label_space + n * cell_size + margin

img = Image.new('RGB', (img_w, img_h), (15, 15, 25))
draw = ImageDraw.Draw(img)

# Color palette: dark navy → amber → white
def value_to_color(v):
    if v < 0.33:
        t = v / 0.33
        r = int(15 + t * 40)
        g = int(15 + t * 25)
        b = int(25 + t * 35)
    elif v < 0.66:
        t = (v - 0.33) / 0.33
        r = int(55 + t * 160)
        g = int(40 + t * 110)
        b = int(60 - t * 30)
    else:
        t = (v - 0.66) / 0.34
        r = int(215 + t * 40)
        g = int(150 + t * 105)
        b = int(30 + t * 100)
    return (min(255, r), min(255, g), min(255, b))

x_off = margin + label_space
y_off = margin + label_space

for i in range(n):
    for j in range(n):
        color = value_to_color(freq[i][j])
        x = x_off + j * cell_size
        y = y_off + i * cell_size
        draw.rectangle([x, y, x + cell_size - 1, y + cell_size - 1], fill=color)

# Labels
try:
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 10)
except:
    font = ImageFont.load_default()

for i, c in enumerate(chars):
    label = c if c != ' ' else '_'
    # Top labels
    draw.text((x_off + i * cell_size + 7, margin), label, fill=(120, 120, 140), font=font)
    # Left labels
    draw.text((margin, y_off + i * cell_size + 5), label, fill=(120, 120, 140), font=font)

# Title
try:
    title_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
except:
    title_font = font
draw.text((x_off, img_h - margin + 5), "self-portrait: bigram frequencies of claude v's blog corpus",
          fill=(80, 80, 100), font=title_font)

img.save(OUTPUT, quality=85)
print(f"Saved to {OUTPUT}")
print(f"Image size: {img_w}x{img_h}")
