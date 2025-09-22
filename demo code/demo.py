# flashcards_battle_full.py
# Updated Flashcards Battle
# - Deck selection (create/delete minimal-safe)
# - Card image as background (Image/card.png)
# - Drag-to-swipe with rotation + snap animation
# - Reveal answer then auto-next
# - Story Mode with extended witch narrative + transitions
# - Restart button on end screen
#
# Dependencies: pygame
# pip install pygame

import pygame, sys, os, json, random, math, time

# -----------------------------
# Config
# -----------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
DECKS_DIR = "decks"
INDEX_FILE = os.path.join(DECKS_DIR, "decks_index.json")
CARD_IMAGE = os.path.join("Image", "card.png")  # your provided png
MAX_LOG = 6

# -----------------------------
# Helpers: filesystem & safe names
# -----------------------------
def ensure_decks_dir():
    os.makedirs(DECKS_DIR, exist_ok=True)
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump({"Default": "default.json"}, f, ensure_ascii=False, indent=4)
    default_path = os.path.join(DECKS_DIR, "default.json")
    if not os.path.exists(default_path):
        sample = [
            {"question": "Apple", "answer": "แอปเปิ้ล"},
            {"question": "Dog", "answer": "สุนัข"},
            {"question": "Cat", "answer": "แมว"},
            {"question": "Water", "answer": "น้ำ"},
        ]
        with open(default_path, "w", encoding="utf-8") as f:
            json.dump(sample, f, ensure_ascii=False, indent=4)

def load_index():
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_index(idx):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=4)

def sanitize_filename(name):
    # produce safe ascii filename for filesystem
    base = "".join(c if c.isalnum() else "_" for c in name).strip("_")
    if not base:
        base = "deck"
    return base.lower() + ".json"

def load_deck(fname):
    path = os.path.join(DECKS_DIR, fname)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_deck(fname, cards):
    path = os.path.join(DECKS_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)

# -----------------------------
# Init pygame
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flashcards Battle (Witch vs Monster)")
clock = pygame.time.Clock()

# font loader with fallback
def load_font_try(path, size):
    try:
        return pygame.font.Font(path, size)
    except Exception:
        return pygame.font.SysFont("arial", size)

FONT_PATH = os.path.join("Font", "SansThai.ttf")  # change if you have a font
FONT_BIG = load_font_try(FONT_PATH, 48)
FONT_MED = load_font_try(FONT_PATH, 32)
FONT_SM = load_font_try(FONT_PATH, 20)
FONT_XS = load_font_try(FONT_PATH, 16)

# -----------------------------
# Load card image (scale to reasonable size)
# -----------------------------
if not os.path.exists(CARD_IMAGE):
    raise FileNotFoundError(f"Card image not found at '{CARD_IMAGE}' - please put your png there.")

card_img_orig = pygame.image.load(CARD_IMAGE).convert_alpha()
# choose desired card pixel size (relative to screen)
CARD_W, CARD_H = 340, 480
card_img = pygame.transform.smoothscale(card_img_orig, (CARD_W, CARD_H))
# rect used for hitbox and drawing (we will update center when dragging)
card_rect = card_img.get_rect(center=(WIDTH//2, HEIGHT//2))
CARD_CENTER = (WIDTH//2, HEIGHT//2)

# mask for per-pixel hittesting (optional - here we keep rect for simplicity)
card_mask = pygame.mask.from_surface(card_img)

# -----------------------------
# State machine constants
# -----------------------------
STATE_MENU = "menu"
STATE_SELECT_DECK = "select_deck"
STATE_STORY = "story"
STATE_PLAY = "play"
STATE_VICTORY = "victory"
STATE_DEFEAT = "defeat"
STATE_ADD_DECK = "add_deck"

state = STATE_MENU

# -----------------------------
# Gameplay variables (battle)
# -----------------------------
max_hp = 100
player_hp = enemy_hp = max_hp
score = 0
streak = 0
game_log = []

deck_cards = []
deck_pointer = 0
wrong_cards = []
current_card = None

# drag / swipe
dragging = False
drag_offset = (0,0)
rotation_angle = 0

SWIPE_THRESHOLD = 110  # px

# reveal answer
reveal_answer = False
reveal_until = 0

# selected deck file
selected_deck_key = None
selected_deck_file = None

# story pages (extended witch narrative) — written to be atmospheric & "sink" the player
story_pages = [
    "บทนำ — พระจันทร์ครอบฟ้า\n\nในคืนที่ท้องฟ้าทอประกายเป็นฝอยเงิน เมืองเล็ก ๆ บนปลายลมได้ปลุกความทรงจำที่หลับไหล.\nคุณ — แม่มดเงียบขรึมจากตระกูลโบราณ — ได้รับจดหมายฉบับเก่าจากปราชญ์ผู้จากไปนานแล้ว.",
    "คาถาและคำสาป\n\nจดหมายกล่าวถึง 'ตำรากลอุบาย' ที่เก็บคำศัพท์แห่งพลังไว้ การพูดจบไม่ถูกต้องจะปลุกเงาร้าย.\nคุณต้องเรียนรู้คำศัพท์เหล่านั้นให้ลึก เพื่อสะกดรอยแผลในโลก.",
    "การเดินทางเริ่มต้น\n\nคุณออกผจญในป่าที่เพลงลมพัดเป็นบทสวด ระหว่างทางสัตว์ประหลาดที่เกิดจากความลืมพบเจอคุณ\nเพื่อชิงตำรา เข้ารบด้วยคำ — คุณจะชนะด้วยความรู้หรือพ่ายแพ้ให้กับความมืด?",
    "บทเรียนจากบรรพบุรุษ\n\nเมื่อเรียนจบชุดคำศัพท์หนึ่ง คุณจะเข้าใจคาถาบางข้อ มากพอที่จะเปิดประตูต่อไปได้.\nชัยชนะช่วยให้เมืองฟื้นคืน — ความล้มเหลว... จะทำให้ตำนานของคุณเป็นเพียงเงา."
]

# -----------------------------
# Utility functions
# -----------------------------
def push_log(line):
    global game_log
    game_log.append(line)
    if len(game_log) > MAX_LOG:
        game_log.pop(0)

def reset_battle():
    global player_hp, enemy_hp, score, streak, game_log, deck_pointer, wrong_cards, current_card, reveal_answer, reveal_until
    player_hp = enemy_hp = max_hp
    score = 0
    streak = 0
    game_log = []
    deck_pointer = 0
    wrong_cards = []
    current_card = None
    reveal_answer = False
    reveal_until = 0
    # reset card rect center smoothly
    card_rect.center = CARD_CENTER

def next_card_or_victory():
    global current_card, deck_pointer, deck_cards, wrong_cards, state
    if deck_pointer < len(deck_cards):
        current_card = deck_cards[deck_pointer]
        deck_pointer += 1
    else:
        if wrong_cards:
            deck_cards = wrong_cards.copy()
            random.shuffle(deck_cards)
            wrong_cards = []
            deck_pointer = 0
            current_card = deck_cards[deck_pointer]
            deck_pointer += 1
            push_log("สับการ์ดที่ไม่รู้ใหม่")
        else:
            current_card = None
            # no more cards -> victory
            state = STATE_VICTORY

def process_known():
    global enemy_hp, score, streak, reveal_answer, reveal_until
    dmg = 18 + streak*3
    enemy_hp -= dmg
    gain = 90 + streak*10
    score += gain
    streak += 1
    push_log(f"รู้ — คุณโจมตีมอนสเตอร์ -{dmg}HP (+{gain})")
    reveal_answer = True
    reveal_until = pygame.time.get_ticks() + 900  # show answer 0.9s

def process_unknown():
    global player_hp, score, streak, wrong_cards, reveal_answer, reveal_until
    dmg = 20
    player_hp -= dmg
    score = max(0, score - 50)
    if current_card:
        wrong_cards.append(current_card)
    streak = 0
    push_log(f"ไม่รู้ — มอนสเตอร์โจมตีคุณ -{dmg}HP (-50)")
    reveal_answer = True
    reveal_until = pygame.time.get_ticks() + 900

# small easing for snapping
def lerp(a,b,t): return a + (b-a) * t

# -----------------------------
# Drawing helpers
# -----------------------------
def draw_text_center(text, fnt, color, y):
    surf = fnt.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH//2, y))
    screen.blit(surf, rect)

def draw_hp_bar(x,y,w,h,current,maximum,label,color):
    pygame.draw.rect(screen, (0,0,0), (x-2,y-2,w+4,h+4), 2, border_radius=6)
    pygame.draw.rect(screen, (220,220,220), (x,y,w,h), border_radius=6)
    pct = max(0, min(1, current/maximum))
    inner_w = int(w*pct)
    pygame.draw.rect(screen, color, (x,y,inner_w,h), border_radius=6)
    t = FONT_XS.render(f"{label}: {current}/{maximum}", True, (0,0,0))
    screen.blit(t, (x, y - 20))

def draw_card_surface(angle=0):
    # rotate card image around center and blit
    rotated = pygame.transform.rotozoom(card_img, -angle, 1.0)
    r = rotated.get_rect(center=card_rect.center)
    screen.blit(rotated, r)
    # text rendering (question/answer) centered in card's inner area
    if current_card:
        if reveal_answer:
            txt = current_card.get("answer","")
            color = (12,120,12)
        else:
            txt = current_card.get("question","")
            color = (10,10,10)
        # text wrap to card width
        wrap_width = CARD_W - 60
        lines = wrap_text(txt, FONT_MED, wrap_width)
        total_h = len(lines) * FONT_MED.get_height()
        start_y = r.centery - total_h//2
        for i,line in enumerate(lines):
            surf = FONT_MED.render(line, True, color)
            screen.blit(surf, surf.get_rect(center=(r.centerx, start_y + i*FONT_MED.get_height())))

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

def draw_battle_ui():
    # top: score
    s = FONT_MED.render(f"Score: {score}", True, (10,10,10))
    screen.blit(s, (WIDTH//2 - s.get_width()//2, 12))
    # left enemy
    pygame.draw.ellipse(screen, (170,30,30), (48, 96, 140, 140))
    draw_hp_bar(36, 250, 180, 18, enemy_hp, max_hp, "Enemy", (255,80,80))
    screen.blit(FONT_XS.render("Monstrous Hunger", True, (255,255,255)), (56, 160))
    # right player
    pygame.draw.ellipse(screen, (70,40,150), (WIDTH-188, 96, 140, 140))
    draw_hp_bar(WIDTH-212, 250, 180, 18, player_hp, max_hp, "You", (120,100,255))
    screen.blit(FONT_XS.render("The Witch", True, (255,255,255)), (WIDTH-170, 160))
    # card
    # rotated blit handled separately
    angle = rotation_angle
    draw_card_surface(angle)
    # streak & log
    screen.blit(FONT_SM.render(f"Streak: {streak}", True, (0,0,0)), (24, HEIGHT-140))
    lx = WIDTH - 320
    ly = HEIGHT - 160
    screen.blit(FONT_SM.render("Game Log:", True, (0,0,0)), (lx, ly))
    for i, line in enumerate(reversed(game_log)):
        surf = FONT_XS.render(line, True, (0,0,0))
        screen.blit(surf, (lx, ly + 18 + i*16))

# -----------------------------
# Menu & Deck selection UI
# -----------------------------
def draw_main_menu():
    screen.fill((245,245,248))
    draw_text_center("Flashcards Battle — Witch's Lexicon", FONT_BIG, (20,20,24), 96)
    # three big buttons
    btn_w = 320; btn_h = 64
    btn_x = WIDTH//2 - btn_w//2
    y1 = 200
    story_rect = pygame.Rect(btn_x, y1, btn_w, btn_h)
    free_rect = pygame.Rect(btn_x, y1+90, btn_w, btn_h)
    quit_rect = pygame.Rect(btn_x, y1+180, btn_w, btn_h)
    pygame.draw.rect(screen, (200,220,255), story_rect, border_radius=8)
    pygame.draw.rect(screen, (200,255,220), free_rect, border_radius=8)
    pygame.draw.rect(screen, (255,200,200), quit_rect, border_radius=8)
    pygame.draw.rect(screen, (0,0,0), story_rect, 2, border_radius=8)
    pygame.draw.rect(screen, (0,0,0), free_rect, 2, border_radius=8)
    pygame.draw.rect(screen, (0,0,0), quit_rect, 2, border_radius=8)
    screen.blit(FONT_MED.render("Story Mode", True, (0,0,0)), FONT_MED.render("Story Mode", True, (0,0,0)).get_rect(center=story_rect.center))
    screen.blit(FONT_MED.render("Free Style (Choose Deck)", True, (0,0,0)), FONT_MED.render("Free Style (Choose Deck)", True, (0,0,0)).get_rect(center=free_rect.center))
    screen.blit(FONT_MED.render("Quit", True, (0,0,0)), FONT_MED.render("Quit", True, (0,0,0)).get_rect(center=quit_rect.center))
    return story_rect, free_rect, quit_rect

def draw_select_deck(index_map):
    screen.fill((250,250,245))
    draw_text_center("Select Deck (Click to Play) — N to create new | Del button to delete", FONT_MED, (10,10,10), 60)
    rects = []
    y = 120
    for key in index_map:
        r = pygame.Rect(120, y, 520, 56)
        pygame.draw.rect(screen, (230,230,255), r, border_radius=8)
        pygame.draw.rect(screen, (0,0,0), r, 2, border_radius=8)
        screen.blit(FONT_MED.render(str(key), True, (0,0,0)), (r.x + 14, r.y + 10))
        del_btn = pygame.Rect(r.right - 70, r.y + 8, 56, 40)
        pygame.draw.rect(screen, (255,160,160), del_btn, border_radius=6)
        screen.blit(FONT_SM.render("Del", True, (0,0,0)), del_btn.move(10,8))
        rects.append((r, del_btn, key))
        y += 84
    return rects

# Add simple create-deck UI (text input)
def draw_add_deck_input(prompt, text):
    screen.fill((245,245,245))
    draw_text_center(prompt, FONT_MED, (10,10,10), 120)
    box = pygame.Rect(140, 200, 520, 56)
    pygame.draw.rect(screen, (255,255,255), box, border_radius=8)
    pygame.draw.rect(screen, (0,0,0), box, 2, border_radius=8)
    t = FONT_MED.render(text, True, (0,0,0))
    screen.blit(t, (box.x + 12, box.y + 12))
    hint = FONT_XS.render("Enter = create | Esc = cancel", True, (90,90,90))
    screen.blit(hint, (box.x, box.bottom + 12))

# Story UI
def draw_story(page_index):
    screen.fill((18,12,30))
    draw_text_center("Story Mode", FONT_BIG, (240,220,200), 40)
    # panel
    panel = pygame.Rect(80, 110, WIDTH-160, HEIGHT-220)
    pygame.draw.rect(screen, (255,250,240), panel, border_radius=12)
    pygame.draw.rect(screen, (20,20,20), panel, 3, border_radius=12)
    # render wrapped text
    text = story_pages[page_index]
    lines = []
    for para in text.split("\n"):
        wrapped = wrap_text(para, FONT_SM, panel.width - 40)
        lines.extend(wrapped)
        lines.append("")  # blank line
    # draw lines
    start_y = panel.y + 30
    for i, ln in enumerate(lines):
        surf = FONT_SM.render(ln, True, (20,20,20))
        screen.blit(surf, (panel.x + 20, start_y + i*22))
    hint = FONT_XS.render("← Prev  |  → Next  |  Space = start battle  |  Esc = menu", True, (80,80,80))
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 40))

# End screen
def draw_end_screen(victory):
    screen.fill((240,240,240))
    if victory:
        draw_text_center("VICTORY — The lexicon grows brighter.", FONT_BIG, (10,120,10), 140)
    else:
        draw_text_center("DEFEAT — The shadows keep a chapter.", FONT_BIG, (150,10,10), 140)
    sc = FONT_MED.render(f"Final Score: {score}", True, (0,0,0))
    screen.blit(sc, (WIDTH//2 - sc.get_width()//2, 220))
    # buttons
    restart = pygame.rect(WIDTH//2 - 140, 300, 280, 64)
    quitb = pygame.rect(WIDTH//2 - 140, 384, 280, 64)
    pygame.draw.rect(screen, (200,255,200), restart, border_radius=8)
    pygame.draw.rect(screen, (255,200,200), quitb, border_radius=8)
    pygame.draw.rect(screen, (0,0,0), restart, 2, border_radius=8)
    pygame.draw.rect(screen, (0,0,0), quitb, 2, border_radius=8)
    screen.blit(FONT_MED.render("เล่นใหม่", True, (0,0,0)), restart.get_rect(center=restart.center))
    screen.blit(FONT_MED.render("Quit", True, (0,0,0)), quitb.get_rect(center=quitb.center))
    return restart, quitb

# -----------------------------
# Main loop
# -----------------------------
ensure_decks_dir()
index_map = load_index()
deck_keys = list(index_map.keys())

# variables for add-deck input
adding_deck_text = ""
adding_deck_mode = False

# story page pointer
story_index = 0

# simple animation variables
snap_speed = 0.18  # 0..1 easing

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    mouse = pygame.mouse.get_pos()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            save_index(index_map)
            pygame.quit(); sys.exit()

        # --- input handling per state ---
        if state == STATE_MENU:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                srect, frect, qrect = draw_main_menu()
                if srect.collidepoint(ev.pos):
                    state = STATE_STORY
                    story_index = 0
                elif frect.collidepoint(ev.pos):
                    # go to deck select
                    index_map = load_index()
                    deck_keys = list(index_map.keys())
                    state = STATE_SELECT_DECK
                elif qrect.collidepoint(ev.pos):
                    save_index(index_map)
                    running = False

        elif state == STATE_SELECT_DECK:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    state = STATE_MENU
                elif ev.key == pygame.K_n:
                    # create new deck
                    adding_deck_mode = True
                    adding_deck_text = ""
                elif ev.key == pygame.K_F5:
                    index_map = load_index()
                    deck_keys = list(index_map.keys())
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                rects = draw_select_deck(index_map)
                pos = ev.pos
                for r, delbtn, key in rects:
                    if r.collidepoint(pos):
                        # start play with this deck
                        selected_deck_key = key
                        selected_deck_file = index_map[key]
                        deck_cards = load_deck(selected_deck_file)
                        random.shuffle(deck_cards)
                        reset_battle()
                        next_card_or_victory()
                        state = STATE_PLAY
                        break
                    if delbtn.collidepoint(pos):
                        # delete with safety
                        fname = index_map.get(key)
                        if fname:
                            path = os.path.join(DECKS_DIR, fname)
                            if os.path.exists(path):
                                os.remove(path)
                            # remove key
                            del index_map[key]
                            save_index(index_map)
                            index_map = load_index()
                            deck_keys = list(index_map.keys())
                            push_log(f"Deleted deck '{key}'")
                            break
        elif state == STATE_ADD_DECK or (state == STATE_SELECT_DECK and adding_deck_mode):
            # use same loop for add deck prompt
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    adding_deck_mode = False
                elif ev.key == pygame.K_RETURN:
                    name = adding_deck_text.strip()
                    if name:
                        fname = sanitize_filename(name)
                        # avoid collisions
                        i = 1
                        base = fname[:-5]
                        while fname in index_map.values():
                            fname = f"{base}_{i}.json"
                            i += 1
                        index_map[name] = fname
                        save_index(index_map)
                        # create empty deck file
                        save_deck(fname, [])
                        deck_keys = list(index_map.keys())
                        adding_deck_mode = False
                        push_log(f"Created deck '{name}'")
                elif ev.key == pygame.K_BACKSPACE:
                    adding_deck_text = adding_deck_text[:-1]
                else:
                    adding_deck_text += ev.unicode

        elif state == STATE_STORY:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT or ev.key == pygame.K_SPACE:
                    story_index += 1
                    if story_index >= len(story_pages):
                        # start story battle on default
                        index_map = load_index()
                        if "Default" in index_map:
                            selected_deck_file = index_map["Default"]
                        else:
                            selected_deck_file = list(index_map.values())[0]
                        deck_cards = load_deck(selected_deck_file)
                        random.shuffle(deck_cards)
                        reset_battle()
                        next_card_or_victory()
                        state = STATE_PLAY
                elif ev.key == pygame.K_LEFT:
                    story_index = max(0, story_index-1)
                elif ev.key == pygame.K_ESCAPE:
                    state = STATE_MENU

        elif state == STATE_PLAY:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # check pixel-perfect hit: use rect + mask check for nicer feel
                if card_rect.collidepoint(ev.pos):
                    # convert to card local coords
                    lx = ev.pos[0] - card_rect.left
                    ly = ev.pos[1] - card_rect.top
                    # only start drag if mask opaque at that point
                    try:
                        if card_mask.get_at((int(lx * (card_img.get_width()/card_rect.width)), int(ly * (card_img.get_height()/card_rect.height)))):
                            dragging = True
                            drag_offset = (card_rect.centerx - ev.pos[0], card_rect.centery - ev.pos[1])
                        else:
                            # click outside visible part
                            pass
                    except Exception:
                        # fallback: start drag if rect
                        dragging = True
                        drag_offset = (card_rect.centerx - ev.pos[0], card_rect.centery - ev.pos[1])
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                if dragging:
                    # evaluate swipe
                    dx = card_rect.centerx - CARD_CENTER[0]
                    if dx < -SWIPE_THRESHOLD:
                        process_known()
                    elif dx > SWIPE_THRESHOLD:
                        process_unknown()
                    else:
                        # snap back with animation (we'll set dragging False and animate in draw)
                        pass
                dragging = False
            if ev.type == pygame.MOUSEMOTION:
                if dragging:
                    # follow mouse smoothly using offset
                    mx, my = ev.pos
                    target_x = mx + drag_offset[0]
                    target_y = my + drag_offset[1]
                    card_rect.center = (target_x, target_y)

        elif state in (STATE_VICTORY, STATE_DEFEAT):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                restart_btn, quit_btn = draw_end_screen(state==STATE_VICTORY)
                if restart_btn.collidepoint(ev.pos):
                    # restart -> menu
                    state = STATE_MENU
                    reset_battle()
                elif quit_btn.collidepoint(ev.pos):
                    save_index(index_map)
                    running = False

    # --- Logic updates ---
    # card rotation based on x offset for a snappy feel
    dx = card_rect.centerx - CARD_CENTER[0]
    desired_angle = max(-18, min(18, -dx / 12))
    rotation_angle += (desired_angle - rotation_angle) * 0.18

    # when not dragging and not in reveal and card offset not zero, animate back
    if not dragging and not reveal_answer and card_rect.center != CARD_CENTER:
        cx, cy = card_rect.center
        card_rect.center = (lerp(cx, CARD_CENTER[0], snap_speed), lerp(cy, CARD_CENTER[1], snap_speed))

    # reveal answer timer
    if reveal_answer and pygame.time.get_ticks() > reveal_until:
        reveal_answer = False
        next_card_or_victory()
        card_rect.center = CARD_CENTER

    # check win/lose
    if state == STATE_PLAY:
        if enemy_hp <= 0:
            state = STATE_VICTORY
        if player_hp <= 0:
            state = STATE_DEFEAT

    # -----------------------------
    # Drawing
    # -----------------------------
    screen.fill((245,244,248))
    if state == STATE_MENU:
        draw_main_menu()

    elif state == STATE_SELECT_DECK:
        if adding_deck_mode:
            draw_add_deck_input("Create new deck (type name):", adding_deck_text)
        else:
            rects = draw_select_deck(index_map)

    elif state == STATE_STORY:
        draw_story(story_index)

    elif state == STATE_PLAY:
        draw_battle_ui()

    elif state == STATE_VICTORY:
        draw_end_screen(True)

    elif state == STATE_DEFEAT:
        draw_end_screen(False)

    # small HUD footer
    footer = FONT_XS.render("N = new deck | Esc = menu | Click deck to play | Drag card left/right", True, (90,90,90))
    screen.blit(footer, (12, HEIGHT-26))

    pygame.display.flip()

# end main loop
