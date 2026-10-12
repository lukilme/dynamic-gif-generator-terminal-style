import random

import numpy as np
from PIL import Image, ImageFilter


def apply_scanlines(img, alpha=30):
    """Add dark scanlines every other row."""
    arr = np.array(img).astype(np.int16)
    for y in range(0, arr.shape[0], 2):
        arr[y] = np.clip(arr[y] - alpha, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def apply_vignette(img):
    """Darken the edges of the image."""
    arr = np.array(img).astype(np.float32)
    h, w = arr.shape[:2]
    cx, cy = w / 2, h / 2
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt(((X - cx) / cx) ** 2 + ((Y - cy) / cy) ** 2)
    mask = 1 - np.clip(dist * 0.6, 0, 0.65)
    arr[:, :, 0] *= mask
    arr[:, :, 1] *= mask
    arr[:, :, 2] *= mask
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def glitch_image(img, intensity=5):
    """Apply random channel shifts, band tears, and noise patches."""
    arr = np.array(img)
    h, w, _ = arr.shape
    # channel shift
    for c in range(3):
        arr[:, :, c] = np.roll(
            arr[:, :, c], random.randint(-intensity, intensity), axis=1
        )
    # horizontal band tears
    for _ in range(random.randint(2, 6)):
        y = random.randint(0, h - 1)
        band = random.randint(1, 5)
        arr[y : y + band] = np.roll(
            arr[y : y + band], random.randint(-intensity * 8, intensity * 8), axis=1
        )
    # random pixel noise patches
    if random.random() < 0.4:
        for _ in range(random.randint(5, 20)):
            px, py = random.randint(0, w - 4), random.randint(0, h - 4)
            arr[py : py + 2, px : px + 4] = [random.randint(80, 255) for _ in range(3)]
    return Image.fromarray(arr)


def add_phosphor_glow(img):
    """Add a subtle green bloom around bright pixels."""
    arr = np.array(img).astype(np.float32)
    glow = np.zeros_like(arr)
    glow[:, :, 1] = arr[:, :, 1]  # green channel only
    glow_img = Image.fromarray(np.clip(glow, 0, 255).astype(np.uint8))
    blurred = glow_img.filter(ImageFilter.GaussianBlur(radius=2))
    blurred_arr = np.array(blurred).astype(np.float32)
    result = np.clip(arr + blurred_arr * 0.3, 0, 255).astype(np.uint8)
    return Image.fromarray(result)
