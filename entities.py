import pygame
import random
from config import SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, run_image, death_image, speed=2):
        super().__init__()
        # images
        self.run_image   = run_image
        self.death_image = death_image

        # start running
        self.image = run_image
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.vx    = speed if random.choice([True, False]) else -speed

        # hit & death tracking
        self.hit_count       = 0
        self.dead            = False
        self.death_start_ms  = None
        self.death_duration  = 500  # ms

    def update(self, platforms):
        # if dead: show corpse, then remove after delay
        if self.dead:
            now = pygame.time.get_ticks()
            self.image = self.death_image
            if now - self.death_start_ms >= self.death_duration:
                self.kill()
            return

        # normal patrol logic
        self.rect.x += self.vx
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                # bounce off walls
                if self.vx > 0:
                    self.rect.right = plat.rect.left
                else:
                    self.rect.left  = plat.rect.right
                self.vx *= -1
                return

        # turn at platform edges
        front_x = self.rect.right if self.vx > 0 else self.rect.left
        foot    = pygame.Rect(front_x, self.rect.bottom+1, 1, 1)
        if not any(foot.colliderect(plat.rect) for plat in platforms):
            self.vx *= -1

    def take_hit(self, count=1):
        """Call this when a bullet hits the enemy."""
        if self.dead:
            return
        self.hit_count += count
        if self.hit_count >= 3:  # 3 hits to die
            # start the death sequence
            self.dead           = True
            self.death_start_ms = pygame.time.get_ticks()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image=None):
        super().__init__()
        # allow you to pass in an image, or fall back to a simple rect:
        if image:
            self.image = image
        else:
            surf = pygame.Surface((10, 5), pygame.SRCALPHA)
            surf.fill((255, 255, 0))
            self.image = surf

        self.rect = self.image.get_rect(center=(x, y))
        self.vx   = 12 * direction

    def update(self):
        self.rect.x += self.vx
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
