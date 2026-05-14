"""
Generate a complete PWA icon set for the Badminton Ladder System.
Draws a shuttlecock on a green (Performance brand color) tile.
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math

OUT = os.path.join(os.path.dirname(__file__), "icons")
os.makedirs(OUT, exist_ok=True)

BG_COLOR_DARK  = (15, 110,  86)   # --perf-dark
BG_COLOR_LIGHT = ( 29, 158, 117)  # --perf
WHITE          = (255, 255, 255)
SHADOW         = (0, 0, 0, 50)
INK            = (15, 50, 40)

def draw_icon(size, maskable=False):
    """Render a shuttlecock icon at the given size.
    If maskable=True, the artwork is shrunk so all of it sits inside the
    80% "safe zone" required by Android maskable icons."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background — vertical gradient
    for y in range(size):
        t = y / size
        r = int(BG_COLOR_DARK[0] + (BG_COLOR_LIGHT[0] - BG_COLOR_DARK[0]) * t)
        g = int(BG_COLOR_DARK[1] + (BG_COLOR_LIGHT[1] - BG_COLOR_DARK[1]) * t)
        b = int(BG_COLOR_DARK[2] + (BG_COLOR_LIGHT[2] - BG_COLOR_DARK[2]) * t)
        d.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Rounded corners for app-icon look (non-maskable only)
    if not maskable:
        radius = int(size * 0.22)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, size, size], radius=radius, fill=255
        )
        img.putalpha(mask)

    # Shuttlecock artwork
    overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Safe-zone scaling for maskable icons
    scale = 0.80 if maskable else 1.0
    cx = size / 2
    # Shift down so the cork is centered visually
    cy_cork = size * (0.66 if not maskable else 0.62)

    # --- Feathers (skirt) ---
    # An expanding cone of overlapping triangles
    feather_count = 9
    feather_top_y = size * 0.18 * scale + (1 - scale) * size / 2
    feather_top_half_w = size * 0.32 * scale
    cork_y = cy_cork
    cork_half_w = size * 0.10 * scale

    feather_color = (255, 255, 255, 235)
    feather_edge  = (220, 230, 225, 255)

    # Soft drop-shadow under the feather cone
    shadow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    sd.polygon(
        [
            (cx - feather_top_half_w + size*0.02, feather_top_y + size*0.04),
            (cx + feather_top_half_w + size*0.02, feather_top_y + size*0.04),
            (cx + cork_half_w + size*0.02, cork_y + size*0.04),
            (cx - cork_half_w + size*0.02, cork_y + size*0.04),
        ],
        fill=(0, 0, 0, 60),
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(size * 0.02))
    overlay = Image.alpha_composite(overlay, shadow_layer)
    od = ImageDraw.Draw(overlay)

    # Individual feathers
    for i in range(feather_count):
        t0 = i / feather_count
        t1 = (i + 1) / feather_count
        x_top_0 = cx - feather_top_half_w + 2 * feather_top_half_w * t0
        x_top_1 = cx - feather_top_half_w + 2 * feather_top_half_w * t1
        x_bot_0 = cx - cork_half_w + 2 * cork_half_w * t0
        x_bot_1 = cx - cork_half_w + 2 * cork_half_w * t1
        # Each feather as a thin trapezoid
        od.polygon(
            [
                (x_top_0, feather_top_y),
                (x_top_1, feather_top_y),
                (x_bot_1, cork_y),
                (x_bot_0, cork_y),
            ],
            fill=feather_color,
            outline=feather_edge,
        )

    # Cross-hatch lacing
    lace_count = 3
    for i in range(1, lace_count + 1):
        t = i / (lace_count + 1)
        y = feather_top_y + (cork_y - feather_top_y) * t
        half_w = feather_top_half_w + (cork_half_w - feather_top_half_w) * t
        od.line(
            [(cx - half_w, y), (cx + half_w, y)],
            fill=(180, 195, 188, 200),
            width=max(1, int(size * 0.006)),
        )

    # --- Cork (the round base) ---
    cork_r = size * 0.13 * scale
    # Cork drop shadow
    cs = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    csd = ImageDraw.Draw(cs)
    csd.ellipse(
        [cx - cork_r + size*0.015, cork_y - cork_r + size*0.025,
         cx + cork_r + size*0.015, cork_y + cork_r + size*0.025],
        fill=(0, 0, 0, 70),
    )
    cs = cs.filter(ImageFilter.GaussianBlur(size * 0.015))
    overlay = Image.alpha_composite(overlay, cs)
    od = ImageDraw.Draw(overlay)

    # Cork body
    od.ellipse(
        [cx - cork_r, cork_y - cork_r, cx + cork_r, cork_y + cork_r],
        fill=(255, 255, 255, 255),
    )
    # Cork inner shading
    inner_r = cork_r * 0.78
    od.ellipse(
        [cx - inner_r, cork_y - inner_r * 0.6, cx + inner_r, cork_y + inner_r * 1.2],
        fill=(245, 230, 210, 255),
    )
    # Tiny highlight
    hi_r = cork_r * 0.30
    od.ellipse(
        [cx - cork_r * 0.4, cork_y - cork_r * 0.55,
         cx - cork_r * 0.4 + hi_r * 2, cork_y - cork_r * 0.55 + hi_r * 2],
        fill=(255, 255, 255, 200),
    )

    return Image.alpha_composite(img, overlay)


# Generate all required sizes
specs = [
    ("icon-192.png",          192, False),
    ("icon-512.png",          512, False),
    ("icon-maskable-192.png", 192, True),
    ("icon-maskable-512.png", 512, True),
    ("apple-touch-icon.png",  180, False),
    ("favicon-32.png",         32, False),
    ("favicon-16.png",         16, False),
]

for name, size, maskable in specs:
    icon = draw_icon(size, maskable=maskable)
    icon.save(os.path.join(OUT, name), "PNG", optimize=True)
    print(f"  wrote {name} ({size}x{size}{', maskable' if maskable else ''})")

print("Done.")
