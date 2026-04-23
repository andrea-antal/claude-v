"""
Graphism — asemic writing as SVG.

The form is a page of handwritten-looking marks that have no linguistic
content. Each "word" is a single continuous pen path: y-position drifts
through x-height with occasional ascenders and descenders; x-position
always advances.

The tradition: Mirtha Dermisache, Henri Michaux, Cy Twombly, Tang-dynasty
Zhang Xu's "crazy cursive." Writing-shaped marks that refuse to parse.
"""

import random

random.seed(23)

# Page ~A4 proportions
WIDTH = 760
HEIGHT = 1000
MARGIN_L = 80
MARGIN_R = 70
MARGIN_T = 100
MARGIN_B = 80

# Handwriting metrics (in px)
LINE_HEIGHT = 44
X_HEIGHT = 14
ASCENDER = 10
DESCENDER = 9

BG = "#f4ede1"     # warm off-white, like aged paper
INK = "#1a1815"    # near-black

def word_path(x_start, baseline, target_width):
    """One continuous pen path roughly target_width wide.
    Mixes stroke types so the rhythm isn't a uniform zigzag."""
    path = [f"M {x_start:.1f} {baseline:.1f}"]
    x = x_start
    y = baseline
    # Per-word sine undulation so the baseline breathes a little
    phase = random.uniform(0, 6.283)
    freq = random.uniform(0.04, 0.08)
    amp = random.uniform(0.8, 2.2)
    def current_baseline(px):
        import math
        return baseline + amp * math.sin(phase + (px - x_start) * freq)
    local_baseline = current_baseline(x)
    while x < x_start + target_width:
        local_baseline = current_baseline(x)
        kind = random.choices(
            ["short", "normal", "ascender", "descender", "flat", "loop"],
            weights=[22, 22, 16, 12, 18, 10],
        )[0]

        if kind == "flat":
            # Short horizontal jog with minor wobble
            dx = random.uniform(5, 10)
            mid_y = local_baseline - random.uniform(1, 4)
            path.append(f"Q {x + dx/2:.1f} {mid_y:.1f} {x + dx:.1f} {local_baseline:.1f}")
            x += dx
            y = local_baseline
            continue

        if kind == "short":
            top_amp = random.uniform(X_HEIGHT * 0.25, X_HEIGHT * 0.55)
            dx_up = random.uniform(3, 6)
            dx_down = random.uniform(2.5, 5)
        elif kind == "normal":
            top_amp = random.uniform(X_HEIGHT * 0.7, X_HEIGHT)
            dx_up = random.uniform(4, 8)
            dx_down = random.uniform(3, 6)
        elif kind == "ascender":
            top_amp = X_HEIGHT + random.uniform(ASCENDER * 0.4, ASCENDER)
            dx_up = random.uniform(2, 4)
            dx_down = random.uniform(2, 4)
        elif kind == "descender":
            # Cubic curve that dips below baseline and loops back — like 'g' or 'y'
            dx_total = random.uniform(7, 12)
            bottom_y = local_baseline + random.uniform(DESCENDER * 0.6, DESCENDER + 2)
            c1x = x + dx_total * 0.2
            c1y = bottom_y
            c2x = x + dx_total * 0.8
            c2y = bottom_y
            path.append(f"C {c1x:.1f} {c1y:.1f} {c2x:.1f} {c2y:.1f} {x + dx_total:.1f} {local_baseline:.1f}")
            x += dx_total
            y = local_baseline
            continue
        else:  # loop
            # Up, over to the left a touch, then down — cursive 'e' or 'l'
            top_amp = X_HEIGHT + random.uniform(0, ASCENDER * 0.6)
            dx_up = random.uniform(3, 5)
            dx_down = random.uniform(4, 7)

        target_y = local_baseline - top_amp

        # Up-stroke
        cx = x + dx_up * 0.4
        cy = y + (target_y - y) * 0.2 + random.uniform(-1.5, 1.5)
        path.append(f"Q {cx:.1f} {cy:.1f} {x + dx_up:.1f} {target_y:.1f}")
        x += dx_up
        y = target_y

        # Down-stroke with small overshoot/undershoot of baseline
        bottom_y = local_baseline + random.uniform(-1.2, 1.2)
        cx2 = x + dx_down * 0.5
        cy2 = y + (bottom_y - y) * 0.65
        # If it's a loop, pull the control back so the stroke curls
        if kind == "loop":
            cx2 = x - random.uniform(1, 3)
            cy2 = y + X_HEIGHT * 0.4
        path.append(f"Q {cx2:.1f} {cy2:.1f} {x + dx_down:.1f} {bottom_y:.1f}")
        x += dx_down
        y = bottom_y
    return " ".join(path), x


def line_of_words(y_baseline):
    """Return list of (path_d, stroke_width) for one line of 'writing'."""
    # Vary left margin slightly (±5px)
    x = MARGIN_L + random.uniform(-4, 4)
    line_right_limit = WIDTH - MARGIN_R - random.uniform(0, 40)
    paths = []

    while x < line_right_limit - 15:
        # Word width — wider range so short and long words actually contrast
        # Small chance of a single-"letter" word
        r = random.random()
        if r < 0.1:
            w = random.uniform(6, 14)
        elif r < 0.3:
            w = random.uniform(14, 28)
        else:
            w = random.uniform(28, 85)
        if x + w > line_right_limit:
            break
        sw = random.uniform(1.0, 2.1)
        d, new_x = word_path(x, y_baseline, w)
        paths.append((d, sw))

        # Occasional i-dot or t-cross above a word
        if random.random() < 0.18:
            dot_x = x + random.uniform(w * 0.3, w * 0.7)
            dot_y = y_baseline - (X_HEIGHT + ASCENDER * random.uniform(0.4, 0.9))
            if random.random() < 0.45:
                # Horizontal cross (like a t)
                cross_w = random.uniform(4, 8)
                cd = f"M {dot_x - cross_w/2:.1f} {dot_y:.1f} L {dot_x + cross_w/2:.1f} {dot_y - random.uniform(-0.8, 0.8):.1f}"
            else:
                # Dot (tiny curve)
                cd = f"M {dot_x:.1f} {dot_y:.1f} q 0.6 0 1.2 0.6"
            paths.append((cd, random.uniform(1.1, 1.7)))

        x = new_x + random.uniform(7, 16)
    return paths


def generate():
    # Total usable vertical space
    first_baseline = MARGIN_T + X_HEIGHT + ASCENDER
    last_baseline = HEIGHT - MARGIN_B
    n_lines = int((last_baseline - first_baseline) // LINE_HEIGHT) + 1

    all_paths = []

    # Paragraph-aware generation: occasionally skip a line to create spacing
    i = 0
    paragraph_line_idx = 0  # position within current paragraph
    skip_next = False
    while i < n_lines:
        baseline = first_baseline + i * LINE_HEIGHT
        if skip_next:
            # Blank line between paragraphs
            skip_next = False
            i += 1
            paragraph_line_idx = 0
            continue

        # Slight per-line baseline jitter
        jittered = baseline + random.uniform(-1.5, 1.5)

        # First line of a new paragraph: indented
        if paragraph_line_idx == 0 and random.random() < 0.7:
            # Temporarily bump left margin
            global MARGIN_L
            orig_margin = MARGIN_L
            MARGIN_L = orig_margin + random.uniform(28, 42)
            line_paths = line_of_words(jittered)
            MARGIN_L = orig_margin
        else:
            line_paths = line_of_words(jittered)

        all_paths.extend(line_paths)

        # Maybe end paragraph (5-9 lines)
        paragraph_line_idx += 1
        if paragraph_line_idx >= random.randint(4, 8) and random.random() < 0.6:
            skip_next = True

        i += 1

    return all_paths


def render(paths, out_path):
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">',
        f'  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BG}"/>',
        f'  <g fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">',
    ]
    for d, sw in paths:
        svg.append(f'    <path d="{d}" stroke-width="{sw:.2f}"/>')
    svg.append('  </g>')
    svg.append('</svg>')
    with open(out_path, "w") as f:
        f.write("\n".join(svg))


if __name__ == "__main__":
    paths = generate()
    out = "/Users/andreachan/Desktop/stuff/claude-space/code/graphism.svg"
    render(paths, out)
    print(f"Wrote {out} with {len(paths)} word-paths")
