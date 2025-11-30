from pathlib import Path
from math import sin, pi
from random import Random
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

def _load_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


WIDTH, HEIGHT = 460, 150
FRAMES = 24

FONT_SMALL = _load_font("C:/Windows/Fonts/SEGOEUI.TTF", 17)
FONT_LARGE = _load_font("C:/Windows/Fonts/SEGOEUIB.TTF", 26)
FONT_EMOJI = _load_font("C:/Windows/Fonts/seguiemj.ttf", 32)
FONT_MONO = _load_font("C:/Windows/Fonts/consola.ttf", 15)


def _blend(c1, c2, factor):
    return tuple(int(c1[i] * factor + c2[i] * (1 - factor)) for i in range(3))

root = Path(__file__).parent
assets_dir = root / "assets" / "connect"
assets_dir.mkdir(parents=True, exist_ok=True)
rng = Random(42)

for conf in OUTPUTS:
    frames = []
    for idx in range(FRAMES):
        frame = Image.new("RGBA", (WIDTH, HEIGHT), (5, 8, 16, 255))
        draw = ImageDraw.Draw(frame)
        # soft gradient background with gentle shimmer
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            base = _blend(conf["colors"][0], conf["colors"][1], ratio)
            draw.line([(0, y), (WIDTH, y)], fill=(*base, 255))

        beam_phase = (idx / FRAMES) * WIDTH
        beam_width = 90
        draw.rectangle((beam_phase - beam_width, 0, beam_phase, HEIGHT), fill=(255, 255, 255, 30))

        draw.rounded_rectangle((6, 6, WIDTH - 6, HEIGHT - 6), radius=26, outline=(255, 255, 255, 80), width=2)

        badge_box = (24, 38, 24 + 68, 38 + 68)
        draw.rounded_rectangle(badge_box, radius=20, fill=(0, 0, 0, 110))
        draw.text((badge_box[0] + 12, badge_box[1] + 6), conf["emoji"], font=FONT_EMOJI, fill=(255, 255, 255, 230))

        label_x = badge_box[2] + 18
        draw.text((label_x, 40), conf["label"].upper(), font=FONT_SMALL, fill=(230, 235, 250))
        wrapped = textwrap.wrap(conf["value"], width=26)
        for wrap_idx, line in enumerate(wrapped[:2]):
            draw.text((label_x, 72 + wrap_idx * 30), line, font=FONT_LARGE, fill=(255, 255, 255))

        draw.text((label_x, HEIGHT - 32), "Response within a day", font=FONT_MONO, fill=(230, 235, 245))

        frames.append(frame)
    out_path = assets_dir / f"connect_{conf['key']}.gif"
    frames[0].save(out_path, save_all=True, append_images=frames[1:], loop=0, duration=80, disposal=2)
    print(f"Wrote {out_path}")
