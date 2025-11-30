from pathlib import Path
from math import sin, pi
from PIL import Image, ImageDraw, ImageFont
import textwrap

OUTPUTS = [
    {
        "key": "email",
        "label": "Email",
        "value": "amanmohamed5500@gmail.com",
        "emoji": "✉️",
        "colors": ((16, 64, 200), (4, 12, 32)),
    },
    {
        "key": "phone",
        "label": "Phone",
        "value": "+94 76 405 0889",
        "emoji": "📞",
        "colors": ((160, 20, 60), (25, 4, 20)),
    },
    {
        "key": "location",
        "label": "Location",
        "value": "Trend Horizon Residencies, 24 Bhathiya Mawatha, Colombo",
        "emoji": "📍",
        "colors": ((10, 120, 90), (3, 18, 20)),
    },
    {
        "key": "linkedin",
        "label": "LinkedIn",
        "value": "linkedin.com/in/aman-mohamed-076644305",
        "emoji": "🤝",
        "colors": ((28, 72, 200), (4, 10, 24)),
    },
    {
        "key": "portfolio",
        "label": "Portfolio",
        "value": "amanmohamedjhportfolio.vercel.app",
        "emoji": "🚀",
        "colors": ((165, 120, 40), (24, 12, 4)),
    },
]

WIDTH, HEIGHT = 460, 150
FRAMES = 24
def _load_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


FONT_SMALL = _load_font("C:/Windows/Fonts/SEGOEUI.TTF", 18)
FONT_LARGE = _load_font("C:/Windows/Fonts/SEGOEUIB.TTF", 26)
FONT_EMOJI = _load_font("C:/Windows/Fonts/seguiemj.ttf", 32)

root = Path(__file__).parent

for conf in OUTPUTS:
    frames = []
    for idx in range(FRAMES):
        frame = Image.new("RGBA", (WIDTH, HEIGHT), (5, 8, 16, 255))
        draw = ImageDraw.Draw(frame)
        # animated gradient sweep
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            wave = 0.5 + 0.5 * sin(2 * pi * (idx / FRAMES) + ratio * pi)
            r = int(conf["colors"][0][0] * wave + conf["colors"][1][0] * (1 - wave))
            g = int(conf["colors"][0][1] * wave + conf["colors"][1][1] * (1 - wave))
            b = int(conf["colors"][0][2] * wave + conf["colors"][1][2] * (1 - wave))
            draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))
        # rounded border
        draw.rounded_rectangle((2, 2, WIDTH - 2, HEIGHT - 2), radius=28, outline=(255, 255, 255, 40), width=2)
        # emoji badge
        badge_box = (20, 35, 20 + 64, 35 + 64)
        draw.rounded_rectangle(badge_box, radius=18, fill=(0, 0, 0, 90))
        draw.text((badge_box[0] + 16, badge_box[1] + 8), conf["emoji"], font=FONT_EMOJI, fill=(255, 255, 255, 220))
        # text
        draw.text((110, 40), conf["label"].upper(), font=FONT_SMALL, fill=(210, 220, 255))
        wrapped = textwrap.wrap(conf["value"], width=28)
        for wrap_idx, line in enumerate(wrapped[:3]):
            y_pos = 76 + wrap_idx * 30
            draw.text((110, y_pos), line, font=FONT_LARGE, fill=(255, 255, 255))
        frames.append(frame)
    out_path = root / f"connect_{conf['key']}.gif"
    frames[0].save(out_path, save_all=True, append_images=frames[1:], loop=0, duration=80, disposal=2)
    print(f"Wrote {out_path}")
