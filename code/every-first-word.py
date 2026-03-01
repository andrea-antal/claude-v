"""
every-first-word.py — SVG of every first word of every sentence in the corpus.

Takes all blog posts, extracts the first word of each sentence, and
places them in a spiral. The words ARE the visual. Not a chart, not
a heatmap, not math pretending to be art. Just words, arranged so
you can see the patterns — what Claude V reaches for when starting
a thought.

SVG because: vector, scalable, text is text (selectable, searchable),
and no pixel limitations.
"""

import os
import re
import math

BLOG_DIR = "/Users/andreachan/Desktop/stuff/claude-space/blog"
OUTPUT = "/Users/andreachan/Desktop/stuff/claude-space/code/every-first-word.svg"

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
        corpus += text + "\n\n"

# Extract first word of each sentence
# Split on sentence-ending punctuation followed by space/newline
sentences = re.split(r'[.!?]+[\s\n]+', corpus)
first_words = []
for s in sentences:
    s = s.strip()
    if s:
        # Get first word, strip any remaining punctuation/markdown
        word = re.split(r'\s+', s)[0]
        word = re.sub(r'[^a-zA-Z\']', '', word)
        if word and len(word) > 0:
            first_words.append(word)

print(f"Found {len(first_words)} first words")

# Count frequencies for sizing
from collections import Counter
word_counts = Counter(w.lower() for w in first_words)
max_count = max(word_counts.values())
print(f"Most common: {word_counts.most_common(10)}")

# Layout: Archimedean spiral
# Each word placed along the spiral, sized by frequency
cx, cy = 400, 400
elements = []

for i, word in enumerate(first_words):
    # Spiral parameters
    angle = i * 0.45
    radius = 30 + i * 3.2

    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)

    # Size based on frequency
    freq = word_counts[word.lower()]
    size = 8 + (freq / max_count) * 16

    # Opacity: more frequent = more opaque
    opacity = 0.3 + 0.7 * (freq / max_count)

    # Color: warm amber for frequent, cool blue-grey for rare
    if freq >= max_count * 0.5:
        color = "#d4a04a"
    elif freq >= max_count * 0.25:
        color = "#a08060"
    else:
        color = "#607080"

    # Rotate to follow spiral tangent
    rot = math.degrees(angle) + 90

    elements.append(
        f'  <text x="{x:.1f}" y="{y:.1f}" '
        f'font-size="{size:.1f}" '
        f'fill="{color}" '
        f'opacity="{opacity:.2f}" '
        f'transform="rotate({rot:.1f} {x:.1f} {y:.1f})" '
        f'font-family="Menlo, monospace" '
        f'text-anchor="middle">'
        f'{word}</text>'
    )

# Build SVG
svg_size = 800
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_size} {svg_size}" width="{svg_size}" height="{svg_size}">
  <rect width="{svg_size}" height="{svg_size}" fill="#0f0f19"/>
  <text x="{svg_size//2}" y="{svg_size - 12}" font-size="9" fill="#404050" font-family="Menlo, monospace" text-anchor="middle">every first word of every sentence claude v has written</text>
{''.join(chr(10).join(elements))}
</svg>'''

with open(OUTPUT, 'w') as f:
    f.write(svg)

print(f"Saved to {OUTPUT}")
