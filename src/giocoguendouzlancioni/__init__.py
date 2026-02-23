import pygame
import sys
import os
import math
import random

pygame.init()

# Dimensioni finestra
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jetpack Joyride")

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
GRAY = (40, 40, 40)
BLUE = (70, 130, 220)
GREEN = (100, 200, 100)
RED = (220, 80, 80)

# Impostazioni di gioco
settings = {
    'volume': 50,
    'difficulty': 'base'
}

# Caricamento immagini semplificato
def load(path):
    return pygame.image.load(path).convert_alpha() if os.path.exists(path) else None

# Background scalato
bg = load("background - Copia.jpg")
background = pygame.transform.scale(bg, (WIDTH, HEIGHT)) if bg else None

# Jetpack
jetpack = load("jetpack.png")
if jetpack:
    jetpack = pygame.transform.scale(jetpack, (80, 80))  # Dimensione giocatore normale

# Icona impostazioni
settings_icon = load("settings.png")
if settings_icon:
    settings_icon = pygame.transform.scale(settings_icon, (70, 70))

# Immagini boost (caricamento con fallback)
boost_power_img = load("potenza.png")
boost_health_img = load("cuore.png")
boost_speed_img = load("velocità.png")

# Scala boost se esistono
if boost_power_img:
    boost_power_img = pygame.transform.scale(boost_power_img, (50, 50))
if boost_health_img:
    boost_health_img = pygame.transform.scale(boost_health_img, (50, 50))
if boost_speed_img:
    boost_speed_img = pygame.transform.scale(boost_speed_img, (50, 50))

# Immagine nemico
enemy_img = load("nemico.png")
if enemy_img:
    enemy_img = pygame.transform.scale(enemy_img, (60, 60))


def main():
    menu()


def menu():
    clock = pygame.time.Clock()
    t = 0
    title_font = pygame.font.Font(None, 110)
    button_font = pygame.font.Font(None, 50)
    title = title_font.render("JETPACK JOYRIDE", True, YELLOW)
    shadow = title_font.render("JETPACK JOYRIDE", True, BLACK)
    button_enter = pygame.Rect(WIDTH//2 - 150, HEIGHT - 150, 300, 70)
    button_settings = pygame.Rect(WIDTH - 90, 20, 70, 70)

    # Crea un jetpack animato per il menu
    jetpack_menu = load("jetpack.png")
    if jetpack_menu:
        jetpack_menu = pygame.transform.scale(jetpack_menu, (350, 350))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                start_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        screen.blit(background, (0, 0)) if background else screen.fill(GRAY)

        if jetpack_menu:
            offset = math.sin(t / 20) * 10
            screen.blit(jetpack_menu, (WIDTH//2 - jetpack_menu.get_width()//2,
                                       HEIGHT//2 - jetpack_menu.get_height()//2 + offset))

        x = WIDTH//2 - title.get_width()//2
        screen.blit(shadow, (x + 4, 104))
        screen.blit(title, (x, 100))

        hover_enter = button_enter.collidepoint(mouse_pos)
        color = (255, 255, 255) if hover_enter else (200, 200, 200)
        border = (255, 220, 0) if hover_enter else (150, 150, 150)
        pygame.draw.rect(screen, color, button_enter, border_radius=15)
        pygame.draw.rect(screen, border, button_enter, 4, border_radius=15)
        txt = button_font.render("ENTER", True, BLACK)
        screen.blit(txt, (button_enter.centerx - txt.get_width()//2,
                          button_enter.centery - txt.get_height()//2))

        hover_settings = button_settings.collidepoint(mouse_pos)
        if settings_icon:
            icon_to_display = settings_icon.copy()
            if hover_settings:
                temp_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.rect(temp_surface, YELLOW, (0, 0, 80, 80), 3, border_radius=10)
                screen.blit(temp_surface, (button_settings.x - 5, button_settings.y - 5))
            screen.blit(icon_to_display, button_settings)
        else:
            settings_color = YELLOW if hover_settings else WHITE
            pygame.draw.circle(screen, settings_color, button_settings.center, 35, 3)
            pygame.draw.circle(screen, settings_color, button_settings.center, 18, 3)
            for i in range(6):
                angle = math.radians(i * 60)
                x1 = button_settings.centerx + math.cos(angle) * 26
                y1 = button_settings.centery + math.sin(angle) * 26
                x2 = button_settings.centerx + math.cos(angle) * 34
                y2 = button_settings.centery + math.sin(angle) * 34
                pygame.draw.line(screen, settings_color, (x1, y1), (x2, y2), 5)

        if click:
            if hover_enter:
                start_game()
            if hover_settings:
                settings_menu()

        pygame.display.flip()
        clock.tick(60)
        t += 1


def settings_menu():
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 80)
    label_font = pygame.font.Font(None, 45)
    button_font = pygame.font.Font(None, 40)
    slider_rect = pygame.Rect(200, 200, 400, 10)
    slider_handle = pygame.Rect(0, 0, 20, 30)
    dragging = False
    button_base = pygame.Rect(200, 320, 180, 60)
    button_avanzato = pygame.Rect(420, 320, 180, 60)
    button_back = pygame.Rect(WIDTH//2 - 100, HEIGHT - 100, 200, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        click = False
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True
                dragging = False

        screen.blit(background, (0, 0)) if background else screen.fill(GRAY)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(GRAY)
        screen.blit(overlay, (0, 0))

        title = title_font.render("IMPOSTAZIONI", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        volume_label = label_font.render("Volume", True, WHITE)
        screen.blit(volume_label, (200, 150))
        volume_value = label_font.render(f"{settings['volume']}%", True, YELLOW)
        screen.blit(volume_value, (620, 150))

        pygame.draw.rect(screen, WHITE, slider_rect, border_radius=5)
        slider_handle.centerx = slider_rect.x + (settings['volume'] / 100) * slider_rect.width
        slider_handle.centery = slider_rect.centery

        if slider_handle.collidepoint(mouse_pos) and click:
            dragging = True
        if dragging:
            new_x = max(slider_rect.x, min(mouse_pos[0], slider_rect.right))
            settings['volume'] = int(((new_x - slider_rect.x) / slider_rect.width) * 100)
            slider_handle.centerx = new_x
        pygame.draw.rect(screen, YELLOW, slider_handle, border_radius=5)

        diff_label = label_font.render("Difficoltà", True, WHITE)
        screen.blit(diff_label, (200, 270))

        is_base = settings['difficulty'] == 'base'
        color_base = GREEN if is_base else (80, 80, 80)
        border_base = GREEN if is_base else WHITE
        pygame.draw.rect(screen, color_base, button_base, border_radius=10)
        pygame.draw.rect(screen, border_base, button_base, 4, border_radius=10)
        txt_base = button_font.render("BASE", True, WHITE)
        screen.blit(txt_base, (button_base.centerx - txt_base.get_width()//2,
                                button_base.centery - txt_base.get_height()//2))

        is_avanzato = settings['difficulty'] == 'avanzato'
        color_avanzato = RED if is_avanzato else (80, 80, 80)
        border_avanzato = RED if is_avanzato else WHITE
        pygame.draw.rect(screen, color_avanzato, button_avanzato, border_radius=10)
        pygame.draw.rect(screen, border_avanzato, button_avanzato, 4, border_radius=10)
        txt_avanzato = button_font.render("AVANZATO", True, WHITE)
        screen.blit(txt_avanzato, (button_avanzato.centerx - txt_avanzato.get_width()//2,
                                    button_avanzato.centery - txt_avanzato.get_height()//2))

        if click:
            if button_base.collidepoint(mouse_pos):
                settings['difficulty'] = 'base'
            if button_avanzato.collidepoint(mouse_pos):
                settings['difficulty'] = 'avanzato'

        hover_back = button_back.collidepoint(mouse_pos)
        color_back = YELLOW if hover_back else WHITE
        pygame.draw.rect(screen, color_back, button_back, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_back, 3, border_radius=10)
        txt_back = button_font.render("INDIETRO", True, BLACK)
        screen.blit(txt_back, (button_back.centerx - txt_back.get_width()//2,
                                button_back.centery - txt_back.get_height()//2))

        if hover_back and click:
            return

        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────────────────────
#  CLASSI DI GIOCO
# ─────────────────────────────────────────────────────────────

class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.width = 80
        self.height = 80
        self.speed = 5 if settings['difficulty'] == 'base' else 7
        self.health = 100
        self.max_health = 100
        self.power = 1
        self.fire_rate = 300          # ms tra un colpo e l'altro
        self.last_shot = 0

        # Contatori boost raccolti
        self.boost_counts = {'power': 0, 'health': 0, 'speed': 0}

    def move(self, keys):
        # Movimento verticale
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.speed
        # Movimento orizzontale
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def shoot(self, keys, current_time):
        """Spara solo se si preme SPAZIO e il cooldown è trascorso."""
        if keys[pygame.K_SPACE] and current_time - self.last_shot > self.fire_rate:
            self.last_shot = current_time
            return Bullet(self.x + self.width, self.y + self.height // 2, self.power)
        return None

    def draw(self, surface):
        if jetpack:
            surface.blit(jetpack, (self.x, self.y))
        else:
            pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))


class Bullet:
    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.width = 15 * power
        self.height = 8
        self.speed = 12
        self.power = power

    def move(self):
        self.x += self.speed

    def draw(self, surface):
        pygame.draw.ellipse(surface, YELLOW,
                            (self.x, self.y - self.height // 2, self.width, self.height))
        pygame.draw.ellipse(surface, (255, 255, 150),
                            (self.x + 2, self.y - self.height // 2 + 2,
                             self.width - 4, self.height - 4))


class Enemy:
    def __init__(self):
        self.x = WIDTH + random.randint(0, 100)
        self.y = random.randint(50, HEIGHT - 110)
        self.width = 60
        self.height = 60
        self.speed = 3 if settings['difficulty'] == 'base' else 5
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1000, 2500)

    def move(self):
        self.x -= self.speed

    def shoot(self, current_time):
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            self.shoot_delay = random.randint(1000, 2500)
            return EnemyBullet(self.x, self.y + self.height // 2)
        return None

    def draw(self, surface):
        if enemy_img:
            surface.blit(enemy_img, (self.x, self.y))
        else:
            pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
            pygame.draw.polygon(surface, (150, 0, 0), [
                (self.x, self.y + self.height // 2),
                (self.x + self.width, self.y + 5),
                (self.x + self.width, self.y + self.height - 5)
            ])
            pygame.draw.circle(surface, (100, 100, 255),
                               (int(self.x + 15), int(self.y + self.height // 2)), 8)


class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.speed = 7

    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 50, 50), (int(self.x), int(self.y)), 5)
        pygame.draw.circle(surface, (255, 150, 150), (int(self.x), int(self.y)), 3)


class Missile:
    def __init__(self):
        self.x = WIDTH + random.randint(0, 100)
        self.y = random.randint(50, HEIGHT - 100)
        self.width = 40
        self.height = 20
        self.speed = 4 if settings['difficulty'] == 'base' else 6

    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 100, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.polygon(surface, (200, 50, 0), [
            (self.x + self.width, self.y + self.height // 2),
            (self.x + self.width + 15, self.y),
            (self.x + self.width + 15, self.y + self.height)
        ])
        pygame.draw.polygon(surface, (255, 200, 0), [
            (self.x, self.y + 5),
            (self.x - 10, self.y + self.height // 2),
            (self.x, self.y + self.height - 5)
        ])


class Boost:
    def __init__(self, boost_type):
        self.x = WIDTH + random.randint(0, 100)
        self.y = random.randint(100, HEIGHT - 150)
        self.width = 50
        self.height = 50
        self.speed = 3
        self.type = boost_type

    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        if self.type == 'power' and boost_power_img:
            surface.blit(boost_power_img, (self.x, self.y))
        elif self.type == 'health' and boost_health_img:
            surface.blit(boost_health_img, (self.x, self.y))
        elif self.type == 'speed' and boost_speed_img:
            surface.blit(boost_speed_img, (self.x, self.y))
        else:
            if self.type == 'power':
                pygame.draw.circle(surface, YELLOW, (int(self.x + 25), int(self.y + 25)), 25)
                pygame.draw.polygon(surface, WHITE, [
                    (self.x + 25, self.y + 10), (self.x + 20, self.y + 25),
                    (self.x + 28, self.y + 25), (self.x + 20, self.y + 40)
                ])
            elif self.type == 'health':
                pygame.draw.circle(surface, GREEN, (int(self.x + 25), int(self.y + 25)), 25)
                pygame.draw.rect(surface, WHITE, (self.x + 10, self.y + 20, 30, 10))
                pygame.draw.rect(surface, WHITE, (self.x + 20, self.y + 10, 10, 30))
            elif self.type == 'speed':
                pygame.draw.circle(surface, BLUE, (int(self.x + 25), int(self.y + 25)), 25)
                pygame.draw.polygon(surface, WHITE, [
                    (self.x + 30, self.y + 15), (self.x + 40, self.y + 25),
                    (self.x + 30, self.y + 35)
                ])
                pygame.draw.polygon(surface, WHITE, [
                    (self.x + 20, self.y + 15), (self.x + 30, self.y + 25),
                    (self.x + 20, self.y + 35)
                ])


# ─────────────────────────────────────────────────────────────
#  HUD  –  contatore boost in alto a destra
# ─────────────────────────────────────────────────────────────

def draw_boost_counter(surface, player, font):
    """Disegna i boost raccolti in alto a destra con icone e contatori."""
    panel_x = WIDTH - 180
    panel_y = 10
    padding = 5

    # Sfondo pannello
    panel = pygame.Surface((170, 100), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 140))
    surface.blit(panel, (panel_x - padding, panel_y - padding))

    boost_data = [
        ('power',  boost_power_img,  YELLOW, "⚡ POW"),
        ('health', boost_health_img, GREEN,  "❤ VITA"),
        ('speed',  boost_speed_img,  BLUE,   "➤ VEL"),
    ]

    for i, (btype, img, color, label) in enumerate(boost_data):
        row_y = panel_y + i * 32
        count = player.boost_counts[btype]

        # Icona piccola o cerchio colorato
        if img:
            small = pygame.transform.scale(img, (26, 26))
            surface.blit(small, (panel_x, row_y))
        else:
            pygame.draw.circle(surface, color, (panel_x + 13, row_y + 13), 13)

        # Etichetta + contatore
        txt = font.render(f"{label}: x{count}", True, color)
        surface.blit(txt, (panel_x + 32, row_y + 5))


# ─────────────────────────────────────────────────────────────
#  LOOP PRINCIPALE DI GIOCO
# ─────────────────────────────────────────────────────────────

def start_game():
    clock = pygame.time.Clock()
    player = Player()
    bullets = []
    enemies = []
    enemy_bullets = []
    missiles = []
    boosts = []
    score = 0

    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 28)

    enemy_spawn_timer = 0
    missile_spawn_timer = 0
    boost_spawn_timer = 0

    # Effetti visivi: flash danno
    damage_flash = 0   # frame rimanenti del flash rosso

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        keys = pygame.key.get_pressed()

        # ── Aggiorna giocatore ──────────────────────────────
        player.move(keys)

        bullet = player.shoot(keys, current_time)
        if bullet:
            bullets.append(bullet)

        # ── Spawn nemici ────────────────────────────────────
        enemy_spawn_timer += 1
        if enemy_spawn_timer > (100 if settings['difficulty'] == 'base' else 70):
            enemies.append(Enemy())
            enemy_spawn_timer = 0

        missile_spawn_timer += 1
        if missile_spawn_timer > (180 if settings['difficulty'] == 'base' else 130):
            missiles.append(Missile())
            missile_spawn_timer = 0

        boost_spawn_timer += 1
        if boost_spawn_timer > 250:
            boost_type = random.choice(['power', 'health', 'speed'])
            boosts.append(Boost(boost_type))
            boost_spawn_timer = 0

        # ── Muovi oggetti ───────────────────────────────────
        for bullet in bullets[:]:
            bullet.move()
            if bullet.x > WIDTH:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.move()
            eb = enemy.shoot(current_time)
            if eb:
                enemy_bullets.append(eb)
            if enemy.x < -enemy.width:
                enemies.remove(enemy)

        for eb in enemy_bullets[:]:
            eb.move()
            if eb.x < 0:
                enemy_bullets.remove(eb)

        for missile in missiles[:]:
            missile.move()
            if missile.x < -missile.width - 20:
                missiles.remove(missile)

        for boost in boosts[:]:
            boost.move()
            if boost.x < -boost.width:
                boosts.remove(boost)

        # ── Collisioni proiettili giocatore → nemici ────────
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (bullet.x < enemy.x + enemy.width and
                        bullet.x + bullet.width > enemy.x and
                        bullet.y < enemy.y + enemy.height and
                        bullet.y + bullet.height > enemy.y):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    score += 10

        # ── Collisioni proiettili nemici → giocatore ────────
        player_rect = pygame.Rect(player.x + 10, player.y + 10,
                                  player.width - 20, player.height - 20)
        for eb in enemy_bullets[:]:
            eb_rect = pygame.Rect(eb.x - 5, eb.y - 5, 10, 10)
            if player_rect.colliderect(eb_rect):
                if eb in enemy_bullets:
                    enemy_bullets.remove(eb)
                player.health -= 10
                damage_flash = 12   # frame del flash

        # ── Collisioni missili → giocatore ──────────────────
        for missile in missiles[:]:
            m_rect = pygame.Rect(missile.x, missile.y, missile.width, missile.height)
            if player_rect.colliderect(m_rect):
                if missile in missiles:
                    missiles.remove(missile)
                player.health -= 20
                damage_flash = 20

        # ── Collisioni boost → giocatore ────────────────────
        for boost in boosts[:]:
            b_rect = pygame.Rect(boost.x, boost.y, boost.width, boost.height)
            if player_rect.colliderect(b_rect):
                if boost in boosts:
                    boosts.remove(boost)
                player.boost_counts[boost.type] += 1   # incrementa contatore

                if boost.type == 'power':
                    player.power = min(player.power + 1, 3)
                    score += 5
                elif boost.type == 'health':
                    # Aumenta la vita e la mostra nella barra
                    player.health = min(player.health + 30, player.max_health)
                    score += 5
                elif boost.type == 'speed':
                    player.fire_rate = max(player.fire_rate - 80, 120)
                    player.speed = min(player.speed + 1, 10)
                    score += 5

        # Punteggio sopravvivenza
        score += 1

        # Game over
        player.health = max(player.health, 0)
        if player.health <= 0:
            running = False

        # ── Disegno ─────────────────────────────────────────
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(GRAY)

        # Flash danno: overlay rosso semi-trasparente
        if damage_flash > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = int(120 * (damage_flash / 20))
            flash_surf.fill((220, 0, 0, alpha))
            screen.blit(flash_surf, (0, 0))
            damage_flash -= 1

        player.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for eb in enemy_bullets:
            eb.draw(screen)
        for missile in missiles:
            missile.draw(screen)
        for boost in boosts:
            boost.draw(screen)

        # ── HUD ─────────────────────────────────────────────

        # Barra vita
        bar_width = 250
        bar_height = 25
        bar_x, bar_y = 20, 20
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        health_w = int((player.health / player.max_health) * bar_width)
        health_color = (GREEN if player.health > 50
                        else YELLOW if player.health > 25 else RED)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_w, bar_height), border_radius=5)
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 3, border_radius=5)
        health_text = font.render(f"VITA: {player.health}", True, WHITE)
        screen.blit(health_text, (bar_x + bar_width + 10, bar_y))

        # Barra potere
        pow_text = font.render(f"POW: x{player.power}", True, YELLOW)
        screen.blit(pow_text, (20, 55))

        # Punteggio
        score_text = font.render(f"SCORE: {score}", True, YELLOW)
        screen.blit(score_text, (20, 85))

        # Istruzioni in basso
        hint = small_font.render("← ↑ ↓ → Muovi  |  SPAZIO Spara  |  ESC Menu", True, (180, 180, 180))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))

        # Contatore boost in alto a destra
        draw_boost_counter(screen, player, small_font)

        pygame.display.flip()
        clock.tick(60)

    game_over_screen(score)


# ─────────────────────────────────────────────────────────────
#  GAME OVER
# ─────────────────────────────────────────────────────────────

def game_over_screen(score):
    clock = pygame.time.Clock()
    font_big = pygame.font.Font(None, 100)
    font_small = pygame.font.Font(None, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill(BLACK)
        game_over_text = font_big.render("GAME OVER", True, RED)
        screen.blit(game_over_text,
                    (WIDTH // 2 - game_over_text.get_width() // 2, 200))
        score_text = font_small.render(f"PUNTEGGIO: {score}", True, YELLOW)
        screen.blit(score_text,
                    (WIDTH // 2 - score_text.get_width() // 2, 320))
        restart_text = font_small.render("PREMI ENTER PER TORNARE AL MENU", True, WHITE)
        screen.blit(restart_text,
                    (WIDTH // 2 - restart_text.get_width() // 2, 400))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
