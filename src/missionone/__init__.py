# License: See LICENSE file in the project root for details.

# Authors:
# Elena Lancioni
# Aziz Guendouz

# ───────────── SEZIONE 1: IMPORTAZIONE DELLE LIBRERIE ─────────────

# Importa il modulo math per calcoli trigonometrici e vettoriali.
import math
# Importa il modulo os per verificare l'esistenza dei file sul disco.
import os
# Importa il modulo random per generare valori casuali.
import random
# Importa il modulo sys per uscire dal programma in modo pulito.
import sys

# Importa pygame, la libreria principale per la grafica e il gioco.
import pygame
# Importa PlatformDirs per trovare la cartella dati utente corretta per ogni sistema operativo.
from platformdirs import PlatformDirs

# Importa le funzioni helper per trovare i percorsi di immagini e suoni.
from .resources import get_image, get_sound

# ───────────── SEZIONE 2: INIZIALIZZAZIONE DI PYGAME ─────────────

# Inizializza tutti i moduli di pygame necessari per il funzionamento del gioco.
pygame.init()
# Inizializza il sottosistema audio di pygame per la riproduzione di musica e suoni.
pygame.mixer.init()

# ───────────── SEZIONE 3: COSTANTI GLOBALI (CONFIGURAZIONE) ─────────────

# Imposta la larghezza della finestra di gioco in pixel.
WIDTH = 800
# Imposta l'altezza della finestra di gioco in pixel.
HEIGHT = 600
# Raccoglie larghezza e altezza in una tupla usata da pygame.
DIMENSIONS = (WIDTH, HEIGHT)
# Crea la finestra di gioco con le dimensioni definite e la rende visibile.
screen = pygame.display.set_mode(DIMENSIONS)
# Imposta il titolo visualizzato sulla barra del titolo della finestra.
pygame.display.set_caption("MissionOne - Boss Edition")

# ───────────── SEZIONE 4: DEFINIZIONE DEI COLORI ─────────────

# Colore bianco puro, usato per testi e bordi neutri.
WHITE = (255, 255, 255)
# Colore nero puro, usato per sfondi e ombre.
BLACK = (0, 0, 0)
# Colore giallo brillante, usato per punteggi e proiettili.
YELLOW = (255, 220, 0)
# Colore grigio scuro, usato come sfondo alternativo quando manca l'immagine.
GRAY = (40, 40, 40)
# Colore blu medio, usato come fallback per il giocatore.
BLUE = (70, 130, 220)
# Colore verde chiaro, usato per le barre della vita piena.
GREEN = (100, 200, 100)
# Colore rosso medio, usato per i danni e i nemici.
RED = (220, 80, 80)
# Colore ciano brillante, usato per l'effetto invincibilità.
CYAN = (0, 220, 220)
# Colore viola profondo, usato per il boss e i bottoni attivi.
PURPLE = (150, 50, 200)
# Colore rosa vivace, usato per il titolo del gioco.
PINK = (255, 100, 180)
# Colore lilla tenue, usato per i punteggi nella schermata game over.
LILAC = (200, 150, 255)

# ───────────── SEZIONE 5: IMPOSTAZIONI DI GIOCO ─────────────

# Crea il dizionario che raccoglie le impostazioni modificabili dall'utente.
settings = {
    # Volume iniziale impostato al 50%.
    "volume": 50,
    # Difficoltà iniziale impostata su 'base'.
    "difficulty": "base",
}

# Variabile globale che memorizza il punteggio più alto raggiunto.
HIGH_SCORE = 0

# ───────────── SEZIONE 6: GESTIONE AUDIO ─────────────

# Percorso completo del file musicale del menu principale.
MENU_MUSIC_FILE = get_sound("musica_home.mp3")
# Percorso completo del file musicale durante la partita.
GAME_MUSIC_FILE = get_sound("musica_gioco.mp3")

# Variabile per il suono del click, inizializzata a None finché non viene caricata.
click_sound = None


# Funzione helper che avvia la riproduzione di un file audio in loop opzionale.
def play_music(filename, loop=True):
    # Verifica se il file esiste sul disco prima di tentare di caricarlo.
    if os.path.exists(filename):
        # Blocco try per intercettare errori pygame durante il caricamento audio.
        try:
            # Carica il file musicale nel mixer di pygame.
            pygame.mixer.music.load(filename)
            # Imposta il volume del mixer usando il valore percentuale nelle impostazioni.
            pygame.mixer.music.set_volume(settings["volume"] / 100.0)
            # Avvia la riproduzione: -1 indica loop infinito, 0 indica riproduzione singola.
            pygame.mixer.music.play(-1 if loop else 0)
        # Cattura qualsiasi errore specifico di pygame durante la riproduzione.
        except pygame.error as e:
            # Stampa un messaggio diagnostico nella console per aiutare il debug.
            print(f"Errore audio con {filename}: {e}")
    # Se il file non esiste, avvisa lo sviluppatore senza crashare il programma.
    else:
        # Messaggio di avviso stampato nella console.
        print(f"File musicale non trovato: {filename}")


# ───────────── SEZIONE 7: CARICAMENTO RISORSE GRAFICHE ─────────────

# Funzione helper che carica un'immagine dal disco gestendo eventuali errori.
def load(path):
    # Controlla se il percorso indicato esiste effettivamente sul filesystem.
    if os.path.exists(path):
        # Blocco try per gestire errori di formato immagine non supportato.
        try:
            # Carica l'immagine e converte il canale alpha per prestazioni ottimali.
            return pygame.image.load(path).convert_alpha()
        # Se pygame non riesce a leggere il file, restituisce None silenziosamente.
        except pygame.error:
            # Ritorna None per segnalare il fallimento del caricamento.
            return None
    # Se il percorso non esiste, ritorna None senza lanciare eccezioni.
    return None


# Percorso del file audio per il suono del click sui bottoni.
click_sound_path = get_sound("click_sound.wav")
# Verifica se il file del suono click esiste prima di tentare il caricamento.
if os.path.exists(click_sound_path):
    # Blocco try per gestire errori nel caricamento dell'effetto sonoro.
    try:
        # Carica il suono come oggetto Sound di pygame per la riproduzione immediata.
        click_sound = pygame.mixer.Sound(click_sound_path)
    # Se il caricamento fallisce per qualsiasi motivo, mantiene click_sound a None.
    except:
        # Assegna None per indicare che il suono non è disponibile.
        click_sound = None

# ───────────── SEZIONE 8: GESTIONE HIGHSCORE SU DISCO ─────────────

# Usa PlatformDirs per trovare la cartella dati utente appropriata al sistema operativo corrente.
_dirs = PlatformDirs("missionone", "missionone")
# Estrae il percorso della directory dati come oggetto Path di pathlib.
_data_dir = _dirs.user_data_path
# Crea la directory ricorsivamente se non esiste ancora, senza errori se già presente.
_data_dir.mkdir(parents=True, exist_ok=True)
# Costruisce il percorso completo del file di testo che contiene il record.
HIGHSCORE_FILE = _data_dir / "highscore.txt"


# Funzione che legge il record salvato dal file e aggiorna la variabile globale.
def load_high_score():
    # Dichiara l'uso della variabile globale per poterla modificare dall'interno.
    global HIGH_SCORE
    # Blocco try per gestire il caso in cui il file non esiste ancora.
    try:
        # Apre il file in modalità lettura testuale.
        with open(HIGHSCORE_FILE, "r") as f:
            # Legge l'intero contenuto del file come stringa.
            content = f.read()
            # Verifica che il contenuto sia un numero intero valido.
            if content.isdigit():
                # Converte la stringa in intero e la assegna alla variabile globale.
                HIGH_SCORE = int(content)
            # Se il contenuto non è un numero puro, resetta il record a zero.
            else:
                # Imposta il record a zero come valore di default sicuro.
                HIGH_SCORE = 0
    # Gestisce sia il file mancante che valori non convertibili.
    except (FileNotFoundError, ValueError):
        # In caso di errore, il record vale zero.
        HIGH_SCORE = 0


# Funzione che salva il punteggio corrente se supera il record esistente.
def save_high_score(score):
    # Dichiara l'uso della variabile globale per aggiornarla.
    global HIGH_SCORE
    # Aggiorna solo se il punteggio attuale è strettamente maggiore del record.
    if score > HIGH_SCORE:
        # Aggiorna la variabile in memoria con il nuovo valore massimo.
        HIGH_SCORE = score
        # Blocco try per gestire errori di scrittura su disco (permessi, spazio).
        try:
            # Apre il file in scrittura, sovrascrivendo il contenuto precedente.
            with open(HIGHSCORE_FILE, "w") as f:
                # Scrive il nuovo record come stringa nel file.
                f.write(str(score))
        # Cattura qualsiasi errore di I/O durante la scrittura.
        except Exception as e:
            # Stampa il dettaglio dell'errore per facilitare il debug.
            print(f"Errore durante il salvataggio del record: {e}")


# ───────────── SEZIONE 9: CARICAMENTO ASSET GRAFICI ─────────────

# Tenta di caricare l'immagine di sfondo tramite il resolver di risorse.
bg_full_path = get_image("background.jpg")
# Carica l'immagine dal percorso risolto usando la funzione helper.
bg = load(bg_full_path)
# Se il caricamento è avvenuto con successo, scala l'immagine alle dimensioni della finestra.
if bg:
    # Scala lo sfondo per coprire esattamente l'intera finestra di gioco.
    background = pygame.transform.scale(bg, (WIDTH, HEIGHT))
# Se l'immagine non è disponibile, usa None come indicatore di assenza.
else:
    # Imposta background a None per usare il colore di fallback durante il disegno.
    background = None

# Carica l'immagine del razzo del giocatore.
razzo = load(get_image("razzo.png"))
# Se caricata, scala il razzo alla dimensione desiderata per il giocatore.
if razzo:
    # Imposta il razzo a 180x180 pixel.
    razzo = pygame.transform.scale(razzo, (180, 180))

# Carica l'icona dell'ingranaggio per le impostazioni.
settings_icon = load(get_image("settings.png"))
# Se caricata, scala l'icona alle dimensioni del bottone impostazioni.
if settings_icon:
    # Imposta l'icona a 70x70 pixel.
    settings_icon = pygame.transform.scale(settings_icon, (70, 70))

# Carica le quattro immagini per i power-up collezionabili.
boost_power_img = load(get_image("potenza.png"))
# Immagine del cuore per il power-up vita.
boost_health_img = load(get_image("cuore.png"))
# Immagine del fulmine per il power-up velocità.
boost_speed_img = load(get_image("velocità.png"))
# Immagine dello scudo per il power-up invincibilità.
boost_invincibility_img = load(get_image("invincibilità.png"))

# Scala l'immagine del boost potenza se disponibile.
if boost_power_img:
    boost_power_img = pygame.transform.scale(boost_power_img, (50, 50))
# Scala l'immagine del boost vita se disponibile.
if boost_health_img:
    boost_health_img = pygame.transform.scale(boost_health_img, (50, 50))
# Scala l'immagine del boost velocità se disponibile.
if boost_speed_img:
    boost_speed_img = pygame.transform.scale(boost_speed_img, (50, 50))
# Scala l'immagine del boost invincibilità se disponibile.
if boost_invincibility_img:
    boost_invincibility_img = pygame.transform.scale(boost_invincibility_img, (50, 50))

# Carica l'immagine del nemico base.
enemy_img = load(get_image("nemico.png"))
# Scala il nemico se caricato correttamente.
if enemy_img:
    # Imposta il nemico a 60x60 pixel.
    enemy_img = pygame.transform.scale(enemy_img, (60, 60))

# Carica l'immagine del missile nemico.
missile_img = load(get_image("missile.png"))
# Scala il missile se caricato correttamente.
if missile_img:
    # Imposta il missile a 50x20 pixel.
    missile_img = pygame.transform.scale(missile_img, (50, 20))

# Carica l'immagine del Boss finale.
boss_img = load(get_image("boss.png"))
# Scala il boss se caricato correttamente.
if boss_img:
    # Imposta il boss a 150x150 pixel.
    boss_img = pygame.transform.scale(boss_img, (150, 150))

# ───────────── SEZIONE 10: FUNZIONI DI DISEGNO ─────────────


# Funzione che disegna il giocatore con eventuale effetto invincibilità.
def draw_player(surface, p, current_time):
    # Controlla se il buff invincibilità è ancora attivo confrontando i tempi.
    if current_time < p["invincibility_end_time"]:
        # Crea un effetto lampeggiante alternando visibilità ogni 100ms.
        if (current_time // 100) % 2 == 0:
            # Definisce il rettangolo dello scudo leggermente più grande del giocatore.
            rect = (p["x"] - 4, p["y"] - 4, p["width"] + 8, p["height"] + 8)
            # Disegna il bordo ciano dello scudo con angoli arrotondati.
            pygame.draw.rect(surface, CYAN, rect, 4, border_radius=10)
    # Se l'immagine del razzo è disponibile, la usa per il disegno.
    if razzo:
        # Disegna il razzo alla posizione corrente del giocatore.
        surface.blit(razzo, (p["x"], p["y"]))
    # Se l'immagine non è disponibile, usa un rettangolo di fallback.
    else:
        # Disegna un rettangolo blu come placeholder visivo del giocatore.
        pygame.draw.rect(surface, BLUE, (p["x"], p["y"], p["width"], p["height"]))


# Funzione che disegna un nemico con la sua barra della vita.
def draw_enemy(surface, e):
    # Se l'immagine del nemico è caricata, la visualizza alla sua posizione.
    if enemy_img:
        # Disegna l'immagine del nemico.
        surface.blit(enemy_img, (e["x"], e["y"]))
    # Altrimenti usa un rettangolo rosso come rappresentazione di fallback.
    else:
        # Disegna il rettangolo rosso del nemico.
        pygame.draw.rect(surface, RED, (e["x"], e["y"], e["width"], e["height"]))
    # Calcola il rapporto vita corrente/massima per la barra.
    health_ratio = e["health"] / e["max_health"]
    # Imposta la larghezza totale della barra della vita del nemico.
    bar_width = 40
    # Imposta l'altezza della barra della vita.
    bar_height = 5
    # Calcola la coordinata X centrando la barra rispetto al nemico.
    bar_x = e["x"] + (e["width"] - bar_width) // 2
    # Posiziona la barra sopra il nemico con un margine di 10 pixel.
    bar_y = e["y"] - 10
    # Disegna lo sfondo rosso della barra (rappresenta la vita mancante).
    pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
    # Disegna la porzione verde proporzionale alla vita rimanente.
    pygame.draw.rect(surface, GREEN, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))


# Funzione che disegna il Boss con la sua barra della vita prominente.
def draw_boss(surface, b):
    # Se l'immagine del boss è disponibile, la visualizza alla sua posizione.
    if boss_img:
        # Disegna l'immagine del boss.
        surface.blit(boss_img, (b["x"], b["y"]))
    # Se non è disponibile, disegna forme geometriche come fallback visivo.
    else:
        # Disegna il rettangolo scuro del corpo del boss.
        pygame.draw.rect(surface, BLACK, (b["x"], b["y"], b["width"], b["height"]))
        # Disegna il bordo viola per distinguere il boss dagli altri elementi.
        pygame.draw.rect(surface, PURPLE, (b["x"], b["y"], b["width"], b["height"]), 4)
    # Calcola il rapporto vita per determinare quanto della barra colorare.
    health_ratio = b["health"] / b["max_health"]
    # La barra del boss è più larga di quella dei nemici normali.
    bar_width = 120
    # L'altezza è anche maggiore per indicare l'importanza del boss.
    bar_height = 12
    # Centra la barra orizzontalmente rispetto al boss.
    bar_x = b["x"] + (b["width"] - bar_width) // 2
    # Posiziona la barra sopra il boss con un margine di 20 pixel.
    bar_y = b["y"] - 20
    # Disegna lo sfondo rosso della barra vita del boss.
    pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
    # Disegna la vita rimanente del boss in verde.
    pygame.draw.rect(surface, GREEN, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
    # Aggiunge un bordo bianco per rendere la barra più leggibile.
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)


# Funzione che disegna un power-up con la sua immagine o colore di fallback.
def draw_boost(surface, b):
    # Inizializza le variabili per immagine e colore prima del controllo del tipo.
    img = None
    # Colore di fallback bianco usato solo se nessuna immagine è disponibile.
    color = WHITE
    # Seleziona immagine e colore in base al tipo di power-up.
    if b["type"] == "power":
        # Usa l'immagine della potenza e il colore giallo.
        img = boost_power_img
        color = YELLOW
    elif b["type"] == "health":
        # Usa l'immagine del cuore e il colore verde.
        img = boost_health_img
        color = GREEN
    elif b["type"] == "speed":
        # Usa l'immagine della velocità e il colore blu.
        img = boost_speed_img
        color = BLUE
    elif b["type"] == "invincibility":
        # Usa l'immagine dell'invincibilità e il colore ciano.
        img = boost_invincibility_img
        color = CYAN
    # Se l'immagine specifica è disponibile, la disegna alla posizione del boost.
    if img:
        # Visualizza l'immagine del power-up.
        surface.blit(img, (b["x"], b["y"]))
    # Se nessuna immagine è caricata, disegna un cerchio colorato come fallback.
    else:
        # Disegna un cerchio colorato centrato nel rettangolo del boost.
        pygame.draw.circle(surface, color, (int(b["x"] + 25), int(b["y"] + 25)), 25)


# Funzione che disegna l'HUD con vita, punteggio e stato dei power-up.
def draw_hud(surface, player, score, font, small_font, current_time):
    # Posizione X del bordo sinistro della barra della vita.
    bar_x = 20
    # Posizione Y del bordo superiore della barra della vita.
    bar_y = 20
    # Larghezza totale della barra della vita.
    bar_width = 250
    # Altezza della barra della vita.
    bar_height = 25
    # Disegna lo sfondo scuro della barra per creare contrasto visivo.
    pygame.draw.rect(surface, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
    # Calcola i pixel occupati dalla vita proporzionalmente al massimo.
    health_w = int((player["health"] / player["max_health"]) * bar_width)
    # Scegli il colore della barra in base alla percentuale di vita rimasta.
    if player["health"] > 50:
        # Verde per vita alta (oltre 50%).
        health_color = GREEN
    elif player["health"] > 25:
        # Giallo per vita media (tra 25% e 50%).
        health_color = YELLOW
    else:
        # Rosso per vita bassa (sotto 25%), segnale di pericolo.
        health_color = RED
    # Disegna la porzione colorata della barra vita.
    pygame.draw.rect(surface, health_color, (bar_x, bar_y, health_w, bar_height), border_radius=5)
    # Disegna il bordo bianco della barra per definirne i contorni.
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 3, border_radius=5)
    # Renderizza il testo numerico della vita corrente.
    health_text = font.render(f"VITA: {player['health']}", True, WHITE)
    # Posiziona il testo della vita immediatamente a destra della barra.
    surface.blit(health_text, (bar_x + bar_width + 10, bar_y))
    # Renderizza il testo del moltiplicatore di potenza corrente.
    pow_text = font.render(f"POW: x{player['power']}", True, YELLOW)
    # Disegna il testo della potenza sotto la barra vita.
    surface.blit(pow_text, (20, 55))
    # Renderizza il testo del punteggio corrente.
    score_text = font.render(f"SCORE: {score}", True, YELLOW)
    # Disegna il punteggio sotto il testo della potenza.
    surface.blit(score_text, (20, 85))
    # Posizione X del pannello dei power-up attivi nell'angolo in alto a destra.
    panel_x = WIDTH - 200
    # Posizione Y del pannello, vicino al bordo superiore dello schermo.
    panel_y = 10
    # Crea una superficie con canale alpha per effetto trasparenza del pannello.
    panel = pygame.Surface((190, 130), pygame.SRCALPHA)
    # Riempie il pannello con nero semi-trasparente per leggibilità.
    panel.fill((0, 0, 0, 140))
    # Disegna il pannello sullo schermo con un piccolo offset per il bordo.
    surface.blit(panel, (panel_x - 5, panel_y - 5))
    # Lista di tuple con i dati di ciascun power-up da mostrare nel pannello.
    boost_data = [
        ("power", boost_power_img, YELLOW, "POW", "power_end_time"),
        ("speed", boost_speed_img, BLUE, "VEL", "speed_end_time"),
        ("invincibility", boost_invincibility_img, CYAN, "INV", "invincibility_end_time"),
        ("health", boost_health_img, GREEN, "VITA", None),
    ]
    # Itera su ogni power-up per disegnarne l'icona e il timer nel pannello.
    for i, (btype, img, color, label, timer_key) in enumerate(boost_data):
        # Calcola la posizione Y della riga corrente nel pannello.
        row_y = panel_y + i * 30
        # Se l'immagine del boost è disponibile, mostra l'icona ridimensionata.
        if img:
            # Scala l'icona a 24x24 per adattarla al pannello compatto.
            small = pygame.transform.scale(img, (24, 24))
            # Disegna l'icona del boost nella riga corrente del pannello.
            surface.blit(small, (panel_x, row_y))
        # Per il boost vita non c'è timer, quindi mostra semplicemente "PRONTO".
        if btype == "health":
            # Testo fisso per il boost vita che non ha durata.
            txt = small_font.render(f"{label}: PRONTO", True, color)
        else:
            # Legge il tempo di fine del buff dal dizionario del giocatore.
            end_time = player[timer_key]
            # Se il buff è ancora attivo, mostra il countdown in secondi.
            if current_time < end_time:
                # Calcola i secondi rimanenti con un decimale di precisione.
                seconds_left = (end_time - current_time) / 1000.0
                # Renderizza il countdown con colore attivo.
                txt = small_font.render(f"{label}: {seconds_left:.1f}s", True, color)
            # Se il buff è scaduto, mostra "OFF" con colore grigio spento.
            else:
                # Renderizza il testo OFF in grigio per indicare assenza del buff.
                txt = small_font.render(f"{label}: OFF", True, (80, 80, 80))
        # Disegna il testo del power-up accanto all'icona con un piccolo offset verticale.
        surface.blit(txt, (panel_x + 30, row_y + 3))


# ───────────── SEZIONE 11: SCHERMATE UI ─────────────


# Funzione che mostra e gestisce il menu delle impostazioni.
def show_settings():
    # Crea l'orologio per limitare il framerate a 60fps.
    clock = pygame.time.Clock()
    # Font grande per il titolo della schermata impostazioni.
    title_font = pygame.font.Font(None, 80)
    # Font medio per le etichette delle singole impostazioni.
    label_font = pygame.font.Font(None, 45)
    # Font per il testo dei bottoni interattivi.
    button_font = pygame.font.Font(None, 40)
    # Rettangolo della barra di scorrimento del volume.
    slider_rect = pygame.Rect(200, 200, 400, 10)
    # Rettangolo della maniglia trascinabile dello slider.
    slider_handle = pygame.Rect(0, 0, 20, 30)
    # Flag che indica se l'utente sta trascinando la maniglia del volume.
    dragging = False
    # Rettangolo del bottone per selezionare la difficoltà base.
    button_base = pygame.Rect(200, 320, 180, 60)
    # Rettangolo del bottone per selezionare la difficoltà avanzata.
    button_avanzato = pygame.Rect(420, 320, 180, 60)
    # Rettangolo del bottone per tornare al menu principale.
    button_back = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)
    # Loop principale della schermata impostazioni.
    while True:
        # Posizione corrente del cursore del mouse.
        mouse_pos = pygame.mouse.get_pos()
        # Flag click reset a False ogni frame.
        click = False
        # Cicla tutti gli eventi in coda.
        for event in pygame.event.get():
            # Se l'utente chiude la finestra, termina il programma.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Rileva la pressione del mouse per click e inizio drag.
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                dragging = False
            # Rileva il rilascio del mouse per terminare il drag.
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
        # Disegna lo sfondo o il colore di fallback.
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(GRAY)
        # Crea un overlay semi-trasparente scuro per migliorare la leggibilità.
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Riempie l'overlay con grigio scuro semi-opaco.
        overlay.fill((40, 40, 40, 200))
        # Applica l'overlay sopra lo sfondo.
        screen.blit(overlay, (0, 0))
        # Renderizza il titolo "IMPOSTAZIONI" in viola.
        title = title_font.render("IMPOSTAZIONI", True, PURPLE)
        # Centra e disegna il titolo in alto nella schermata.
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        # Renderizza l'etichetta "Volume" sopra lo slider.
        volume_label = label_font.render("Volume", True, PURPLE)
        # Posiziona l'etichetta volume a sinistra dello slider.
        screen.blit(volume_label, (200, 150))
        # Renderizza il valore percentuale del volume corrente.
        volume_value = label_font.render(f"{settings['volume']}%", True, PURPLE)
        # Posiziona il valore percentuale a destra dello slider.
        screen.blit(volume_value, (620, 150))
        # Disegna la barra bianca dello slider del volume.
        pygame.draw.rect(screen, WHITE, slider_rect, border_radius=5)
        # Posiziona la maniglia proporzionalmente al volume corrente.
        slider_handle.centerx = slider_rect.x + (settings["volume"] / 100) * slider_rect.width
        # Centra verticalmente la maniglia sulla barra.
        slider_handle.centery = slider_rect.centery
        # Se l'utente clicca sulla maniglia, attiva il trascinamento.
        if slider_handle.collidepoint(mouse_pos) and click:
            dragging = True
        # Se il trascinamento è attivo, aggiorna il volume in base alla posizione del mouse.
        if dragging:
            # Limita la posizione X all'interno della barra dello slider.
            new_x = max(slider_rect.x, min(mouse_pos[0], slider_rect.right))
            # Calcola il nuovo volume come percentuale della larghezza barra.
            settings["volume"] = int(((new_x - slider_rect.x) / slider_rect.width) * 100)
            # Aggiorna la posizione visiva della maniglia.
            slider_handle.centerx = new_x
            # Applica immediatamente il nuovo volume alla musica in riproduzione.
            pygame.mixer.music.set_volume(settings["volume"] / 100.0)
        # Disegna la maniglia viola dello slider.
        pygame.draw.rect(screen, PURPLE, slider_handle, border_radius=5)
        # Renderizza l'etichetta della sezione difficoltà.
        diff_label = label_font.render("Difficoltà", True, PURPLE)
        # Posiziona l'etichetta sopra i bottoni di selezione difficoltà.
        screen.blit(diff_label, (200, 270))
        # Determina se la difficoltà corrente è "base".
        is_base = settings["difficulty"] == "base"
        # Usa verde se selezionato, grigio scuro altrimenti.
        color_base = GREEN if is_base else (80, 80, 80)
        # Disegna il rettangolo del bottone BASE.
        pygame.draw.rect(screen, color_base, button_base, border_radius=10)
        # Disegna il bordo del bottone, verde se attivo, bianco altrimenti.
        pygame.draw.rect(screen, GREEN if is_base else WHITE, button_base, 4, border_radius=10)
        # Renderizza il testo "BASE" centrato nel bottone.
        txt_base = button_font.render("BASE", True, WHITE)
        # Disegna il testo centrato nel bottone BASE.
        screen.blit(txt_base, (button_base.centerx - txt_base.get_width() // 2, button_base.centery - txt_base.get_height() // 2))
        # Determina se la difficoltà corrente è "avanzato".
        is_avanzato = settings["difficulty"] == "avanzato"
        # Usa rosso se selezionato, grigio scuro altrimenti.
        color_avanzato = RED if is_avanzato else (80, 80, 80)
        # Disegna il rettangolo del bottone AVANZATO.
        pygame.draw.rect(screen, color_avanzato, button_avanzato, border_radius=10)
        # Disegna il bordo del bottone, rosso se attivo, bianco altrimenti.
        pygame.draw.rect(screen, RED if is_avanzato else WHITE, button_avanzato, 4, border_radius=10)
        # Renderizza il testo "AVANZATO" centrato nel bottone.
        txt_avanzato = button_font.render("AVANZATO", True, WHITE)
        # Disegna il testo centrato nel bottone AVANZATO.
        screen.blit(txt_avanzato, (button_avanzato.centerx - txt_avanzato.get_width() // 2, button_avanzato.centery - txt_avanzato.get_height() // 2))
        # Gestisce i click sui bottoni difficoltà e indietro.
        if click:
            # Se clicca BASE, aggiorna la difficoltà nelle impostazioni.
            if button_base.collidepoint(mouse_pos):
                if click_sound: click_sound.play()
                settings["difficulty"] = "base"
            # Se clicca AVANZATO, aggiorna la difficoltà nelle impostazioni.
            if button_avanzato.collidepoint(mouse_pos):
                if click_sound: click_sound.play()
                settings["difficulty"] = "avanzato"
        # Determina se il mouse è sopra il bottone INDIETRO per l'effetto hover.
        hover_back = button_back.collidepoint(mouse_pos)
        # Usa viola per hover, bianco altrimenti.
        back_color = PURPLE if hover_back else WHITE
        # Disegna il rettangolo del bottone INDIETRO.
        pygame.draw.rect(screen, back_color, button_back, border_radius=10)
        # Disegna il bordo bianco del bottone INDIETRO.
        pygame.draw.rect(screen, WHITE, button_back, 3, border_radius=10)
        # Renderizza il testo "INDIETRO" con colore invertito rispetto allo sfondo.
        txt_back = button_font.render("INDIETRO", True, WHITE if hover_back else BLACK)
        # Disegna il testo centrato nel bottone INDIETRO.
        screen.blit(txt_back, (button_back.centerx - txt_back.get_width() // 2, button_back.centery - txt_back.get_height() // 2))
        # Se l'utente clicca INDIETRO, suona il click e torna al menu.
        if hover_back and click:
            if click_sound: click_sound.play()
            return
        # Aggiorna il display con tutto ciò che è stato disegnato.
        pygame.display.flip()
        # Limita il loop a 60 fotogrammi al secondo.
        clock.tick(60)


# ───────────── SEZIONE 12: FUNZIONE MAIN ─────────────
# La funzione main contiene tutta la logica applicativa principale:
# - Menu principale con animazioni
# - Schermata Game Over
# - Loop di gioco completo (spawn, movimento, collisioni, rendering)


# Funzione principale che gestisce l'intera applicazione.
def main():
    # Carica il record salvato dal disco prima di avviare qualsiasi schermata.
    load_high_score()

    # ── SETUP FONT ──
    # Font grande per il titolo nel menu principale.
    title_font = pygame.font.Font(None, 120)
    # Font medio per i bottoni del menu.
    button_font = pygame.font.Font(None, 50)
    # Font per i testi di gioco come vita e punteggio nell'HUD.
    hud_font = pygame.font.Font(None, 32)
    # Font piccolo per il pannello dei power-up nell'HUD.
    small_font = pygame.font.Font(None, 28)
    # Font enorme per messaggi di avviso come "ONDATA N".
    big_font = pygame.font.Font(None, 100)
    # Font per i titoli nelle schermate di game over.
    go_font_big = pygame.font.Font(None, 100)
    # Font medio per punteggi e record nel game over.
    go_font_small = pygame.font.Font(None, 50)

    # ── STATO APPLICAZIONE ──
    # Stato iniziale dell'applicazione: parte sempre dal menu principale.
    state = "MENU"
    # Orologio globale usato in ogni loop per limitare il framerate.
    clock = pygame.time.Clock()

    # Loop principale dell'intera applicazione, gestisce le transizioni di stato.
    while True:

        # ════════════════════════════════════════════════════════════
        # STATO: MENU PRINCIPALE
        # ════════════════════════════════════════════════════════════
        if state == "MENU":
            # Avvia la musica del menu in loop continuo.
            play_music(MENU_MUSIC_FILE)

            # Rettangolo del bottone ENTER per avviare la partita.
            button_enter = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 150, 300, 70)
            # Rettangolo del bottone impostazioni in alto a destra.
            button_settings = pygame.Rect(WIDTH - 90, 20, 70, 70)

            # Carica la versione grande del razzo usata come decorazione nel menu.
            razzo_menu = load(get_image("razzo.png"))
            # Se caricata, scala il razzo a una versione grande per il menu.
            if razzo_menu:
                razzo_menu = pygame.transform.scale(razzo_menu, (350, 350))

            # Contatore di tempo usato per l'animazione oscillante del razzo.
            t = 0

            # Loop interno del menu: continua finché l'utente non sceglie un'azione.
            while state == "MENU":
                # Posizione corrente del cursore del mouse.
                mouse_pos = pygame.mouse.get_pos()
                # Flag click reset a False ogni frame.
                click = False

                # Cicla tutti gli eventi pygame in coda.
                for event in pygame.event.get():
                    # Se l'utente chiude la finestra, termina l'applicazione.
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    # Controlla la pressione dei tasti da tastiera.
                    if event.type == pygame.KEYDOWN:
                        # Se premi INVIO dal menu, avvia subito la partita.
                        if event.key == pygame.K_RETURN:
                            state = "GAME"
                    # Controlla il click del mouse.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click = True

                # ── DISEGNO MENU ──
                # Disegna lo sfondo del menu se disponibile, altrimenti colore grigio.
                if background:
                    screen.blit(background, (0, 0))
                else:
                    screen.fill(GRAY)

                # Calcola l'offset verticale sinusoidale per l'animazione del razzo.
                if razzo_menu:
                    # Calcola lo spostamento verticale oscillante basato sul tempo.
                    offset = math.sin(t / 20) * 10
                    # Centra il razzo orizzontalmente nella finestra.
                    draw_x = WIDTH // 2 - razzo_menu.get_width() // 2
                    # Centra il razzo verticalmente aggiungendo l'offset oscillante.
                    draw_y = HEIGHT // 2 - razzo_menu.get_height() // 2 + offset
                    # Disegna il razzo animato nella posizione calcolata.
                    screen.blit(razzo_menu, (draw_x, draw_y))

                # Renderizza il titolo "MissionOne" in rosa.
                title_surf = title_font.render("MissionOne", True, PINK)
                # Renderizza l'ombra del titolo in nero per il rilievo.
                shadow_surf = title_font.render("MissionOne", True, BLACK)
                # Crea il rettangolo del titolo centrato in alto.
                title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
                # Disegna prima l'ombra con offset di 4 pixel.
                screen.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
                # Disegna il titolo sopra l'ombra.
                screen.blit(title_surf, title_rect)

                # Renderizza e centra il testo del record in viola.
                record_text = button_font.render(f"RECORD: {HIGH_SCORE}", True, PURPLE)
                # Disegna il record sotto il titolo, centrato orizzontalmente.
                screen.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, 150))

                # Determina se il mouse è sopra il bottone ENTER per l'effetto hover.
                hover_enter = button_enter.collidepoint(mouse_pos)
                # Colore viola per hover, grigio chiaro altrimenti.
                color_e = PURPLE if hover_enter else (200, 200, 200)
                # Colore bordo viola scuro per hover, grigio medio altrimenti.
                border_e = (100, 0, 150) if hover_enter else (150, 150, 150)
                # Disegna il rettangolo del bottone ENTER con angoli arrotondati.
                pygame.draw.rect(screen, color_e, button_enter, border_radius=15)
                # Disegna il bordo del bottone ENTER.
                pygame.draw.rect(screen, border_e, button_enter, 4, border_radius=15)
                # Renderizza il testo "ENTER" con colore invertito per contrasto.
                txt_e = button_font.render("ENTER", True, WHITE if hover_enter else BLACK)
                # Centra il testo nel bottone ENTER.
                screen.blit(txt_e, (button_enter.centerx - txt_e.get_width() // 2, button_enter.centery - txt_e.get_height() // 2))

                # Determina se il mouse è sopra il bottone impostazioni.
                hover_settings = button_settings.collidepoint(mouse_pos)
                # Se l'icona ingranaggio è disponibile, la disegna con eventuale tinta hover.
                if settings_icon:
                    if hover_settings:
                        # Crea una copia dell'icona per applicare la tinta viola senza modificare l'originale.
                        colored_icon = settings_icon.copy()
                        # Applica la tinta viola sopra l'icona con blending additivo.
                        colored_icon.fill(PURPLE, special_flags=pygame.BLEND_RGBA_ADD)
                        # Disegna l'icona con tinta hover.
                        screen.blit(colored_icon, button_settings)
                    else:
                        # Disegna l'icona senza tinta nello stato normale.
                        screen.blit(settings_icon, button_settings)

                # Gestisce i click sui bottoni del menu.
                if click:
                    # Click su ENTER: suono e avvio partita.
                    if hover_enter:
                        if click_sound: click_sound.play()
                        state = "GAME"
                    # Click su impostazioni: suono e apertura pannello settings.
                    if hover_settings:
                        if click_sound: click_sound.play()
                        show_settings()

                # Aggiorna il display con tutto ciò che è stato disegnato.
                pygame.display.flip()
                # Limita il loop a 60 FPS.
                clock.tick(60)
                # Incrementa il contatore per l'animazione oscillante del razzo.
                t += 1

        # ════════════════════════════════════════════════════════════
        # STATO: PARTITA
        # ════════════════════════════════════════════════════════════
        elif state == "GAME":
            # Avvia la musica di gioco in loop continuo.
            play_music(GAME_MUSIC_FILE)

            # ── INIZIALIZZAZIONE STATO GIOCATORE ──
            # Calcola la velocità base in base alla difficoltà selezionata.
            base_speed = 5 if settings["difficulty"] == "base" else 7
            # Crea il dizionario del giocatore con tutti i suoi attributi.
            player = {
                "x": 100, "y": HEIGHT // 2,         # Posizione iniziale.
                "width": 180, "height": 180,          # Dimensioni hitbox.
                "base_speed": base_speed,              # Velocità base senza buff.
                "speed": base_speed,                   # Velocità corrente (modificabile dai buff).
                "health": 100, "max_health": 100,      # Vita attuale e massima.
                "power": 1,                            # Moltiplicatore danno proiettili.
                "fire_rate": 300,                      # Millisecondi tra uno sparo e l'altro.
                "last_shot": 0,                        # Timestamp dell'ultimo sparo effettuato.
                "power_end_time": 0,                   # Timestamp fine buff potenza.
                "speed_end_time": 0,                   # Timestamp fine buff velocità.
                "invincibility_end_time": 0,           # Timestamp fine buff invincibilità.
            }

            # ── LISTE OGGETTI DI GIOCO ──
            # Lista dei proiettili sparati dal giocatore attualmente attivi.
            bullets = []
            # Lista dei nemici attualmente presenti sullo schermo.
            enemies = []
            # Lista dei proiettili sparati dai nemici attualmente attivi.
            enemy_bullets = []
            # Lista dei missili orizzontali attualmente presenti.
            missiles = []
            # Lista dei power-up attualmente presenti sullo schermo.
            boosts = []
            # Lista dei missili del boss attualmente attivi.
            boss_missiles = []

            # ── STATO BOSS ──
            # Boss inizialmente assente; viene creato al raggiungimento della soglia punteggio.
            boss = None
            # Numero dell'ondata boss corrente, aumenta ad ogni boss sconfitto.
            wave_number = 1
            # Soglia di punteggio alla quale apparirà il prossimo boss.
            next_boss_score = 3000
            # Flag che indica se è attiva la schermata di avviso ondata boss.
            warning_active = False
            # Timestamp di inizio dell'avviso ondata boss.
            warning_start_time = 0

            # ── STATO PARTITA ──
            # Punteggio corrente del giocatore, inizia da zero.
            score = 0
            # Contatore di frame per lo spawn dei nemici.
            enemy_spawn_timer = 0
            # Contatore di frame per lo spawn dei missili.
            missile_spawn_timer = 0
            # Contatore di frame per lo spawn dei power-up.
            boost_spawn_timer = 0
            # Contatore di frame per l'effetto flash rosso quando il giocatore subisce danno.
            damage_flash = 0
            # Flag che mantiene il loop di gioco attivo.
            running = True

            # ── LOOP DI GIOCO ──
            # Continua finché il giocatore non muore o non preme ESC.
            while running:
                # Ottieni il timestamp corrente in millisecondi.
                current_time = pygame.time.get_ticks()

                # ── GESTIONE EVENTI ──
                for event in pygame.event.get():
                    # Se l'utente chiude la finestra, interrompi la partita.
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    # Controlla i tasti speciali premuti.
                    if event.type == pygame.KEYDOWN:
                        # ESC durante la partita torna al menu principale.
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            state = "MENU"

                # Se ESC è stato premuto, salta il resto del loop.
                if not running:
                    break

                # ── INPUT CONTINUO ──
                # Legge lo stato di tutti i tasti in questo frame.
                keys = pygame.key.get_pressed()

                # ── LOGICA AVVISO BOSS ──
                # Controlla se il punteggio ha raggiunto la soglia del prossimo boss.
                if score >= next_boss_score and boss is None and not warning_active:
                    # Attiva la schermata di avviso ondata.
                    warning_active = True
                    # Registra il momento in cui l'avviso è iniziato.
                    warning_start_time = current_time
                    # Aggiorna la soglia per il boss successivo.
                    next_boss_score += 3000

                # Controlla se l'avviso è durato abbastanza a lungo.
                if warning_active and current_time - warning_start_time > 3000:
                    # Disattiva l'avviso.
                    warning_active = False
                    # Calcola la vita del boss in base al numero ondata.
                    boss_hp = 1000 + (wave_number - 1) * 400
                    # Calcola il danno dei missili del boss in base all'ondata.
                    boss_dmg = 15 + (wave_number - 1) * 3
                    # Calcola la velocità dei missili del boss in base all'ondata.
                    boss_ms = 5.0 + (wave_number - 1) * 0.5
                    # Calcola il ritardo di sparo del boss, decresce con le ondate.
                    boss_sd = max(400, 900 - wave_number * 100)
                    # Crea il dizionario del boss con tutti i parametri calcolati.
                    boss = {
                        "x": WIDTH + 50, "y": HEIGHT // 2 - 75,    # Posizione iniziale fuori schermo.
                        "width": 150, "height": 150,                 # Dimensioni del boss.
                        "speed": 2,                                  # Velocità di movimento verticale.
                        "health": boss_hp, "max_health": boss_hp,    # Vita totale.
                        "damage": boss_dmg,                          # Danno per colpo.
                        "missile_speed": boss_ms,                    # Velocità missili.
                        "last_shot": current_time,                   # Timestamp ultimo sparo.
                        "shoot_delay": boss_sd,                      # Millisecondi tra spari.
                        "direction": 1,                              # 1 = giù, -1 = su.
                        "entering": True,                            # True mentre entra da destra.
                    }
                    # Incrementa il numero ondata per il boss successivo.
                    wave_number += 1
                    # Elimina tutti i nemici e proiettili presenti durante l'ondata boss.
                    enemies.clear()
                    enemy_bullets.clear()
                    missiles.clear()
                    boosts.clear()

                # ── AGGIORNAMENTO GIOCATORE ──
                # Muovi il giocatore su in base all'input, rispettando il bordo superiore.
                if keys[pygame.K_UP] and player["y"] > 0:
                    player["y"] -= player["speed"]
                # Muovi il giocatore giù in base all'input, rispettando il bordo inferiore.
                if keys[pygame.K_DOWN] and player["y"] < HEIGHT - player["height"]:
                    player["y"] += player["speed"]
                # Muovi il giocatore a sinistra, rispettando il bordo sinistro.
                if keys[pygame.K_LEFT] and player["x"] > 0:
                    player["x"] -= player["speed"]
                # Muovi il giocatore a destra, rispettando il bordo destro.
                if keys[pygame.K_RIGHT] and player["x"] < WIDTH - player["width"]:
                    player["x"] += player["speed"]

                # Applica il buff velocità se ancora attivo, altrimenti resetta.
                if current_time < player["speed_end_time"]:
                    # Buff attivo: velocità aumentata e rateo di fuoco più alto.
                    player["speed"] = player["base_speed"] + 3
                    player["fire_rate"] = 100
                else:
                    # Buff scaduto: ripristina i valori base.
                    player["speed"] = player["base_speed"]
                    player["fire_rate"] = 300

                # Applica il buff potenza se ancora attivo, altrimenti resetta.
                if current_time < player["power_end_time"]:
                    # Buff attivo: potenza di fuoco triplicata.
                    player["power"] = 3
                else:
                    # Buff scaduto: potenza normale.
                    player["power"] = 1

                # ── SPARO GIOCATORE ──
                # Controlla se SPAZIO è premuto e se è trascorso abbastanza tempo dall'ultimo sparo.
                if keys[pygame.K_SPACE] and current_time - player["last_shot"] > player["fire_rate"]:
                    # Aggiorna il timestamp dell'ultimo sparo.
                    player["last_shot"] = current_time
                    # Crea un nuovo proiettile partendo dal bordo destro del giocatore.
                    bullets.append({
                        "x": player["x"] + player["width"],          # Parte dal bordo destro.
                        "y": player["y"] + player["height"] // 2,    # Centrato verticalmente.
                        "width": 15 * player["power"],               # Larghezza proporzionale alla potenza.
                        "height": 8,                                  # Altezza fissa.
                        "speed": 12,                                  # Velocità costante.
                        "power": player["power"],                     # Potenza corrente.
                    })

                # ── SPAWN NEMICI E OGGETTI (solo fuori ondata boss) ──
                if not warning_active and boss is None:
                    # Incrementa il timer di spawn nemici.
                    enemy_spawn_timer += 1
                    # Spawn un nemico ogni 100 frame in base (70 in avanzato).
                    if enemy_spawn_timer > (100 if settings["difficulty"] == "base" else 70):
                        # Crea un nemico con posizione casuale fuori schermo.
                        enemies.append({
                            "x": WIDTH + random.randint(0, 100),        # Entra da destra.
                            "y": random.randint(50, HEIGHT - 110),       # Altezza casuale.
                            "width": 60, "height": 60,                   # Dimensioni nemico.
                            "speed": 3 if settings["difficulty"] == "base" else 5,  # Velocità.
                            "last_shot": current_time,                   # Timestamp sparo.
                            "shoot_delay": random.randint(1000, 2500),   # Ritardo sparo casuale.
                            "health": 100, "max_health": 100,            # Vita piena.
                        })
                        # Resetta il timer di spawn nemici.
                        enemy_spawn_timer = 0

                    # Incrementa il timer di spawn missili.
                    missile_spawn_timer += 1
                    # Spawn un missile ogni 180 frame in base (130 in avanzato).
                    if missile_spawn_timer > (180 if settings["difficulty"] == "base" else 130):
                        # Crea un missile con posizione casuale fuori schermo.
                        missiles.append({
                            "x": WIDTH + random.randint(0, 100),        # Entra da destra.
                            "y": random.randint(50, HEIGHT - 100),       # Altezza casuale.
                            "width": 50, "height": 20,                   # Dimensioni visive.
                            "speed": 4 if settings["difficulty"] == "base" else 6,  # Velocità.
                        })
                        # Resetta il timer di spawn missili.
                        missile_spawn_timer = 0

                    # Incrementa il timer di spawn power-up.
                    boost_spawn_timer += 1
                    # Spawn un power-up ogni 250 frame.
                    if boost_spawn_timer > 250:
                        # Crea un power-up di tipo casuale tra i quattro disponibili.
                        boosts.append({
                            "x": WIDTH + random.randint(0, 100),                           # Entra da destra.
                            "y": random.randint(100, HEIGHT - 150),                         # Altezza casuale.
                            "width": 50, "height": 50,                                      # Dimensioni icona.
                            "speed": 3,                                                      # Velocità costante.
                            "type": random.choice(["power", "health", "speed", "invincibility"]),  # Tipo casuale.
                        })
                        # Resetta il timer di spawn power-up.
                        boost_spawn_timer = 0

                # ── AGGIORNAMENTO BOSS ──
                if boss:
                    # Se il boss sta ancora entrando da destra, muovilo verso sinistra.
                    if boss["entering"]:
                        if boss["x"] > WIDTH - boss["width"] - 50:
                            # Avanza il boss verso la posizione di combattimento.
                            boss["x"] -= 3
                        else:
                            # Il boss ha raggiunto la posizione, inizia a combattere.
                            boss["entering"] = False
                    # Movimento verticale del boss quando non sta entrando.
                    if not boss["entering"]:
                        # Sposta il boss verticalmente nella direzione corrente.
                        boss["y"] += boss["speed"] * boss["direction"]
                        # Inverte la direzione se tocca il bordo superiore.
                        if boss["y"] <= 20:
                            boss["direction"] = 1
                        # Inverte la direzione se tocca il bordo inferiore.
                        elif boss["y"] + boss["height"] >= HEIGHT - 20:
                            boss["direction"] = -1
                    # Sparo boss: controlla il cooldown e spara se pronto.
                    if not boss["entering"] and current_time - boss["last_shot"] > boss["shoot_delay"]:
                        # Aggiorna il timestamp dell'ultimo sparo del boss.
                        boss["last_shot"] = current_time
                        # Calcola il centro del giocatore come target del missile.
                        tx = player["x"] + player["width"] // 2
                        ty = player["y"] + player["height"] // 2
                        # Calcola la differenza di posizione tra boss e giocatore.
                        dx = tx - boss["x"]
                        dy = ty - (boss["y"] + boss["height"] // 2)
                        # Calcola la distanza euclidea tra boss e giocatore.
                        dist = math.hypot(dx, dy)
                        # Normalizza il vettore direzione se la distanza non è zero.
                        if dist != 0:
                            dx /= dist
                            dy /= dist
                        else:
                            # Direzione default verso sinistra se il boss è sovrapposto al giocatore.
                            dx, dy = -1, 0
                        # Crea il missile del boss con direzione normalizzata verso il giocatore.
                        boss_missiles.append({
                            "x": boss["x"],                              # Parte dal bordo sinistro del boss.
                            "y": boss["y"] + boss["height"] // 2,        # Centrato verticalmente.
                            "width": 30, "height": 15,                   # Dimensioni visive.
                            "dx": dx, "dy": dy,                          # Direzione normalizzata.
                            "speed": boss["missile_speed"],              # Velocità del missile.
                            "damage": boss["damage"],                    # Danno per impatto.
                        })

                # ── MOVIMENTO PROIETTILI GIOCATORE ──
                for b in bullets[:]:
                    # Muovi il proiettile verso destra.
                    b["x"] += b["speed"]
                    # Rimuovi il proiettile se esce dal bordo destro dello schermo.
                    if b["x"] > WIDTH:
                        bullets.remove(b)

                # ── MOVIMENTO NEMICI ──
                for e in enemies[:]:
                    # Muovi il nemico verso sinistra.
                    e["x"] -= e["speed"]
                    # Controlla se il nemico può sparare in base al cooldown.
                    if current_time - e["last_shot"] > e["shoot_delay"]:
                        # Aggiorna il timestamp dello sparo del nemico.
                        e["last_shot"] = current_time
                        # Assegna un nuovo ritardo di sparo casuale.
                        e["shoot_delay"] = random.randint(1000, 2500)
                        # Crea un proiettile nemico centrato verticalmente.
                        enemy_bullets.append({
                            "x": e["x"],                        # Parte dal bordo sinistro del nemico.
                            "y": e["y"] + e["height"] // 2,     # Centrato verticalmente.
                            "width": 10, "height": 10,          # Dimensioni proiettile nemico.
                            "speed": 7,                         # Velocità costante verso sinistra.
                        })
                    # Rimuovi il nemico se esce completamente dal bordo sinistro.
                    if e["x"] < -e["width"]:
                        enemies.remove(e)

                # ── MOVIMENTO PROIETTILI NEMICI ──
                for eb in enemy_bullets[:]:
                    # Muovi il proiettile verso sinistra.
                    eb["x"] -= eb["speed"]
                    # Rimuovi il proiettile se esce dal bordo sinistro.
                    if eb["x"] < 0:
                        enemy_bullets.remove(eb)

                # ── MOVIMENTO MISSILI ──
                for m in missiles[:]:
                    # Muovi il missile verso sinistra.
                    m["x"] -= m["speed"]
                    # Rimuovi il missile se esce completamente dal bordo sinistro.
                    if m["x"] < -m["width"] - 20:
                        missiles.remove(m)

                # ── MOVIMENTO POWER-UP ──
                for b in boosts[:]:
                    # Muovi il power-up verso sinistra.
                    b["x"] -= b["speed"]
                    # Rimuovi il power-up se esce dal bordo sinistro.
                    if b["x"] < -b["width"]:
                        boosts.remove(b)

                # ── MOVIMENTO MISSILI BOSS ──
                for hm in boss_missiles[:]:
                    # Muovi il missile nella direzione normalizzata moltiplicata per la velocità.
                    hm["x"] += hm["dx"] * hm["speed"]
                    hm["y"] += hm["dy"] * hm["speed"]
                    # Rimuovi il missile se esce dai bordi della finestra.
                    if hm["x"] < -50 or hm["x"] > WIDTH + 50 or hm["y"] < -50 or hm["y"] > HEIGHT + 50:
                        if hm in boss_missiles:
                            boss_missiles.remove(hm)

                # ── CALCOLO HITBOX GIOCATORE ──
                # Usa una hitbox ridotta al centro del razzo per maggiore precisione.
                player_rect = pygame.Rect(player["x"] + 20, player["y"] + 55, 140, 70)

                # ── COLLISIONI PROIETTILI -> BOSS ──
                if boss:
                    # Rettangolo del boss per il rilevamento collisioni.
                    boss_rect = pygame.Rect(boss["x"], boss["y"], boss["width"], boss["height"])
                    for b in bullets[:]:
                        # Rettangolo del proiettile.
                        b_rect = pygame.Rect(b["x"], b["y"], b["width"], b["height"])
                        # Controlla la collisione tra proiettile e boss.
                        if b_rect.colliderect(boss_rect):
                            # Rimuovi il proiettile che ha colpito.
                            if b in bullets: bullets.remove(b)
                            # Calcola il danno: triplo se potenziato, normale altrimenti.
                            damage = 100 if b["power"] > 1 else 50
                            # Riduci la vita del boss del danno calcolato.
                            boss["health"] -= damage
                            # Se la vita del boss arriva a zero, eliminalo.
                            if boss["health"] <= 0:
                                # Assegna il bonus punti per la sconfitta del boss.
                                score += 500
                                # Rimuovi il boss dal gioco.
                                boss = None
                                # Elimina tutti i missili del boss rimasti.
                                boss_missiles.clear()
                            # Interrompi il ciclo dopo il primo impatto per evitare duplicati.
                            break

                # ── COLLISIONI PROIETTILI -> NEMICI ──
                for b in bullets[:]:
                    for e in enemies[:]:
                        # Controlla collisione AABB tra proiettile e nemico.
                        if (b["x"] < e["x"] + e["width"] and b["x"] + b["width"] > e["x"] and
                                b["y"] < e["y"] + e["height"] and b["y"] + b["height"] > e["y"]):
                            # Rimuovi il proiettile dal gioco.
                            if b in bullets: bullets.remove(b)
                            # Danno potenziato o normale.
                            damage = 100 if b["power"] > 1 else 50
                            # Riduce la vita del nemico.
                            e["health"] -= damage
                            # Se il nemico è eliminato, rimuovilo e assegna punti.
                            if e["health"] <= 0:
                                if e in enemies: enemies.remove(e)
                                score += 10

                # ── COLLISIONI NEMICI -> GIOCATORE (solo senza invincibilità) ──
                if current_time >= player["invincibility_end_time"]:
                    # Controlla collisione con i proiettili nemici.
                    for eb in enemy_bullets[:]:
                        # Hitbox leggermente ridotta del proiettile nemico.
                        eb_rect = pygame.Rect(eb["x"] - 5, eb["y"] - 5, 10, 10)
                        if player_rect.colliderect(eb_rect):
                            # Rimuovi il proiettile nemico.
                            if eb in enemy_bullets: enemy_bullets.remove(eb)
                            # Applica danno al giocatore.
                            player["health"] -= 10
                            # Attiva il flash di danno per 12 frame.
                            damage_flash = 12

                    # Controlla collisione con i missili orizzontali.
                    for m in missiles[:]:
                        # Hitbox ridotta del missile per maggiore precisione.
                        m_rect = pygame.Rect(m["x"] + 15, m["y"] + 6, 20, 8)
                        if player_rect.colliderect(m_rect):
                            # Rimuovi il missile collidente.
                            if m in missiles: missiles.remove(m)
                            # I missili fanno più danno dei proiettili nemici.
                            player["health"] -= 20
                            # Flash più lungo per danno maggiore.
                            damage_flash = 20

                    # Controlla collisione con i missili del boss.
                    for hm in boss_missiles[:]:
                        # Hitbox del missile boss.
                        hm_rect = pygame.Rect(hm["x"], hm["y"], hm["width"], hm["height"])
                        if player_rect.colliderect(hm_rect):
                            # Rimuovi il missile boss collidente.
                            if hm in boss_missiles: boss_missiles.remove(hm)
                            # Il danno del boss è variabile e dipende dall'ondata.
                            player["health"] -= hm["damage"]
                            # Flash medio per danno boss.
                            damage_flash = 15

                # ── COLLISIONI POWER-UP -> GIOCATORE ──
                for b in boosts[:]:
                    # Rettangolo del power-up.
                    b_rect = pygame.Rect(b["x"], b["y"], b["width"], b["height"])
                    if player_rect.colliderect(b_rect):
                        # Rimuovi il power-up raccolto.
                        if b in boosts: boosts.remove(b)
                        # Durata dei buff temporanei in millisecondi.
                        duration = 7000
                        # Applica l'effetto in base al tipo di power-up.
                        if b["type"] == "power":
                            # Attiva il buff potenza per 7 secondi.
                            player["power_end_time"] = current_time + duration
                        elif b["type"] == "speed":
                            # Attiva il buff velocità per 7 secondi.
                            player["speed_end_time"] = current_time + duration
                        elif b["type"] == "invincibility":
                            # Attiva il buff invincibilità per 7 secondi.
                            player["invincibility_end_time"] = current_time + duration
                        elif b["type"] == "health":
                            # Ripristina 30 punti vita senza superare il massimo.
                            player["health"] = min(player["health"] + 30, player["max_health"])
                        # Assegna 5 punti per ogni power-up raccolto.
                        score += 5

                # ── PUNTEGGIO PROGRESSIVO ──
                # Incrementa il punteggio di 1 ogni frame (circa 60 punti al secondo).
                score += 1
                # Assicura che la vita non scenda sotto zero.
                player["health"] = max(player["health"], 0)
                # Se la vita arriva a zero, termina il loop di gioco.
                if player["health"] <= 0:
                    running = False

                # ── RENDERING ──
                # Disegna lo sfondo o il colore di fallback grigio.
                if background:
                    screen.blit(background, (0, 0))
                else:
                    screen.fill(GRAY)

                # Disegna il flash di danno rosso semi-trasparente se attivo.
                if damage_flash > 0:
                    # Crea una superficie trasparente per il flash.
                    flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    # Calcola l'alpha proporzionale ai frame rimanenti.
                    alpha = int(120 * (damage_flash / 20))
                    # Riempie con rosso semi-trasparente.
                    flash_surf.fill((220, 0, 0, alpha))
                    # Applica il flash sopra lo sfondo.
                    screen.blit(flash_surf, (0, 0))
                    # Decrementa il contatore del flash.
                    damage_flash -= 1

                # Disegna tutti i proiettili del giocatore come ellissi gialle.
                for b in bullets:
                    pygame.draw.ellipse(screen, YELLOW, (b["x"], b["y"], b["width"], b["height"]))

                # Disegna tutti i nemici con la loro barra vita.
                for e in enemies:
                    draw_enemy(screen, e)

                # Disegna i proiettili nemici come piccoli cerchi rossi.
                for eb in enemy_bullets:
                    pygame.draw.circle(screen, (255, 50, 50), (int(eb["x"]), int(eb["y"])), 5)

                # Disegna i missili con immagine o forma geometrica di fallback.
                for m in missiles:
                    if missile_img:
                        # Usa l'immagine del missile se disponibile.
                        screen.blit(missile_img, (m["x"], m["y"]))
                    else:
                        # Calcola il centro verticale del missile per il fallback.
                        cy = m["y"] + m["height"] // 2
                        # Disegna il corpo ellittico grigio del missile.
                        pygame.draw.ellipse(screen, (160, 160, 170), (m["x"], m["y"] + 3, m["width"], m["height"] - 6))
                        # Disegna il cono di fuoco arancione dietro il missile.
                        pygame.draw.polygon(screen, (255, 180, 0), [
                            (m["x"] + m["width"] + 10, cy - 4),
                            (m["x"] + m["width"] + 10, cy + 4),
                            (m["x"] + m["width"] + 22, cy),
                        ])

                # Disegna tutti i power-up presenti.
                for b in boosts:
                    draw_boost(screen, b)

                # Disegna il boss e i suoi missili se presente.
                if boss:
                    # Usa la funzione dedicata per il boss con barra vita.
                    draw_boss(screen, boss)
                    # Disegna i missili del boss come ellissi viola.
                    for hm in boss_missiles:
                        pygame.draw.ellipse(screen, (150, 0, 150), (hm["x"], hm["y"], hm["width"], hm["height"]))

                # Disegna il giocatore con eventuale effetto invincibilità.
                draw_player(screen, player, current_time)
                # Disegna l'HUD con vita, punteggio e stato power-up.
                draw_hud(screen, player, score, hud_font, small_font, current_time)

                # Mostra il messaggio di avviso ondata boss lampeggiante.
                if warning_active:
                    # Renderizza il testo dell'ondata in rosso.
                    warn_text = big_font.render(f"ONDATA {wave_number}", True, RED)
                    # Fa lampeggiare il testo ogni 200ms.
                    if (current_time // 200) % 2 == 0:
                        # Centra il testo nella finestra.
                        text_rect = warn_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        # Disegna il testo di avviso al centro dello schermo.
                        screen.blit(warn_text, text_rect)

                # Disegna il suggerimento sui controlli in basso centrato.
                hint = small_font.render("← ↑ ↓ → Muovi  |  SPAZIO Spara  |  ESC Menu", True, (180, 180, 180))
                # Posiziona il suggerimento nella parte bassa della finestra.
                screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))

                # Aggiorna il display con tutto ciò che è stato disegnato.
                pygame.display.flip()
                # Limita il loop a 60 FPS per un gameplay fluido e coerente.
                clock.tick(60)

            # Al termine del loop di gioco, aggiorna lo stato in base all'uscita.
            if state != "MENU":
                # Solo se non è ESC, vai al game over.
                state = "GAMEOVER"

        # ════════════════════════════════════════════════════════════
        # STATO: GAME OVER
        # ════════════════════════════════════════════════════════════
        elif state == "GAMEOVER":
            # Ferma la musica di gioco appena si entra nel game over.
            pygame.mixer.music.stop()
            # Salva il punteggio finale se supera il record precedente.
            save_high_score(score)

            # Rettangolo del bottone RIPROVA nel game over.
            button_retry = pygame.Rect(WIDTH // 2 - 150, 420, 140, 60)
            # Rettangolo del bottone MENU nel game over.
            button_menu_go = pygame.Rect(WIDTH // 2 + 10, 420, 140, 60)

            # Loop della schermata game over.
            while state == "GAMEOVER":
                # Posizione corrente del cursore del mouse.
                mouse_pos = pygame.mouse.get_pos()
                # Flag click reset a False ogni frame.
                click = False

                # Cicla tutti gli eventi pygame in coda.
                for event in pygame.event.get():
                    # Se l'utente chiude la finestra, termina l'applicazione.
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    # Rileva click del mouse.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click = True

                # Riempie lo sfondo di nero per il game over.
                screen.fill(BLACK)

                # Renderizza il testo "GAME OVER" in rosso grande.
                go_text = go_font_big.render("GAME OVER", True, RED)
                # Centra e disegna il titolo game over.
                screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, 120))

                # Disegna una linea separatrice orizzontale bianca.
                pygame.draw.line(screen, WHITE, (100, 230), (WIDTH - 100, 230), 2)

                # Mostra "NUOVO RECORD!" se il punteggio attuale è il nuovo massimo.
                if score == HIGH_SCORE and score > 0:
                    # Messaggio nuovo record in giallo.
                    new_rec = go_font_small.render("NUOVO RECORD!", True, YELLOW)
                    # Centra e disegna il messaggio.
                    screen.blit(new_rec, (WIDTH // 2 - new_rec.get_width() // 2, 260))
                    # Punteggio finale in lilla sotto il messaggio record.
                    sc_text = go_font_small.render(f"PUNTEGGIO: {score}", True, LILAC)
                    # Centra e disegna il punteggio.
                    screen.blit(sc_text, (WIDTH // 2 - sc_text.get_width() // 2, 310))
                else:
                    # Punteggio finale in lilla se non è record.
                    sc_text = go_font_small.render(f"PUNTEGGIO: {score}", True, LILAC)
                    # Centra e disegna il punteggio.
                    screen.blit(sc_text, (WIDTH // 2 - sc_text.get_width() // 2, 260))
                    # Record attuale in lilla sotto il punteggio.
                    rec_text = go_font_small.render(f"RECORD: {HIGH_SCORE}", True, LILAC)
                    # Centra e disegna il record.
                    screen.blit(rec_text, (WIDTH // 2 - rec_text.get_width() // 2, 310))

                # Determina se il mouse è sopra il bottone RIPROVA.
                hover_retry = button_retry.collidepoint(mouse_pos)
                # Colore viola per hover, bianco altrimenti.
                retry_color = PURPLE if hover_retry else WHITE
                # Disegna il rettangolo del bottone RIPROVA.
                pygame.draw.rect(screen, retry_color, button_retry, border_radius=10)
                # Disegna il bordo bianco del bottone.
                pygame.draw.rect(screen, WHITE, button_retry, 3, border_radius=10)
                # Testo con colore invertito per contrasto.
                txt_retry = button_font.render("RIPROVA", True, WHITE if hover_retry else BLACK)
                # Centra e disegna il testo nel bottone RIPROVA.
                screen.blit(txt_retry, (button_retry.centerx - txt_retry.get_width() // 2, button_retry.centery - txt_retry.get_height() // 2))

                # Determina se il mouse è sopra il bottone MENU.
                hover_menu_go = button_menu_go.collidepoint(mouse_pos)
                # Colore viola per hover, bianco altrimenti.
                menu_go_color = PURPLE if hover_menu_go else WHITE
                # Disegna il rettangolo del bottone MENU.
                pygame.draw.rect(screen, menu_go_color, button_menu_go, border_radius=10)
                # Disegna il bordo bianco del bottone.
                pygame.draw.rect(screen, WHITE, button_menu_go, 3, border_radius=10)
                # Testo con colore invertito per contrasto.
                txt_menu_go = button_font.render("MENU", True, WHITE if hover_menu_go else BLACK)
                # Centra e disegna il testo nel bottone MENU.
                screen.blit(txt_menu_go, (button_menu_go.centerx - txt_menu_go.get_width() // 2, button_menu_go.centery - txt_menu_go.get_height() // 2))

                # Gestisce i click sui bottoni del game over.
                if click:
                    # Click su RIPROVA: suono e nuova partita.
                    if hover_retry:
                        if click_sound: click_sound.play()
                        state = "GAME"
                    # Click su MENU: suono e ritorno al menu principale.
                    if hover_menu_go:
                        if click_sound: click_sound.play()
                        state = "MENU"

                # Aggiorna il display.
                pygame.display.flip()
                # Limita a 60 FPS.
                clock.tick(60)


# ───────────── SEZIONE 13: PUNTO DI INGRESSO ─────────────

# Punto di ingresso: esegue main solo se il file è avviato direttamente.
if __name__ == "__main__":
    # Carica il record e avvia il ciclo principale dell'applicazione.
    main()