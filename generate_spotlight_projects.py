from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = Path("assets") / "spotlight_projects.png"
CANVAS_WIDTH = 1100
CANVAS_HEIGHT = 820
BACKGROUND_TOP = (4, 6, 16)
BACKGROUND_BOTTOM = (14, 18, 34)
CARD_FILL = (10, 17, 35)
CARD_BORDER = (28, 43, 80)
CARD_WIDTH = 460
CARD_HEIGHT = 180
CARD_RADIUS = 32
GRID_COLUMNS = 2
GRID_ROWS = 2
GRID_GAP_X = 40
GRID_GAP_Y = 36
PADDING_X = 70
PADDING_Y = 110
TITLE_COLOR = (197, 213, 255)
ACCENT_COLOR = (140, 195, 255)
TEXT_COLOR = (223, 231, 255)
SUBTEXT_COLOR = (147, 164, 209)
SHADOW_COLOR = (0, 0, 0, 60)

FONT_PATHS = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/calibri.ttf",
]
BOLD_FONT_PATHS = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

PROJECTS = [
    {
        "title": "INQ Admin Suite",
        "stack": "Node.js · NestJS · MongoDB · MFA",
        "description": "Hierarchical RBAC, MFA-enforced Super Admin flows, permission versioning, and audit-ready logging.",
    },
    {
        "title": "Portfolio v2",
        "stack": "Next.js 15 · TypeScript · Tailwind · shadcn/ui",
        "description": "Motion-driven UI, typed content models, serverless email, Vercel deployments, and evolving blog/experiments.",
    },
    {
        "title": "GymHub Platform",
        "stack": "MERN · Stripe · JWT",
        "description": "Multi-tenant gym management, trainer hiring, subscription billing, and real-time analytics dashboards.",
    },
    {
        "title": "WalletWhiz",
        "stack": "Kotlin · Android SDK · Jetpack",
        "description": "Expense tracking, goal-based budgeting, MPAndroidChart insights, coroutine persistence, and smooth onboarding.",
    },
]


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = BOLD_FONT_PATHS if bold else FONT_PATHS
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def lerp_color(top: Tuple[int, int, int], bottom: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    return tuple(int(t + (b - t) * factor) for t, b in zip(top, bottom))


def draw_background(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    for y in range(canvas.height):
        ratio = y / max(canvas.height - 1, 1)
        color = lerp_color(BACKGROUND_TOP, BACKGROUND_BOTTOM, ratio)
        draw.line([(0, y), (canvas.width, y)], fill=color)


def draw_card(draw: ImageDraw.ImageDraw, *, top_left: Tuple[int, int], title: str, stack: str, description: str, fonts):
    x, y = top_left
    shadow_box = (x + 6, y + 10, x + CARD_WIDTH + 6, y + CARD_HEIGHT + 10)
    draw.rounded_rectangle(shadow_box, radius=CARD_RADIUS, fill=SHADOW_COLOR)

    card_box = (x, y, x + CARD_WIDTH, y + CARD_HEIGHT)
    draw.rounded_rectangle(card_box, radius=CARD_RADIUS, fill=CARD_FILL, outline=CARD_BORDER, width=2)

    title_font, text_font = fonts
    draw.text((x + 28, y + 28), title, font=title_font, fill=TITLE_COLOR)
    draw.text((x + 28, y + 70), stack, font=text_font, fill=ACCENT_COLOR)

    description_width = CARD_WIDTH - 56
    wrapped = wrap_text(description, description_width, text_font)
    text_y = y + 108
    for line in wrapped:
        draw.text((x + 28, text_y), line, font=text_font, fill=TEXT_COLOR)
        text_y += text_font.size + 6


def wrap_text(text: str, max_width: int, font: ImageFont.ImageFont) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current = ""
    for word in words:
        test_line = f"{current} {word}".strip()
        width = font.getlength(test_line)
        if width <= max_width:
            current = test_line
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def build_image() -> Image.Image:
    canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    draw_background(canvas)
    draw = ImageDraw.Draw(canvas)

    header_font = load_font(42, bold=True)
    sub_font = load_font(20)
    card_title_font = load_font(26, bold=True)
    body_font = load_font(20)

    draw.text((PADDING_X, 40), "Spotlight Projects", font=header_font, fill=TITLE_COLOR)

    for idx, project in enumerate(PROJECTS):
        row = idx // GRID_COLUMNS
        col = idx % GRID_COLUMNS
        x = PADDING_X + col * (CARD_WIDTH + GRID_GAP_X)
        y = PADDING_Y + row * (CARD_HEIGHT + GRID_GAP_Y)
        draw_card(
            draw,
            top_left=(x, y),
            title=project["title"],
            stack=project["stack"],
            description=project["description"],
            fonts=(card_title_font, body_font),
        )

    return canvas


def save_image() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    image = build_image()
    image.save(OUTPUT_PATH)
    print(f"Saved Spotlight Projects card to {OUTPUT_PATH}")


if __name__ == "__main__":
    save_image()
