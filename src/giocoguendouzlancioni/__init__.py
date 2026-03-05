import pygame
import sys
import os
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MissionOne - Boss Edition")

# ───────────── COLORI ─────────────
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
GRAY = (40, 40, 40)
BLUE = (70, 130, 220)
GREEN = (100, 200, 100)
RED = (220, 80, 80)
CYAN = (0, 220, 220)
PURPLE = (150, 50, 200)
# Colori Titolo e Impostazioni
MAGENTA = (255, 0, 255)
PINK = (255, 100, 180)      # Rosa per Titolo e Impostazioni

# ───────────── IMPOSTAZIONI ─────────────
settings = {
    'volume': 50,
    'difficulty': 'base'
}

# ───────────── CARICAMENTO IMMAGINI ─────────────
def load(path):
    return pygame.image.load(path).convert_alpha() if os.path.exists(path) else None

# Percorsi file specificati dall'utente
bg = load("C:/Users/s14685928/Documents/GitHub/GiocoGuendouzLancioni/src/giocoguendouzlancioni/background.jpg")
background = pygame.transform.scale(bg, (WIDTH, HEIGHT)) if bg else None

jetpack = load("jetpack.png")
if jetpack:
    jetpack = pygame.transform.scale(jetpack, (120, 120))

settings_icon = load("settings.png")
if settings_icon:
    settings_icon = pygame.transform.scale(settings_icon, (70, 70))

# Immagini boost
boost_power_img = load("potenza.png")
boost_health_img = load("cuore.png")
boost_speed_img = load("velocità.png")
boost_invincibility_img = load("invincibilità.png")

if boost_power_img:
    boost_power_img = pygame.transform.scale(boost_power_img, (50, 50))
if boost_health_img:
    boost_health_img = pygame.transform.scale(boost_health_img, (50, 50))
if boost_speed_img:
    boost_speed_img = pygame.transform.scale(boost_speed_img, (50, 50))
if boost_invincibility_img:
    boost_invincibility_img = pygame.transform.scale(boost_invincibility_img, (50, 50))

enemy_img = load("nemico.png")
if enemy_img:
    enemy_img = pygame.transform.scale(enemy_img, (60, 60))

# --- BOSS ---
boss_image_file = "C:/Users/s14685928/Documents/GitHub/GiocoGuendouzLancioni/src/giocoguendouzlancioni/boss.png"

boss_img = load(boss_image_file)
if boss_img:
    boss_img = pygame.transform.scale(boss_img, (150, 150))
# --------------------------------------


# ─────────────────────────────────────────────────────────────
#  FUNZIONI DI GIOCO
# ─────────────────────────────────────────────────────────────

def make_player():
    return {
        'x': 100, 'y': HEIGHT // 2,
        'width': 120, 'height': 120,
        'base_speed': 5 if settings['difficulty'] == 'base' else 7,
        'speed': 5 if settings['difficulty'] == 'base' else 7,
        'health': 100, 'max_health': 100,
        'power': 1,
        'fire_rate': 300,
        'last_shot': 0,
        'power_end_time': 0,
        'speed_end_time': 0,
        'invincibility_end_time': 0
    }

def move_player(p, keys):
    if keys[pygame.K_UP] and p['y'] > 0:
        p['y'] -= p['speed']
    if keys[pygame.K_DOWN] and p['y'] < HEIGHT - p['height']:
        p['y'] += p['speed']
    if keys[pygame.K_LEFT] and p['x'] > 0:
        p['x'] -= p['speed']
    if keys[pygame.K_RIGHT] and p['x'] < WIDTH - p['width']:
        p['x'] += p['speed']

def update_player_effects(p, current_time):
    if current_time < p['power_end_time']:
        p['power'] = 3
    else:
        p['power'] = 1
       
    if current_time < p['speed_end_time']:
        p['speed'] = p['base_speed'] + 3
        p['fire_rate'] = 100
    else:
        p['speed'] = p['base_speed']
        p['fire_rate'] = 300

def is_invincible(p, current_time):
    return current_time < p['invincibility_end_time']

def shoot_player(p, keys, current_time):
    if keys[pygame.K_SPACE] and current_time - p['last_shot'] > p['fire_rate']:
        p['last_shot'] = current_time
        return make_bullet(p['x'] + p['width'], p['y'] + p['height'] // 2, p['power'])
    return None

def draw_player(surface, p, current_time):
    # Effetto invincibilità
    if is_invincible(p, current_time):
        if (current_time // 100) % 2 == 0:
            pygame.draw.rect(surface, CYAN, (p['x'] - 4, p['y'] - 4, p['width'] + 8, p['height'] + 8), 4, border_radius=10)
   
    # RIMOSSO EFFETTO LUCE VELOCITA'
   
    if jetpack:
        surface.blit(jetpack, (p['x'], p['y']))
    else:
        pygame.draw.rect(surface, BLUE, (p['x'], p['y'], p['width'], p['height']))

# --- PROIETTILI PLAYER ---
def make_bullet(x, y, power):
    return {'x': x, 'y': y, 'width': 15 * power, 'height': 8, 'speed': 12, 'power': power}

def move_bullet(b):
    b['x'] += b['speed']

def draw_bullet(surface, b):
    color = (255, 100, 0) if b['power'] > 1 else YELLOW
    pygame.draw.ellipse(surface, color, (b['x'], b['y'] - b['height'] // 2, b['width'], b['height']))
    pygame.draw.ellipse(surface, (255, 255, 150), (b['x'] + 2, b['y'] - b['height'] // 2 + 2, b['width'] - 4, b['height'] - 4))

# --- NEMICI COMUNI ---
def make_enemy():
    return {
        'x': WIDTH + random.randint(0, 100), 'y': random.randint(50, HEIGHT - 110),
        'width': 60, 'height': 60,
        'speed': 3 if settings['difficulty'] == 'base' else 5,
        'last_shot': pygame.time.get_ticks(),
        'shoot_delay': random.randint(1000, 2500),
        'health': 100, 'max_health': 100
    }

def move_enemy(e):
    e['x'] -= e['speed']

def shoot_enemy(e, current_time):
    if current_time - e['last_shot'] > e['shoot_delay']:
        e['last_shot'] = current_time
        e['shoot_delay'] = random.randint(1000, 2500)
        return make_enemy_bullet(e['x'], e['y'] + e['height'] // 2)
    return None

def draw_enemy(surface, e):
    if enemy_img:
        surface.blit(enemy_img, (e['x'], e['y']))
    else:
        pygame.draw.rect(surface, RED, (e['x'], e['y'], e['width'], e['height']))
   
    bar_width = 40; bar_height = 5; health_ratio = e['health'] / e['max_health']
    bar_x = e['x'] + (e['width'] - bar_width) // 2; bar_y = e['y'] - 10
    pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(surface, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)

def make_enemy_bullet(x, y):
    return {'x': x, 'y': y, 'width': 10, 'height': 10, 'speed': 7}

def move_enemy_bullet(eb):
    eb['x'] -= eb['speed']

def draw_enemy_bullet(surface, eb):
    pygame.draw.circle(surface, (255, 50, 50), (int(eb['x']), int(eb['y'])), 5)

# --- MISSILI NORMALI ---
def make_missile():
    return {
        'x': WIDTH + random.randint(0, 100), 'y': random.randint(50, HEIGHT - 100),
        'width': 40, 'height': 20,
        'speed': 4 if settings['difficulty'] == 'base' else 6
    }

def move_missile(m):
    m['x'] -= m['speed']

def draw_missile(surface, m):
    cy = m['y'] + m['height'] // 2
    pygame.draw.ellipse(surface, (160, 160, 170), (m['x'], m['y'] + 3, m['width'], m['height'] - 6))
    pygame.draw.polygon(surface, (255, 180, 0), [
        (m['x'] + m['width'] + 10, cy - 4), (m['x'] + m['width'] + 10, cy + 4),
        (m['x'] + m['width'] + 22, cy)
    ])

# --- BOOST ---
def make_boost(boost_type):
    return {
        'x': WIDTH + random.randint(0, 100), 'y': random.randint(100, HEIGHT - 150),
        'width': 50, 'height': 50, 'speed': 3, 'type': boost_type
    }

def move_boost(b):
    b['x'] -= b['speed']

def draw_boost(surface, b):
    img = None; color = WHITE
    if b['type'] == 'power': img = boost_power_img; color = YELLOW
    elif b['type'] == 'health': img = boost_health_img; color = GREEN
    elif b['type'] == 'speed': img = boost_speed_img; color = BLUE
    elif b['type'] == 'invincibility': img = boost_invincibility_img; color = CYAN

    if img:
        surface.blit(img, (b['x'], b['y']))
    else:
        pygame.draw.circle(surface, color, (int(b['x'] + 25), int(b['y'] + 25)), 25)
        if b['type'] == 'invincibility':
            points = []; cx, cy = b['x'] + 25, b['y'] + 25
            for i in range(5):
                angle_out = math.radians(i * 72 - 90); angle_in = math.radians(i * 72 - 90 + 36)
                points.append((cx + math.cos(angle_out) * 15, cy + math.sin(angle_out) * 15))
                points.append((cx + math.cos(angle_in) * 7, cy + math.sin(angle_in) * 7))
            pygame.draw.polygon(surface, WHITE, points)

# ───────────── HUD POTENZIAMENTI ─────────────

def draw_boost_counter(surface, player, font, current_time):
    panel_x = WIDTH - 200
    panel_y = 10
    padding = 5

    panel = pygame.Surface((190, 130), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 140))
    surface.blit(panel, (panel_x - padding, panel_y - padding))

    boost_data = [
        ('power',  boost_power_img,  YELLOW, "POW",  'power_end_time'),
        ('speed',  boost_speed_img,  BLUE,   "VEL",  'speed_end_time'),
        ('invincibility', boost_invincibility_img, CYAN, "INV",  'invincibility_end_time'),
        ('health', boost_health_img, GREEN,  "VITA", None)
    ]

    for i, (btype, img, color, label, timer_key) in enumerate(boost_data):
        row_y = panel_y + i * 30
       
        if img:
            small = pygame.transform.scale(img, (24, 24))
            surface.blit(small, (panel_x, row_y))
        else:
            pygame.draw.circle(surface, color, (panel_x + 12, row_y + 12), 10)

        if btype == 'health':
            txt = font.render(f"{label}: PRONTO", True, color)
        else:
            end_time = player[timer_key]
            if current_time < end_time:
                seconds_left = (end_time - current_time) / 1000.0
                txt = font.render(f"{label}: {seconds_left:.1f}s", True, color)
            else:
                txt = font.render(f"{label}: OFF", True, (80, 80, 80))
           
        surface.blit(txt, (panel_x + 30, row_y + 3))

# ─────────────────── BOSS ───────────────────

def make_boss(wave_number):
    w, h = 150, 150
    base_hp = 1000
    hp_bonus = (wave_number - 1) * 400
    damage = 15 + (wave_number - 1) * 3
    missile_speed = 5.0 + (wave_number - 1) * 0.5
    shoot_delay = max(400, 900 - (wave_number * 100))

    return {
        'x': WIDTH + 50,
        'y': HEIGHT // 2 - h//2,
        'width': w, 'height': h,
        'speed': 2,
        'health': base_hp + hp_bonus,
        'max_health': base_hp + hp_bonus,
        'damage': damage,
        'missile_speed': missile_speed,
        'last_shot': pygame.time.get_ticks(),
        'shoot_delay': shoot_delay,
        'direction': 1,
        'entering': True
    }

def move_boss(b):
    if b['entering']:
        if b['x'] > WIDTH - b['width'] - 50:
            b['x'] -= 3
        else:
            b['entering'] = False
   
    if not b['entering']:
        b['y'] += b['speed'] * b['direction']
        if b['y'] <= 20: b['direction'] = 1
        elif b['y'] + b['height'] >= HEIGHT - 20: b['direction'] = -1

def draw_boss(surface, b):
    if boss_img:
        surface.blit(boss_img, (b['x'], b['y']))
    else:
        pygame.draw.rect(surface, BLACK, (b['x'], b['y'], b['width'], b['height']))
        pygame.draw.rect(surface, PURPLE, (b['x'], b['y'], b['width'], b['height']), 4)
   
    bar_width = 120; bar_height = 12; health_ratio = b['health'] / b['max_health']
    bar_x = b['x'] + (b['width'] - bar_width) // 2; bar_y = b['y'] - 20
    pygame.draw.rect(surface, BLACK, (bar_x-2, bar_y-2, bar_width+4, bar_height+4))
    pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(surface, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

# --- RAZZI BOSS ---
def make_boss_missile(x, y, player_rect, speed, damage):
    tx, ty = player_rect.centerx, player_rect.centery
    dx = tx - x
    dy = ty - y
    dist = math.hypot(dx, dy)
    if dist != 0:
        dx /= dist
        dy /= dist
    else:
        dx = -1
    return {
        'x': x, 'y': y,
        'width': 30, 'height': 15,
        'dx': dx, 'dy': dy,
        'speed': speed,
        'damage': damage
    }

def move_boss_missile(m):
    m['x'] += m['dx'] * m['speed']
    m['y'] += m['dy'] * m['speed']

def draw_boss_missile(surface, m):
    pygame.draw.ellipse(surface, (150, 0, 150), (m['x'], m['y'], m['width'], m['height']))
    pygame.draw.circle(surface, (255, 100, 255), (int(m['x'] - m['dx']*10), int(m['y'] + m['height']//2)), 5)

# ───────────── MENU ─────────────

def main():
    menu()

def menu():
    clock = pygame.time.Clock()
    t = 0
   
    # Font più "gioco" (più grande e spesso)
    title_font = pygame.font.Font(None, 120)
    button_font = pygame.font.Font(None, 50)
   
    title_text = "MissionOne"
   
    button_enter = pygame.Rect(WIDTH//2 - 150, HEIGHT - 150, 300, 70)
    button_settings = pygame.Rect(WIDTH - 90, 20, 70, 70)

    jetpack_menu = load("jetpack.png")
    if jetpack_menu:
        jetpack_menu = pygame.transform.scale(jetpack_menu, (350, 350))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: start_game()
            if event.type == pygame.MOUSEBUTTONDOWN: click = True

        screen.blit(background, (0, 0)) if background else screen.fill(GRAY)

        if jetpack_menu:
            offset = math.sin(t / 20) * 10
            screen.blit(jetpack_menu, (WIDTH//2 - jetpack_menu.get_width()//2, HEIGHT//2 - jetpack_menu.get_height()//2 + offset))

        # --- DISEGNO TITOLO ROSA ---
        title_surf = title_font.render(title_text, True, PINK)
        title_x = WIDTH//2 - title_surf.get_width()//2
        title_y = 80 # Alzato leggermente per il font più grande
       
        # Ombra
        shadow_surf = title_font.render(title_text, True, BLACK)
        screen.blit(shadow_surf, (title_x + 4, title_y + 4))
       
        # Testo
        screen.blit(title_surf, (title_x, title_y))

        # --- BOTTONE ENTER VIOLA ---
        hover_enter = button_enter.collidepoint(mouse_pos)
       
        if hover_enter:
            color = PURPLE
            border = (100, 0, 150)
            text_color = WHITE
        else:
            color = (200, 200, 200)
            border = (150, 150, 150)
            text_color = BLACK
           
        pygame.draw.rect(screen, color, button_enter, border_radius=15)
        pygame.draw.rect(screen, border, button_enter, 4, border_radius=15)
       
        txt = button_font.render("ENTER", True, text_color)
        screen.blit(txt, (button_enter.centerx - txt.get_width()//2, button_enter.centery - txt.get_height()//2))

        # --- ICONA IMPOSTAZIONI ROSA ---
        hover_settings = button_settings.collidepoint(mouse_pos)
        if settings_icon:
            if hover_settings:
                # Evidenza gialla se hover
                colored_icon = settings_icon.copy()
                colored_icon.fill((255, 255, 0, 150), special_flags=pygame.BLEND_RGBA_ADD)
                screen.blit(colored_icon, button_settings)
                pygame.draw.rect(screen, YELLOW, (button_settings.x - 2, button_settings.y - 2, 74, 74), 3, border_radius=10)
            else:
                # Colora di Rosa (come il titolo) se normale
                pink_icon = settings_icon.copy()
                # Applichiamo un layer rosa sopra l'icona bianca
                pink_icon.fill(PINK, special_flags=pygame.BLEND_RGBA_MULT)
                # La rendiamo più luminosa per vedersi bene
                bright_icon = settings_icon.copy()
                bright_icon.fill(PINK, special_flags=pygame.BLEND_RGBA_ADD)
                screen.blit(bright_icon, button_settings)
       
        if click:
            if hover_enter: start_game()
            if hover_settings: settings_menu()

        pygame.display.flip()
        clock.tick(60)
        t += 1


def settings_menu():
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 80); label_font = pygame.font.Font(None, 45); button_font = pygame.font.Font(None, 40)
    slider_rect = pygame.Rect(200, 200, 400, 10); slider_handle = pygame.Rect(0, 0, 20, 30)
    dragging = False
    button_base = pygame.Rect(200, 320, 180, 60); button_avanzato = pygame.Rect(420, 320, 180, 60)
    button_back = pygame.Rect(WIDTH//2 - 100, HEIGHT - 100, 200, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos(); click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: click = True
            if event.type == pygame.MOUSEBUTTONUP: dragging = False

        screen.blit(background, (0, 0)) if background else screen.fill(GRAY)
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(200); overlay.fill(GRAY); screen.blit(overlay, (0, 0))

        # MODIFICA: Titolo Impostazioni VIOLA
        title = title_font.render("IMPOSTAZIONI", True, PURPLE); screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
       
        # MODIFICA: Label Volume VIOLA
        volume_label = label_font.render("Volume", True, PURPLE); screen.blit(volume_label, (200, 150))
        volume_value = label_font.render(f"{settings['volume']}%", True, PURPLE); screen.blit(volume_value, (620, 150))

        pygame.draw.rect(screen, WHITE, slider_rect, border_radius=5)
        slider_handle.centerx = slider_rect.x + (settings['volume'] / 100) * slider_rect.width
        slider_handle.centery = slider_rect.centery
        if slider_handle.collidepoint(mouse_pos) and click: dragging = True
        if dragging:
            new_x = max(slider_rect.x, min(mouse_pos[0], slider_rect.right))
            settings['volume'] = int(((new_x - slider_rect.x) / slider_rect.width) * 100)
            slider_handle.centerx = new_x
        pygame.draw.rect(screen, PURPLE, slider_handle, border_radius=5) # Slider handle viola

        # MODIFICA: Label Difficoltà VIOLA
        diff_label = label_font.render("Difficoltà", True, PURPLE); screen.blit(diff_label, (200, 270))
       
        is_base = settings['difficulty'] == 'base'
        color_base = GREEN if is_base else (80, 80, 80)
        pygame.draw.rect(screen, color_base, button_base, border_radius=10)
        pygame.draw.rect(screen, GREEN if is_base else WHITE, button_base, 4, border_radius=10)
        txt_base = button_font.render("BASE", True, WHITE)
        screen.blit(txt_base, (button_base.centerx - txt_base.get_width()//2, button_base.centery - txt_base.get_height()//2))

        is_avanzato = settings['difficulty'] == 'avanzato'
        color_avanzato = RED if is_avanzato else (80, 80, 80)
        pygame.draw.rect(screen, color_avanzato, button_avanzato, border_radius=10)
        pygame.draw.rect(screen, RED if is_avanzato else WHITE, button_avanzato, 4, border_radius=10)
        txt_avanzato = button_font.render("AVANZATO", True, WHITE)
        screen.blit(txt_avanzato, (button_avanzato.centerx - txt_avanzato.get_width()//2, button_avanzato.centery - txt_avanzato.get_height()//2))

        if click:
            if button_base.collidepoint(mouse_pos): settings['difficulty'] = 'base'
            if button_avanzato.collidepoint(mouse_pos): settings['difficulty'] = 'avanzato'

        hover_back = button_back.collidepoint(mouse_pos)
        # MODIFICA: Colore bottone Indietro
        back_color = PURPLE if hover_back else WHITE
        pygame.draw.rect(screen, back_color, button_back, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_back, 3, border_radius=10)
        txt_back = button_font.render("INDIETRO", True, WHITE if hover_back else BLACK)
        screen.blit(txt_back, (button_back.centerx - txt_back.get_width()//2, button_back.centery - txt_back.get_height()//2))
        if hover_back and click: return

        pygame.display.flip()
        clock.tick(60)


# ─────────────────── LOOP DI GIOCO ───────────────────

def start_game():
    clock = pygame.time.Clock()
    player = make_player()
    bullets, enemies, enemy_bullets, missiles, boosts = [], [], [], [], []
   
    boss = None
    boss_missiles = []
    wave_number = 1
    next_boss_score = 3000
    warning_active = False
    warning_start_time = 0
   
    score = 0
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 28)
    big_font = pygame.font.Font(None, 100)

    enemy_spawn_timer, missile_spawn_timer, boost_spawn_timer, damage_flash = 0, 0, 0, 0

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return

        keys = pygame.key.get_pressed()

        # --- LOGICA ---
       
        if score >= next_boss_score and boss is None and not warning_active:
            warning_active = True
            warning_start_time = current_time
            next_boss_score += 3000

        if warning_active:
            if current_time - warning_start_time > 3000:
                warning_active = False
                boss = make_boss(wave_number)
                wave_number += 1
                enemies.clear(); enemy_bullets.clear(); missiles.clear()

        update_player_effects(player, current_time)
        move_player(player, keys)
        bullet = shoot_player(player, keys, current_time)
        if bullet: bullets.append(bullet)

        if not warning_active and boss is None:
            enemy_spawn_timer += 1
            if enemy_spawn_timer > (100 if settings['difficulty'] == 'base' else 70):
                enemies.append(make_enemy()); enemy_spawn_timer = 0

            missile_spawn_timer += 1
            if missile_spawn_timer > (180 if settings['difficulty'] == 'base' else 130):
                missiles.append(make_missile()); missile_spawn_timer = 0

            boost_spawn_timer += 1
            if boost_spawn_timer > 250:
                boosts.append(make_boost(random.choice(['power', 'health', 'speed', 'invincibility'])))
                boost_spawn_timer = 0

        for b in bullets[:]:
            move_bullet(b)
            if b['x'] > WIDTH: bullets.remove(b)

        for e in enemies[:]:
            move_enemy(e)
            eb = shoot_enemy(e, current_time)
            if eb: enemy_bullets.append(eb)
            if e['x'] < -e['width']: enemies.remove(e)

        for eb in enemy_bullets[:]:
            move_enemy_bullet(eb)
            if eb['x'] < 0: enemy_bullets.remove(eb)

        for m in missiles[:]:
            move_missile(m)
            if m['x'] < -m['width'] - 20: missiles.remove(m)

        for b in boosts[:]:
            move_boost(b)
            if b['x'] < -b['width']: boosts.remove(b)

        if boss:
            move_boss(boss)
            if not boss['entering'] and current_time - boss['last_shot'] > boss['shoot_delay']:
                boss['last_shot'] = current_time
                player_rect = pygame.Rect(player['x'], player['y'], player['width'], player['height'])
                new_missile = make_boss_missile(
                    boss['x'],
                    boss['y'] + boss['height']//2,
                    player_rect,
                    boss['missile_speed'],
                    boss['damage']
                )
                boss_missiles.append(new_missile)
           
            for hm in boss_missiles[:]:
                move_boss_missile(hm)
                if hm['x'] < -50 or hm['x'] > WIDTH + 50 or hm['y'] < -50 or hm['y'] > HEIGHT + 50:
                    boss_missiles.remove(hm)

        player_rect = pygame.Rect(player['x'] + 10, player['y'] + 10, player['width'] - 20, player['height'] - 20)
       
        if boss:
            for b in bullets[:]:
                b_rect = pygame.Rect(b['x'], b['y'], b['width'], b['height'])
                boss_rect = pygame.Rect(boss['x'], boss['y'], boss['width'], boss['height'])
                if b_rect.colliderect(boss_rect):
                    if b in bullets: bullets.remove(b)
                    damage = 100 if b['power'] > 1 else 50
                    boss['health'] -= damage
                    if boss['health'] <= 0:
                        score += 500
                        boss = None
                        boss_missiles.clear()
       
        for b in bullets[:]:
            for e in enemies[:]:
                if (b['x'] < e['x'] + e['width'] and b['x'] + b['width'] > e['x'] and
                    b['y'] < e['y'] + e['height'] and b['y'] + b['height'] > e['y']):
                    if b in bullets: bullets.remove(b)
                    damage = 100 if b['power'] > 1 else 50
                    e['health'] -= damage
                    if e['health'] <= 0:
                        if e in enemies: enemies.remove(e)
                        score += 10

        if not is_invincible(player, current_time):
            for eb in enemy_bullets[:]:
                eb_rect = pygame.Rect(eb['x'] - 5, eb['y'] - 5, 10, 10)
                if player_rect.colliderect(eb_rect):
                    if eb in enemy_bullets: enemy_bullets.remove(eb)
                    player['health'] -= 10; damage_flash = 12

            for m in missiles[:]:
                m_rect = pygame.Rect(m['x'], m['y'], m['width'], m['height'])
                if player_rect.colliderect(m_rect):
                    if m in missiles: missiles.remove(m)
                    player['health'] -= 20; damage_flash = 20
           
            for hm in boss_missiles[:]:
                hm_rect = pygame.Rect(hm['x'], hm['y'], hm['width'], hm['height'])
                if player_rect.colliderect(hm_rect):
                    if hm in boss_missiles: boss_missiles.remove(hm)
                    player['health'] -= hm['damage']; damage_flash = 15

        for b in boosts[:]:
            b_rect = pygame.Rect(b['x'], b['y'], b['width'], b['height'])
            if player_rect.colliderect(b_rect):
                if b in boosts: boosts.remove(b)
                duration = 7000
                if b['type'] == 'power': player['power_end_time'] = current_time + duration
                elif b['type'] == 'speed': player['speed_end_time'] = current_time + duration
                elif b['type'] == 'invincibility': player['invincibility_end_time'] = current_time + duration
                elif b['type'] == 'health': player['health'] = min(player['health'] + 30, player['max_health'])
                score += 5

        score += 1
        player['health'] = max(player['health'], 0)
        if player['health'] <= 0: running = False

        # --- DISEGNO ---
        if background: screen.blit(background, (0, 0))
        else: screen.fill(GRAY)

        if damage_flash > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = int(120 * (damage_flash / 20))
            flash_surf.fill((220, 0, 0, alpha))
            screen.blit(flash_surf, (0, 0))
            damage_flash -= 1

        for b in bullets: draw_bullet(screen, b)
        for e in enemies: draw_enemy(screen, e)
        for eb in enemy_bullets: draw_enemy_bullet(screen, eb)
        for m in missiles: draw_missile(screen, m)
        for b in boosts: draw_boost(screen, b)
       
        if boss:
            draw_boss(screen, boss)
            for hm in boss_missiles: draw_boss_missile(screen, hm)

        draw_player(screen, player, current_time)

        # HUD Base
        bar_width = 250; bar_height = 25; bar_x, bar_y = 20, 20
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        health_w = int((player['health'] / player['max_health']) * bar_width)
        health_color = GREEN if player['health'] > 50 else YELLOW if player['health'] > 25 else RED
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_w, bar_height), border_radius=5)
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 3, border_radius=5)
        health_text = font.render(f"VITA: {player['health']}", True, WHITE)
        screen.blit(health_text, (bar_x + bar_width + 10, bar_y))

        pow_text = font.render(f"POW: x{player['power']}", True, YELLOW)
        screen.blit(pow_text, (20, 55))

        score_text = font.render(f"SCORE: {score}", True, YELLOW)
        screen.blit(score_text, (20, 85))

        hint = small_font.render("← ↑ ↓ → Muovi  |  SPAZIO Spara  |  ESC Menu", True, (180, 180, 180))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))

        # HUD Potenziamenti
        draw_boost_counter(screen, player, small_font, current_time)

        if warning_active:
            warn_text = big_font.render(f"ONDATA {wave_number}", True, RED)
            if (current_time // 200) % 2 == 0:
                text_rect = warn_text.get_rect(center=(WIDTH//2, HEIGHT//2))
                screen.blit(warn_text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    game_over_screen(score)


# ───────────── GAME OVER ─────────────

def game_over_screen(score):
    clock = pygame.time.Clock()
    font_big = pygame.font.Font(None, 100); font_small = pygame.font.Font(None, 50); button_font = pygame.font.Font(None, 40)
    button_retry = pygame.Rect(WIDTH//2 - 150, 350, 140, 60); button_menu = pygame.Rect(WIDTH//2 + 10, 350, 140, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos(); click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: click = True

        screen.fill(BLACK)
        go = font_big.render("GAME OVER", True, RED)
        screen.blit(go, (WIDTH // 2 - go.get_width() // 2, 200))
        sc = font_small.render(f"PUNTEGGIO: {score}", True, YELLOW)
        screen.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 280))

        # MODIFICA: Bottoni Game Over viola quando hover
        hover_retry = button_retry.collidepoint(mouse_pos)
        retry_color = PURPLE if hover_retry else WHITE
        pygame.draw.rect(screen, retry_color, button_retry, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_retry, 3, border_radius=10)
        txt_retry = button_font.render("RIPROVA", True, WHITE if hover_retry else BLACK)
        screen.blit(txt_retry, (button_retry.centerx - txt_retry.get_width()//2, button_retry.centery - txt_retry.get_height()//2))

        hover_menu = button_menu.collidepoint(mouse_pos)
        menu_color = PURPLE if hover_menu else WHITE
        pygame.draw.rect(screen, menu_color, button_menu, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_menu, 3, border_radius=10)
        txt_menu = button_font.render("MENU", True, WHITE if hover_menu else BLACK)
        screen.blit(txt_menu, (button_menu.centerx - txt_menu.get_width()//2, button_menu.centery - txt_menu.get_height()//2))

        if click:
            if hover_retry: start_game(); return
            if hover_menu: return

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

