#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news summary image (1024x1024 PNG).

Six story panels plus a footer strip, drawn with PIL only. All text is
hand-set with DejaVu so it stays legible at ~300 px wide. Run:
    python3 make_image.py   ->  writes entry.png beside this file.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (14, 30, 61)          # deep navy
GOLD = (245, 197, 66)
WHITE = (255, 255, 255)
CARD = (247, 249, 252)
INK = (18, 28, 48)
SUBINK = (64, 78, 102)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(d, text, path, size, max_width):
    """Largest font at or below `size` whose rendered width fits max_width."""
    while size > 18:
        fnt = font(path, size)
        box = d.textbbox((0, 0), text, font=fnt)
        if box[2] - box[0] <= max_width:
            return fnt
        size -= 2
    return font(path, size)


def center_text(d, cx, y, text, fnt, fill):
    box = d.textbbox((0, 0), text, font=fnt)
    tw = box[2] - box[0]
    d.text((cx - tw / 2 - box[0], y), text, font=fnt, fill=fill)
    return box[3] - box[1]


def draw_rocket(d, cx, cy, s, color):
    """Simple rocket: body, window, fins, flame, two stars."""
    d.rounded_rectangle([cx - 0.22 * s, cy - 0.55 * s, cx + 0.22 * s, cy + 0.25 * s],
                        radius=0.20 * s, fill=color)
    d.ellipse([cx - 0.11 * s, cy - 0.38 * s, cx + 0.11 * s, cy - 0.16 * s], fill=WHITE)
    d.polygon([(cx - 0.22 * s, cy + 0.02 * s), (cx - 0.42 * s, cy + 0.38 * s),
               (cx - 0.20 * s, cy + 0.30 * s)], fill=color)
    d.polygon([(cx + 0.22 * s, cy + 0.02 * s), (cx + 0.42 * s, cy + 0.38 * s),
               (cx + 0.20 * s, cy + 0.30 * s)], fill=color)
    d.polygon([(cx - 0.13 * s, cy + 0.27 * s), (cx + 0.13 * s, cy + 0.27 * s),
               (cx, cy + 0.58 * s)], fill=GOLD)
    for sx, sy in ((cx - 0.55 * s, cy - 0.45 * s), (cx + 0.52 * s, cy - 0.30 * s)):
        d.line([(sx - 0.09 * s, sy), (sx + 0.09 * s, sy)], fill=color, width=4)
        d.line([(sx, sy - 0.09 * s), (sx, sy + 0.09 * s)], fill=color, width=4)


def draw_bars(d, cx, cy, s, color):
    """Ascending bar chart with an arrow."""
    base = cy + 0.42 * s
    heights = [0.30, 0.48, 0.68, 0.92]
    bw = 0.20 * s
    for i, h in enumerate(heights):
        x0 = cx - 0.52 * s + i * 0.28 * s
        d.rectangle([x0, base - h * s, x0 + bw, base], fill=color)
    d.line([(cx - 0.58 * s, cy - 0.05 * s), (cx + 0.55 * s, cy - 0.55 * s)],
           fill=GOLD, width=7)
    d.polygon([(cx + 0.55 * s, cy - 0.55 * s), (cx + 0.30 * s, cy - 0.52 * s),
               (cx + 0.50 * s, cy - 0.30 * s)], fill=GOLD)


def draw_ship(d, cx, cy, s, color):
    """Container ship: hull, stacked boxes, waves."""
    hull_y = cy + 0.18 * s
    d.polygon([(cx - 0.55 * s, hull_y), (cx + 0.55 * s, hull_y),
               (cx + 0.40 * s, hull_y + 0.28 * s), (cx - 0.40 * s, hull_y + 0.28 * s)],
              fill=color)
    boxes = [(-0.48, 0.16), (-0.24, 0.16), (0.0, 0.16), (0.24, 0.16),
             (-0.36, 0.0), (-0.12, 0.0), (0.12, 0.0)]
    for bx, by in boxes:
        x0 = cx + bx * s
        y1 = hull_y - by * s
        d.rectangle([x0, y1 - 0.15 * s, x0 + 0.21 * s, y1 - 0.015 * s], fill=color)
    for k in range(2):
        wy = hull_y + 0.38 * s + k * 0.11 * s
        d.arc([cx - 0.55 * s, wy - 0.07 * s, cx - 0.18 * s, wy + 0.07 * s],
              180, 360, fill=color, width=4)
        d.arc([cx - 0.18 * s, wy - 0.07 * s, cx + 0.19 * s, wy + 0.07 * s],
              180, 360, fill=color, width=4)
        d.arc([cx + 0.19 * s, wy - 0.07 * s, cx + 0.56 * s, wy + 0.07 * s],
              180, 360, fill=color, width=4)


def draw_court(d, cx, cy, s, color):
    """Courthouse: pediment, columns, steps."""
    top = cy - 0.45 * s
    d.polygon([(cx - 0.55 * s, top + 0.22 * s), (cx + 0.55 * s, top + 0.22 * s),
               (cx, top - 0.08 * s)], fill=color)
    d.rectangle([cx - 0.55 * s, top + 0.26 * s, cx + 0.55 * s, top + 0.36 * s], fill=color)
    for i in range(4):
        x0 = cx - 0.46 * s + i * 0.26 * s
        d.rectangle([x0, top + 0.42 * s, x0 + 0.13 * s, top + 0.82 * s], fill=color)
    d.rectangle([cx - 0.58 * s, top + 0.86 * s, cx + 0.58 * s, top + 0.96 * s], fill=color)


def draw_tower(d, cx, cy, s, color):
    """Skyscraper with windows and a burst mark."""
    x0, x1 = cx - 0.26 * s, cx + 0.26 * s
    y0, y1 = cy - 0.52 * s, cy + 0.50 * s
    d.rectangle([x0, y0, x1, y1], fill=color)
    d.rectangle([cx - 0.05 * s, y0 - 0.16 * s, cx + 0.05 * s, y0], fill=color)
    for r in range(4):
        for c in range(2):
            wx = x0 + 0.08 * s + c * 0.24 * s
            wy = y0 + 0.10 * s + r * 0.24 * s
            d.rectangle([wx, wy, wx + 0.12 * s, wy + 0.14 * s], fill=WHITE)
    bx, by = cx + 0.48 * s, cy - 0.38 * s
    for ang in range(0, 360, 45):
        import math
        rad = math.radians(ang)
        d.line([(bx + 0.10 * s * math.cos(rad), by + 0.10 * s * math.sin(rad)),
                (bx + 0.22 * s * math.cos(rad), by + 0.22 * s * math.sin(rad))],
               fill=(214, 48, 49), width=5)
    d.ellipse([bx - 0.07 * s, by - 0.07 * s, bx + 0.07 * s, by + 0.07 * s],
              fill=(214, 48, 49))


def draw_ball(d, cx, cy, s, color):
    """Soccer ball: circle with dark patches."""
    r = 0.46 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=6, fill=WHITE)
    import math
    # centre patch
    pts = []
    for k in range(5):
        a = math.radians(-90 + k * 72)
        pts.append((cx + 0.16 * s * math.cos(a), cy + 0.16 * s * math.sin(a)))
    d.polygon(pts, fill=color)
    for k in range(5):
        a = math.radians(-90 + k * 72)
        px, py = cx + 0.34 * s * math.cos(a), cy + 0.34 * s * math.sin(a)
        d.ellipse([px - 0.075 * s, py - 0.075 * s, px + 0.075 * s, py + 0.075 * s],
                  fill=color)
        d.line([(cx + 0.16 * s * math.cos(a), cy + 0.16 * s * math.sin(a)), (px, py)],
               fill=color, width=4)


PANELS = [
    # (category, accent, icon, headline lines, detail lines)
    ("S P A C E", (0, 119, 182), draw_rocket,
     ["SHENZHOU-24"],
     ["Pakistan's first astronaut", "reaches Tiangong station"]),
    ("E C O N O M Y", (0, 150, 90), draw_bars,
     ["US GROWTH", "+4.3%"],
     ["Q3 GDP revised up", "Core inflation 3.3%", "Jobless claims 189K"]),
    ("T R A D E", (230, 126, 34), draw_ship,
     ["NEW US", "TARIFFS"],
     ["14 partners targeted", "over overcapacity"]),
    ("T E C H", (108, 92, 231), draw_court,
     ["HUAWEI", "GUILTY"],
     ["10 of 12 fraud &", "sanctions counts, NY"]),
    ("M I D E A S T", (214, 48, 49), draw_tower,
     ["RIYADH", "STRUCK"],
     ["Houthi strike hits tower", "11 wounded"]),
    ("S P O R T", (0, 140, 120), draw_ball,
     ["LILLE 2-1", "BAYERN"],
     ["Champions League upset", "ends unbeaten run"]),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- header -----------------------------------------------------------
    center_text(d, W // 2, 22, "W E D N E S D A Y", font(BOLD, 29), GOLD)
    center_text(d, W // 2, 56, "25 NOVEMBER 2026", font(BOLD, 84), WHITE)
    center_text(d, W // 2, 156, "WORLD NEWS IN ONE IMAGE", font(BOLD, 33),
                (180, 200, 235))
    d.rectangle([48, 202, W - 48, 207], fill=GOLD)

    # --- story grid: 3 cols x 2 rows --------------------------------------
    margin, gap = 36, 18
    grid_top = 222
    grid_bottom = 888
    cols, rows = 3, 2
    pw = (W - 2 * margin - (cols - 1) * gap) // cols
    ph = (grid_bottom - grid_top - (rows - 1) * gap) // rows

    f_cat = font(BOLD, 21)
    f_det = font(REG, 24)

    for i, (cat, accent, icon, head_lines, det_lines) in enumerate(PANELS):
        col, row = i % cols, i // cols
        x0 = margin + col * (pw + gap)
        y0 = grid_top + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=CARD)
        # accent strip on top of the card
        d.rounded_rectangle([x0, y0, x1, y0 + 14], radius=7, fill=accent)
        d.rectangle([x0, y0 + 8, x1, y0 + 14], fill=accent)

        cx = (x0 + x1) // 2
        center_text(d, cx, y0 + 24, cat, f_cat, accent)
        icon(d, cx, y0 + 98, 80, accent)

        hy = y0 + 158
        for line in head_lines:
            f_head = fit_font(d, line, BOLD, 40, pw - 28)
            center_text(d, cx, hy, line, f_head, INK)
            hy += 42
        dy = hy + 2
        for line in det_lines:
            f_line = fit_font(d, line, REG, 24, pw - 24)
            center_text(d, cx, dy, line, f_line, SUBINK)
            dy += 27

    # --- footer strip ------------------------------------------------------
    d.rectangle([48, 900, W - 48, 904], fill=GOLD)
    center_text(d, W // 2, 912, "ALSO TODAY", font(BOLD, 23), GOLD)
    center_text(d, W // 2, 940,
                "Ebola emergency in DR Congo: 11,700 cases",
                font(REG, 25), WHITE)
    center_text(d, W // 2, 970,
                "Cairo tanker fire kills 30  ·  Spain votes Sunday",
                font(REG, 25), WHITE)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
