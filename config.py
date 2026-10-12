from PIL import ImageFont

# ---------- DIMENSIONS ----------
WIDTH, HEIGHT = 860, 520
PANEL_W = 260  # right stats panel
TERM_W = WIDTH - PANEL_W

# ---------- COLOR PALETTE ----------
BG = (6, 10, 6)
BG_PANEL = (10, 16, 10)
GREEN = (100, 255, 100)
GREEN_DIM = (50, 140, 50)
GREEN_PALE = (160, 255, 160)
CYAN = (80, 220, 220)
YELLOW = (220, 220, 80)
RED = (255, 80, 80)
WHITE = (200, 210, 200)
BORDER = (40, 90, 40)
CURSOR_COL = (100, 255, 100)

# Language → color (extended for new languages)
LANG_COLORS = {
    "Go": (0, 173, 216),
    "Python": (53, 114, 165),
    "JavaScript": (241, 224, 90),
    "Rust": (222, 165, 132),
    "Dart": (0, 180, 216),
    "PHP": (119, 123, 179),
    "HTML": (227, 76, 38),
    "CSS": (86, 61, 124),
    "Shell": (137, 224, 81),
    "Markdown": (150, 150, 150),
    "Protocol Buffer": (200, 80, 200),
    "TOML": (180, 130, 70),
    "YAML": (200, 200, 100),
    "Jupyter Notebook": (240, 120, 0),
    # New languages
    "HiveQL": (200, 150, 100),
    "Scala": (220, 80, 60),
    "XML": (70, 130, 180),
    "Perl": (80, 120, 160),
    "INI": (150, 150, 150),
    "SQL": (230, 120, 40),
    "Makefile": (100, 180, 100),
    "Dockerfile": (0, 150, 200),
}

# ---------- FONTS ----------
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

try:
    font = ImageFont.truetype(FONT_PATH, 13)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, 13)
except OSError:
    # Fallback to default if font not found
    font = ImageFont.load_default()
    font_bold = ImageFont.load_default()

line_h = 17
margin = 14
