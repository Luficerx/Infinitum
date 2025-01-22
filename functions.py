from random import randint

def random_color(start: int = 0) -> tuple[int, int, int]:
    R, G, B = randint(start, 255), randint(start, 255), randint(start, 255)
    return (R,G,B)

def outside_bounds(pos: tuple[int, int], bounds: list[int, int, int, int], offset: int = 0) -> bool:
    x, y = pos
    a, b, c, d = bounds

    return any([x < a-offset, x > c+offset, y < b-offset, y > d+offset])

def render_text_on_screen(surface, text: str, x: int, y: int, size: int, color: str, adjust: bool = False):
    import pygame.freetype as pygfont

    font = pygfont.Font('JetBrains Mono Bold.ttf', size)
    
    surf, _ = font.render(text)
    wid, hei = surf.get_width(), surf.get_height()

    if adjust: pos = (x-wid/2, y-hei/2)

    else: pos = (x, y)

    font.render_to(surface, pos, text, color)

def toggle(*args):
    """*Unsafe*"""
    for i in args:
        globals()[i] = not globals()[i]
