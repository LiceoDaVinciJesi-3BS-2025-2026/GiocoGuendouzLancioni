import pygame
import sys
import os
import math

pygame.init()

# Dimensioni finestra
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jetpack Joyride - Menu")

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
GRAY = (40, 40, 40)

# Caricamento immagini semplificato
def load(path):
    return pygame.image.load(path).convert_alpha() if os.path.exists(path) else None

# Background scalato
bg = load("background - Copia.jpg")
background = pygame.transform.scale(bg, (WIDTH, HEIGHT)) if bg else None

# Jetpack
jetpack = load("jetpack.png")

def main():
    menu()

def menu():
    clock = pygame.time.Clock()
    t = 0

    # Font
    title_font = pygame.font.Font(None, 110)
    button_font = pygame.font.Font(None, 50)

    # Titolo
    title = title_font.render("JETPACK JOYRIDE", True, YELLOW)
    shadow = title_font.render("JETPACK JOYRIDE", True, BLACK)

    # Pulsante ENTER
    button = pygame.Rect(WIDTH//2 - 150, HEIGHT - 150, 300, 70)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                start_game()

        # Sfondo
        screen.blit(background, (0, 0)) if background else screen.fill(GRAY)

        # Jetpack oscillante
        if jetpack:
            offset = math.sin(t / 20) * 10
            screen.blit(jetpack, (WIDTH//2 - jetpack.get_width()//2,
                                  HEIGHT//2 - jetpack.get_height()//2 + offset))

        # Titolo con ombra
        x = WIDTH//2 - title.get_width()//2
        screen.blit(shadow, (x + 4, 64))
        screen.blit(title, (x, 60))

        # Pulsante ENTER
        hover = button.collidepoint(mouse_pos)
        color = (255, 255, 255) if hover else (200, 200, 200)
        border = (255, 220, 0) if hover else (150, 150, 150)

        pygame.draw.rect(screen, color, button, border_radius=15)
        pygame.draw.rect(screen, border, button, 4, border_radius=15)

        # Testo ENTER
        txt = button_font.render("ENTER", True, BLACK)
        screen.blit(txt, (button.centerx - txt.get_width()//2,
                          button.centery - txt.get_height()//2))

        # Click del mouse
        if hover and click:
            start_game()

        pygame.display.flip()
        clock.tick(60)
        t += 1

def start_game():
    print("Inizio del gioco...")

if __name__ == "__main__":
    main()
