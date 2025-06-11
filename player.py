# player.py
import pygame
from config import GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, animations):
        super().__init__()
        self.animations = animations
        self.state      = 'idle'
        self.frame      = 0
        self.image      = animations[self.state][0]
        self.rect       = self.image.get_rect(topleft=(x, y))
        self.x          = float(x)
        self.y          = float(y)

        self.vel_y      = 0
        self.on_ground  = False
        self.facing     = 1

    def update(self, keys, platforms):
        # 1) if dead, only play death anim
        if self.state == 'death':
            # animations['death'] is a list [frame0, frame1, frame2, …],
            # we pick the **last** one (col 3)
            self.image = self.animations['death'][-1]
            return

        # 2) horizontal input & direction
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -5
            if self.on_ground: self.state = 'run'
            self.facing = -1
        elif keys[pygame.K_RIGHT]:
            dx = 5
            if self.on_ground: self.state = 'run'
            self.facing = 1
        else:
            if self.on_ground:
                self.state = 'idle'

        # 3) jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y     = -12
            self.on_ground = False
            self.state     = 'jump'

        # 4) gravity
        self.vel_y = min(self.vel_y + GRAVITY, 10)
        dy = self.vel_y

        # 5) horizontal move + platform collide
        self.x      += dx
        self.rect.x  = int(self.x)
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if dx > 0:
                    self.rect.right = plat.rect.left
                elif dx < 0:
                    self.rect.left  = plat.rect.right
                self.x = float(self.rect.x)

        # 6) vertical move + platform collide
        self.y      += dy
        self.rect.y  = int(self.y)
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if dy > 0:   # landing
                    self.rect.bottom = plat.rect.top
                    self.vel_y       = 0
                    self.on_ground   = True
                elif dy < 0: # head‐bump
                    self.rect.top     = plat.rect.bottom
                    self.vel_y        = 0
                self.y = float(self.rect.y)

        # 7) clamp to screen bounds
        # horizontal
        if self.rect.left < 0:
            self.rect.left = 0
            self.x         = float(self.rect.x)
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.x          = float(self.rect.x)
        # vertical (optional—prevents jumping off top or falling below bottom)
        if self.rect.top < 0:
            self.rect.top = 0
            self.y        = float(self.rect.y)
            self.vel_y    = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.y           = float(self.rect.y)
            self.vel_y       = 0
            self.on_ground   = True

        # 8) animate
        frames = self.animations[self.state]
        self.frame = (self.frame + 0.2) % len(frames)
        self.image = frames[int(self.frame)]
