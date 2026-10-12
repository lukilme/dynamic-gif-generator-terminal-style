import random

from config import (
    BG_PANEL,
    BORDER,
    CYAN,
    GREEN,
    GREEN_DIM,
    HEIGHT,
    LANG_COLORS,
    PANEL_W,
    TERM_W,
    WIDTH,
    YELLOW,
    font,
    font_bold,
    line_h,
)


def draw_border(draw, x0, y0, x1, y1, color=BORDER, radius=4):
    """Draw a rounded rectangle border."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=color, width=1)


def draw_mini_bar(draw, x, y, w, h, pct, color):
    """Draw a small horizontal progress bar."""
    draw.rectangle([x, y, x + w, y + h], fill=(20, 30, 20))
    fill_w = int(w * pct / 100)
    if fill_w > 0:
        draw.rectangle([x, y, x + fill_w, y + h], fill=color)


def progress_bar(p, width=20):
    """Return a string representing a text progress bar."""
    filled = int(p * width / 100)
    return "█" * filled + "░" * (width - filled)


def draw_title_bar(draw, title="lukilme@github: ~/repositories"):
    """Draw the top title bar with fake traffic lights."""
    # top bar
    draw.rectangle([0, 0, WIDTH, 20], fill=(18, 30, 18))
    # traffic lights
    for i, c in enumerate([(255, 90, 90), (255, 190, 50), (80, 200, 80)]):
        draw.ellipse([8 + i * 16, 6, 20 + i * 16, 14], fill=c)
    draw.text((60, 4), title, fill=GREEN_DIM, font=font_bold)
    # top separator
    draw.line([(0, 20), (WIDTH, 20)], fill=BORDER, width=1)


def draw_stats_panel(draw, repos_done, total, lang_tally):
    """Draw the right‑hand statistics panel."""
    # Panel background and left border
    draw.rectangle([TERM_W, 0, WIDTH, HEIGHT], fill=BG_PANEL)
    draw.line([(TERM_W, 0), (TERM_W, HEIGHT)], fill=BORDER, width=1)
    draw.text((TERM_W + 8, 25), "── STATS ──────────────", fill=GREEN_DIM, font=font)

    y = 45
    draw.text((TERM_W + 8, y), "Repos scanned:", fill=GREEN_DIM, font=font)
    y += 14
    pct_done = repos_done / total if total else 0
    draw.text((TERM_W + 8, y), f"  {repos_done:>2}/{total}", fill=GREEN, font=font)
    y += 16

    # overall progress bar
    bar_w = PANEL_W - 20
    draw_mini_bar(draw, TERM_W + 8, y, bar_w, 6, pct_done * 100, GREEN)
    y += 14

    draw.text((TERM_W + 8, y), "Languages found:", fill=GREEN_DIM, font=font)
    y += 14

    # Sort languages by total percentage
    sorted_langs = sorted(lang_tally.items(), key=lambda x: x[1], reverse=True)[:8]
    for lang, total_pct in sorted_langs:
        color = LANG_COLORS.get(lang, (150, 150, 150))
        lname = lang[:14]

        # Desenha o nome da linguagem
        draw.text((TERM_W + 8, y), f"  {lname}", fill=color, font=font)

        # Posiciona a barra abaixo do texto, com um pequeno espaçamento
        bar_y = y + line_h + 2  # 2px de espaçamento após o texto
        draw_mini_bar(
            draw, TERM_W + 8, bar_y, bar_w - 4, 4, min(total_pct / 2, 100), color
        )

        # Atualiza y para a próxima linha: altura do texto + barra + espaçamentos
        y = bar_y + 4 + 4  # 4 (altura da barra) + 4 (espaço extra)

    y += 4
    draw.line([(TERM_W + 4, y), (WIDTH - 4, y)], fill=BORDER)
    y += 8

    # Fake git stats
    commits = repos_done * random.randint(12, 28)
    draw.text((TERM_W + 8, y), "Est. commits:", fill=GREEN_DIM, font=font)
    y += 14
    draw.text((TERM_W + 8, y), f"  ~{commits}", fill=CYAN, font=font)
    y += 18

    stars = repos_done * random.randint(1, 5)
    draw.text((TERM_W + 8, y), "GitHub stars:", fill=GREEN_DIM, font=font)
    y += 14
    draw.text((TERM_W + 8, y), f"  ★ {stars}", fill=YELLOW, font=font)
    y += 18

    # Status indicator
    y = HEIGHT - 30
    pulse = "●" if random.random() < 0.7 else "○"
    draw.text((TERM_W + 8, y), f"{pulse} INDEXING...", fill=GREEN, font=font)
