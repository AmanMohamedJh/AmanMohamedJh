from __future__ import annotations

from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = Path("assets") / "night_ops_scorecard.png"
CARD_WIDTH = 520
CARD_HEIGHT = 360
PADDING = 40
GAP = 36
IMG_WIDTH = CARD_WIDTH * 2 + GAP + PADDING * 2
IMG_HEIGHT = CARD_HEIGHT + PADDING * 2
BACKGROUND_TOP = (6, 8, 16)
BACKGROUND_BOTTOM = (14, 20, 40)
CARD_FILL = (11, 17, 32)
CARD_BORDER = (33, 46, 82)
TITLE_COLOR = (138, 195, 255)
TEXT_COLOR = (224, 232, 255)
SUBDUED_COLOR = (147, 164, 209)
PROGRESS_BG = (7, 10, 20)

FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/seguisb.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/calibri.ttf",
]
BOLD_FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/seguisb.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = BOLD_FONT_CANDIDATES if bold else FONT_CANDIDATES
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def lerp_color(top: Tuple[int, int, int], bottom: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    return tuple(int(t + (b - t) * factor) for t, b in zip(top, bottom))


def draw_background(img: Image.Image) -> None:
    draw = ImageDraw.Draw(img)
    for i in range(img.height):
        ratio = i / (img.height - 1)
        color = lerp_color(BACKGROUND_TOP, BACKGROUND_BOTTOM, ratio)
        draw.line([(0, i), (img.width, i)], fill=color)


def draw_rounded_rectangle(draw: ImageDraw.ImageDraw, box, radius: int, *, fill, outline) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def draw_stats_card(base_img: Image.Image, draw: ImageDraw.ImageDraw, top_left: Tuple[int, int], fonts):
    x, y = top_left
    box = (x, y, x + CARD_WIDTH, y + CARD_HEIGHT)
    draw_rounded_rectangle(draw, box, radius=32, fill=CARD_FILL, outline=CARD_BORDER)

    title_font, body_font, badge_font = fonts
    draw.text((x + 28, y + 28), "Aman Mohamed Jh's GitHub Stats", font=title_font, fill=TITLE_COLOR)

    stats = [
        ("⭐", "Total Stars", "0"),
        ("🕒", "Total Commits", "715"),
        ("🔗", "Total PRs", "56"),
        ("❗", "Total Issues", "0"),
        ("📦", "Contributed to", "2"),
    ]

    y_offset = y + 90
    for icon, label, value in stats:
        line = f"{icon}  {label}: {value}"
        draw.text((x + 32, y_offset), line, font=body_font, fill=TEXT_COLOR)
        y_offset += 36

    circle_size = 150
    circle_x = x + CARD_WIDTH - circle_size - 48
    circle_y = y + CARD_HEIGHT - circle_size - 32
    circle_bounds = (circle_x, circle_y, circle_x + circle_size, circle_y + circle_size)
    circle_fill = Image.new("RGBA", (circle_size, circle_size), (0, 0, 0, 0))
    circle_draw = ImageDraw.Draw(circle_fill)
    circle_draw.ellipse((0, 0, circle_size, circle_size), fill=(30, 53, 101, 255))
    circle_draw.ellipse((8, 8, circle_size - 8, circle_size - 8), fill=(21, 36, 68, 255))
    base_img.alpha_composite(circle_fill, (circle_x, circle_y))
    draw.text((circle_x + circle_size / 2, circle_y + circle_size / 2), "A+", font=badge_font, fill=TEXT_COLOR, anchor="mm")


def draw_language_card(draw: ImageDraw.ImageDraw, top_left: Tuple[int, int], fonts):
    x, y = top_left
    box = (x, y, x + CARD_WIDTH, y + CARD_HEIGHT)
    draw_rounded_rectangle(draw, box, radius=32, fill=CARD_FILL, outline=CARD_BORDER)

    title_font, body_font, small_font = fonts
    draw.text((x + 28, y + 28), "Most Used Languages", font=title_font, fill=TITLE_COLOR)

    languages = [
        ("JavaScript", 58.30, (230, 207, 82)),
        ("CSS", 23.26, (93, 61, 180)),
        ("Java", 12.73, (184, 115, 47)),
        ("Kotlin", 5.41, (154, 107, 255)),
        ("EJS", 0.30, (194, 24, 91)),
    ]

    bar_x = x + 32
    bar_y = y + 96
    bar_width = CARD_WIDTH - 64
    bar_height = 20
    draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_width, bar_y + bar_height), radius=12, fill=PROGRESS_BG)

    current_x = bar_x
    for _, percent, color in languages:
        segment_width = max(int(bar_width * (percent / 100)), 1)
        draw.rounded_rectangle(
            (current_x, bar_y, current_x + segment_width, bar_y + bar_height),
            radius=12,
            fill=color,
        )
        current_x += segment_width

    grid_y = bar_y + 40
    for name, percent, color in languages:
        draw.ellipse((bar_x, grid_y, bar_x + 12, grid_y + 12), fill=color)
        text = f"{name} · {percent:.2f}%"
        draw.text((bar_x + 20, grid_y - 2), text, font=small_font, fill=TEXT_COLOR)
        grid_y += 30


def build_scorecard_image() -> Image.Image:
    base = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0, 0))
    draw_background(base)
    draw = ImageDraw.Draw(base)

    title_font = load_font(26, bold=True)
    body_font = load_font(20)
    badge_font = load_font(48, bold=True)
    small_font = load_font(18)

    draw_stats_card(base, draw, (PADDING, PADDING), (title_font, body_font, badge_font))
    draw_language_card(draw, (PADDING + CARD_WIDTH + GAP, PADDING), (title_font, body_font, small_font))

    header_font = load_font(32, bold=True)
    draw.text((IMG_WIDTH / 2, 28), "Night Ops Scorecard", font=header_font, fill=TITLE_COLOR, anchor="mm")

    return base


def save_scorecard() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    image = build_scorecard_image()
    image.save(OUTPUT_PATH)
    print(f"Saved Night Ops scorecard to {OUTPUT_PATH}")


if __name__ == "__main__":
    save_scorecard()
