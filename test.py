# WitchMemo_Reforged.py
"""
Consolidated + upgraded Witch's Memo
- Theme colors: basecolor, triadic_2, triadic_3
- FPS 60
- Free For All mode -> select deck -> choose stage (5/10/15) -> battle
- Options: set answer time (default 10s)
- Skills: Heal(1), Shield(2), StopTime(2), MaxHP+(3)
- Deck JSON format: {"style":"Image/cards/ank.png","cards":[{"word":"..","meaning":".."}, ...]}
- If deck file is old list format, code will handle and convert on save.
"""
import pygame, sys, os, json, random, socket, getpass, time
from math import floor

pygame.init()
pygame.mixer.init()
# -------------------------------------------------------
# Config / Globals
# -------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WitchMemo Reforged")

clock = pygame.time.Clock()
FPS = 60

DECK_DIR = "decks"
os.makedirs(DECK_DIR, exist_ok=True)

computer_name = socket.gethostname()
user_name = getpass.getuser()

# load some assets paths (if missing, code will continue)
BG_PATH = "Image/Background/forestbackground.jpg"
CARD_BASE_PATH = "Image/cards/card.png"

# theme colors
basecolor = (120, 60, 160)  # fallback if random not desired
# allow original randomization like your code
basecolor = (random.randint(50,130), random.randint(30,100), random.randint(100,200))
triadic_2 = [(basecolor[0]+85)%256, (basecolor[1]+85)%256, (basecolor[2]+85)%256]
triadic_3 = [(triadic_2[0]+85)%256, (triadic_2[1]+85)%256, (triadic_2[2]+85)%256]

# SFX / BGM settings
background_music_volume = 0.5
current_music = None

def background_music(path, volume, loop=-1):
    global current_music, background_music_volume
    try:
        if current_music != path:
            current_music = path
            pygame.mixer.music.fadeout(300)
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(background_music_volume)
            pygame.mixer.music.play(loop)
    except Exception as e:
        print("BGM load error:", e)

def click_sound():
    try:
        pygame.mixer.Sound("SFX/Click.mp3").play()
    except Exception:
        pass

def sfx_func(path):
    try:
        pygame.mixer.Sound(path).play()
    except Exception:
        pass

# fonts
def get_font(sz):
    try:
        return pygame.font.Font("Font/SansThai.ttf", sz)
    except Exception:
        return pygame.font.SysFont("arial", sz)

# helper for drawing centered text
def draw_text(text, font, color, pos):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=pos)
    SCREEN.blit(surf, rect)
    return rect

# -------------------------------------------------------
# Deck helpers (JSON structure handling)
# Each deck file: {"style": "<path>", "cards":[{"word":..., "meaning":...}, ...]}
# -------------------------------------------------------
def list_decks():
    files = [f for f in os.listdir(DECK_DIR) if f.endswith(".json")]
    files.sort()
    return files

def load_deck_file(fname):
    path = os.path.join(DECK_DIR, fname)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # support old format (list)
        if isinstance(data, list):
            # convert to new structure
            data = {"style": CARD_BASE_PATH, "cards": []} if data==[] else {"style": CARD_BASE_PATH, "cards": []}
            # if old list contains dicts with q/a, migrate:
            try:
                with open(path, "r", encoding="utf-8") as f2:
                    raw = json.load(f2)
                # if raw is list of dicts with question/answer or word/meaning
                for item in raw:
                    if isinstance(item, dict):
                        if "question" in item and "answer" in item:
                            data["cards"].append({"word": item["question"], "meaning": item["answer"]})
                        elif "word" in item and "meaning" in item:
                            data["cards"].append({"word": item["word"], "meaning": item["meaning"]})
            except Exception:
                pass
        # ensure keys
        if "style" not in data:
            data["style"] = CARD_BASE_PATH
        if "cards" not in data or not isinstance(data["cards"], list):
            data["cards"] = []
        # clamp to 30
        if len(data["cards"]) > 30:
            data["cards"] = data["cards"][:30]
        return data
    except Exception as e:
        print("load_deck_file error", e)
        return {"style": CARD_BASE_PATH, "cards": []}

def save_deck_file(fname, data):
    path = os.path.join(DECK_DIR, fname)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("save_deck_file error", e)

# -------------------------------------------------------
# Basic UI components (simple buttons)
# -------------------------------------------------------
class Button:
    def __init__(self, rect, text="", font=None, base=triadic_2, hover=triadic_3):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font or get_font(32)
        self.base = base
        self.hover = hover
    def draw(self, mousepos):
        hovering = self.rect.collidepoint(mousepos)
        pygame.draw.rect(SCREEN, self.base if not hovering else self.hover, self.rect, border_radius=10)
        pygame.draw.rect(SCREEN, (0,0,0), self.rect, 2, border_radius=10)
        text_surf = self.font.render(self.text, True, (255,255,255) if sum(self.base)//3 < 180 else (0,0,0))
        SCREEN.blit(text_surf, text_surf.get_rect(center=self.rect.center))
    def is_clicked(self, mousepos):
        return self.rect.collidepoint(mousepos)

# -------------------------------------------------------
# Game battle system (simplified but feature-rich)
# -------------------------------------------------------
def battle_screen(deck_name, count_cards, answer_time):
    """
    deck_name: filename without .json
    count_cards: 5 or 10 or 15
    answer_time: seconds (int)
    """
    # load deck data
    fname = deck_name + ".json"
    data = load_deck_file(fname)
    cards = data["cards"][:]  # list of dicts
    if len(cards) < count_cards:
        # cannot start
        print("Deck too small")
        return

    # choose sample of size count_cards (random)
    selected = random.sample(cards, count_cards)
    # We'll use indexes as card queue
    queue = selected[:]
    wrong_cards = []
    random.shuffle(queue)

    # player stats
    max_hp = 3
    hp = max_hp
    streak = 0
    skill_points = 0
    shield_active = False
    time_stopped_for_card = False

    # monsters logic:
    # According to request: for count N:
    # - if N==5 -> 1 monster
    # - if N==10 -> 2 monsters
    # - if N==15 -> 3 monsters
    monsters_count = 1 if count_cards <=5 else (2 if count_cards <= 10 else 3)
    # Each monster requires 5 correct hits to die (per original)
    monster_hp = [5]*monsters_count
    current_monsters = monsters_count

    # timer
    per_card_time = answer_time
    boss_time = max(1, answer_time//2)

    # UI buttons
    btn_width = 160
    btn_h = 64
    know_btn = Button((WIDTH-220, HEIGHT-220, btn_width, btn_h), text="KNOWN", font=get_font(28), base=(40,160,40), hover=(80,200,80))
    unk_btn  = Button((WIDTH-420, HEIGHT-220, btn_width, btn_h), text="DON'T KNOW", font=get_font(28), base=(160,40,40), hover=(200,80,80))
    skill_heal_btn = Button((40, HEIGHT-160, 140, 48), text="Heal (1)", font=get_font(20))
    skill_shield_btn = Button((200, HEIGHT-160, 140, 48), text="Shield (2)", font=get_font(20))
    skill_stop_btn = Button((360, HEIGHT-160, 140, 48), text="Stop (2)", font=get_font(20))
    skill_maxhp_btn = Button((520, HEIGHT-160, 160, 48), text="MAX+ (3)", font=get_font(20))

    last_tick = pygame.time.get_ticks()
    card_start_time = pygame.time.get_ticks()
    current_card = None
    reveal_answer = False
    reveal_until = 0

    game_log = []
    def log(msg):
        game_log.append(msg)
        if len(game_log) > 8:
            game_log.pop(0)

    def next_card():
        nonlocal current_card, card_start_time, reveal_answer, time_stopped_for_card
        if queue:
            current_card = queue.pop(0)
            card_start_time = pygame.time.get_ticks()
            reveal_answer = False
            time_stopped_for_card = False
        else:
            # if queue empty and we have wrong_cards, reshuffle
            if wrong_cards:
                queue.extend(wrong_cards)
                random.shuffle(queue)
                wrong_cards.clear()
                log("Shuffled wrong cards back into queue.")
                next_card()
            else:
                # player completed stage -> victory for this stage
                log("Stage complete! You win the stage.")
                return "stage_complete"
        return "ok"

    next_card()

    running = True
    result = None
    while running:
        dt = clock.tick(FPS)
        mousepos = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if know_btn.is_clicked(mousepos) and current_card and not reveal_answer:
                    # answered known
                    # apply damage to one monster (player attacks)
                    # find first alive monster index
                    for i in range(len(monster_hp)):
                        if monster_hp[i] > 0:
                            monster_hp[i] -= 1
                            log(f"Hit monster #{i+1}! (-1 HP)")
                            break
                    streak += 1
                    if streak % 3 == 0:
                        skill_points += 1
                        log("Skill point earned!")
                    reveal_answer = True
                    reveal_until = pygame.time.get_ticks() + 700
                    # no wrong addition
                if unk_btn.is_clicked(mousepos) and current_card and not reveal_answer:
                    # answered don't know
                    log("You didn't know that card.")
                    wrong_cards.append(current_card)
                    streak = 0
                    # monster attacks (player takes heart)
                    if shield_active:
                        shield_active = False
                        log("Shield blocked the damage!")
                    else:
                        hp -= 1
                        log("You lost 1 heart!")
                    reveal_answer = True
                    reveal_until = pygame.time.get_ticks() + 700
                # skills
                if skill_heal_btn.is_clicked(mousepos):
                    if skill_points >= 1 and hp < max_hp:
                        skill_points -= 1
                        hp = min(max_hp, hp + 1)
                        log("Heal used (+1 heart).")
                if skill_shield_btn.is_clicked(mousepos):
                    if skill_points >= 2:
                        skill_points -= 2
                        shield_active = True
                        log("Shield active for next hit.")
                if skill_stop_btn.is_clicked(mousepos):
                    if skill_points >= 2 and not time_stopped_for_card:
                        skill_points -= 2
                        time_stopped_for_card = True
                        log("Time stopped for this card.")
                if skill_maxhp_btn.is_clicked(mousepos):
                    if skill_points >= 3:
                        skill_points -= 3
                        max_hp += 1
                        hp += 1
                        log("Max HP increased by 1!")
        # update timer
        now = pygame.time.get_ticks()
        if current_card and not reveal_answer and not time_stopped_for_card:
            elapsed = (now - card_start_time)/1000.0
            if elapsed > per_card_time:
                # timeout -> wrong
                log("Time out! counted as wrong.")
                wrong_cards.append(current_card)
                streak = 0
                if shield_active:
                    shield_active = False
                    log("Shield blocked the damage!")
                else:
                    hp -= 1
                    log("You lost 1 heart!")
                reveal_answer = True
                reveal_until = pygame.time.get_ticks() + 700

        # after reveal, show answer then next card
        if reveal_answer and pygame.time.get_ticks() > reveal_until:
            # check if monster died
            # if any monster hp <=0, reduce current_monsters
            current_monsters = sum(1 for m in monster_hp if m>0)
            # if all monsters dead -> stage cleared
            if all(m <= 0 for m in monster_hp):
                log("All monsters defeated in this stage!")
                result = "stage_victory"
                running = False
            else:
                n = next_card()
                if n == "stage_complete":
                    result = "stage_victory"
                    running = False

        # check lose
        if hp <= 0:
            log("You have no hearts left. Defeat.")
            result = "defeat"
            running = False

        # draw UI
        SCREEN.fill(basecolor)
        # header
        draw_text("Battle Mode", get_font(36), triadic_3, (WIDTH//2, 30))
        # deck and stage info
        draw_text(f"Deck: {deck_name}  |  Cards used: {count_cards}", get_font(22), triadic_2, (WIDTH//2, 70))

        # monsters display
        monster_x = 160
        for i,mhp in enumerate(monster_hp):
            color = (200,60,60) if mhp>0 else (80,80,80)
            pygame.draw.rect(SCREEN, color, (monster_x + i*200, 110, 140, 60), border_radius=8)
            draw_text(f"Monster {i+1}", get_font(20), (255,255,255), (monster_x + i*200 + 70, 130))
            draw_text(f"HP: {mhp}", get_font(18), (255,255,255), (monster_x + i*200 + 70, 155))

        # card display center
        card_box = pygame.Rect(WIDTH//2-260, 200, 520, 260)
        pygame.draw.rect(SCREEN, (255,255,255), card_box, border_radius=12)
        pygame.draw.rect(SCREEN, triadic_3, card_box, 4, border_radius=12)

        if current_card:
            q = current_card.get("word","")
            a = current_card.get("meaning","")
            draw_text(q, get_font(36), (10,10,10), card_box.center)
            if reveal_answer:
                draw_text(a, get_font(28), (60,140,60), (card_box.centerx, card_box.centery+60))

        # timer bar
        if current_card:
            tleft = per_card_time
            if not time_stopped_for_card and not reveal_answer:
                elapsed = (pygame.time.get_ticks() - card_start_time)/1000.0
                tleft = max(0, per_card_time - elapsed)
            # bar width
            bar_w = 400
            pct = max(0, min(1, tleft / (per_card_time if per_card_time>0 else 1)))
            pygame.draw.rect(SCREEN, (200,200,200), (WIDTH//2-200, 480, bar_w, 16), border_radius=8)
            pygame.draw.rect(SCREEN, (80,160,240), (WIDTH//2-200, 480, int(bar_w*pct), 16), border_radius=8)
            draw_text(f"Time: {tleft:.1f}s", get_font(18), (30,30,30), (WIDTH//2, 500))

        # buttons
        know_btn.draw(mousepos)
        unk_btn.draw(mousepos)
        # skills area
        skill_heal_btn.draw(mousepos)
        skill_shield_btn.draw(mousepos)
        skill_stop_btn.draw(mousepos)
        skill_maxhp_btn.draw(mousepos)

        # stats
        draw_text(f"HP: {hp}/{max_hp}", get_font(20), triadic_2, (90,40))
        draw_text(f"Streak: {streak}", get_font(20), triadic_2, (90,70))
        draw_text(f"Skill Pts: {skill_points}", get_font(20), triadic_2, (90,100))
        draw_text(f"Shield: {'ON' if shield_active else 'OFF'}", get_font(16), triadic_2, (90,130))

        # game log
        log_y = HEIGHT - 140
        for i, ln in enumerate(reversed(game_log)):
            txt = get_font(18).render(ln, True, (255,255,255))
            SCREEN.blit(txt, (20, log_y + i*22))

        pygame.display.flip()

    # battle ended
    return result, {"hp":hp,"max_hp":max_hp,"log":game_log}

# -------------------------------------------------------
# UI flows: main menu, free for all, create/edit decks, options
# -------------------------------------------------------
def main_menu():
    while True:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        SCREEN.fill(basecolor)
        draw_text("Witch's Memo — Reforged", get_font(48), triadic_3, (WIDTH//2, 70))

        play_btn = Button((WIDTH//2-140, 160, 280, 64), "Free For All", get_font(28))
        opt_btn  = Button((WIDTH//2-140, 240, 280, 64), "Options", get_font(28))
        quit_btn = Button((WIDTH//2-140, 320, 280, 64), "Quit", get_font(28))
        for b in (play_btn, opt_btn, quit_btn):
            b.draw(mouse)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button==1:
                if play_btn.is_clicked(mouse):
                    click_sound(); free_for_all()
                if opt_btn.is_clicked(mouse):
                    click_sound(); options_screen()
                if quit_btn.is_clicked(mouse):
                    pygame.quit(); sys.exit()

        pygame.display.flip()

def options_screen():
    global background_music_volume, current_music
    while True:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        SCREEN.fill(triadic_2)
        draw_text("Options", get_font(40), triadic_3, (WIDTH//2, 60))

        # music vol
        vol_text = get_font(24).render(f"Music Volume: {int(background_music_volume*100)}%", True, (0,0,0))
        SCREEN.blit(vol_text, (WIDTH//2-120, 140))
        plus = Button((WIDTH//2+60, 130, 48, 40), "+", get_font(26))
        minus= Button((WIDTH//2-170,130,48,40), "-", get_font(26))
        plus.draw(mouse); minus.draw(mouse)

        # answer time setting
        draw_text("Answer time (seconds):", get_font(24), triadic_3, (WIDTH//2, 220))
        # display and simple +/- buttons
        if "answer_time_setting" not in options_screen.__dict__:
            options_screen.answer_time_setting = 10
        at = options_screen.answer_time_setting
        time_text = get_font(32).render(str(at), True, (0,0,0))
        SCREEN.blit(time_text, (WIDTH//2-20, 260))
        tplus = Button((WIDTH//2+60, 250, 48, 40), "+", get_font(26))
        tminus= Button((WIDTH//2-170,250,48,40), "-", get_font(26))
        tplus.draw(mouse); tminus.draw(mouse)

        back = Button((WIDTH//2-100, 340, 200, 60), "Back", get_font(24), base=triadic_3, hover=triadic_2)
        back.draw(mouse)

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                click_sound()
                if plus.is_clicked(mouse):
                    background_music_volume = min(1.0, round(background_music_volume+0.1, 2))
                    pygame.mixer.music.set_volume(background_music_volume)
                if minus.is_clicked(mouse):
                    background_music_volume = max(0.0, round(background_music_volume-0.1,2))
                    pygame.mixer.music.set_volume(background_music_volume)
                if tplus.is_clicked(mouse):
                    options_screen.answer_time_setting = min(30, options_screen.answer_time_setting+1)
                if tminus.is_clicked(mouse):
                    options_screen.answer_time_setting = max(3, options_screen.answer_time_setting-1)
                if back.is_clicked(mouse):
                    return
        pygame.display.flip()

def create_deck_flow(style_path=None):
    # create new deck: choose name, choose style if style_path None
    name = ""
    while True:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        SCREEN.fill(triadic_2)
        draw_text("Create New Deck", get_font(36), triadic_3, (WIDTH//2, 60))
        # input box
        box = pygame.Rect(WIDTH//2-300, 140, 600, 60)
        pygame.draw.rect(SCREEN, (255,255,255), box, border_radius=8)
        pygame.draw.rect(SCREEN, triadic_3, box, 3, border_radius=8)
        txt = get_font(32).render(name or "Enter deck name...", True, (40,40,40))
        SCREEN.blit(txt, (box.x+12, box.y+12))

        create_btn = Button((WIDTH//2-120, 260, 240, 60), "Create", get_font(28), base=triadic_3, hover=triadic_2)
        back_btn   = Button((WIDTH//2-120, 340, 240, 60), "Back", get_font(28), base=triadic_3, hover=triadic_2)
        create_btn.draw(mouse); back_btn.draw(mouse)
        draw_text("Choose style after creating (you'll be prompted)", get_font(18), (10,10,10), (WIDTH//2, 420))
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_BACKSPACE:
                    name = name[:-1]
                elif ev.key==pygame.K_RETURN:
                    if name.strip():
                        fname = name.strip() + ".json"
                        data = {"style": style_path or CARD_BASE_PATH, "cards": []}
                        save_deck_file(fname, data)
                        click_sound()
                        return fname
                else:
                    if len(name) < 20:
                        name += ev.unicode
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                if create_btn.is_clicked(mouse) and name.strip():
                    fname = name.strip() + ".json"
                    data = {"style": style_path or CARD_BASE_PATH, "cards": []}
                    save_deck_file(fname, data)
                    click_sound()
                    return fname
                if back_btn.is_clicked(mouse):
                    return None
        pygame.display.flip()

def edit_deck_flow(deck_filename):
    # open deck, allow adding up to 30 words
    path = os.path.join(DECK_DIR, deck_filename)
    data = load_deck_file(deck_filename)
    cards = data["cards"]
    style = data.get("style", CARD_BASE_PATH)
    input_word = ""
    input_meaning = ""
    active = "word"
    MAX_WORDS = 30
    while True:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        SCREEN.fill(basecolor)
        draw_text(f"Edit Deck: {deck_filename}", get_font(34), triadic_3, (WIDTH//2, 40))

        # boxes
        wbox = pygame.Rect(120, 120, 480, 60)
        mbox = pygame.Rect(680, 120, 480, 60)
        pygame.draw.rect(SCREEN, (255,255,255), wbox, border_radius=8)
        pygame.draw.rect(SCREEN, triadic_3, wbox, 3, border_radius=8)
        pygame.draw.rect(SCREEN, (255,255,255), mbox, border_radius=8)
        pygame.draw.rect(SCREEN, triadic_3, mbox, 3, border_radius=8)
        txtw = get_font(26).render(input_word or "Word (Tab to switch)", True, (10,10,10))
        txtm = get_font(26).render(input_meaning or "Meaning", True, (10,10,10))
        SCREEN.blit(txtw, (wbox.x+12, wbox.y+14)); SCREEN.blit(txtm, (mbox.x+12, mbox.y+14))

        add_btn = Button((WIDTH//2-120, 220, 240, 60), "Add Word", get_font(26), base=triadic_3, hover=triadic_2)
        back_btn = Button((WIDTH//2-120, 300, 240, 60), "Back", get_font(26), base=triadic_3, hover=triadic_2)
        add_btn.draw(mouse); back_btn.draw(mouse)

        # show list of words (paginated)
        start_y = 340
        for i, item in enumerate(cards[-12:]):  # show last 12
            txt = f"{i+1}. {item.get('word','')} - {item.get('meaning','')}"
            SCREEN.blit(get_font(22).render(txt, True, (255,255,255)), (120, start_y + i*28))

        draw_text(f"{len(cards)}/{MAX_WORDS} words (max 30)", get_font(20), triadic_2, (WIDTH-220, 40))

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_TAB:
                    active = "meaning" if active=="word" else "word"
                elif ev.key==pygame.K_BACKSPACE:
                    if active=="word":
                        input_word = input_word[:-1]
                    else:
                        input_meaning = input_meaning[:-1]
                elif ev.key==pygame.K_RETURN:
                    if input_word.strip() and input_meaning.strip() and len(cards) < MAX_WORDS:
                        cards.append({"word": input_word.strip(), "meaning": input_meaning.strip()})
                        input_word = ""; input_meaning = ""
                        data["cards"] = cards
                        data["style"] = style
                        save_deck_file(deck_filename, data)
                        click_sound()
                else:
                    if active=="word" and len(input_word) < 30:
                        input_word += ev.unicode
                    elif active=="meaning" and len(input_meaning) < 60:
                        input_meaning += ev.unicode
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                if add_btn.is_clicked(mouse):
                    if input_word.strip() and input_meaning.strip() and len(cards) < MAX_WORDS:
                        cards.append({"word": input_word.strip(), "meaning": input_meaning.strip()})
                        input_word = ""; input_meaning = ""
                        data["cards"] = cards
                        data["style"] = style
                        save_deck_file(deck_filename, data)
                        click_sound()
                if back_btn.is_clicked(mouse):
                    return

        pygame.display.flip()

def choose_style_flow():
    # allow user to pick a style image; present existing images in Image/cards/
    available = []
    card_folder = "Image/cards"
    if os.path.exists(card_folder):
        for f in os.listdir(card_folder):
            if f.lower().endswith((".png",".jpg",".jpeg")):
                available.append(os.path.join(card_folder, f))
    # if none found fallback to base
    if not available:
        available = [CARD_BASE_PATH]

    idx = 0
    while True:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        SCREEN.fill(triadic_2)
        draw_text("Choose card style (Left/Right). Enter to select. Esc to cancel.", get_font(22), triadic_3, (WIDTH//2, 40))
        # show thumbnail center
        p = available[idx]
        try:
            img = pygame.image.load(p).convert_alpha()
            img = pygame.transform.smoothscale(img, (300,420))
            SCREEN.blit(img, img.get_rect(center=(WIDTH//2, HEIGHT//2)))
        except Exception:
            draw_text("Image load error", get_font(20), (255,0,0), (WIDTH//2, HEIGHT//2))

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_LEFT:
                    idx = (idx-1) % len(available)
                if ev.key==pygame.K_RIGHT:
                    idx = (idx+1) % len(available)
                if ev.key==pygame.K_RETURN:
                    return available[idx]
                if ev.key==pygame.K_ESCAPE:
                    return None
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                # treat left/right click
                x,y = ev.pos
                if x < WIDTH//2:
                    idx = (idx-1)%len(available)
                else:
                    idx = (idx+1)%len(available)
        pygame.display.flip()

def free_for_all():
    # listing deck thumbnails and create/edit/play
    scroll = 0
    while True:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        SCREEN.fill(basecolor)
        draw_text("Free For All - Select Deck (Click to Edit / Play)", get_font(26), triadic_3, (WIDTH//2, 30))

        decks = list_decks()
        # draw grid of thumbnails 4 per row
        per_row = 4
        box_w, box_h = 220, 280
        spacing_x, spacing_y = 260, 320
        start_x = (WIDTH - (per_row*spacing_x - (spacing_x - box_w)))//2
        start_y = 80 + scroll

        deck_rects = []
        for i, fname in enumerate(decks):
            row = i // per_row; col = i % per_row
            x = start_x + col*spacing_x
            y = start_y + row*spacing_y
            rect = pygame.Rect(x, y, box_w, box_h)
            # load deck style
            data = load_deck_file(fname)
            style = data.get("style", CARD_BASE_PATH)
            try:
                thumb = pygame.image.load(style).convert_alpha()
                thumb = pygame.transform.smoothscale(thumb, (box_w, box_h))
            except Exception:
                # fallback colored rect
                thumb = pygame.Surface((box_w,box_h))
                thumb.fill((200,200,200))
            SCREEN.blit(thumb, (x,y))
            # border
            pygame.draw.rect(SCREEN, triadic_3, rect, 4, border_radius=12)
            # deck name under
            nm = fname.replace(".json","")
            draw_text(nm, get_font(20), triadic_2, (x+box_w//2, y+box_h+18))
            deck_rects.append((rect,fname))

        # create new deck thumb
        idx = len(decks)
        row = idx//per_row; col = idx%per_row
        cx = start_x + col*spacing_x; cy = start_y + row*spacing_y
        create_rect = pygame.Rect(cx, cy, box_w, box_h)
        pygame.draw.rect(SCREEN, (240,240,255), create_rect, border_radius=12)
        pygame.draw.rect(SCREEN, triadic_3, create_rect, 4, border_radius=12)
        draw_text("+", get_font(60), triadic_2, create_rect.center)
        draw_text("Create Deck", get_font(20), triadic_2, (cx + box_w//2, cy+box_h+18))

        # BACK
        back = Button((WIDTH-160, HEIGHT-60, 140, 44), "Back", get_font(20), base=triadic_3, hover=triadic_2)
        back.draw(mouse)

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEWHEEL:
                scroll += ev.y*40
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                click_sound()
                # check deck clicks
                for rect, fname in deck_rects:
                    if rect.collidepoint(mouse):
                        # open small menu: Edit / Play / Delete / Choose Style
                        deck_choice_menu(fname)
                        break
                if create_rect.collidepoint(mouse):
                    # choose style then name then create
                    style = choose_style_flow()
                    fname = create_deck_flow(style_path=style)
                    if fname:
                        click_sound()
                if back.is_clicked(mouse):
                    return
        pygame.display.flip()

def deck_choice_menu(fname):
    # small popup offering Edit / Play / Delete / Choose Style
    while True:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        SCREEN.fill((50,0,70))
        draw_text(f"Deck: {fname}", get_font(26), triadic_2, (WIDTH//2, 60))
        edit = Button((WIDTH//2-140, 140, 280, 64), "Edit Deck", get_font(24))
        play = Button((WIDTH//2-140, 220, 280, 64), "Play Deck", get_font(24))
        choose_style = Button((WIDTH//2-140, 300, 280, 64), "Change Style", get_font(24))
        delete = Button((WIDTH//2-140, 380, 280, 64), "Delete Deck", get_font(24), base=(180,30,30))
        back = Button((WIDTH//2-140, 460, 280, 64), "Back", get_font(24))
        for b in (edit,play,choose_style,delete,back):
            b.draw(mouse)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                click_sound()
                if edit.is_clicked(mouse):
                    edit_deck_flow(fname); return
                if play.is_clicked(mouse):
                    # choose stage 5/10/15 selection popup
                    choose_stage_and_start(fname)
                    return
                if choose_style.is_clicked(mouse):
                    style = choose_style_flow()
                    if style:
                        data = load_deck_file(fname)
                        data["style"]=style
                        save_deck_file(fname, data)
                        click_sound()
                        return
                if delete.is_clicked(mouse):
                    try:
                        os.remove(os.path.join(DECK_DIR,fname))
                        click_sound()
                    except Exception as e:
                        print("Delete error", e)
                    return
                if back.is_clicked(mouse):
                    return
        pygame.display.flip()

def choose_stage_and_start(deck_fname):
    # allow user to pick 5/10/15 (require deck has at least that many cards)
    data = load_deck_file(deck_fname)
    ncards = len(data["cards"])
    options = [5,10,15]
    valid = [x for x in options if ncards>=x]
    if not valid:
        # cannot start
        while True:
            clock.tick(FPS)
            mouse = pygame.mouse.get_pos()
            SCREEN.fill((40,10,60))
            draw_text("Deck doesn't have enough cards. Add more in Edit.", get_font(24), triadic_2, (WIDTH//2, HEIGHT//2))
            back = Button((WIDTH//2-100, HEIGHT-200, 200, 60), "Back", get_font(22))
            back.draw(mouse)
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and back.is_clicked(mouse):
                    return
            pygame.display.flip()
    else:
        # present buttons for valid
        while True:
            clock.tick(FPS)
            mouse = pygame.mouse.get_pos()
            SCREEN.fill(basecolor)
            draw_text("Choose Stage (cards):", get_font(28), triadic_3, (WIDTH//2, 80))
            btns = []
            for i,val in enumerate(valid):
                b = Button((WIDTH//2-160 + i*180, 160, 160, 60), str(val), get_font(24))
                b.draw(mouse)
                btns.append((b,val))
            back = Button((WIDTH//2-80, 260, 160, 48), "Back", get_font(20))
            back.draw(mouse)
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                    click_sound()
                    for b,val in btns:
                        if b.is_clicked(mouse):
                            # fetch options answer_time
                            at = options_screen.__dict__.get("answer_time_setting", 10)
                            res, meta = battle_screen(deck_fname.replace(".json",""), val, at)
                            # show result
                            show_battle_result(res, meta)
                            return
                    if back.is_clicked(mouse):
                        return
            pygame.display.flip()

def show_battle_result(res, meta):
    # simple result popup
    while True:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        SCREEN.fill(triadic_3)
        draw_text("Battle Result", get_font(34), triadic_2, (WIDTH//2, 80))
        draw_text(f"Result: {res}", get_font(28), (255,255,255), (WIDTH//2, 140))
        draw_text(f"HP left: {meta.get('hp',0)}/{meta.get('max_hp',0)}", get_font(22), (255,255,255), (WIDTH//2, 180))
        back = Button((WIDTH//2-100, 260, 200, 60), "Back", get_font(24))
        back.draw(mouse)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and back.is_clicked(mouse):
                return
        pygame.display.flip()

# entry
if __name__ == "__main__":
    # ensure there's at least one deck default
    if not list_decks():
        save_deck_file("Default.json", {"style": CARD_BASE_PATH, "cards": [
            {"word":"Apple","meaning":"แอปเปิ้ล"},
            {"word":"Dog","meaning":"สุนัข"},
            {"word":"Cat","meaning":"แมว"},
            {"word":"Water","meaning":"น้ำ"},
            {"word":"Sun","meaning":"พระอาทิตย์"},
            {"word":"Moon","meaning":"พระจันทร์"}
        ]})
    # try to load BGM if exists
    try:
        if os.path.exists("Music/034. Memory.mp3"):
            background_music("Music/034. Memory.mp3", background_music_volume)
    except Exception:
        pass
    main_menu()
