"""Shared prompt blocks for the art. The same block order is used in every prompt of a series
(xAI prompting guide). The prompt text is part of the image cache key, so change a block only
when you want new pixels."""

# ---- Flat vector art on a plain pale background (the square set).
STYLE_FLAT = (
    "Flat vector children's picture-book illustration for a two-year-old, drawn with thick clean "
    "dark-navy outlines and large simple shapes. Solid flat colors only, with no gradients, no shading, "
    "no texture and no tiny details, on a plain pale background. There is no text, no letters and no "
    "numbers anywhere in the picture."
)

# What the hero looks like, read from the reference photo. It backs up the photo, it does not replace it.
HERO_LIKENESS = (
    "short light-blond hair, large blue-gray eyes, a round face with rosy cheeks, light skin and a wide "
    "happy smile that shows a few small teeth. The toddler wears a yellow t-shirt, blue shorts and bare feet."
)

TUB = (
    "a clear rectangular plastic tub that is half full of blue water, seen from the side so the "
    "water line is visible"
)

# The hero rule that every page prompt of every book repeats. Change it only to get new pixels.
KEEP = (
    "Keep the same toddler design from the reference picture: the same hair, face, yellow t-shirt and "
    "blue shorts, with the same line weight and the same flat vector style."
)


def sheet_from_photo() -> str:
    return (
        f"Redraw the toddler in the reference photograph as a character reference picture. Keep the real "
        f"face: {HERO_LIKENESS} Shown once, full body, standing in a friendly front view, centered on a "
        f"plain white background with generous empty space on every side. {STYLE_FLAT}"
    )


def scene_flat(action: str, keep: str) -> str:
    return (
        f"{action} One scene, the main subject centered and large, a very simple background with generous "
        f"empty space around it. {keep} {STYLE_FLAT}"
    )
