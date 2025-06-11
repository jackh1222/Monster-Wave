# main.py
import pygame
import random
from config      import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from tilemap     import TileMap
from player      import Player
from entities    import Enemy, Bullet
from animation   import load_animations

def get_platform_y(platforms, x_start, y_max=SCREEN_HEIGHT):
    """Find the top Y of the platform directly under a given x coordinate."""
    min_y = y_max
    for plat in platforms:
        if plat.rect.left <= x_start <= plat.rect.right:
            if plat.rect.top < min_y:
                min_y = plat.rect.top
    return min_y

def setup_level(num_enemies):
    tilemap   = TileMap("level1.csv")
    platforms = list(tilemap.platforms)

    # Spawn player near the left edge
    player_x = 100
    player_y = get_platform_y(platforms, player_x) - 32
    player   = Player(player_x, player_y, player_anims)

    run_img    = enemy_anims['run'][0]
    corpse_img = enemy_anims['death'][-1]
    enemies    = pygame.sprite.Group()

    margin = player.rect.width * 4
    xmax   = SCREEN_WIDTH - run_img.get_width()

    for _ in range(num_enemies):
        left_end    = max(0, player_x - margin)
        right_start = min(xmax, player_x + margin)

        zones = []
        if left_end > 0:
            zones.append((0, left_end))
        if right_start < xmax:
            zones.append((right_start, xmax))

        if zones:
            zone = random.choice(zones)
            enemy_x = random.randint(zone[0], zone[1])
        else:
            enemy_x = random.randint(0, xmax)

        enemy_y = get_platform_y(platforms, enemy_x) - run_img.get_height()
        enemies.add(Enemy(enemy_x, enemy_y, run_img, corpse_img))

    bullets     = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(*platforms, player, *enemies)

    return tilemap, platforms, player, enemies, bullets, all_sprites

def draw_button(screen, rect, text, font, color_bg, color_fg):
    pygame.draw.rect(screen, color_bg, rect)
    txt = font.render(text, True, color_fg)
    screen.blit(txt, txt.get_rect(center=rect.center))

# -------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Monster Waves 怪兽来袭")
    clock  = pygame.time.Clock()

    # load animations once
    global player_anims, enemy_anims
    player_anims = load_animations(
        'sprite_sheet.png', 32, 32,
        states={'idle':(0,1),'run':(0,3),'jump':(0,1),'death':(0,4)}
    )
    enemy_anims = load_animations(
        'sprite_sheet.png', 32, 32,
        states={'run':(1,2),'death':(1,3)}
    )

    # prepare buttons
    font_btn = pygame.font.Font(None, 48)
    btn_start = pygame.Rect(0,0,200,60)
    btn_rules = pygame.Rect(0,0,200,60)
    btn_back  = pygame.Rect(0,0,200,60)
    btn_start.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)
    btn_rules.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)
    btn_back.center  = (SCREEN_WIDTH//2, SCREEN_HEIGHT - 80)

    # — prepare in‐game action buttons, centered on screen —
    btn_restart = pygame.Rect(0, 0, 200, 60)
    btn_next = pygame.Rect(0, 0, 200, 60)
    btn_restart.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
    btn_next.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

    # game state & level
    state = "menu"
    level_count   = 1
    ground, platforms, player, enemies, bullets, all_sprites = setup_level(level_count)
    game_over     = False
    level_cleared = False

    # the rules text
    rules = [
        "Use left / right button to move",
        "SPACE to jump",
        "Z to shoot (4 hits to kill)",
        "Clear all enemies to go next level",
        "Avoid touching enemies (even their dead bodies) or you'll die!"
    ]

    while True:
        dt = clock.tick(FPS) / 1000.0
        mx, my = pygame.mouse.get_pos()

        # handle events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return

            if state == "menu":
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if btn_start.collidepoint(mx,my):
                        state = "playing"
                        # reset level state
                        level_count = 1
                        ground, platforms, player, enemies, bullets, all_sprites = setup_level(level_count)
                        game_over = level_cleared = False
                    elif btn_rules.collidepoint(mx,my):
                        state = "rules"

            elif state == "rules":
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if btn_back.collidepoint(mx,my):
                        state = "menu"

            elif state == "playing":
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_z:
                    if not game_over and not level_cleared:
                        b = Bullet(player.rect.centerx, player.rect.centery, player.facing)
                        bullets.add(b); all_sprites.add(b)

                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if game_over and btn_back.collidepoint(mx,my):
                        # restart
                        ground, platforms, player, enemies, bullets, all_sprites = setup_level(level_count)
                        game_over = level_cleared = False
                    elif level_cleared and btn_back.collidepoint(mx,my):
                        # next level
                        level_count *= 2
                        ground, platforms, player, enemies, bullets, all_sprites = setup_level(level_count)
                        game_over = level_cleared = False

                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if game_over and btn_restart.collidepoint(ev.pos):
                        # restart same level
                        ground, platforms, player, enemies, bullets, all_sprites = setup_level(level_count)
                        game_over = level_cleared = False
                    elif level_cleared and btn_next.collidepoint(ev.pos):
                    # advance to next level
                        level_count *= 2
                        ground, platforms, player, enemies, bullets, all_sprites = setup_level(level_count)
                        game_over = level_cleared = False

        # update and draw by state
        screen.fill((135,206,235))

        if state == "menu":
            draw_button(screen, btn_start, "START", font_btn, (50,50,200), (255,255,255))
            draw_button(screen, btn_rules, "RULES", font_btn, (50,200,50), (255,255,255))

        elif state == "rules":
            # draw rules lines
            font_txt = pygame.font.Font(None, 36)
            for i, line in enumerate(rules):
                txt = font_txt.render(line, True, (0,0,0))
                screen.blit(txt, (50, 50 + i*40))
            draw_button(screen, btn_back, "BACK", font_btn, (200,50,50), (255,255,255))

        elif state == "playing":
            # always update player (so death frame shows)
            keys = pygame.key.get_pressed()
            player.update(keys, platforms)

            if not game_over and not level_cleared:
                for g in enemies: g.update(platforms)
                bullets.update()
                # bullet hits
                hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
                for e, blist in hits.items(): e.take_hit(len(blist))
                # player death
                if player.state!="death" and pygame.sprite.spritecollideany(player, enemies):
                    player.state = 'death'; player.frame = 0
                    player.image = player.animations['death'][-1]
                    game_over = True
                # clear level?
                if not enemies: level_cleared = True

            # draw game world
            all_sprites.draw(screen)

            # overlay game over or next-level
            if game_over:
                txt = pygame.font.Font(None,72).render("GAME OVER", True, (200,30,30))
                screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)))
                draw_button(screen, btn_restart, "RESTART", font_btn, (50,50,50), (100,255,255))
            elif level_cleared:
                txt = pygame.font.Font(None,72).render("LEVEL CLEARED!", True, (30,200,30))
                screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)))
                draw_button(screen, btn_next, "NEXT LEVEL", font_btn, (50,50,50), (255,255,255))

        pygame.display.flip()

if __name__ == "__main__":
    main()
