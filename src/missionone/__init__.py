# ───────────── SEZIONE 1: IMPORTAZIONE DELLE LIBRERIE ─────────────

import math
import os
import random
import sys
from importlib.resources import files

import pygame

# ───────────── SEZIONE 2: INIZIALIZZAZIONE DI PYGAME ─────────────
# Inizializza tutti i moduli di pygame necessari.
pygame.init()
# Inizializza il modulo specifico per l'audio.
pygame.mixer.init()

# ───────────── SEZIONE 3: COSTANTI GLOBALI (CONFIGURAZIONE) ─────────────
# Imposta la larghezza della finestra di gioco a 800 pixel.
WIDTH = 800
# Imposta l'altezza della finestra di gioco a 600 pixel.
HEIGHT = 600
# Crea una tupla che contiene le dimensioni della finestra.
DIMENSIONS = (WIDTH, HEIGHT)
# Crea la finestra di gioco visualizzabile con le dimensioni definite.
screen = pygame.display.set_mode(DIMENSIONS)
# Imposta il titolo che appare sulla barra della finestra.
pygame.display.set_caption("MissionOne - Boss Edition")

# ───────────── SEZIONE 4: DEFINIZIONE DEI COLORI ─────────────
# Definisce il colore Bianco con i valori RGB massimi.
WHITE = (255, 255, 255)
# Definisce il colore Nero con i valori RGB minimi.
BLACK = (0, 0, 0)
# Definisce il colore Giallo.
YELLOW = (255, 220, 0)
# Definisce il colore Grigio scuro.
GRAY = (40, 40, 40)
# Definisce il colore Blu.
BLUE = (70, 130, 220)
# Definisce il colore Verde.
GREEN = (100, 200, 100)
# Definisce il colore Rosso.
RED = (220, 80, 80)
# Definisce il colore Ciano (azzurro).
CYAN = (0, 220, 220)
# Definisce il colore Viola.
PURPLE = (150, 50, 200)
# Definisce il colore Rosa.
PINK = (255, 100, 180)
# Definisce il colore Lilla.
LILAC = (200, 150, 255)

# ───────────── SEZIONE 5: IMPOSTAZIONI DI GIOCO ─────────────
# Crea il dizionario per le impostazioni.
settings = {
    # Imposta il volume iniziale al 50%.
    "volume": 50,
    # Imposta la difficoltà iniziale su 'base'.
    "difficulty": "base",
}

# Variabile globale per memorizzare il punteggio più alto.
HIGH_SCORE = 0

# ───────────── SEZIONE 6: GESTIONE AUDIO (MUSICA) ─────────────
# Stringa con il percorso completo del file musicale del menu.
MENU_MUSIC_FILE = files("missionone") / "the_mountain-space-133254.mp3"
# Stringa con il percorso completo del file musicale di gioco.
GAME_MUSIC_FILE = (
    files("missionone") / "momotmusic-speed-of-light-447363.mp3"
)
# Variabile globale per il suono del click, inizialmente nulla.
click_sound = None


# Definisce la funzione per avviare la musica.
def play_music(filename, loop=True):
    # Controlla se il file musicale esiste sul disco.
    if os.path.exists(filename):
        # Inizia un blocco try per gestire eventuali errori.
        try:
            # Carica il file musicale nella memoria.
            pygame.mixer.music.load(filename)
            # Imposta il volume basandosi sulle impostazioni salvate.
            pygame.mixer.music.set_volume(settings["volume"] / 100.0)
            # Avvia la riproduzione della musica.
            pygame.mixer.music.play(-1 if loop else 0)
        # Cattura eventuali errori di pygame.
        except pygame.error as e:
            # Stampa un messaggio di errore nella console.
            print(f"Errore audio con {filename}: {e}")
    # Se il file non viene trovato.
    else:
        # Stampa un messaggio di avviso.
        print(f"File musicale non trovato: {filename}")


# ───────────── SEZIONE 7: CARICAMENTO RISORSE GRAFICHE ─────────────
# Definisce la funzione helper per caricare le immagini.
def load(path):
    # Controlla se il percorso del file esiste.
    if os.path.exists(path):
        # Prova a eseguire il caricamento.
        try:
            # Carica l'immagine e applica la trasparenza alpha.
            return pygame.image.load(path).convert_alpha()
        # Se si verifica un errore durante il caricamento.
        except pygame.error:
            # Restituisce None per indicare il fallimento.
            return None
    # Se il percorso non esiste.
    return None


# --- CARICAMENTO SUONO CLICK ---
# Controlla se il file del suono del click esiste.
if os.path.exists(
    # PROF: nome ASSURDO per un file da caricare...
    files("missionone")
    / "ES_User Interface, Click, Pop Up, Alert Tones - Epidemic Sound - 0813-1088.wav"
):
    # Prova a caricare il suono.
    try:
        # Assegna il suono caricato alla variabile globale.
        click_sound = pygame.mixer.Sound(
            files("missionone")
            / "ES_User Interface, Click, Pop Up, Alert Tones - Epidemic Sound - 0813-1088.wav"
        )
    # Se il caricamento fallisce.
    except:
        # Mantiene la variabile su None.
        click_sound = None


# --- FUNZIONI SALVATAGGIO RECORD ---
# Definisce la funzione per caricare il record.
def load_high_score():
    # Dichiara l'uso della variabile globale HIGH_SCORE.
    global HIGH_SCORE
    # Prova ad aprire il file di testo.
    try:
        # Apre il file in modalità lettura.
        # PROF: sistema con platformdirs
        with open("highscore.txt", "r") as f:
            # Legge tutto il contenuto del file.
            content = f.read()
            # Controlla se il contenuto è composto solo da cifre.
            if content.isdigit():
                # Converte la stringa in un numero intero.
                HIGH_SCORE = int(content)
            # Se il contenuto non è un numero valido.
            else:
                # Imposta il record a 0.
                HIGH_SCORE = 0
    # Se il file non esiste o c'è un errore di valore.
    except (FileNotFoundError, ValueError):
        # Imposta il record a 0 di default.
        HIGH_SCORE = 0


# Definisce la funzione per salvare il nuovo record.
def save_high_score(score):
    # Dichiara l'uso della variabile globale.
    global HIGH_SCORE
    # Verifica se il punteggio attuale supera il record.
    if score > HIGH_SCORE:
        # Aggiorna la variabile globale con il nuovo punteggio.
        HIGH_SCORE = score
        # Prova a scrivere su file.
        try:
            # Apre il file in modalità scrittura (sovrascrive).
            with open("highscore.txt", "w") as f:
                # Scrive il nuovo record nel file.
                f.write(str(score))
        # Se si verifica un errore durante il salvataggio.
        except Exception as e:
            # Stampa l'errore nella console.
            print(f"Errore durante il salvataggio del record: {e}")


# --- CARICAMENTO SFONDO ---
# Tenta di caricare l'immagine di sfondo dal nome file semplice.
bg = load("background.jpg")
# Definisce il percorso completo alternativo.
bg_full_path = files("missionone") / "background.jpg"
# Controlla se il percorso completo esiste.
if os.path.exists(bg_full_path):
    # Carica l'immagine dal percorso completo.
    bg = load(bg_full_path)

# Se l'immagine è stata caricata con successo.
if bg:
    # Ridimensiona l'immagine per adattarla alla finestra.
    background = pygame.transform.scale(bg, (WIDTH, HEIGHT))
# Se l'immagine non è stata trovata.
else:
    # Imposta lo sfondo su None.
    background = None

# --- CARICAMENTO GIOCATORE (RAZZO) ---
# Carica l'immagine del razzo dal percorso specificato.
razzo = load(files("missionone") / "razzo.png")
# Se l'immagine è stata caricata.
if razzo:
    # Ridimensiona l'immagine a 180x180 pixel.
    razzo = pygame.transform.scale(razzo, (180, 180))

# --- CARICAMENTO ICONA IMPOSTAZIONI ---
# Carica l'icona delle impostazioni (ingranaggio).
settings_icon = load(files("missionone") / "settings.png")
# Se l'icona è stata caricata.
if settings_icon:
    # Ridimensiona l'icona a 70x70 pixel.
    settings_icon = pygame.transform.scale(settings_icon, (70, 70))

# --- CARICAMENTO POTENZIAMENTI (BOOST) ---
# Carica l'immagine per il boost potenza.
boost_power_img = load(files("missionone") / "potenza.png")
# Carica l'immagine per il boost vita.
boost_health_img = load(files("missionone") / "cuore.png")
# Carica l'immagine per il boost velocità.
boost_speed_img = load(files("missionone") / "velocità.png")
# Carica l'immagine per il boost invincibilità.
boost_invincibility_img = load(files("missionone") / "invincibilità.png")

# Se l'immagine boost potenza esiste, la ridimensiona.
if boost_power_img:
    boost_power_img = pygame.transform.scale(boost_power_img, (50, 50))
# Se l'immagine boost vita esiste, la ridimensiona.
if boost_health_img:
    boost_health_img = pygame.transform.scale(boost_health_img, (50, 50))
# Se l'immagine boost velocità esiste, la ridimensiona.
if boost_speed_img:
    boost_speed_img = pygame.transform.scale(boost_speed_img, (50, 50))
# Se l'immagine boost invincibilità esiste, la ridimensiona.
if boost_invincibility_img:
    boost_invincibility_img = pygame.transform.scale(boost_invincibility_img, (50, 50))

# --- CARICAMENTO NEMICO ---
# Carica l'immagine del nemico.
enemy_img = load(files("missionone") / "nemico.png")
# Se caricata, la ridimensiona.
if enemy_img:
    # Imposta le dimensioni a 60x60.
    enemy_img = pygame.transform.scale(enemy_img, (60, 60))

# --- CARICAMENTO MISSILE ---
# Carica l'immagine del missile.
missile_img = load(files("missionone") / "missile.png")
# Se caricata.
if missile_img:
    # Ridimensiona a 50x20 pixel.
    missile_img = pygame.transform.scale(missile_img, (50, 20))

# --- CARICAMENTO BOSS ---
# Definisce il percorso del file del Boss.
boss_image_file = files("missionone") / "boss.png"
# Carica l'immagine del Boss.
boss_img = load(boss_image_file)
# Se caricata.
if boss_img:
    # Ridimensiona a 150x150 pixel.
    boss_img = pygame.transform.scale(boss_img, (150, 150))


# ───────────── SEZIONE 8: COSTRUTTORI OGGETTI (DIZIONARI) ─────────────
# Definisce la funzione per creare il dizionario del giocatore.
def make_player():
    # Imposta la velocità base in base alla difficoltà.
    base_speed = 5 if settings["difficulty"] == "base" else 7
    # Crea il dizionario vuoto per il giocatore.
    player_data = {}
    # Imposta la posizione iniziale X.
    player_data["x"] = 100
    # Imposta la posizione iniziale Y centrata.
    player_data["y"] = HEIGHT // 2
    # Imposta la larghezza del rettangolo.
    player_data["width"] = 180
    # Imposta l'altezza del rettangolo.
    player_data["height"] = 180
    # Imposta la velocità base.
    player_data["base_speed"] = base_speed
    # Imposta la velocità attuale.
    player_data["speed"] = base_speed
    # Imposta la vita iniziale.
    player_data["health"] = 100
    # Imposta la vita massima.
    player_data["max_health"] = 100
    # Imposta la potenza di fuoco iniziale.
    player_data["power"] = 1
    # Imposta il rateo di fuoco iniziale.
    player_data["fire_rate"] = 300
    # Imposta il tempo dell'ultimo sparo a zero.
    player_data["last_shot"] = 0
    # Imposta il tempo di fine effetto potenza.
    player_data["power_end_time"] = 0
    # Imposta il tempo di fine effetto velocità.
    player_data["speed_end_time"] = 0
    # Imposta il tempo di fine invincibilità.
    player_data["invincibility_end_time"] = 0
    # Ritorna il dizionario completo.
    return player_data


# Definisce la funzione per creare un proiettile.
def make_bullet(x, y, power):
    # Crea il dizionario del proiettile.
    bullet_data = {}
    # Imposta la coordinata X.
    bullet_data["x"] = x
    # Imposta la coordinata Y.
    bullet_data["y"] = y
    # Imposta la larghezza in base alla potenza.
    bullet_data["width"] = 15 * power
    # Imposta l'altezza.
    bullet_data["height"] = 8
    # Imposta la velocità.
    bullet_data["speed"] = 12
    # Imposta la potenza.
    bullet_data["power"] = power
    # Ritorna il dizionario.
    return bullet_data


# Definisce la funzione per creare un nemico.
def make_enemy():
    # Crea il dizionario del nemico.
    enemy_data = {}
    # Imposta la posizione X casuale fuori schermo.
    enemy_data["x"] = WIDTH + random.randint(0, 100)
    # Imposta la posizione Y casuale.
    enemy_data["y"] = random.randint(50, HEIGHT - 110)
    # Imposta la larghezza.
    enemy_data["width"] = 60
    # Imposta l'altezza.
    enemy_data["height"] = 60
    # Imposta la velocità in base alla difficoltà.
    enemy_data["speed"] = 3 if settings["difficulty"] == "base" else 5
    # Imposta il timer dell'ultimo sparo.
    enemy_data["last_shot"] = pygame.time.get_ticks()
    # Imposta il ritardo di sparo casuale.
    enemy_data["shoot_delay"] = random.randint(1000, 2500)
    # Imposta la vita.
    enemy_data["health"] = 100
    # Imposta la vita massima.
    enemy_data["max_health"] = 100
    # Ritorna il dizionario.
    return enemy_data


# Definisce la funzione per creare un proiettile nemico.
def make_enemy_bullet(x, y):
    # Crea il dizionario.
    bullet_data = {}
    # Imposta X.
    bullet_data["x"] = x
    # Imposta Y.
    bullet_data["y"] = y
    # Imposta larghezza.
    bullet_data["width"] = 10
    # Imposta altezza.
    bullet_data["height"] = 10
    # Imposta velocità.
    bullet_data["speed"] = 7
    # Ritorna il dizionario.
    return bullet_data


# Definisce la funzione per creare un missile.
def make_missile():
    # Crea il dizionario.
    missile_data = {}
    # Imposta X casuale.
    missile_data["x"] = WIDTH + random.randint(0, 100)
    # Imposta Y casuale.
    missile_data["y"] = random.randint(50, HEIGHT - 100)
    # Imposta larghezza visiva.
    missile_data["width"] = 50
    # Imposta altezza visiva.
    missile_data["height"] = 20
    # Imposta velocità in base alla difficoltà.
    missile_data["speed"] = 4 if settings["difficulty"] == "base" else 6
    # Ritorna il dizionario.
    return missile_data


# Definisce la funzione per creare un boost.
def make_boost(boost_type):
    # Crea il dizionario.
    boost_data = {}
    # Imposta X.
    boost_data["x"] = WIDTH + random.randint(0, 100)
    # Imposta Y.
    boost_data["y"] = random.randint(100, HEIGHT - 150)
    # Imposta larghezza.
    boost_data["width"] = 50
    # Imposta altezza.
    boost_data["height"] = 50
    # Imposta velocità.
    boost_data["speed"] = 3
    # Imposta il tipo passato come argomento.
    boost_data["type"] = boost_type
    # Ritorna il dizionario.
    return boost_data


# Definisce la funzione per creare il Boss.
def make_boss(wave_number):
    # Imposta la larghezza.
    w = 150
    # Imposta l'altezza.
    h = 150
    # Definisce la vita base.
    base_hp = 1000
    # Calcola il bonus vita per ondata.
    hp_bonus = (wave_number - 1) * 400
    # Calcola il danno.
    damage = 15 + (wave_number - 1) * 3
    # Calcola la velocità missili.
    missile_speed = 5.0 + (wave_number - 1) * 0.5
    # Calcola il ritardo di sparo.
    shoot_delay = max(400, 900 - (wave_number * 100))
    # Crea il dizionario.
    boss_data = {}
    # Imposta X iniziale.
    boss_data["x"] = WIDTH + 50
    # Imposta Y centrata.
    boss_data["y"] = HEIGHT // 2 - h // 2
    # Imposta larghezza.
    boss_data["width"] = w
    # Imposta altezza.
    boss_data["height"] = h
    # Imposta velocità movimento.
    boss_data["speed"] = 2
    # Imposta vita totale.
    boss_data["health"] = base_hp + hp_bonus
    # Imposta vita massima.
    boss_data["max_health"] = base_hp + hp_bonus
    # Imposta danno.
    boss_data["damage"] = damage
    # Imposta velocità missili.
    boss_data["missile_speed"] = missile_speed
    # Imposta timer sparo.
    boss_data["last_shot"] = pygame.time.get_ticks()
    # Imposta ritardo.
    boss_data["shoot_delay"] = shoot_delay
    # Imposta direzione.
    boss_data["direction"] = 1
    # Imposta flag di entrata.
    boss_data["entering"] = True
    # Ritorna il dizionario.
    return boss_data


# Definisce la funzione per creare un missile del Boss.
def make_boss_missile(x, y, player_rect, speed, damage):
    # Prende il centro X del giocatore.
    tx = player_rect.centerx
    # Prende il centro Y del giocatore.
    ty = player_rect.centery
    # Calcola differenza X.
    dx = tx - x
    # Calcola differenza Y.
    dy = ty - y
    # Calcola distanza ipotenusa.
    dist = math.hypot(dx, dy)
    # Se la distanza non è zero.
    if dist != 0:
        # Normalizza il vettore X.
        dx = dx / dist
        # Normalizza il vettore Y.
        dy = dy / dist
    # Se la distanza è zero.
    else:
        # Imposta direzione default X.
        dx = -1
        # Imposta direzione default Y.
        dy = 0
    # Crea il dizionario.
    missile_data = {}
    # Imposta X.
    missile_data["x"] = x
    # Imposta Y.
    missile_data["y"] = y
    # Imposta larghezza.
    missile_data["width"] = 30
    # Imposta altezza.
    missile_data["height"] = 15
    # Imposta direzione X normalizzata.
    missile_data["dx"] = dx
    # Imposta direzione Y normalizzata.
    missile_data["dy"] = dy
    # Imposta velocità.
    missile_data["speed"] = speed
    # Imposta danno.
    missile_data["damage"] = damage
    # Ritorna il dizionario.
    return missile_data


# ───────────── SEZIONE 9: FUNZIONI DI LOGICA (AGGIORNAMENTO) ─────────────


# Funzione per aggiornare il giocatore.
def update_player(p, keys, current_time):
    # Controlla se il tasto SU è premuto.
    if keys[pygame.K_UP]:
        # Controlla se il giocatore è dentro il bordo.
        if p["y"] > 0:
            # Muove il giocatore in alto.
            p["y"] -= p["speed"]
    # Controlla se il tasto GIU è premuto.
    if keys[pygame.K_DOWN]:
        # Controlla il bordo inferiore.
        if p["y"] < HEIGHT - p["height"]:
            # Muove il giocatore in basso.
            p["y"] += p["speed"]
    # Controlla se il tasto SINISTRA è premuto.
    if keys[pygame.K_LEFT]:
        # Controlla il bordo sinistro.
        if p["x"] > 0:
            # Muove a sinistra.
            p["x"] -= p["speed"]
    # Controlla se il tasto DESTRA è premuto.
    if keys[pygame.K_RIGHT]:
        # Controlla il bordo destro.
        if p["x"] < WIDTH - p["width"]:
            # Muove a destra.
            p["x"] += p["speed"]

    # Controlla se il buff velocità è attivo.
    if current_time < p["speed_end_time"]:
        # Aumenta la velocità.
        p["speed"] = p["base_speed"] + 3
        # Aumenta il rateo di fuoco.
        p["fire_rate"] = 100
    # Se il buff è finito.
    else:
        # Resetta la velocità.
        p["speed"] = p["base_speed"]
        # Resetta il rateo.
        p["fire_rate"] = 300

    # Controlla se il buff potenza è attivo.
    if current_time < p["power_end_time"]:
        # Imposta potenza a 3.
        p["power"] = 3
    # Se il buff è finito.
    else:
        # Resetta potenza a 1.
        p["power"] = 1


# Funzione per verificare l'invincibilità.
def is_invincible(p, current_time):
    # Ritorna True se il tempo attuale è minore del tempo di fine.
    result = current_time < p["invincibility_end_time"]
    # Ritorna il risultato.
    return result


# Funzione per aggiornare il Boss.
def update_boss(b):
    # Controlla se il boss sta entrando in scena.
    if b["entering"]:
        # Controlla se non ha raggiunto la posizione finale.
        if b["x"] > WIDTH - b["width"] - 50:
            # Sposta il boss a sinistra.
            b["x"] -= 3
        # Se ha raggiunto la posizione.
        else:
            # Imposta entering a False.
            b["entering"] = False

    # Controlla se il boss non sta più entrando.
    if not b["entering"]:
        # Muove il boss verticalmente.
        b["y"] += b["speed"] * b["direction"]
        # Controlla se tocca il bordo superiore.
        if b["y"] <= 20:
            # Cambia direzione verso il basso.
            b["direction"] = 1
        # Controlla se tocca il bordo inferiore.
        elif b["y"] + b["height"] >= HEIGHT - 20:
            # Cambia direzione verso l'alto.
            b["direction"] = -1


# ───────────── SEZIONE 10: FUNZIONI DI DISEGNO (RENDERING) ─────────────


# Funzione per disegnare il giocatore.
def draw_player(surface, p, current_time):
    # Controlla se il giocatore è invincibile.
    if is_invincible(p, current_time):
        # Crea un effetto lampeggiante.
        if (current_time // 100) % 2 == 0:
            # Definisce il rettangolo dello scudo.
            rect = (p["x"] - 4, p["y"] - 4, p["width"] + 8, p["height"] + 8)
            # Disegna lo scudo ciano.
            pygame.draw.rect(surface, CYAN, rect, 4, border_radius=10)

    # Controlla se l'immagine esiste.
    if razzo:
        # Disegna l'immagine del razzo.
        surface.blit(razzo, (p["x"], p["y"]))
    # Se l'immagine non esiste.
    else:
        # Disegna un rettangolo blu.
        pygame.draw.rect(surface, BLUE, (p["x"], p["y"], p["width"], p["height"]))


# Funzione per disegnare il nemico.
def draw_enemy(surface, e):
    # Controlla se l'immagine esiste.
    if enemy_img:
        # Disegna l'immagine.
        surface.blit(enemy_img, (e["x"], e["y"]))
    # Se non esiste.
    else:
        # Disegna un rettangolo rosso.
        pygame.draw.rect(surface, RED, (e["x"], e["y"], e["width"], e["height"]))

    # Calcola il rapporto della vita.
    health_ratio = e["health"] / e["max_health"]
    # Imposta la larghezza della barra.
    bar_width = 40
    # Imposta l'altezza della barra.
    bar_height = 5
    # Calcola la posizione X.
    bar_x = e["x"] + (e["width"] - bar_width) // 2
    # Calcola la posizione Y.
    bar_y = e["y"] - 10

    # Disegna lo sfondo della barra (rosso).
    pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
    # Disegna la vita attuale (verde).
    pygame.draw.rect(
        surface, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height)
    )


# Funzione per disegnare il Boss.
def draw_boss(surface, b):
    # Controlla se l'immagine esiste.
    if boss_img:
        # Disegna l'immagine.
        surface.blit(boss_img, (b["x"], b["y"]))
    # Se non esiste.
    else:
        # Disegna rettangolo nero.
        pygame.draw.rect(surface, BLACK, (b["x"], b["y"], b["width"], b["height"]))
        # Disegna bordo viola.
        pygame.draw.rect(surface, PURPLE, (b["x"], b["y"], b["width"], b["height"]), 4)

    # Calcola il rapporto della vita.
    health_ratio = b["health"] / b["max_health"]
    # Imposta dimensioni barra.
    bar_width = 120
    bar_height = 12
    # Calcola posizione.
    bar_x = b["x"] + (b["width"] - bar_width) // 2
    bar_y = b["y"] - 20
    # Disegna sfondo rosso.
    pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
    # Disegna vita verde.
    pygame.draw.rect(
        surface, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height)
    )
    # Disegna bordo bianco.
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)


# Funzione per disegnare i boost.
def draw_boost(surface, b):
    # Inizializza le variabili.
    img = None
    color = WHITE
    # Controlla il tipo di boost.
    if b["type"] == "power":
        # Assegna immagine.
        img = boost_power_img
        # Assegna colore.
        color = YELLOW
    # Controlla il tipo.
    elif b["type"] == "health":
        # Assegna immagine.
        img = boost_health_img
        # Assegna colore.
        color = GREEN
    # Controlla il tipo.
    elif b["type"] == "speed":
        # Assegna immagine.
        img = boost_speed_img
        # Assegna colore.
        color = BLUE
    # Controlla il tipo.
    elif b["type"] == "invincibility":
        # Assegna immagine.
        img = boost_invincibility_img
        # Assegna colore.
        color = CYAN

    # Se l'immagine esiste.
    if img:
        # Disegna l'immagine.
        surface.blit(img, (b["x"], b["y"]))
    # Se non esiste.
    else:
        # Disegna un cerchio colorato.
        pygame.draw.circle(surface, color, (int(b["x"] + 25), int(b["y"] + 25)), 25)


# Funzione per disegnare l'HUD (interfaccia).
def draw_hud(surface, player, score, font, small_font, current_time):
    # Imposta la posizione X della barra.
    bar_x = 20
    # Imposta la posizione Y.
    bar_y = 20
    # Imposta la larghezza.
    bar_width = 250
    # Imposta l'altezza.
    bar_height = 25

    # Disegna lo sfondo della barra.
    pygame.draw.rect(
        surface, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height), border_radius=5
    )
    # Calcola i pixel di vita.
    health_w = int((player["health"] / player["max_health"]) * bar_width)
    # Controlla il valore della vita per il colore.
    if player["health"] > 50:
        # Verde se alta.
        health_color = GREEN
    # Se media.
    elif player["health"] > 25:
        # Giallo.
        health_color = YELLOW
    # Se bassa.
    else:
        # Rosso.
        health_color = RED
    # Disegna la barra della vita.
    pygame.draw.rect(
        surface, health_color, (bar_x, bar_y, health_w, bar_height), border_radius=5
    )
    # Disegna il bordo.
    pygame.draw.rect(
        surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 3, border_radius=5
    )

    # Crea il testo della vita.
    health_text = font.render(f"VITA: {player['health']}", True, WHITE)
    # Disegna il testo.
    surface.blit(health_text, (bar_x + bar_width + 10, bar_y))

    # Crea il testo della potenza.
    pow_text = font.render(f"POW: x{player['power']}", True, YELLOW)
    # Disegna il testo.
    surface.blit(pow_text, (20, 55))

    # Crea il testo del punteggio.
    score_text = font.render(f"SCORE: {score}", True, YELLOW)
    # Disegna il testo.
    surface.blit(score_text, (20, 85))

    # --- PANNELLO BOOST ---
    # Imposta posizione X.
    panel_x = WIDTH - 200
    # Imposta posizione Y.
    panel_y = 10
    # Crea la superficie trasparente.
    panel = pygame.Surface((190, 130), pygame.SRCALPHA)
    # Riempie di nero semi-trasparente.
    panel.fill((0, 0, 0, 140))
    # Disegna il pannello.
    surface.blit(panel, (panel_x - 5, panel_y - 5))

    # Lista dei boost.
    boost_data = [
        ("power", boost_power_img, YELLOW, "POW", "power_end_time"),
        ("speed", boost_speed_img, BLUE, "VEL", "speed_end_time"),
        (
            "invincibility",
            boost_invincibility_img,
            CYAN,
            "INV",
            "invincibility_end_time",
        ),
        ("health", boost_health_img, GREEN, "VITA", None),
    ]

    # Cicla per ogni boost.
    for i, (btype, img, color, label, timer_key) in enumerate(boost_data):
        # Calcola la Y della riga.
        row_y = panel_y + i * 30
        # Se l'immagine esiste.
        if img:
            # Scala l'immagine.
            small = pygame.transform.scale(img, (24, 24))
            # Disegna l'icona.
            surface.blit(small, (panel_x, row_y))

        # Se il tipo è health.
        if btype == "health":
            # Crea testo fisso.
            txt = small_font.render(f"{label}: PRONTO", True, color)
        # Se ha un timer.
        else:
            # Ottiene il tempo di fine.
            end_time = player[timer_key]
            # Controlla se attivo.
            if current_time < end_time:
                # Calcola secondi.
                seconds_left = (end_time - current_time) / 1000.0
                # Crea testo con tempo.
                txt = small_font.render(f"{label}: {seconds_left:.1f}s", True, color)
            # Se non attivo.
            else:
                # Crea testo OFF.
                txt = small_font.render(f"{label}: OFF", True, (80, 80, 80))
        # Disegna il testo.
        surface.blit(txt, (panel_x + 30, row_y + 3))


# ───────────── SEZIONE 11: SCHERMATE (MENU, SETTINGS, GAME OVER) ─────────────


# Funzione per mostrare il menu.
def show_menu():
    # Crea l'orologio.
    clock = pygame.time.Clock()
    # Avvia la musica.
    play_music(MENU_MUSIC_FILE)

    # Crea il font del titolo.
    title_font = pygame.font.Font(None, 120)
    # Crea il font dei bottoni.
    button_font = pygame.font.Font(None, 50)
    # Testo del titolo.
    title_text = "MissionOne"

    # Crea il rettangolo del bottone ENTER.
    button_enter = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 150, 300, 70)
    # Crea il rettangolo del bottone settings.
    button_settings = pygame.Rect(WIDTH - 90, 20, 70, 70)

    # Carica l'immagine del razzo.
    razzo_menu = load(files("giocoguendouzlancioni") / "razzo.png")
    # Se caricata.
    if razzo_menu:
        # Scala l'immagine.
        razzo_menu = pygame.transform.scale(razzo_menu, (350, 350))

    # Variabile tempo.
    t = 0

    # Loop del menu.
    while True:
        # Ottiene posizione mouse.
        mouse_pos = pygame.mouse.get_pos()
        # Resetta click.
        click = False

        # Cicla gli eventi.
        for event in pygame.event.get():
            # Se quit.
            if event.type == pygame.QUIT:
                # Ritorna QUIT.
                return "QUIT"
            # Se tasto premuto.
            if event.type == pygame.KEYDOWN:
                # Se INVIO.
                if event.key == pygame.K_RETURN:
                    # Ritorna GAME.
                    return "GAME"
            # Se click mouse.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Imposta click.
                click = True

        # DISEGNO:
        # Se c'è lo sfondo.
        if background:
            # Disegna sfondo.
            screen.blit(background, (0, 0))
        # Se non c'è.
        else:
            # Sfondo grigio.
            screen.fill(GRAY)

        # Se c'è il razzo.
        if razzo_menu:
            # Calcola oscillazione.
            offset = math.sin(t / 20) * 10
            # Posizione X centrata.
            draw_x = WIDTH // 2 - razzo_menu.get_width() // 2
            # Posizione Y centrata con offset.
            draw_y = HEIGHT // 2 - razzo_menu.get_height() // 2 + offset
            # Disegna il razzo.
            screen.blit(razzo_menu, (draw_x, draw_y))

        # Crea il testo del titolo.
        title_surf = title_font.render(title_text, True, PINK)
        # Crea l'ombra.
        shadow_surf = title_font.render(title_text, True, BLACK)
        # Ottiene il rettangolo.
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
        # Disegna l'ombra.
        screen.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
        # Disegna il titolo.
        screen.blit(title_surf, title_rect)

        # --- RECORD VIOLA ---
        # Crea il testo del record in viola.
        record_text = button_font.render(f"RECORD: {HIGH_SCORE}", True, PURPLE)
        # Centra il testo.
        screen.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, 150))

        # Controlla hover ENTER.
        hover_enter = button_enter.collidepoint(mouse_pos)
        # Se hover.
        if hover_enter:
            # Colore viola.
            color = PURPLE
            # Bordo scuro.
            border = (100, 0, 150)
        # Se no hover.
        else:
            # Grigio.
            color = (200, 200, 200)
            # Bordo grigio.
            border = (150, 150, 150)

        # Disegna il rettangolo.
        pygame.draw.rect(screen, color, button_enter, border_radius=15)
        # Disegna il bordo.
        pygame.draw.rect(screen, border, button_enter, 4, border_radius=15)

        # Crea il testo ENTER.
        txt = button_font.render("ENTER", True, WHITE if hover_enter else BLACK)
        # Centra il testo.
        screen.blit(
            txt,
            (
                button_enter.centerx - txt.get_width() // 2,
                button_enter.centery - txt.get_height() // 2,
            ),
        )

        # Controlla hover settings.
        hover_settings = button_settings.collidepoint(mouse_pos)
        # Se esiste l'icona.
        if settings_icon:
            # Se hover.
            if hover_settings:
                # Copia icona.
                colored_icon = settings_icon.copy()
                # Tinta viola.
                colored_icon.fill(PURPLE, special_flags=pygame.BLEND_RGBA_ADD)
                # Disegna.
                screen.blit(colored_icon, button_settings)
            # Se no hover.
            else:
                # Normale.
                screen.blit(settings_icon, button_settings)

        # Se click.
        if click:
            # Se ENTER.
            if hover_enter:
                # Suono.
                if click_sound:
                    click_sound.play()
                # Game.
                return "GAME"
            # Se settings.
            if hover_settings:
                # Suono.
                if click_sound:
                    click_sound.play()
                # Apri settings.
                show_settings()

        # Aggiorna display.
        pygame.display.flip()
        # Tick.
        clock.tick(60)
        # Avanza tempo.
        t += 1


# Funzione per mostrare le impostazioni.
def show_settings():
    # Orologio.
    clock = pygame.time.Clock()
    # Font.
    title_font = pygame.font.Font(None, 80)
    label_font = pygame.font.Font(None, 45)
    button_font = pygame.font.Font(None, 40)

    # Rettangoli slider.
    slider_rect = pygame.Rect(200, 200, 400, 10)
    slider_handle = pygame.Rect(0, 0, 20, 30)
    # Flag dragging.
    dragging = False

    # Bottoni difficoltà.
    button_base = pygame.Rect(200, 320, 180, 60)
    button_avanzato = pygame.Rect(420, 320, 180, 60)
    button_back = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)

    # Loop settings.
    while True:
        # Mouse.
        mouse_pos = pygame.mouse.get_pos()
        # Click.
        click = False
        # Eventi.
        for event in pygame.event.get():
            # Quit.
            if event.type == pygame.QUIT:
                # Chiudi.
                pygame.quit()
                # Esci.
                sys.exit()
            # Mouse down.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click true.
                click = True
                # Dragging false.
                dragging = False
            # Mouse up.
            if event.type == pygame.MOUSEBUTTONUP:
                # Dragging false.
                dragging = False

        # Sfondo.
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(GRAY)
        # Overlay.
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((40, 40, 40, 200))
        screen.blit(overlay, (0, 0))

        # Titolo.
        title = title_font.render("IMPOSTAZIONI", True, PURPLE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Etichetta volume.
        volume_label = label_font.render("Volume", True, PURPLE)
        screen.blit(volume_label, (200, 150))
        # Valore.
        volume_value = label_font.render(f"{settings['volume']}%", True, PURPLE)
        screen.blit(volume_value, (620, 150))

        # Barra slider.
        pygame.draw.rect(screen, WHITE, slider_rect, border_radius=5)
        # Posizione handle.
        slider_handle.centerx = (
            slider_rect.x + (settings["volume"] / 100) * slider_rect.width
        )
        slider_handle.centery = slider_rect.centery

        # Se collide.
        if slider_handle.collidepoint(mouse_pos) and click:
            # Dragging true.
            dragging = True
        # Se dragging.
        if dragging:
            # Nuova X.
            new_x = max(slider_rect.x, min(mouse_pos[0], slider_rect.right))
            # Calcolo volume.
            settings["volume"] = int(
                ((new_x - slider_rect.x) / slider_rect.width) * 100
            )
            # Posizione handle.
            slider_handle.centerx = new_x
            # Imposta volume.
            pygame.mixer.music.set_volume(settings["volume"] / 100.0)

        # Disegna handle.
        pygame.draw.rect(screen, PURPLE, slider_handle, border_radius=5)

        # Etichetta diff.
        diff_label = label_font.render("Difficoltà", True, PURPLE)
        screen.blit(diff_label, (200, 270))

        # Difficoltà base.
        is_base = settings["difficulty"] == "base"
        color_base = GREEN if is_base else (80, 80, 80)
        pygame.draw.rect(screen, color_base, button_base, border_radius=10)
        pygame.draw.rect(
            screen, GREEN if is_base else WHITE, button_base, 4, border_radius=10
        )
        txt_base = button_font.render("BASE", True, WHITE)
        screen.blit(
            txt_base,
            (
                button_base.centerx - txt_base.get_width() // 2,
                button_base.centery - txt_base.get_height() // 2,
            ),
        )

        # Difficoltà avanzato.
        is_avanzato = settings["difficulty"] == "avanzato"
        color_avanzato = RED if is_avanzato else (80, 80, 80)
        pygame.draw.rect(screen, color_avanzato, button_avanzato, border_radius=10)
        pygame.draw.rect(
            screen, RED if is_avanzato else WHITE, button_avanzato, 4, border_radius=10
        )
        txt_avanzato = button_font.render("AVANZATO", True, WHITE)
        screen.blit(
            txt_avanzato,
            (
                button_avanzato.centerx - txt_avanzato.get_width() // 2,
                button_avanzato.centery - txt_avanzato.get_height() // 2,
            ),
        )

        # Click.
        if click:
            # Su base.
            if button_base.collidepoint(mouse_pos):
                # Suono.
                if click_sound:
                    click_sound.play()
                # Imposta.
                settings["difficulty"] = "base"
            # Su avanzato.
            if button_avanzato.collidepoint(mouse_pos):
                # Suono.
                if click_sound:
                    click_sound.play()
                # Imposta.
                settings["difficulty"] = "avanzato"

        # Indietro.
        hover_back = button_back.collidepoint(mouse_pos)
        back_color = PURPLE if hover_back else WHITE
        pygame.draw.rect(screen, back_color, button_back, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_back, 3, border_radius=10)
        txt_back = button_font.render("INDIETRO", True, WHITE if hover_back else BLACK)
        screen.blit(
            txt_back,
            (
                button_back.centerx - txt_back.get_width() // 2,
                button_back.centery - txt_back.get_height() // 2,
            ),
        )

        # Se click indietro.
        if hover_back and click:
            # Suono.
            if click_sound:
                click_sound.play()
            # Ritorna.
            return

        # Flip.
        pygame.display.flip()
        # Tick.
        clock.tick(60)


# Funzione game over.
def show_game_over(score):
    # Stop musica.
    pygame.mixer.music.stop()
    # Orologio.
    clock = pygame.time.Clock()
    # Font.
    font_big = pygame.font.Font(None, 100)
    font_small = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 40)

    # Bottoni.
    button_retry = pygame.Rect(WIDTH // 2 - 150, 420, 140, 60)
    button_menu = pygame.Rect(WIDTH // 2 + 10, 420, 140, 60)

    # Salva record.
    save_high_score(score)

    # Loop.
    while True:
        # Mouse.
        mouse_pos = pygame.mouse.get_pos()
        # Click.
        click = False
        # Eventi.
        for event in pygame.event.get():
            # Quit.
            if event.type == pygame.QUIT:
                return "QUIT"
            # Mouse.
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # Sfondo.
        screen.fill(BLACK)

        # Titolo.
        go = font_big.render("GAME OVER", True, RED)
        screen.blit(go, (WIDTH // 2 - go.get_width() // 2, 120))

        # Linea.
        pygame.draw.line(screen, WHITE, (100, 230), (WIDTH - 100, 230), 2)

        # --- PUNTEGGIO E RECORD LILLA ---
        # Se nuovo record.
        if score == HIGH_SCORE and score > 0:
            # Testo nuovo record.
            new_rec = font_small.render("NUOVO RECORD!", True, YELLOW)
            # Disegna.
            screen.blit(new_rec, (WIDTH // 2 - new_rec.get_width() // 2, 260))
            # Punteggio LILLA.
            sc = font_small.render(f"PUNTEGGIO: {score}", True, LILAC)
            # Disegna.
            screen.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 310))
        # Se non record.
        else:
            # Punteggio LILLA.
            sc = font_small.render(f"PUNTEGGIO: {score}", True, LILAC)
            # Disegna.
            screen.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 260))
            # Record LILLA.
            rec = font_small.render(f"RECORD: {HIGH_SCORE}", True, LILAC)
            # Disegna.
            screen.blit(rec, (WIDTH // 2 - rec.get_width() // 2, 310))

        # Retry.
        hover_retry = button_retry.collidepoint(mouse_pos)
        retry_color = PURPLE if hover_retry else WHITE
        pygame.draw.rect(screen, retry_color, button_retry, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_retry, 3, border_radius=10)
        txt_retry = button_font.render("RIPROVA", True, WHITE if hover_retry else BLACK)
        screen.blit(
            txt_retry,
            (
                button_retry.centerx - txt_retry.get_width() // 2,
                button_retry.centery - txt_retry.get_height() // 2,
            ),
        )

        # Menu.
        hover_menu = button_menu.collidepoint(mouse_pos)
        menu_color = PURPLE if hover_menu else WHITE
        pygame.draw.rect(screen, menu_color, button_menu, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_menu, 3, border_radius=10)
        txt_menu = button_font.render("MENU", True, WHITE if hover_menu else BLACK)
        screen.blit(
            txt_menu,
            (
                button_menu.centerx - txt_menu.get_width() // 2,
                button_menu.centery - txt_menu.get_height() // 2,
            ),
        )

        # Click.
        if click:
            # Retry.
            if hover_retry:
                # Suono.
                if click_sound:
                    click_sound.play()
                # Game.
                return "GAME"
            # Menu.
            if hover_menu:
                # Suono.
                if click_sound:
                    click_sound.play()
                # Menu.
                return "MENU"

        # Flip.
        pygame.display.flip()
        # Tick.
        clock.tick(60)


# ───────────── SEZIONE 12: LOOP DI GIOCO PRINCIPALE ─────────────


# Funzione loop principale.
def run_game():
    # Musica.
    play_music(GAME_MUSIC_FILE)
    # Orologio.
    clock = pygame.time.Clock()
    # Font.
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 28)
    big_font = pygame.font.Font(None, 100)

    # Giocatore.
    player = make_player()
    # Liste.
    bullets = []
    enemies = []
    enemy_bullets = []
    missiles = []
    boosts = []
    boss = None
    boss_missiles = []
    # Stato.
    wave_number = 1
    next_boss_score = 3000
    warning_active = False
    warning_start_time = 0
    score = 0
    # Timer.
    enemy_spawn_timer = 0
    missile_spawn_timer = 0
    boost_spawn_timer = 0
    damage_flash = 0
    # Running.
    running = True
    # Loop.
    while running:
        # Tempo.
        current_time = pygame.time.get_ticks()
        # Eventi.
        for event in pygame.event.get():
            # Quit.
            if event.type == pygame.QUIT:
                return score
            # Tasto.
            if event.type == pygame.KEYDOWN:
                # Esc.
                if event.key == pygame.K_ESCAPE:
                    return -1
        # Tasti.
        keys = pygame.key.get_pressed()
        # Logica boss.
        if score >= next_boss_score and boss is None and not warning_active:
            warning_active = True
            warning_start_time = current_time
            next_boss_score += 3000
        if warning_active:
            if current_time - warning_start_time > 3000:
                warning_active = False
                boss = make_boss(wave_number)
                wave_number += 1
                enemies.clear()
                enemy_bullets.clear()
                missiles.clear()
                boosts.clear()
        # Muovi player.
        update_player(player, keys, current_time)
        # Sparo.
        if (
            keys[pygame.K_SPACE]
            and current_time - player["last_shot"] > player["fire_rate"]
        ):
            player["last_shot"] = current_time
            bullets.append(
                make_bullet(
                    player["x"] + player["width"],
                    player["y"] + player["height"] // 2,
                    player["power"],
                )
            )
        # Spawn.
        if not warning_active and boss is None:
            enemy_spawn_timer += 1
            if enemy_spawn_timer > (100 if settings["difficulty"] == "base" else 70):
                enemies.append(make_enemy())
                enemy_spawn_timer = 0
            missile_spawn_timer += 1
            if missile_spawn_timer > (180 if settings["difficulty"] == "base" else 130):
                missiles.append(make_missile())
                missile_spawn_timer = 0
            boost_spawn_timer += 1
            if boost_spawn_timer > 250:
                boosts.append(
                    make_boost(
                        random.choice(["power", "health", "speed", "invincibility"])
                    )
                )
                boost_spawn_timer = 0
        # Muovi proiettili.
        for b in bullets[:]:
            b["x"] += b["speed"]
            if b["x"] > WIDTH:
                bullets.remove(b)
        # Muovi nemici.
        for e in enemies[:]:
            e["x"] -= e["speed"]
            if current_time - e["last_shot"] > e["shoot_delay"]:
                e["last_shot"] = current_time
                e["shoot_delay"] = random.randint(1000, 2500)
                enemy_bullets.append(
                    make_enemy_bullet(e["x"], e["y"] + e["height"] // 2)
                )
            if e["x"] < -e["width"]:
                enemies.remove(e)
        # Muovi proiettili nemici.
        for eb in enemy_bullets[:]:
            eb["x"] -= eb["speed"]
            if eb["x"] < 0:
                enemy_bullets.remove(eb)
        # Muovi missili.
        for m in missiles[:]:
            m["x"] -= m["speed"]
            if m["x"] < -m["width"] - 20:
                missiles.remove(m)
        # Muovi boost.
        for b in boosts[:]:
            b["x"] -= b["speed"]
            if b["x"] < -b["width"]:
                boosts.remove(b)
        # Boss.
        if boss:
            update_boss(boss)
            if (
                not boss["entering"]
                and current_time - boss["last_shot"] > boss["shoot_delay"]
            ):
                boss["last_shot"] = current_time
                player_rect = pygame.Rect(
                    player["x"], player["y"], player["width"], player["height"]
                )
                boss_missiles.append(
                    make_boss_missile(
                        boss["x"],
                        boss["y"] + boss["height"] // 2,
                        player_rect,
                        boss["missile_speed"],
                        boss["damage"],
                    )
                )
            for hm in boss_missiles[:]:
                hm["x"] += hm["dx"] * hm["speed"]
                hm["y"] += hm["dy"] * hm["speed"]
                if (
                    hm["x"] < -50
                    or hm["x"] > WIDTH + 50
                    or hm["y"] < -50
                    or hm["y"] > HEIGHT + 50
                ):
                    if hm in boss_missiles:
                        boss_missiles.remove(hm)
        # Collisioni.
        # Hitbox player.
        player_rect = pygame.Rect(player["x"] + 20, player["y"] + 55, 140, 70)
        # Bullets -> Boss.
        if boss:
            boss_rect = pygame.Rect(boss["x"], boss["y"], boss["width"], boss["height"])
            for b in bullets[:]:
                b_rect = pygame.Rect(b["x"], b["y"], b["width"], b["height"])
                if b_rect.colliderect(boss_rect):
                    if b in bullets:
                        bullets.remove(b)
                    damage = 100 if b["power"] > 1 else 50
                    boss["health"] -= damage
                    if boss["health"] <= 0:
                        score += 500
                        boss = None
                        boss_missiles.clear()
                    break
        # Bullets -> Enemies.
        for b in bullets[:]:
            for e in enemies[:]:
                if (
                    b["x"] < e["x"] + e["width"]
                    and b["x"] + b["width"] > e["x"]
                    and b["y"] < e["y"] + e["height"]
                    and b["y"] + b["height"] > e["y"]
                ):
                    if b in bullets:
                        bullets.remove(b)
                    damage = 100 if b["power"] > 1 else 50
                    e["health"] -= damage
                    if e["health"] <= 0:
                        if e in enemies:
                            enemies.remove(e)
                        score += 10
        # Nemici -> Player.
        if not is_invincible(player, current_time):
            for eb in enemy_bullets[:]:
                eb_rect = pygame.Rect(eb["x"] - 5, eb["y"] - 5, 10, 10)
                if player_rect.colliderect(eb_rect):
                    if eb in enemy_bullets:
                        enemy_bullets.remove(eb)
                    player["health"] -= 10
                    damage_flash = 12
            # Missili.
            for m in missiles[:]:
                # Hitbox missili ridotta.
                m_rect = pygame.Rect(m["x"] + 15, m["y"] + 6, 20, 8)
                if player_rect.colliderect(m_rect):
                    if m in missiles:
                        missiles.remove(m)
                    player["health"] -= 20
                    damage_flash = 20
            for hm in boss_missiles[:]:
                hm_rect = pygame.Rect(hm["x"], hm["y"], hm["width"], hm["height"])
                if player_rect.colliderect(hm_rect):
                    if hm in boss_missiles:
                        boss_missiles.remove(hm)
                    player["health"] -= hm["damage"]
                    damage_flash = 15
        # Boost -> Player.
        for b in boosts[:]:
            b_rect = pygame.Rect(b["x"], b["y"], b["width"], b["height"])
            if player_rect.colliderect(b_rect):
                if b in boosts:
                    boosts.remove(b)
                duration = 7000
                if b["type"] == "power":
                    player["power_end_time"] = current_time + duration
                elif b["type"] == "speed":
                    player["speed_end_time"] = current_time + duration
                elif b["type"] == "invincibility":
                    player["invincibility_end_time"] = current_time + duration
                elif b["type"] == "health":
                    player["health"] = min(player["health"] + 30, player["max_health"])
                score += 5
        # Sconfitta.
        score += 1
        player["health"] = max(player["health"], 0)
        if player["health"] <= 0:
            running = False
        # Disegno.
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(GRAY)
        if damage_flash > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = int(120 * (damage_flash / 20))
            flash_surf.fill((220, 0, 0, alpha))
            screen.blit(flash_surf, (0, 0))
            damage_flash -= 1
        for b in bullets:
            pygame.draw.ellipse(
                screen, YELLOW, (b["x"], b["y"], b["width"], b["height"])
            )
        for e in enemies:
            draw_enemy(screen, e)
        for eb in enemy_bullets:
            pygame.draw.circle(screen, (255, 50, 50), (int(eb["x"]), int(eb["y"])), 5)
        for m in missiles:
            if missile_img:
                screen.blit(missile_img, (m["x"], m["y"]))
            else:
                cy = m["y"] + m["height"] // 2
                pygame.draw.ellipse(
                    screen,
                    (160, 160, 170),
                    (m["x"], m["y"] + 3, m["width"], m["height"] - 6),
                )
                pygame.draw.polygon(
                    screen,
                    (255, 180, 0),
                    [
                        (m["x"] + m["width"] + 10, cy - 4),
                        (m["x"] + m["width"] + 10, cy + 4),
                        (m["x"] + m["width"] + 22, cy),
                    ],
                )
        for b in boosts:
            draw_boost(screen, b)
        if boss:
            draw_boss(screen, boss)
            for hm in boss_missiles:
                pygame.draw.ellipse(
                    screen, (150, 0, 150), (hm["x"], hm["y"], hm["width"], hm["height"])
                )
        draw_player(screen, player, current_time)
        draw_hud(screen, player, score, font, small_font, current_time)
        if warning_active:
            warn_text = big_font.render(f"ONDATA {wave_number}", True, RED)
            if (current_time // 200) % 2 == 0:
                text_rect = warn_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(warn_text, text_rect)
        hint = small_font.render(
            "← ↑ ↓ → Muovi  |  SPAZIO Spara  |  ESC Menu", True, (180, 180, 180)
        )
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))
        pygame.display.flip()
        clock.tick(60)
    return score


# ───────────── SEZIONE 13: FUNZIONE MAIN ─────────────


# Funzione main.
def main():
    # Carica record.
    load_high_score()
    # Stato iniziale.
    state = "MENU"
    # Loop.
    while True:
        # Menu.
        if state == "MENU":
            state = show_menu()
        # Game.
        elif state == "GAME":
            final_score = run_game()
            if final_score == -1:
                state = "MENU"
            else:
                state = show_game_over(final_score)
        # Quit.
        elif state == "QUIT":
            pygame.quit()
            sys.exit()
        # Break.
        if state not in ["MENU", "GAME", "QUIT"]:
            break


# Punto di ingresso.
if __name__ == "__main__":
    main()
