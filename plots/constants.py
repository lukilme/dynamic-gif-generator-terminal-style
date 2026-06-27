class Palette:
    BG = (8, 8, 24)
    GRID = (20, 20, 48)
    WHITE = (220, 220, 255)
    CYAN = (0, 255, 240)
    MAGENTA = (255, 0, 180)
    YELLOW = (255, 220, 0)
    GREEN = (0, 255, 80)
    ORANGE = (255, 140, 0)
    PINK = (255, 80, 160)
    LBLUE = (80, 160, 255)
    RED = (255, 50, 50)

    LANG: dict[str, tuple] = {
        "Python": (0, 255, 80),
        "Shell": (0, 255, 240),
        "HiveQL": (255, 220, 0),
        "Scala": (255, 140, 0),
        "XML": (255, 80, 160),
        "Dockerfile": (80, 160, 255),
        "Perl": (255, 0, 180),
        "INI": (255, 50, 50),
        "JavaScript": (240, 219, 79),
        "TypeScript": (49, 120, 198),
        "Rust": (222, 94, 34),
        "Go": (0, 173, 216),
        "C": (85, 85, 255),
        "C++": (243, 75, 12),
        "Java": (176, 14, 14),
        "Ruby": (204, 52, 45),
        "HTML": (227, 106, 23),
        "CSS": (86, 169, 211),
    }

    DEFAULT_CYCLE = [
        (0, 255, 240),
        (255, 0, 180),
        (255, 220, 0),
        (0, 255, 80),
        (255, 140, 0),
        (255, 80, 160),
        (80, 160, 255),
        (255, 50, 50),
    ]

    @classmethod
    def for_lang(cls, lang: str, index: int = 0) -> tuple:
        return cls.LANG.get(lang, cls.DEFAULT_CYCLE[index % len(cls.DEFAULT_CYCLE)])
    