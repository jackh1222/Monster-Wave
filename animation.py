# animation.py
import pygame

def load_animations(spritesheet_path, frame_width, frame_height, states):
    """
    spritesheet_path: path to your sprite-sheet image
    frame_width, frame_height: size of each frame in pixels
    states: dict mapping state names to (row_index, frame_count), e.g.
        { 'idle': (0,1), 'run': (1,3), 'jump': (2,1) }
    """
    sheet = pygame.image.load(spritesheet_path).convert_alpha()
    animations = {}
    for state, (row, count) in states.items():
        frames = []
        for i in range(count):
            rect = pygame.Rect(
                i * frame_width,
                row * frame_height,
                frame_width,
                frame_height
            )
            frames.append(sheet.subsurface(rect))
        animations[state] = frames
    return animations
