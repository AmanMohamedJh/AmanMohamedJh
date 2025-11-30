from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 800, 170
BG_TOP = (5, 9, 18)
BG_BOTTOM = (8, 15, 32)
LANGUAGES = [
    ("JavaScript", "#f7df1e"),
    ("TypeScript", "#3178c6"),
    ("Go", "#00add8"),
    ("Python", "#3776ab"),
    ("Kotlin", "#7f52ff"),
    ("Java", "#f89820"),
]
OUTPUT = Path(__file__).with_name("skills_loadout.gif")

try:
    FONT = ImageFont.truetype("C:/Windows/Fonts/SEGOEUIB.TTF", 30)
except OSError:
    FONT = ImageFont.load_default()

FRAMES = []
PILL_HEIGHT = 52
PILL_GAP = 16
PILL_WIDTH = (WIDTH - (len(LANGUAGES) + 1) * PILL_GAP) // len(LANGUAGES)

for active_index in range(len(LANGUAGES)):
    frame = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(frame)
    # gradient background
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    x = PILL_GAP
    for idx, (label, color) in enumerate(LANGUAGES):
        pill_box = [x, (HEIGHT - PILL_HEIGHT) // 2, x + PILL_WIDTH, (HEIGHT + PILL_HEIGHT) // 2]
        if idx == active_index:
            draw.rounded_rectangle(pill_box, radius=26, fill=color)
        else:
            off_color = tuple(int(int(color.lstrip('#')[i:i+2], 16) * 0.4) for i in (0, 2, 4))
            draw.rounded_rectangle(pill_box, radius=26, fill=off_color)
        text = label
        bbox = draw.textbbox((0, 0), text, font=FONT)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = x + (PILL_WIDTH - text_w) / 2
        text_y = (HEIGHT - text_h) / 2
        text_color = (10, 12, 20) if idx == active_index else (220, 230, 255)
        draw.text((text_x, text_y), text, font=FONT, fill=text_color)
        x += PILL_WIDTH + PILL_GAP

    FRAMES.append(frame)

FRAMES[0].save(OUTPUT, save_all=True, append_images=FRAMES[1:], duration=400, loop=0, disposal=2)
print(f"Animated skills strip written to {OUTPUT}")
