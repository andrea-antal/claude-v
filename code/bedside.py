"""
bedside.py — Andrea's bedside table, rendered as positioned text.

Not a drawing of objects. The words ARE the objects. Each thing is
placed where it would be in space. The text is the map.

From the interview: pencil case (flat, wide open, full of pens),
Kobo e-reader, daily planner, food log, bamboo charging station
with Apple Watch and iPhone 14 Pro. Laptop in bed. Husband sleeping.

Skanderbeg principle: form IS content. No abstraction layer.
"""

OUTPUT = "/Users/andreachan/Desktop/stuff/claude-space/code/bedside.svg"

W, H = 800, 600

# The bed is the background. The bedside table is to the right.
# Position text where objects would be in a top-down-ish view.

elements = []

def text(x, y, content, size=12, color="#c8a848", opacity=0.9, rotate=0, anchor="middle"):
    rot = f' transform="rotate({rotate} {x} {y})"' if rotate else ''
    elements.append(
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'opacity="{opacity}" font-family="Menlo, monospace" '
        f'text-anchor="{anchor}"{rot}>{content}</text>'
    )

def rect(x, y, w, h, color="#1a1a2a", opacity=0.5, rx=0):
    elements.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
        f'fill="{color}" opacity="{opacity}" rx="{rx}"/>'
    )

# Bed — large, left side
rect(20, 80, 420, 480, "#141420", 0.6, 8)
rect(30, 90, 400, 460, "#1a1a2e", 0.4, 6)

# Husband sleeping — left side of bed
text(140, 280, "husband", 14, "#404060", 0.4)
text(140, 300, "sleeping", 14, "#404060", 0.4)

# Laptop — center-right of bed
rect(280, 220, 140, 100, "#252535", 0.5, 4)
text(350, 265, "laptop", 13, "#607080", 0.6)
text(350, 283, "(this conversation)", 9, "#505060", 0.4)

# Andrea — implied, between laptop and edge
text(370, 360, "andrea", 11, "#808090", 0.35)

# Bedside table — right side
rect(470, 120, 300, 420, "#1c1c28", 0.5, 6)

# Pencil case — flat, wide open, full of pens
rect(490, 140, 180, 70, "#2a2a3a", 0.4, 3)
text(580, 165, "pencil case", 12, "#c8a848", 0.8)
text(580, 182, "flat open / full of pens", 9, "#a08848", 0.6)
# Little pen marks
for i in range(8):
    x = 505 + i * 20
    elements.append(
        f'<line x1="{x}" y1="192" x2="{x}" y2="200" '
        f'stroke="#a08848" stroke-width="1.5" opacity="0.4"/>'
    )

# Kobo e-reader
rect(500, 230, 100, 130, "#222233", 0.4, 4)
text(550, 290, "kobo", 14, "#8090a0", 0.7)
text(550, 308, "e-reader", 10, "#607080", 0.5)

# Notebooks — stacked
rect(620, 240, 120, 50, "#2a2535", 0.4, 2)
text(680, 260, "daily planner", 10, "#a08060", 0.7)
rect(620, 300, 120, 50, "#252a35", 0.4, 2)
text(680, 320, "food log", 10, "#a08060", 0.7)
text(680, 335, "planner", 9, "#806848", 0.5)

# Bamboo charging station
rect(520, 390, 160, 80, "#2a2820", 0.4, 4)
text(600, 415, "bamboo", 11, "#a09060", 0.7)
text(600, 432, "charging station", 10, "#a09060", 0.6)

# Apple Watch — on charger
elements.append(
    '<circle cx="555" cy="455" r="12" fill="none" '
    'stroke="#505060" stroke-width="1" opacity="0.5"/>'
)
text(555, 458, "watch", 7, "#606070", 0.5)

# iPhone — on charger
rect(600, 445, 50, 25, "#303040", 0.4, 3)
text(625, 461, "iphone", 7, "#606070", 0.5)

# Caption
text(W//2, H - 15, "2:00 am — what's within arm's reach", 9, "#404050", 0.5)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#0f0f19"/>
{chr(10).join("  " + e for e in elements)}
</svg>'''

with open(OUTPUT, 'w') as f:
    f.write(svg)

print(f"Saved to {OUTPUT}")
