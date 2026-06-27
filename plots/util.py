from __future__ import annotations

import math
import os
import random
import platform
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from plots.gif_canvas import GifCanvas


def save_gif(
    path:   str,
    frames: list[Image.Image],
    duration: int = 80,
    loop:     int = 0,
    hold_last: int = 8,
    canvas: GifCanvas | None = None,
    glitch_hold: bool = True,
    glitch_probability: float = 0.3,
) -> None:
    if not frames:
        raise ValueError("No frames to save")

    all_frames = list(frames)
    last = frames[-1]
    
    for _ in range(hold_last):
        if glitch_hold and canvas and random.random() < glitch_probability:
            all_frames.append(canvas.apply_glitch(last, intensity=0.04))
        else:
            all_frames.append(last.copy())  # copy() evita problemas de referência

    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)


    all_frames[0].save(
        path,
        save_all=True,
        append_images=all_frames[1:],
        loop=loop,
        duration=duration,
        optimize=True,
    )
    
    print(f"GIF salvo: {path}  ({len(all_frames)} frames, {duration}ms/frame)")


def load_fonts() -> dict:
    """Load fonts for different platforms."""
    
    font_paths = {
        "Linux": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        ],
        "Darwin": [  # macOS
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/Monaco.dfont",
        ],
        "Windows": [
            "C:/Windows/Fonts/consola.ttf",
            "C:/Windows/Fonts/CascadiaCode.ttf",
            "C:/Windows/Fonts/JetBrainsMono.ttf",
            "C:/Windows/Fonts/DejaVuSansMono.ttf",
        ]
    }
    
    system = platform.system()
    paths = font_paths.get(system, [])
    
    if not paths:
        paths = font_paths["Linux"]
    
    bold_path = next((p for p in paths if "Bold" in p or "bold" in p and os.path.exists(p)), None)
    reg_path = next((p for p in paths if "Bold" not in p and "bold" not in p and os.path.exists(p)), None)
    
    if not bold_path:
        bold_path = next((p for p in paths if os.path.exists(p)), None)
    if not reg_path:
        reg_path = bold_path

    def get_font(path: str | None, size: int) -> ImageFont.FreeTypeFont:
        """Load font or return default."""
        try:
            return ImageFont.truetype(path, size) if path else ImageFont.load_default()
        except Exception as e:
            print(f"⚠️  Font loading failed: {e}")
            return ImageFont.load_default()

    return {
        "big":   get_font(bold_path, 18),
        "med":   get_font(bold_path, 13),
        "small": get_font(reg_path, 11),
    }