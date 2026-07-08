import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

COLOR_BG = (17, 17, 17)       # preto quase puro, sólido
COLOR_TEXT = (196, 30, 40)    # vermelho — cor da frase
COLOR_ACCENT = (196, 30, 40)
COLOR_MUTED = (140, 140, 140)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def build_gradient():
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    return img, draw


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_font(draw, text, max_width, max_height, font_path, start_size=90, min_size=44):
    size = start_size
    while size >= min_size:
        font = ImageFont.truetype(font_path, size)
        lines = wrap_text(draw, text, font, max_width)
        line_height = draw.textbbox((0, 0), "Ay", font=font)[3] + 18
        total_height = line_height * len(lines)
        if total_height <= max_height:
            return font, lines, line_height
        size -= 4
    font = ImageFont.truetype(font_path, min_size)
    lines = wrap_text(draw, text, font, max_width)
    line_height = draw.textbbox((0, 0), "Ay", font=font)[3] + 18
    return font, lines, line_height


def generate(quote_text, source_text, output_path):
    img, draw = build_gradient()

    # frase principal, centralizada vertical e horizontalmente, em vermelho
    max_width = W - 160
    max_height = 1400
    font, lines, line_height = fit_font(draw, quote_text, max_width, max_height, FONT_BOLD)
    total_height = line_height * len(lines)
    y = (H - total_height) / 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (W - (bbox[2] - bbox[0])) / 2
        draw.text((x, y), line, font=font, fill=COLOR_TEXT)
        y += line_height

    # assinatura discreta
    source_font = ImageFont.truetype(FONT_REGULAR, 32)
    source_line = f"@protocolo.forja  ·  {source_text}"
    bbox = draw.textbbox((0, 0), source_line, font=source_font)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, H - 160), source_line, font=source_font, fill=COLOR_MUTED)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")


if __name__ == "__main__":
    generate(
        "As coisas que você possui acabam possuindo você.",
        "Fight Club (1999)",
        "docs/frase.png",
    )
