# witch_memo_full.py
# Witch's Memo — Flashcards Battle (Improved, purple/white theme)
# Single-file runnable. Designed to be robust to missing assets (fallbacks).
# Features: menu, story, deck select (create/delete), play (drag-swipe),
# transitions (fade), BGM manager (safe), autosave index + achievements,
# hints, simple particle VFX, clamp story index, end screen with restart.
#
# Requires: pygame
# pip install pygame

import pygame, sys, os, json, random, math, time

# -----------------------------
# Config / Theme
# -----------------------------
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Colors (purple / white theme)
PURPLE = (110, 44, 140)
LIGHT_PURPLE = (165, 120, 200)
WHITE = (250, 250, 252)
TEXT = (18, 18, 20)
ACCENT = (200, 170, 255)
DANGER = (200, 80, 80)

DECKS_DIR = "decksdemo"
INDEX_FILE = os.path.join(DECKS_DIR, "decks_index.json")
ACHIEV_FILE = "achievements.json"

CARD_IMAGE = os.path.join("Image", "card.png")
BG_IMAGE = os.path.join("Image", "forestbackground.jpg")
SFX_DIR = "SFX"
MUSIC_DIR = "Music"

MAX_LOG = 6

# -----------------------------
# Filesystem helpers
# -----------------------------
def ensure_dirs():
    os.makedirs(DECKS_DIR, exist_ok=True)

def safe_load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def safe_save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Save error:", e)

# -----------------------------
# Deck helpers
# -----------------------------
def sanitize_filename(name):
    base = "".join(c if c.isalnum() else "_" for c in name).strip("_")
    if not base:
        base = "deck"
    return base.lower() + ".json"

def ensure_default_deck():
    idx = safe_load_json(INDEX_FILE, None)
    if idx is None:
        idx = {"Default": "default.json"}
        safe_save_json(INDEX_FILE, idx)
    default_path = os.path.join(DECKS_DIR, "default.json")
    if not os.path.exists(default_path):
        sample = [
            {"question": "Apple", "answer": "แอปเปิ้ล"},
            {"question": "Dog", "answer": "สุนัข"},
            {"question": "Cat", "answer": "แมว"},
            {"question": "Water", "answer": "น้ำ"},
        ]
        safe_save_json(default_path, sample)
    return idx

def load_index():
    return safe_load_json(INDEX_FILE, {})

def save_index(idx): safe_save_json(INDEX_FILE, idx)

def load_deck(fname):
    path = os.path.join(DECKS_DIR, fname)
    return safe_load_json(path, [])

def save_deck(fname, cards):
    path = os.path.join(DECKS_DIR, fname)
    safe_save_json(path, cards)

# -----------------------------
# Init pygame & resources
# -----------------------------
pygame.init()
pygame.mixer.init()  # best effort; if fails, program still runs
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Witch's Memo — Flashcards Battle")
clock = pygame.time.Clock()

# Fonts (fallback-aware)
def load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except Exception:
        return pygame.font.SysFont("arial", size)

FONT_PATH = os.path.join("Font", "SansThai.ttf")
FONT_BIG = load_font(FONT_PATH, 56)
FONT_MED = load_font(FONT_PATH, 30)
FONT_SM = load_font(FONT_PATH, 20)
FONT_XS = load_font(FONT_PATH, 14)

# Background image fallback
if os.path.exists(BG_IMAGE):
    try:
        BG = pygame.image.load(BG_IMAGE).convert()
        BG = pygame.transform.smoothscale(BG, (WIDTH, HEIGHT))
    except Exception:
        BG = None
else:
    BG = None

# Card image fallback
CARD_W, CARD_H = 420, 560
if os.path.exists(CARD_IMAGE):
    try:
        CARD_IMG = pygame.image.load(CARD_IMAGE).convert_alpha()
        CARD_IMG = pygame.transform.smoothscale(CARD_IMG, (CARD_W, CARD_H))
    except Exception:
        CARD_IMG = None
else:
    CARD_IMG = None

if CARD_IMG is None:
    # create placeholder card
    CARD_IMG = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
    pygame.draw.rect(CARD_IMG, WHITE, CARD_IMG.get_rect(), border_radius=18)
    pygame.draw.rect(CARD_IMG, PURPLE, CARD_IMG.get_rect(), 4, border_radius=18)
    label = load_font(FONT_PATH, 28).render("CARD", True, PURPLE)
    CARD_IMG.blit(label, label.get_rect(center=CARD_IMG.get_rect().center))

CARD_RECT = CARD_IMG.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
CARD_CENTER = CARD_RECT.center
CARD_MASK = pygame.mask.from_surface(CARD_IMG)

# -----------------------------
# Audio manager (safe)
# -----------------------------
class MusicManager:
    def __init__(self):
        self.current = None
        self.volume = 0.5
    def play(self, path, loop=-1, fade_ms=600):
        try:
            if path is None: return
            if self.current == path: return
            # fadeout current
            pygame.mixer.music.fadeout(fade_ms)
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loop)
            self.current = path
        except Exception as e:
            # ignore audio errors
            # print("Music error:", e)
            self.current = None
    def stop(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
music_manager = MusicManager()

def load_sfx(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

SFX_CLICK = load_sfx(os.path.join(SFX_DIR, "Click.mp3"))
SFX_LAUGH = load_sfx(os.path.join(SFX_DIR, "OMG Laugh.mp3"))

# -----------------------------
# Game state
# -----------------------------
STATE_MENU = "menu"
STATE_SELECT = "select"
STATE_STORY = "story"
STATE_PLAY = "play"
STATE_VICTORY = "victory"
STATE_DEFEAT = "defeat"

state = STATE_MENU

# gameplay
max_hp = 100
player_hp = enemy_hp = max_hp
score = 0
streak = 0
game_log = []

deck_cards = []
deck_pointer = 0
wrong_cards = []
current_card = None

# dragging/swipe
dragging = False
drag_offset = (0,0)
rotation = 0.0
SWIPE_THRESHOLD = 120

reveal = False
reveal_until = 0

selected_deck_key = None
selected_deck_file = None

# UI / Deck create
adding_mode = False
adding_text = ""

# story
story_pages = [
    "บทนำ — พระจันทร์ครอบฟ้า\n\nในคืนที่ท้องฟ้าทอประกายเป็นฝอยเงิน...\nแม่มดผู้เรียนรู้ต้องฟื้นตำราคำสาป...",
    "คาถาและคำสาป\n\nตำราเก่าเก็บคำศัพท์แห่งพลังไว้ จงศึกษาและท่องจำให้แม่นยำ",
    "การเดินทางเริ่มต้น\n\nคุณออกสำรวจป่า เก็บสมุนไพร ทำยา และต่อสู้กับมอนสเตอร์แห่งความลืม",
    "บทเรียนจากบรรพบุรุษ\n\nทุกชุดการ์ดพาไปสู่คาถาใหม่ จงอย่าท้อถอย"
]

# achievements / autosave
achievements = safe_load_json(ACHIEV_FILE, {"unlocked": []})
index_map = {}
ensure_dirs()
index_map = ensure_default_deck()  # ensures default exists and returns index map

# hints
HINTS_DAY = [
    "การจดจำเพียงอย่างเดียวอาจไม่ได้ช่วยอะไร จงมั่นฝึกฝนด้วย!",
    "ทุกการจดจำคือการเรียนรู้!",
    "การทบทวนทีละนิดนั้นชนะความลืม!",
    "แฟลชการ์ดคือเวทมนตร์ที่ทำให้ความรู้คงทน"
]
HINTS_DARK = [
    "Why? ... you came back.",
    "You shouldn't forget me...",
    "Do you really want to leave, witch?",
    "01000001 01101100 01110100"
]

# particles simple
particles = []

# -----------------------------
# Utility functions
# -----------------------------
def push_log(text):
    global game_log
    game_log.append(text)
    if len(game_log) > MAX_LOG:
        game_log.pop(0)

def reset_battle():
    global player_hp, enemy_hp, score, streak, game_log, deck_pointer, wrong_cards, current_card, reveal
    player_hp = enemy_hp = max_hp
    score = 0
    streak = 0
    game_log = []
    deck_pointer = 0
    wrong_cards = []
    current_card = None
    reveal = False
    CARD_RECT.center = CARD_CENTER

def next_card_or_victory():
    global current_card, deck_pointer, deck_cards, wrong_cards, state
    # prevent out-of-range when deck empty
    if not deck_cards:
        push_log("เด็คนี้ยังไม่มีการ์ด — กรุณาเพิ่มการ์ดหรือเลือกเด็คอื่น")
        state = STATE_SELECT
        return
    if deck_pointer < len(deck_cards):
        current_card = deck_cards[deck_pointer]
        deck_pointer += 1
    else:
        if wrong_cards:
            deck_cards[:] = wrong_cards.copy()
            random.shuffle(deck_cards)
            wrong_cards.clear()
            deck_pointer = 0
            current_card = deck_cards[deck_pointer]
            deck_pointer += 1
            push_log("สับการ์ดที่ไม่รู้ใหม่")
        else:
            current_card = None
            state = STATE_VICTORY

def process_known():
    global enemy_hp, score, streak, reveal, reveal_until
    crit = 1.0
    if random.random() < 0.08:  # critical 8%
        crit = 2.0
    dmg = int((18 + streak*3) * crit)
    enemy_hp = max(0, enemy_hp - dmg)
    gain = int(90 + streak*10)
    score += gain
    streak += 1
    push_log(f"รู้ — คุณโจมตีมอนสเตอร์ -{dmg}HP (+{gain})")
    reveal = True
    reveal_until = pygame.time.get_ticks() + 900
    spawn_particles(CARD_RECT.centerx, CARD_RECT.centery, color=ACCENT)

def process_unknown():
    global player_hp, score, streak, wrong_cards, reveal, reveal_until
    dmg = 20
    player_hp = max(0, player_hp - dmg)
    score = max(0, score - 50)
    if current_card: wrong_cards.append(current_card)
    streak = 0
    push_log(f"ไม่รู้ — มอนสเตอร์โจมตีคุณ -{dmg}HP (-50)")
    reveal = True
    reveal_until = pygame.time.get_ticks() + 900
    spawn_particles(CARD_RECT.centerx, CARD_RECT.centery, color=DANGER)

def lerp(a,b,t): return a + (b-a) * t

# -----------------------------
# Particles (very simple)
# -----------------------------
def spawn_particles(x,y,count=12,color=ACCENT):
    for _ in range(count):
        angle = random.random() * math.pi * 2
        speed = random.uniform(1.5, 4.5)
        particles.append({
            "pos":[x,y],
            "vel":[math.cos(angle)*speed, math.sin(angle)*speed],
            "life": random.randint(30, 70),
            "color": color,
            "size": random.randint(2,5)
        })

def update_particles():
    for p in particles[:]:
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        p["vel"][1] += 0.08  # gravity
        p["life"] -= 1
        p["size"] *= 0.99
        if p["life"] <= 0 or p["size"] < 0.5:
            particles.remove(p)

def draw_particles(surface):
    for p in particles:
        pygame.draw.circle(surface, p["color"], (int(p["pos"][0]), int(p["pos"][1])), int(max(1, p["size"])))

# -----------------------------
# Transition (fade in/out) — draws scene snapshot and fades white -> scene
# -----------------------------
def transition_to(next_state, music_path=None, fade_color=WHITE, speed=10):
    # snapshot current screen
    snapshot = screen.copy()
    fade_s = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
    fade_s.fill(fade_color)
    alpha = 0
    start_vol = pygame.mixer.music.get_volume() if pygame.mixer.get_init() else 0.5

    # fade-in (to color)
    while alpha < 255:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                safe_save_json(ACHIEV_FILE, achievements)
                pygame.quit(); sys.exit()
        screen.blit(snapshot, (0,0))
        fade_s.set_alpha(alpha)
        screen.blit(fade_s, (0,0))
        pygame.display.flip()
        alpha += speed
        # fade music volume
        try:
            pygame.mixer.music.set_volume(max(0, start_vol * (1 - alpha/255)))
        except Exception:
            pass
        clock.tick(FPS)

    # switch music
    if music_path:
        if os.path.exists(music_path):
            music_manager.play(music_path)
    # Draw the first frame of next state (to show behind the fade)
    render_state_once(next_state)

    # fade-out (color -> scene)
    while alpha > 0:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                safe_save_json(ACHIEV_FILE, achievements)
                pygame.quit(); sys.exit()
        # render_state_once(next_state)  # already drawn once; we redraw each time to ensure dynamic background
        render_state_once(next_state)
        fade_s.set_alpha(alpha)
        screen.blit(fade_s, (0,0))
        pygame.display.flip()
        alpha -= speed
        clock.tick(FPS)

    # finally switch to the requested state
    global state
    state = next_state

def render_state_once(st):
    # draws one frame of given state (used during transitions)
    if st == STATE_MENU:
        draw_main_menu(draw_now=True)
    elif st == STATE_SELECT:
        draw_select_deck(index_map, draw_now=True)
    elif st == STATE_STORY:
        draw_story(story_index, draw_now=True)
    elif st == STATE_PLAY:
        draw_battle_ui(draw_now=True)
    elif st == STATE_VICTORY:
        draw_end_screen(True, draw_now=True)
    elif st == STATE_DEFEAT:
        draw_end_screen(False, draw_now=True)
    else:
        screen.fill(WHITE)

# -----------------------------
# Draw UI functions (draw_now flag used by transition)
# -----------------------------
def draw_text_center(text, font, color, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH//2, y))
    screen.blit(surf, rect)
    return rect

def draw_main_menu(draw_now=False):
    if BG: screen.blit(BG, (0,0))
    else: screen.fill(PURPLE)
    draw_text_center("Witch's Memo — Flashcards Battle", FONT_BIG, WHITE, 90)
    bx, by, bw, bh = WIDTH//2 - 220, 190, 440, 72
    story_r = pygame.Rect(bx, by, bw, bh)
    free_r = pygame.Rect(bx, by+110, bw, bh)
    quit_r = pygame.Rect(bx, by+220, bw, bh)

    pygame.draw.rect(screen, ACCENT, story_r, border_radius=10)
    pygame.draw.rect(screen, ACCENT, free_r, border_radius=10)
    pygame.draw.rect(screen, (240,140,160), quit_r, border_radius=10)
    pygame.draw.rect(screen, (30,10,40), story_r, 3, border_radius=10)
    pygame.draw.rect(screen, (30,10,40), free_r, 3, border_radius=10)
    pygame.draw.rect(screen, (30,10,40), quit_r, 3, border_radius=10)

    screen.blit(FONT_MED.render("Story Mode", True, TEXT), FONT_MED.render("Story Mode", True, TEXT).get_rect(center=story_r.center))
    screen.blit(FONT_MED.render("Free Style (Choose Deck)", True, TEXT), FONT_MED.render("Free Style (Choose Deck)", True, TEXT).get_rect(center=free_r.center))
    screen.blit(FONT_MED.render("Quit", True, TEXT), FONT_MED.render("Quit", True, TEXT).get_rect(center=quit_r.center))

    if draw_now: return story_r, free_r, quit_r
    return story_r, free_r, quit_r

def draw_select_deck(idx_map, draw_now=False):
    screen.fill(WHITE)
    draw_text_center("Select Deck (Click to Play) — N to create new | Del to delete", FONT_MED, TEXT, 60)
    rects = []
    y = 120
    for key in idx_map:
        r = pygame.Rect(120, y, 760, 56)
        pygame.draw.rect(screen, (240,230,255), r, border_radius=8)
        pygame.draw.rect(screen, (30,10,40), r, 2, border_radius=8)
        screen.blit(FONT_MED.render(str(key), True, TEXT), (r.x + 14, r.y + 10))
        del_btn = pygame.Rect(r.right - 80, r.y + 8, 64, 40)
        pygame.draw.rect(screen, (255,170,170), del_btn, border_radius=6)
        screen.blit(FONT_XS.render("Del", True, TEXT), del_btn.move(14,8))
        rects.append((r, del_btn, key))
        y += 84
    if draw_now: return rects
    return rects

def draw_add_deck_input(prompt, text):
    screen.fill(WHITE)
    draw_text_center(prompt, FONT_MED, TEXT, 120)
    box = pygame.Rect(140, 200, 760, 56)
    pygame.draw.rect(screen, (245,245,245), box, border_radius=8)
    pygame.draw.rect(screen, TEXT, box, 2, border_radius=8)
    t = FONT_MED.render(text, True, TEXT)
    screen.blit(t, (box.x + 12, box.y + 12))
    hint = FONT_XS.render("Enter = create | Esc = cancel", True, (100,100,100))
    screen.blit(hint, (box.x, box.bottom + 12))

def draw_story(page_index, draw_now=False):
    screen.fill(PURPLE)
    draw_text_center("Story Mode", FONT_BIG, WHITE, 60)
    panel = pygame.Rect(80, 110, WIDTH-160, HEIGHT-220)
    pygame.draw.rect(screen, WHITE, panel, border_radius=12)
    pygame.draw.rect(screen, (30,10,40), panel, 3, border_radius=12)
    # clamp index
    page_index = max(0, min(page_index, len(story_pages)-1))
    text = story_pages[page_index]
    lines = []
    for para in text.split("\n"):
        wrapped = wrap_text(para, FONT_SM, panel.width - 40)
        lines.extend(wrapped)
        lines.append("")
    start_y = panel.y + 24
    for i, ln in enumerate(lines):
        surf = FONT_SM.render(ln, True, (30,30,30))
        screen.blit(surf, (panel.x + 20, start_y + i*22))
    hint = FONT_XS.render("← Prev  |  → Next  |  Space = start battle  |  Esc = menu", True, (80,80,80))
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 40))
    if draw_now: return

def wrap_text(text, fnt, max_width):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if fnt.size(test)[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_battle_ui(draw_now=False):
    screen.fill(WHITE)
    # header
    draw_text_center(f"Score: {score}", FONT_MED, TEXT, 36)
    # enemy
    pygame.draw.ellipse(screen, (180,60,80), (36, 80, 140, 140))
    draw_hp_bar(24, 232, 200, 18, enemy_hp, max_hp, "Enemy", (220,80,80))
    screen.blit(FONT_XS.render("Monstrous Hunger", True, WHITE), (48, 150))
    # player
    pygame.draw.ellipse(screen, (90,58,150), (WIDTH-176, 80, 140, 140))
    draw_hp_bar(WIDTH-220, 232, 200, 18, player_hp, max_hp, "You", (120,90,220))
    screen.blit(FONT_XS.render("The Witch", True, WHITE), (WIDTH-160, 150))
    # current deck name
    if selected_deck_key:
        s2 = FONT_XS.render(f"Deck: {selected_deck_key}", True, (50,50,60))
        screen.blit(s2, (WIDTH//2 - s2.get_width()//2, 72))
    # card + particles
    draw_card_surface(rotation)
    draw_particles(screen)
    # streak & log
    screen.blit(FONT_SM.render(f"Streak: {streak}", True, TEXT), (24, HEIGHT-140))
    lx = WIDTH - 360
    ly = HEIGHT - 180
    screen.blit(FONT_SM.render("Game Log:", True, TEXT), (lx, ly))
    for i, line in enumerate(reversed(game_log)):
        surf = FONT_XS.render(line, True, TEXT)
        screen.blit(surf, (lx, ly + 18 + i*16))
    if draw_now: return

def draw_hp_bar(x,y,w,h,current,maximum,label,color):
    pygame.draw.rect(screen, (30,10,40), (x-2,y-2,w+4,h+4), 2, border_radius=6)
    pygame.draw.rect(screen, (245,245,248), (x,y,w,h), border_radius=6)
    pct = max(0, min(1, current/maximum))
    inner_w = int(w*pct)
    pygame.draw.rect(screen, color, (x,y,inner_w,h), border_radius=6)
    t = FONT_XS.render(f"{label}: {current}/{maximum}", True, (30,30,30))
    screen.blit(t, (x, y - 20))

def draw_card_surface(angle=0):
    rotated = pygame.transform.rotozoom(CARD_IMG, -angle, 1.0)
    r = rotated.get_rect(center=CARD_RECT.center)
    screen.blit(rotated, r)
    # text
    if current_card:
        txt = current_card.get("answer") if reveal else current_card.get("question")
        color = (20,90,30) if reveal else (20,20,20)
        wrap_w = CARD_W - 60
        lines = wrap_text(txt or "", FONT_MED, wrap_w)
        total_h = len(lines) * FONT_MED.get_height()
        start_y = r.centery - total_h//2
        for i,line in enumerate(lines):
            surf = FONT_MED.render(line, True, color)
            screen.blit(surf, surf.get_rect(center=(r.centerx, start_y + i*FONT_MED.get_height())))

def draw_end_screen(victory, draw_now=False):
    screen.fill(WHITE)
    if victory:
        draw_text_center("VICTORY — The lexicon grows brighter.", FONT_BIG, PURPLE, 140)
    else:
        draw_text_center("DEFEAT — The shadows keep a chapter.", FONT_BIG, DANGER, 140)
    sc = FONT_MED.render(f"Final Score: {score}", True, TEXT)
    screen.blit(sc, (WIDTH//2 - sc.get_width()//2, 220))
    restart = pygame.Rect(WIDTH//2 - 160, 300, 320, 64)
    quitb = pygame.Rect(WIDTH//2 - 160, 384, 320, 64)
    pygame.draw.rect(screen, ACCENT, restart, border_radius=8)
    pygame.draw.rect(screen, (255,180,180), quitb, border_radius=8)
    pygame.draw.rect(screen, (30,10,40), restart, 2, border_radius=8)
    pygame.draw.rect(screen, (30,10,40), quitb, 2, border_radius=8)
    screen.blit(FONT_MED.render("Restart (to Menu)", True, TEXT), FONT_MED.render("Restart (to Menu)", True, TEXT).get_rect(center=restart.center))
    screen.blit(FONT_MED.render("Quit", True, TEXT), FONT_MED.render("Quit", True, TEXT).get_rect(center=quitb.center))
    if draw_now: return restart, quitb
    return restart, quitb

# -----------------------------
# Helpers for multiline binary/horror output (optional)
# -----------------------------
def draw_multiline(text, font, color, x, y, line_height=None):
    lines = text.split("\n")
    if line_height is None:
        line_height = font.get_height() + 6
    for i, line in enumerate(lines):
        surf = font.render(line, True, color)
        screen.blit(surf, (x, y + i*line_height))

# -----------------------------
# Main game loop
# -----------------------------
ensure_dirs()
index_map = load_index()
deck_keys = list(index_map.keys())

# create default if missing
if not index_map:
    index_map = ensure_default_deck()

adding_text = ""
adding_mode = False
story_index = 0

# Start default music (if present)
default_music = os.path.join(MUSIC_DIR, "034. Memory.mp3")
if os.path.exists(default_music):
    music_manager.play(default_music)

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    mx, my = pygame.mouse.get_pos()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            safe_save_json(ACHIEV_FILE, achievements)
            save_index(index_map)
            running = False

        if state == STATE_MENU:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                srect, frect, qrect = draw_main_menu(draw_now=True)
                if srect.collidepoint(ev.pos):
                    # go to story with transition
                    transition_to(STATE_STORY, music_path=None, fade_color=PURPLE, speed=14)
                    story_index = 0
                elif frect.collidepoint(ev.pos):
                    transition_to(STATE_SELECT, music_path=None, fade_color=WHITE, speed=14)
                elif qrect.collidepoint(ev.pos):
                    safe_save_json(ACHIEV_FILE, achievements)
                    save_index(index_map)
                    running = False

        elif state == STATE_SELECT:
            if adding_mode:
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        adding_mode = False
                        adding_text = ""
                    elif ev.key == pygame.K_RETURN:
                        name = adding_text.strip()
                        if name:
                            fname = sanitize_filename(name)
                            i = 1
                            base = fname[:-5]
                            while fname in index_map.values():
                                fname = f"{base}_{i}.json"; i += 1
                            index_map[name] = fname
                            save_index(index_map)
                            save_deck(fname, [])
                            deck_keys = list(index_map.keys())
                            adding_mode = False
                            adding_text = ""
                            push_log(f"Created deck '{name}'")
                    elif ev.key == pygame.K_BACKSPACE:
                        adding_text = adding_text[:-1]
                    else:
                        adding_text += ev.unicode
            else:
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        transition_to(STATE_MENU, music_path=None, fade_color=PURPLE, speed=14)
                    elif ev.key == pygame.K_n:
                        adding_mode = True
                        adding_text = ""
                    elif ev.key == pygame.K_F5:
                        index_map = load_index()
                        deck_keys = list(index_map.keys())
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    rects = draw_select_deck(index_map, draw_now=True)
                    for r, delbtn, key in rects:
                        if r.collidepoint(ev.pos):
                            selected_deck_key = key
                            selected_deck_file = index_map.get(key)
                            deck_cards = load_deck(selected_deck_file) if selected_deck_file else []
                            random.shuffle(deck_cards)
                            reset_battle()
                            next_card_or_victory()
                            transition_to(STATE_PLAY, music_path=None, fade_color=WHITE, speed=12)
                            break
                        if delbtn.collidepoint(ev.pos):
                            fname = index_map.get(key)
                            if fname:
                                path = os.path.join(DECKS_DIR, fname)
                                try:
                                    if os.path.exists(path): os.remove(path)
                                except Exception:
                                    pass
                                if key in index_map: del index_map[key]
                                save_index(index_map)
                                index_map = load_index()
                                deck_keys = list(index_map.keys())
                                push_log(f"Deleted deck '{key}'")
                                break

        elif state == STATE_STORY:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT or ev.key == pygame.K_SPACE:
                    story_index += 1
                    if story_index >= len(story_pages):
                        # clamp and start battle
                        story_index = len(story_pages)-1
                        # use default deck
                        idx = load_index()
                        if "Default" in idx:
                            selected_deck_file = idx["Default"]
                        elif idx:
                            selected_deck_file = list(idx.values())[0]
                        else:
                            selected_deck_file = None
                        if selected_deck_file:
                            deck_cards = load_deck(selected_deck_file)
                            random.shuffle(deck_cards)
                            reset_battle()
                            next_card_or_victory()
                            transition_to(STATE_PLAY, music_path=None, fade_color=WHITE, speed=12)
                elif ev.key == pygame.K_LEFT:
                    story_index = max(0, story_index-1)
                elif ev.key == pygame.K_ESCAPE:
                    transition_to(STATE_MENU, music_path=None, fade_color=PURPLE, speed=14)

        elif state == STATE_PLAY:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if CARD_RECT.collidepoint(ev.pos):
                    lx = ev.pos[0] - CARD_RECT.left
                    ly = ev.pos[1] - CARD_RECT.top
                    try:
                        mx = int(lx * (CARD_IMG.get_width()/CARD_RECT.width))
                        my = int(ly * (CARD_IMG.get_height()/CARD_RECT.height))
                        if 0 <= mx < CARD_IMG.get_width() and 0 <= my < CARD_IMG.get_height() and CARD_MASK.get_at((mx,my)):
                            dragging = True
                            drag_offset = (CARD_RECT.centerx - ev.pos[0], CARD_RECT.centery - ev.pos[1])
                        else:
                            dragging = False
                    except Exception:
                        dragging = True
                        drag_offset = (CARD_RECT.centerx - ev.pos[0], CARD_RECT.centery - ev.pos[1])
            if ev.type == pygame.MOUSEMOTION:
                try:
                    if dragging:
                        mx, my = ev.pos
                        CARD_RECT.center = (mx + drag_offset[0], my + drag_offset[1])
                except Exception:
                    pass
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                if 'dragging' in locals() and dragging:
                    dx = CARD_RECT.centerx - CARD_CENTER[0]
                    if dx < -SWIPE_THRESHOLD:
                        process_known()
                        CARD_RECT.center = (CARD_CENTER[0] - WIDTH, CARD_CENTER[1])
                    elif dx > SWIPE_THRESHOLD:
                        process_unknown()
                        CARD_RECT.center = (CARD_CENTER[0] + WIDTH, CARD_CENTER[1])
                    else:
                        # snap back (animation in logic)
                        pass
                dragging = False

        elif state in (STATE_VICTORY, STATE_DEFEAT):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                restart, quitb = draw_end_screen(state == STATE_VICTORY, draw_now=True)
                if restart.collidepoint(ev.pos):
                    transition_to(STATE_MENU, music_path=None, fade_color=PURPLE, speed=12)
                    reset_battle()
                elif quitb.collidepoint(ev.pos):
                    safe_save_json(ACHIEV_FILE, achievements)
                    save_index(index_map)
                    running = False

    # --- logic updates ---
    # rotation by offset
    dx = CARD_RECT.centerx - CARD_CENTER[0]
    desired = max(-18, min(18, -dx/12))
    rotation += (desired - rotation) * 0.18

    # snap back if not dragging
    if not ('dragging' in locals() and dragging) and not reveal:
        if CARD_RECT.center != CARD_CENTER:
            cx, cy = CARD_RECT.center
            CARD_RECT.center = (lerp(cx, CARD_CENTER[0], 0.18), lerp(cy, CARD_CENTER[1], 0.18))

    # reveal timer
    if reveal and pygame.time.get_ticks() > reveal_until:
        reveal = False
        next_card_or_victory()
        CARD_RECT.center = CARD_CENTER

    # check win/lose
    if state == STATE_PLAY:
        if enemy_hp <= 0:
            state = STATE_VICTORY
            push_log("Victory achieved!")
        if player_hp <= 0:
            state = STATE_DEFEAT
            push_log("You were defeated...")

    # update particles
    update_particles()

    # --- draw ---
    if state == STATE_MENU:
        draw_main_menu()
    elif state == STATE_SELECT:
        if adding_mode:
            draw_add_deck_input("Create new deck (type name):", adding_text)
        else:
            draw_select_deck(index_map)
    elif state == STATE_STORY:
        draw_story(story_index)
    elif state == STATE_PLAY:
        draw_battle_ui()
    elif state == STATE_VICTORY:
        draw_end_screen(True)
    elif state == STATE_DEFEAT:
        draw_end_screen(False)

    # footer
    footer = FONT_XS.render("N = new deck | Esc = menu | Drag card left/right | F5 reload decks", True, (80,80,100))
    screen.blit(footer, (12, HEIGHT-28))

    # minor hint (occasionally)
    if random.random() < 0.002 and state == STATE_PLAY:
        h = random.choice(HINTS_DAY if random.random() < 0.6 else HINTS_DARK)
        push_log(h)

    pygame.display.flip()

# exit cleanup
safe_save_json(ACHIEV_FILE, achievements)
save_index(index_map)
pygame.quit()
sys.exit()
