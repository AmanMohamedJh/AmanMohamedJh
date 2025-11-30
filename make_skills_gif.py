import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path

ICONS = [
    ("JavaScript", "https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png"),
    ("TypeScript", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Typescript_logo_2020.svg/512px-Typescript_logo_2020.svg.png"),
    ("Go", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Go_Logo_Blue.svg/512px-Go_Logo_Blue.svg.png"),
    ("Python", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/512px-Python-logo-notext.svg.png"),
    ("Kotlin", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Kotlin_Icon.png/512px-Kotlin_Icon.png"),
    ("Java", "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Java_programming_language_logo.svg/512px-Java_programming_language_logo.svg.png"),
]

WIDTH, HEIGHT = 720, 200
STEPS_PER_ICON = 6
BACKGROUND = (8, 12, 24, 255)
BORDER_COLOR = (35, 50, 90, 255)
ACTIVE_TEXT = (190, 210, 255)
IDLE_TEXT = (120, 140, 180)


def load_icons():
    loaded = []
    for name, url in ICONS:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGBA")
        loaded.append((name, img))
    return loaded


def build_frames(icons):
    frames = []
    font = ImageFont.load_default()
    for step in range(len(icons) * STEPS_PER_ICON):
        active = step // STEPS_PER_ICON
        frame = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND)
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle((10, 10, WIDTH - 10, HEIGHT - 10), radius=28, outline=BORDER_COLOR, width=2)
        for idx, (name, icon) in enumerate(icons):
            size = 96 if idx == active else 72
            resized = ImageOps.contain(icon, (size, size))
            x = 40 + idx * 105
            y = 40 if idx == active else 58
            frame.paste(resized, (x, y), resized)
            text = ACTIVE_TEXT if idx == active else IDLE_TEXT
            text_w, text_h = draw.textsize(name, font=font)
            draw.text((x + (size - text_w) / 2, HEIGHT - 40), name, fill=text, font=font)
        frames.append(frame)
    return frames


def save_gif(frames, path):
    palette_frames = [frame.convert("P", palette=Image.ADAPTIVE) for frame in frames]
    palette_frames[0].save(
        path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=160,
        loop=0,
        disposal=2,
    )


def main():
    icons = load_icons()
    frames = build_frames(icons)
    output = Path("skills-loadout.gif")
    save_gif(frames, output)
    print(f"Saved {output.resolve()}")


if __name__ == "__main__":
    main()
