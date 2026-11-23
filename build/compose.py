#!/usr/bin/env python3
"""Composite the GTA 6 meme: scene + make.fun ghost on the couch + captions."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK = "/home/hatch/workspace/makefun/gta6-meme-x-01"
SCENE = f"{WORK}/media-generation-scene-0-9dd5d06a-4c27-423d-8151-2f8de24a103a.webp"
GHOST = f"{WORK}/ref-ghost.png"
OUT = f"{WORK}/meme.png"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MAGENTA = (214, 51, 132)  # close to make.fun brand magenta

base = Image.open(SCENE).convert("RGB")
W, H = base.size  # 2048 x 1152
print("canvas", W, H)

def fit_font(text, max_w, start_size):
    size = start_size
    while size > 20:
        f = ImageFont.truetype(FONT_BOLD, size)
        bbox = ImageDraw.Draw(Image.new("RGB", (10, 10))).textbbox((0, 0), text, font=f)
        if bbox[2] - bbox[0] <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(FONT_BOLD, 20)

def outlined(draw, xy, text, font, fill, stroke_fill, stroke_w):
    draw.text(xy, text, font=font, fill=fill, stroke_width=stroke_w,
              stroke_fill=stroke_fill, anchor="ma")

# --- 1. ghost on the middle couch cushion (with soft drop shadow) ---
ghost = Image.open(GHOST).convert("RGBA")
GD = 440  # ghost diameter
ghost = ghost.resize((GD, GD), Image.LANCZOS)
gx = (W - GD) // 2          # centered horizontally
gy = 835 - GD // 2          # center y ~835, sits on the seat
# shadow: dark ellipse just under the ghost, blurred
shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow_layer)
sd.ellipse([gx + 20, gy + GD - 55, gx + GD - 20, gy + GD + 5], fill=(0, 0, 0, 150))
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(18))
base = Image.alpha_composite(base.convert("RGBA"), shadow_layer)
base.paste(ghost, (gx, gy), ghost)

draw = ImageDraw.Draw(base)

# --- 2. top caption ---
top = "WAITED 13 YEARS FOR GTA 6"
f_top = fit_font(top, 1900, 100)
outlined(draw, (W // 2, 30), top, f_top, (255, 255, 255), (0, 0, 0), 7)

# --- 3. bottom caption ---
bot = "CALLED IN SICK. WORTH IT."
f_bot = fit_font(bot, 1500, 64)
outlined(draw, (W // 2, H - 92), bot, f_bot, (255, 255, 255), (0, 0, 0), 5)

# --- 4. make.fun wordmark, bottom-right, magenta ---
f_brand = ImageFont.truetype(FONT_BOLD, 46)
brand = "make.fun"
bbox = draw.textbbox((0, 0), brand, font=f_brand)
bw = bbox[2] - bbox[0]
draw.text((W - 28 - bw, H - 78), brand, font=f_brand, fill=MAGENTA,
          stroke_width=2, stroke_fill=(0, 0, 0))

base.convert("RGB").save(OUT, "PNG")
print("saved", OUT)
im = Image.open(OUT)
print("final:", im.size, im.mode)
