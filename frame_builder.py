from PIL import Image, ImageDraw

import effects
from config import (
    BG,
    BORDER,
    CURSOR_COL,
    HEIGHT,
    TERM_W,
    WHITE,
    WIDTH,
    font,
    line_h,
    margin,
)
from draw_utils import draw_stats_panel, draw_title_bar


def build_frame(
    lines, repos_done, total_repos, lang_tally, cursor=True, highlight_last=True
):
    """Create a PIL Image of the terminal with the given lines and stats."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw_title_bar(draw)

    # Stats panel
    draw_stats_panel(draw, repos_done, total_repos, lang_tally)

    # Terminal body (left side)
    top = 24
    y = top
    visible = lines[-(int((HEIGHT - top - 10) / line_h)) :]

    for i, (text, color) in enumerate(visible):
        is_last = i == len(visible) - 1
        col = color
        if is_last and highlight_last:
            col = WHITE
        draw.text((margin, y), text, fill=col, font=font)
        y += line_h

    # Blinking cursor on last line – now using accurate character width
    if cursor and visible:
        last_text = visible[-1][0]
        # Get precise width of the last line
        bbox = font.getbbox(last_text)
        text_width = bbox[2] - bbox[0]
        cx = margin + text_width

        # Get width of a single character (monospaced)
        space_bbox = font.getbbox(" ")
        char_width = space_bbox[2] - space_bbox[0]

        cy = y - line_h  # y-coordinate of last line
        draw.rectangle([cx, cy + 1, cx + char_width, cy + line_h - 2], fill=CURSOR_COL)

    # Right panel border continuation
    draw.line([(0, 20), (TERM_W, 20)], fill=BORDER, width=1)

    return img


def post_process(img, do_glitch=False, glitch_intensity=5):
    """Apply a chain of effects to the image."""
    if do_glitch:
        img = effects.glitch_image(img, glitch_intensity)
    img = effects.add_phosphor_glow(img)
    img = effects.apply_scanlines(img)
    img = effects.apply_vignette(img)
    return img
