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
    jetpack = pygame.transform.scale(jetpack, (350, 350))  # Ingrandito

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
        
        if jetpack:
            offset = math.sin(t / 20) * 10
            screen.blit(jetpack, (WIDTH//2 - jetpack.get_width()//2,
                                  HEIGHT//2 - jetpack.get_height()//2 + offset))
        
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

# Classi per il gioco
class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.width = 80
        self.height = 80
        self.vel_y = 0
        self.speed_vertical = 5 if settings['difficulty'] == 'base' else 7
        self.speed_horizontal = 2  # Velocità avanzamento automatico
        self.scroll_offset = 0  # Per il movimento automatico
        self.health = 100
        self.max_health = 100
        self.power = 1
        self.fire_rate = 500
        self.last_shot = 0
        
    def move(self, keys):
        # Movimento verticale con frecce
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed_vertical
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.speed_vertical
        
        # Movimento orizzontale automatico
        self.scroll_offset += self.speed_horizontal
            
    def shoot(self, current_time):
        if current_time - self.last_shot > self.fire_rate:
            self.last_shot = current_time
            return Bullet(self.x + self.width, self.y + self.height // 2, self.power)
        return None
    
    def draw(self, screen):
        if jetpack:
            screen.blit(jetpack, (self.x, self.y))
        else:
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

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
        
    def draw(self, screen):
        pygame.draw.ellipse(screen, YELLOW, (self.x, self.y - self.height//2, self.width, self.height))
        # Effetto brillante
        pygame.draw.ellipse(screen, (255, 255, 150), (self.x + 2, self.y - self.height//2 + 2, self.width - 4, self.height - 4))

class Enemy:
    def __init__(self, scroll_offset):
        self.x = WIDTH + scroll_offset
        self.y = random.randint(50, HEIGHT - 110)
        self.width = 60
        self.height = 60
        self.speed = 3 if settings['difficulty'] == 'base' else 5
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1000, 2000)
        
    def move(self):
        self.x -= self.speed
        
    def shoot(self, current_time):
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            self.shoot_delay = random.randint(1000, 2000)
            return EnemyBullet(self.x, self.y + self.height // 2)
        return None
    
    def draw(self, screen):
        if enemy_img:
            screen.blit(enemy_img, (self.x, self.y))
        else:
            # Fallback: disegna un razzo nemico rosso
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
            pygame.draw.polygon(screen, (150, 0, 0), [
                (self.x, self.y + self.height // 2),
                (self.x + self.width, self.y + 5),
                (self.x + self.width, self.y + self.height - 5)
            ])
            # Finestra
            pygame.draw.circle(screen, (100, 100, 255), (int(self.x + 15), int(self.y + self.height // 2)), 8)

class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.speed = 7
        
    def move(self):
        self.x -= self.speed
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), 5)
        pygame.draw.circle(screen, (255, 150, 150), (int(self.x), int(self.y)), 3)

class Missile:
    def __init__(self, scroll_offset):
        self.x = WIDTH + scroll_offset
        self.y = random.randint(50, HEIGHT - 100)
        self.width = 40
        self.height = 20
        self.speed = 4 if settings['difficulty'] == 'base' else 6
        
    def move(self):
        self.x -= self.speed
        
    def draw(self, screen):
        # Corpo missile
        pygame.draw.rect(screen, (255, 100, 0), (self.x, self.y, self.width, self.height))
        # Punta
        pygame.draw.polygon(screen, (200, 50, 0), [
            (self.x + self.width, self.y + self.height // 2),
            (self.x + self.width + 15, self.y),
            (self.x + self.width + 15, self.y + self.height)
        ])
        # Fiamma
        pygame.draw.polygon(screen, (255, 200, 0), [
            (self.x, self.y + 5),
            (self.x - 10, self.y + self.height // 2),
            (self.x, self.y + self.height - 5)
        ])

class Boost:
    def __init__(self, boost_type, scroll_offset):
        self.x = WIDTH + scroll_offset
        self.y = random.randint(100, HEIGHT - 150)
        self.width = 50
        self.height = 50
        self.speed = 3
        self.type = boost_type
        
    def move(self):
        self.x -= self.speed
        
    def draw(self, screen):
        if self.type == 'power' and boost_power_img:
            screen.blit(boost_power_img, (self.x, self.y))
        elif self.type == 'health' and boost_health_img:
            screen.blit(boost_health_img, (self.x, self.y))
        elif self.type == 'speed' and boost_speed_img:
            screen.blit(boost_speed_img, (self.x, self.y))
        else:
            # Fallback: disegna forme colorate
            if self.type == 'power':
                pygame.draw.circle(screen, YELLOW, (int(self.x + 25), int(self.y + 25)), 25)
                pygame.draw.circle(screen, (255, 180, 0), (int(self.x + 25), int(self.y + 25)), 18)
                # Simbolo fulmine
                pygame.draw.polygon(screen, WHITE, [
                    (self.x + 25, self.y + 10),
                    (self.x + 20, self.y + 25),
                    (self.x + 28, self.y + 25),
                    (self.x + 20, self.y + 40)
                ])
            elif self.type == 'health':
                pygame.draw.circle(screen, GREEN, (int(self.x + 25), int(self.y + 25)), 25)
                # Croce
                pygame.draw.rect(screen, WHITE, (self.x + 10, self.y + 20, 30, 10))
                pygame.draw.rect(screen, WHITE, (self.x + 20, self.y + 10, 10, 30))
            elif self.type == 'speed':
                pygame.draw.circle(screen, BLUE, (int(self.x + 25), int(self.y + 25)), 25)
                # Frecce
                pygame.draw.polygon(screen, WHITE, [
                    (self.x + 30, self.y + 15),
                    (self.x + 40, self.y + 25),
                    (self.x + 30, self.y + 35)
                ])
                pygame.draw.polygon(screen, WHITE, [
                    (self.x + 20, self.y + 15),
                    (self.x + 30, self.y + 25),
                    (self.x + 20, self.y + 35)
                ])

def start_game():
    clock = pygame.time.Clock()
    
    player = Player()
    bullets = []
    enemies = []
    enemy_bullets = []
    missiles = []
    boosts = []
    
    score = 0
    font = pygame.font.Font(None, 36)
    
    enemy_spawn_timer = 0
    missile_spawn_timer = 0
    boost_spawn_timer = 0
    
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
        
        # Movimento giocatore (automatico in avanti + controllo verticale)
        player.move(keys)
        
        # Sparo automatico continuo
        bullet = player.shoot(current_time)
        if bullet:
            bullets.append(bullet)
        
        # Spawn nemici
        enemy_spawn_timer += 1
        if enemy_spawn_timer > (100 if settings['difficulty'] == 'base' else 70):
            enemies.append(Enemy(player.scroll_offset))
            enemy_spawn_timer = 0
        
        # Spawn missili
        missile_spawn_timer += 1
        if missile_spawn_timer > (180 if settings['difficulty'] == 'base' else 130):
            missiles.append(Missile(player.scroll_offset))
            missile_spawn_timer = 0
        
        # Spawn boost
        boost_spawn_timer += 1
        if boost_spawn_timer > 250:
            boost_type = random.choice(['power', 'health', 'speed'])
            boosts.append(Boost(boost_type, player.scroll_offset))
            boost_spawn_timer = 0
        
        # Muovi proiettili giocatore
        for bullet in bullets[:]:
            bullet.move()
            if bullet.x > WIDTH:
                bullets.remove(bullet)
        
        # Muovi nemici e falli sparare
        for enemy in enemies[:]:
            enemy.move()
            enemy_bullet = enemy.shoot(current_time)
            if enemy_bullet:
                enemy_bullets.append(enemy_bullet)
            if enemy.x < -enemy.width:
                enemies.remove(enemy)
        
        # Muovi proiettili nemici
        for eb in enemy_bullets[:]:
            eb.move()
            if eb.x < 0:
                enemy_bullets.remove(eb)
        
        # Muovi missili
        for missile in missiles[:]:
            missile.move()
            if missile.x < -missile.width:
                missiles.remove(missile)
        
        # Muovi boost
        for boost in boosts[:]:
            boost.move()
            if boost.x < -boost.width:
                boosts.remove(boost)
        
        # Collisioni proiettili giocatore con nemici
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
        
        # Collisioni proiettili nemici con giocatore
        for eb in enemy_bullets[:]:
            if (eb.x < player.x + player.width and
                eb.x + eb.width > player.x and
                eb.y < player.y + player.height and
                eb.y + eb.height > player.y):
                if eb in enemy_bullets:
                    enemy_bullets.remove(eb)
                player.health -= 10
        
        # Collisioni missili con giocatore
        for missile in missiles[:]:
            if (missile.x < player.x + player.width and
                missile.x + missile.width > player.x and
                missile.y < player.y + player.height and
                missile.y + missile.height > player.y):
                if missile in missiles:
                    missiles.remove(missile)
                player.health -= 20
        
        # Collisioni boost con giocatore
        for boost in boosts[:]:
            if (boost.x < player.x + player.width and
                boost.x + boost.width > player.x and
                boost.y < player.y + player.height and
                boost.y + boost.height > player.y):
                if boost in boosts:
                    boosts.remove(boost)
                    if boost.type == 'power':
                        player.power = min(player.power + 1, 3)
                        score += 5
                    elif boost.type == 'health':
                        player.health = min(player.health + 30, player.max_health)
                        score += 5
                    elif boost.type == 'speed':
                        player.fire_rate = max(player.fire_rate - 100, 150)
                        score += 5
        
        # Incrementa punteggio per sopravvivenza
        score += 1
        
        # Game over
        if player.health <= 0:
            running = False
        
        # Disegna tutto
        screen.blit(background, (0, 0)) if background else screen.fill(GRAY)
        
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
        
        # Barra vita in alto
        bar_width = 250
        bar_height = 25
        bar_x = 20
        bar_y = 20
        
        # Sfondo barra
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        # Barra vita
        health_width = int((player.health / player.max_health) * bar_width)
        health_color = GREEN if player.health > 50 else YELLOW if player.health > 25 else RED
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height), border_radius=5)
        # Bordo
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 3, border_radius=5)
        
        # Testo vita
        health_text = font.render(f"VITA: {player.health}", True, WHITE)
        screen.blit(health_text, (bar_x + bar_width + 15, bar_y - 2))
        
        # Punteggio
        score_text = font.render(f"SCORE: {score}", True, YELLOW)
        screen.blit(score_text, (WIDTH - 220, 20))
        
        # Info power
        power_text = font.render(f"POW: x{player.power}", True, YELLOW)
        screen.blit(power_text, (20, 60))
        
        pygame.display.flip()
        clock.tick(60)
    
    # Game Over
    game_over_screen(score)

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
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 200))
        
        score_text = font_small.render(f"PUNTEGGIO: {score}", True, YELLOW)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 320))
        
        restart_text = font_small.render("PREMI ENTER PER TORNARE AL MENU", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 400))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()