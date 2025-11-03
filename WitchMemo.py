"""Witch Memo Game Script"""
import pygame, sys, random, socket, getpass, json, os, time
from button import Button
from math import floor # เพิ่ม math.floor สำหรับการคำนวณเวลาบอส

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 1920, 1080
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Witch's Memo")

background_music_volume = 0.5
ishint = False #Fast mode
answer_time = 5 #เริ่มที่ 5 วิ

computer_name = socket.gethostname()
user_name = getpass.getuser()

DECK_DIR = "decks"
os.makedirs(DECK_DIR, exist_ok=True)

BG = pygame.image.load("Image/Background/forestbackground.jpg")
BG = pygame.transform.scale(BG, (screen_width, screen_height))
basecolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) #สุ่มสีเริ่มต้น
triadic_2 = [basecolor[0] + 85, basecolor[1] + 85, basecolor[2] + 85] #การทำสีที่สองของ Triadic Theory
triadic_3 = [triadic_2[0] + 85, triadic_2[1] + 85, triadic_2[2] + 85] #การทำสีที่สามของ Triadic Theory
#pygame.mouse.set_visible(False)
for i in range(3): #แปลงรหัสสีตาม Triadic Theory
    if triadic_2[i] > 255:
        triadic_2[i] -= 255
    if triadic_3[i] > 255:
        triadic_3[i] -= 255

intro_time = 0

current_music = None
def background_music(path, volume, loop):
    global current_music, background_music_volume, ishint
    try:
        if intro_time > 3:
            path = "Music/So cold.mp3"
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
        elif current_music != path and not intro_time > 3:
            current_music = path
            if ishint:
                pygame.mixer.music.fadeout(500)
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(background_music_volume)
            pygame.mixer.music.play(loop)
    except Exception as e:
        print("Error Please Check :", e)

def get_font(size, which_font):
    if intro_time > 4:
        return pygame.font.SysFont("Wingdings", size)
    else:
        if which_font == 1:
            return pygame.font.Font("Font/PixelMedium.ttf", size)
        elif which_font == 2:
            return pygame.font.Font("Font/SansThai.ttf", size)

def sfx_func(sfx):
    try:
        pygame.mixer.Sound(sfx).play()
    except Exception as e:
        print(f"SFX Error: {e}")

def screen_color():
    if intro_time > 3:
        SCREEN.fill("black")
    else:
        SCREEN.fill(basecolor)

count_hints = 0
def hint(hint_number):
    global count_hints
    pygame.time.Clock().tick(5)
    if not intro_time > 3:
        hints = [
        "การจดจำเพียงอย่างเดียวอาจไม่ได้ช่วยอะไร จงหมั่นฝึกฝนด้วย!", "ทุกการจดจำคือการเรียนรู้!",
        "การทบทวนทีละนิดนั้นดีกว่าการไม่ทำอะไรเลย!", "การเรียนรู้คือเวทย์มนตร์ที่แท้จริง!",
        "ยิ่งจดจำได้มากเท่าไหร่ก็ยิ่งมีความสามารถมากเท่านั้น!", "เวทมนตร์เชื่อมโยงกับความรู้และความจำ!",
        "ความผิดพลาดคือส่วนหนึ่งของการฝึกฝนไม่มีใครร่ายถูกตั้งแต่ครั้งแรก!", "จงกล้าที่จะจำ จงกล้าที่จะลืม และจงกล้าที่จะเรียนรู้ใหม่อีกครั้ง!",
        "การฝึกจำคือการชุบชีวิตให้ความรู้เก่าอีกครั้งหนึ่ง!", "แม่มดที่ยิ่งใหญ่ ไม่ได้มีพลังมากที่สุด แต่เรียนรู้และจดจำได้เร็วที่สุด!",
        "ความเข้าใจคือรากฐานของเวทมนตร์ทุกแขนง!", "การใช้แฟลชการ์ดก็เหมือนการฝึกคาถาซ้ำ ๆ จนชำนาญ!",
        "สมุนไพรไม่เติบโตในวันเดียว เช่นเดียวกับความรู้ของคุณ!", "อย่ากลัวที่จะผิด เพราะทุกครั้งที่ผิดคือการก้าวไปข้างหน้าอีกขั้น!"
#       "เมื่อเจ้าพร้อมเปิดใจ โลกของเวทมนตร์แห่งความรู้จะเปิดออกให้เจ้าเห็น!", "จงสร้างพลังแห่งความจำจากการฝึกซ้ำในทุก ๆ วัน!",
#        "จิตใจที่สงบจะช่วยให้เวทย์แห่งการจดจำชัดเจนยิ่งขึ้น!", "อย่าหยุดเรียนรู้ เพราะเวทมนตร์นั้นจะสลายไปเมื่อเจ้าหยุดฝึก!",
#        "การเรียนรู้คือการเดินทาง ไม่ใช่จุดหมายปลายทาง!", "วันนี้เจ้าทบทวนไปกี่คำแล้วล่ะ แม่มดน้อยแห่งความรู้?"
        ]
        count_hints = len(hints) - 1
        hint_text = hints[hint_number]
        PLAY_TEXT = get_font(35, 2).render(hint_text, True, triadic_2)
    else:
        hints = [
        "Why?", "You wanna leave me alone?",
        "Do you really want this " + user_name + "?", "why? why? why? why? why?",
        user_name + " " + user_name + " " + user_name+ " " + user_name + " " + user_name
        , "01000001 01101100 01110100",
        "AHAHHAHAHAHAHHAAHHAAHHAHAHA!", "00101011 01000110 00110100",
        "Logic Error. . .", "01101100 01100101 01100001 01110110 01100101",
        "? ? ?", "Won't you remember me?",
        "Don't you want me anymore?", "Really?",
        "Will you remember me?", "No no no no no no no no no no no no no no no no no no no no no no no no no no no no no no no no no no no",
        user_name + "why?", user_name + " " + computer_name + " " + user_name + " " + computer_name + " " + user_name + " " + computer_name,
        "Ahhhhhhhhhhhhhhhhhhhhhhhh!", "01110100 01101111"
        ]
        count_hints = len(hints) - 1
        hint_text = hints[hint_number]
        PLAY_TEXT = get_font(45, 2).render(hint_text, True, (255, 255, 255))
    PLAY_RECT = PLAY_TEXT.get_rect(center=(screen_width//2, screen_height//2))
    SCREEN.blit(PLAY_TEXT, PLAY_RECT)

def click_to_skip(random_text):
    pygame.time.Clock().tick(5)
    TEST_LIST = ["Click To Skip", "You Can Disable Hint In The Options"]
    PLAY_TEXT = get_font(25, 2).render(TEST_LIST[random_text], True, (220, 220, 220))
    PLAY_RECT = PLAY_TEXT.get_rect(center=(screen_width//2, screen_height//2 + 400))
    SCREEN.blit(PLAY_TEXT, PLAY_RECT)

def transition_to(next_function, next_music_path):
    global ishint
    hint_number = random.randint(0,count_hints)
    random_skip = random.randint(0, 1)

    clock = pygame.time.Clock()
    fade_surface = pygame.Surface((screen_width, screen_height))

    if intro_time > 3:
        fade_surface.fill((138, 3, 3))  # เลือด
        fade_speed = 5
    else:
        fade_surface.fill((255, 255, 255))  # ขาว
        fade_speed = 25

    if ishint:
        alpha = 0
    elif not ishint and intro_time > 3:
        alpha = 0
    else:
        alpha = 256
    start_volume = pygame.mixer.music.get_volume()

    current_scene = SCREEN.copy()

    while alpha < 255:
        SCREEN.blit(current_scene, (0, 0))
        fade_surface.set_alpha(alpha)
        SCREEN.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(100)

        current_vol = max(0, start_volume * (1 - alpha / 255))
        pygame.mixer.music.set_volume(current_vol)
        alpha += fade_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    background_music(next_music_path, background_music_volume, -1)

    if ishint:
        alpha = 255
    elif not ishint and intro_time > 3:
        alpha = 255
    else:
        alpha = -1
    fade_surface.set_alpha(alpha)

    while alpha > 0:
        if not intro_time > 3:
            hint(hint_number)
            click_to_skip(random_skip)
        else:
            hint(random.randint(0, count_hints))
        fade_surface.set_alpha(alpha)
        SCREEN.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(100)
        alpha -= fade_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not intro_time > 3:
                if event.button == 1:
                    sfx_func("SFX/Click.mp3")
                    next_function()
                    return

    if intro_time > 10:
        pygame.time.wait(1500)
        pygame.quit()
    if ishint:
        pygame.time.wait(1000)
    next_function()

# =================================================================
# ===== [ 1. เพิ่ม HELPER FUNCTIONS และ CLASS ใหม่ ] =====
# =================================================================

# --- [ CACHE สำหรับมอนสเตอร์ ] ---
MONSTER_SPRITE_CACHE = []
BOSS_SPRITE_CACHE = []

def load_sprite_cache_from_folder(folder_path, fallback_color=(100, 0, 100)):
    """
    [ฟังก์ชันใหม่ที่รวมกันแล้ว]
    สแกนโฟลเดอร์ที่ระบุ และโหลดรูปทั้งหมดกลับมาเป็น List
    """
    if not os.path.exists(folder_path):
        print(f"!!! Sprite Error: ไม่พบโฟลเดอร์ '{folder_path}'")
        # สร้าง Sprite สำรอง
        fallback = pygame.Surface((100, 100))
        fallback.fill(fallback_color)
        return [fallback] # คืนค่า list ที่มีรูปสำรอง

    loaded_sprites = []
    for f in os.listdir(folder_path):
        if f.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(folder_path, f)
            img = load_image_asset(full_path) 
            if img:
                loaded_sprites.append(img)
    
    if not loaded_sprites:
        print(f"!!! Sprite Error: ไม่พบไฟล์รูปภาพใน '{folder_path}'")
        # สร้าง Sprite สำรอง
        fallback = pygame.Surface((100, 100))
        fallback.fill(fallback_color)
        loaded_sprites.append(fallback)
        
    return loaded_sprites

def load_image_asset(path, size=None):
    """
    ฟังก์ชันช่วยโหลดรูปภาพพร้อมปรับขนาด และจัดการหากไฟล์ไม่เจอ
    """
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception as e:
        print(f"!!! Asset Error: ไม่สามารถโหลดไฟล์ '{path}'. {e}")
        # สร้าง Surface สีแดงแทนถ้าโหลดไม่ได้
        fallback = pygame.Surface(size if size else (50, 50))
        fallback.fill((255, 0, 0))
        return fallback

def load_deck_file(deck_name_without_json):
    """
    ฟังก์ชันสำหรับโหลดข้อมูล deck จากไฟล์ .json
    (ปรับปรุงจากโค้ดเดิมใน free_for_all)
    """
    path = os.path.join(DECK_DIR, deck_name_without_json + ".json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # ตรวจสอบโครงสร้างไฟล์
        if "style" not in data:
            data["style"] = "Image/cards/card.png"
        if "cards" not in data or not isinstance(data["cards"], list):
            data["cards"] = []
            
        # กรองการ์ดที่ไม่มีคำศัพท์หรือความหมาย
        valid_cards = [c for c in data["cards"] if c.get("word") and c.get("meaning")]
        data["cards"] = valid_cards
            
        return data
    except Exception as e:
        print(f"Load deck error: {e}")
        return {"style": "Image/cards/card.png", "cards": []}

class DraggableCard:
    """
    คลาสสำหรับการ์ดที่ผู้เล่นสามารถลากเพื่อตอบได้ (ใช้ระบบ Polling)
    """
    def __init__(self, rect, word, meaning, style_img):
        self.base_rect = pygame.Rect(rect) # ตำแหน่งเดิม
        self.rect = pygame.Rect(rect)      # ตำแหน่งปัจจุบัน
        self.word = word
        self.meaning = meaning
        self.card_img = style_img # ภาพพื้นหลังการ์ด (โหลดมาจาก style)
        
        self.is_dragging = False
        self.show_answer = False
        self.snap_back = False # สถานะที่บอกว่าต้องเด้งกลับ
        self.font_q = get_font(40, 2)
        self.font_a = get_font(32, 2)

    def handle_event(self, event):
        """
        จัดการเฉพาะการกด (Down) และปล่อย (Up) เมาส์
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and not self.show_answer:
                self.is_dragging = True
                self.snap_back = False
                return "DRAGGING"
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                # ตรวจสอบโซนที่ปล่อย
                if self.rect.centerx > screen_width - 400: # โซนขวา (Know)
                    return "ANSWER_KNOW"
                elif self.rect.centerx < 400: # โซนซ้าย (Don't Know)
                    return "ANSWER_DONT_KNOW"
                else:
                    self.snap_back = True # ปล่อยกลางจอ
                    return "NO_ANSWER"
        return None

    def update_pos(self, mouse_pos):
        """
        อัปเดตตำแหน่งการ์ดตามเมาส์ (ถ้ากำลังลาก)
        """
        if self.is_dragging:
            self.rect.center = mouse_pos

    def draw(self, surface):
        """
        วาดการ์ดและข้อความ
        """
        # ถ้าต้องเด้งกลับ ให้ค่อยๆ เคลื่อนกลับไปที่ base_rect
        if self.snap_back and not self.is_dragging:
            self.rect.x += (self.base_rect.x - self.rect.x) * 0.2
            self.rect.y += (self.base_rect.y - self.rect.y) * 0.2
            if abs(self.base_rect.x - self.rect.x) < 1:
                self.rect = pygame.Rect(self.base_rect) # Snap
                self.snap_back = False

        # วาดการ์ด
        surface.blit(self.card_img, self.rect)
        
        # วาดคำถาม (Word)
        word_surf = self.font_q.render(self.word, True, (0,0,0))
        word_rect = word_surf.get_rect(center=self.rect.center)
        surface.blit(word_surf, word_rect)

        # ถ้าระหว่างเฉลย
        if self.show_answer:
            # วาดคำตอบ (Meaning)
            ans_surf = self.font_a.render(self.meaning, True, (20, 120, 50))
            ans_rect = ans_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 60))
            surface.blit(ans_surf, ans_rect)

    def reveal(self):
        """
        สั่งให้การ์ดแสดงเฉลยและเด้งกลับตรงกลาง
        """
        self.show_answer = True
        self.snap_back = True

# =================================================================
# ===== [ 2. ระบบต่อสู้ใหม่ (BATTLE SYSTEM) ] =====
# =================================================================

def battle_screen(deck_name, count_cards, is_boss_stage):
    """
    หน้าจอต่อสู้หลัก (ระบบใหม่ทั้งหมด)
    [Gemini v3 Edit: แก้ไข Layout ทั้งหมดให้ยึด screen_width/height // 2 
     และเปลี่ยนการแสดงผลมอนสเตอร์เป็น Sprite]
    """
    global answer_time # ดึงค่าเวลามาจาก options
    
    # --- 1. Setup ---
    data = load_deck_file(deck_name)
    style_img_path = data.get("style", "Image/cards/card.png")
    cards = data.get("cards", [])
    
    # --- โหลด Assets ---
    try:
        card_style_img = load_image_asset("Image/cards/card_font.png", (335, 458))
        heart_full = load_image_asset("Image/Icon (buff, health-bar)/heart/heart(Full-HP).png", (64, 64))
        heart_dmg = load_image_asset("Image/Icon (buff, health-bar)/heart/heart(damaged).png", (64, 64))
        heart_shield_overlay = load_image_asset("Image/Icon (buff, health-bar)/heart/heart - (Sheild).PNG", (64, 64))
        
        skill_heal_img = load_image_asset("Image/Icon (buff, health-bar)/Icon-buff/Heal.png", (80, 80))
        skill_shield_img = load_image_asset("Image/Icon (buff, health-bar)/Icon-buff/Sheild.png", (80, 80))
        skill_stop_img = load_image_asset("Image/Icon (buff, health-bar)/Icon-buff/Freeze.png", (80, 80))
        skill_ginger_img = load_image_asset("Image/Icon (buff, health-bar)/Icon-buff/Gingerbread (eat 2 gain more hearts).PNG", (80, 80))
        
        # โหลดตัวละคร Witch
        witch_img = load_image_asset("Image/MC Witch.png", (400, 400))
        witch_img = pygame.transform.flip(witch_img, True, False)
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการโหลด Asset: {e}")
        return "DEFEAT" 

    # ตั้งค่า Timer
    if is_boss_stage:
        per_card_time = floor(answer_time / 2)
    else:
        per_card_time = answer_time
    per_card_time = max(1, per_card_time)

    # สุ่มการ์ด
    if len(cards) < count_cards:
        print("Deck มีการ์ดไม่พอ!")
        return "DEFEAT"
    
    selected = random.sample(cards, count_cards)
    queue = selected[:]
    wrong_cards = []
    random.shuffle(queue)

    # --- 2. Player & Monster Stats ---
    max_hp = 3
    hp = max_hp
    streak = 0
    skill_points = 0
    shield_active = False
    skill_used_this_turn = False 
    gingerbread_eaten = 0 
    
    # --- [แก้ไข] ตั้งค่า Monster และ HP สูงสุด ---
    max_monster_hp = 5 # ค่าเริ่มต้นสำหรับมอนปกติ
    if is_boss_stage:
        monsters_count = 1
        monster_hp_value = max(1, count_cards)
        monster_hp = [monster_hp_value] 
        monster_names = ["BOSS"]
        max_monster_hp = monster_hp_value
    else:
        if count_cards <= 5: monsters_count = 1
        elif count_cards <= 10: monsters_count = 2
        else: monsters_count = 3
        monster_hp = [5] * monsters_count
        monster_names = [f"Monster {i+1}" for i in range(monsters_count)]
        # max_monster_hp เป็น 5 อยู่แล้ว

    # --- สุ่ม Sprite มอนสเตอร์ ---
    assigned_monster_sprites = []
    monster_sprite_rects = [] # [เพิ่ม] List สำหรับเก็บ Rect ของมอนสเตอร์
    monster_sprite_size = (150, 150) # [เพิ่ม] ขนาดตัวมอนสเตอร์

    if MONSTER_SPRITE_CACHE:
        # --- [แก้ไข] คำนวณตำแหน่งมอนสเตอร์ (ยึดกลางจอ) ---
        monster_y_pos = screen_height // 4 # ตำแหน่งแกน Y (บนๆ)
        
        # กำหนดตำแหน่ง X ตามจำนวนมอนสเตอร์
        if monsters_count == 1:
            positions_x = [screen_width // 2]
        elif monsters_count == 2:
            positions_x = [screen_width // 2 - 200, screen_width // 2 + 200]
        else: # 3
            positions_x = [screen_width // 2 - 350, screen_width // 2, screen_width // 2 + 350]

        for i in range(monsters_count):
            sprite_img = random.choice(MONSTER_SPRITE_CACHE)
            sprite_img_scaled = pygame.transform.scale(sprite_img, monster_sprite_size)
            sprite_rect = sprite_img_scaled.get_rect(center=(positions_x[i], monster_y_pos))
            
            assigned_monster_sprites.append(sprite_img_scaled)
            monster_sprite_rects.append(sprite_rect)


    # --- 3. Game State & UI ---
    game_state = "NEW_CARD" 
    current_card_obj = None
    current_card_dict = None
    card_start_time = 0
    reveal_until = 0 
    time_stopped_for_card = False

    game_log = []
    def log(msg, color=(255, 255, 255)):
        game_log.append((msg, color))
        if len(game_log) > 5:
            game_log.pop(0)

    log(f"Battle Start! Stage: {count_cards} cards.", (255, 255, 0))

    # --- [แก้ไข] สร้างปุ่มสกิล (ยึดกลางจอ) ---
    skill_y = screen_height - 160 # y = 880
    skill_heal_btn = Button(image=skill_heal_img, pos=((screen_width // 2) - 240, skill_y), text_input="", font=get_font(1,1), base_color="White", hovering_color="Green")
    skill_shield_btn = Button(image=skill_shield_img, pos=((screen_width // 2) - 80, skill_y), text_input="", font=get_font(1,1), base_color="White", hovering_color="Green")
    skill_stop_btn = Button(image=skill_stop_img, pos=((screen_width // 2) + 80, skill_y), text_input="", font=get_font(1,1), base_color="White", hovering_color="Green")
    skill_maxhp_btn = Button(image=skill_ginger_img, pos=((screen_width // 2) + 240, skill_y), text_input="", font=get_font(1,1), base_color="White", hovering_color="Green")
    
    skill_buttons = [skill_heal_btn, skill_shield_btn, skill_stop_btn, skill_maxhp_btn]
    skill_costs = {
        skill_heal_btn: 1,
        skill_shield_btn: 2,
        skill_stop_btn: 2,
        skill_maxhp_btn: 1
    }

    # --- 4. Game Loop (Battle) ---
    running = True
    result = "DEFEAT" 
    
    def handle_answer(answer_type):
        nonlocal game_state, reveal_until, current_card_obj, current_card_dict
        nonlocal streak, skill_points, shield_active, hp, running, result
        
        game_state = "REVEALING"
        reveal_until = pygame.time.get_ticks() + 1500 
        current_card_obj.reveal() 
        sfx_func("SFX/Click.mp3")

        if answer_type == "ANSWER_KNOW":
            sfx_func("SFX/hitted.mp3")
            log("Correct!", (0, 255, 0))
            streak += 1
            if streak % 3 == 0 and streak > 0:
                skill_points += 1
                log("Skill Point +1!", (255, 255, 0))
            
            for i in range(len(monster_hp)):
                if monster_hp[i] > 0:
                    monster_hp[i] -= 1
                    log(f"Hit {monster_names[i]}! (HP: {monster_hp[i]})")
                    if monster_hp[i] <= 0:
                        log(f"{monster_names[i]} defeated!", (0, 255, 0))
                        sfx_func("SFX/boom.mp3")
                    break
        
        else: # "ANSWER_DONT_KNOW" หรือ "TIMEOUT"
            sfx_func("SFX/hitted.mp3")
            log("Wrong / Don't Know", (255, 100, 100))
            streak = 0
            wrong_cards.append(current_card_dict) 
            
            if shield_active:
                shield_active = False
                #sfx_func("SFX/hitsteel.mp3")
                sfx_func("SFX/shield-break.mp3")
                log("Shield blocked 1 damage!", (0, 200, 255))
            else:
                #sfx_func("SFX/hitted.mp3")
                hp -= 1
                log("Lost 1 Heart!", (255, 0, 0))

        if hp <= 0:
            log("HP reached 0... You are defeated.", (255, 0, 0))
            result = "DEFEAT"
            running = False
            
        if all(mhp <= 0 for mhp in monster_hp):
            log("All monsters defeated! VICTORY!", (0, 255, 0))
            result = "VICTORY"
            running = False

    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        MOUSE_POS = pygame.mouse.get_pos()
        
        # --- 5. Logic: Update (Polling) ---
        if game_state == "WAITING" and current_card_obj:
            current_card_obj.update_pos(MOUSE_POS)
        for btn in skill_buttons:
            btn.changeColor(MOUSE_POS)
            
        # --- 6. Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            # 6.1 จัดการการลากการ์ด
            if game_state == "WAITING" and current_card_obj:
                card_event = current_card_obj.handle_event(event) 
                if card_event == "ANSWER_KNOW":
                    handle_answer("ANSWER_KNOW")
                elif card_event == "ANSWER_DONT_KNOW":
                    handle_answer("ANSWER_DONT_KNOW")

            # 6.2 จัดการการกดสกิล
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "WAITING" and not skill_used_this_turn: 
                    if skill_heal_btn.checkForInput(MOUSE_POS):
                        if skill_points >= skill_costs[skill_heal_btn]:
                            if max_hp == hp:
                                log("You HP is max!", (0, 200, 255))
                            else:
                                sfx_func("SFX/heal.mp3")
                                skill_points -= skill_costs[skill_heal_btn]
                                hp = min(max_hp, hp + 1)
                                log("Heal! +1 Heart.", (0, 255, 0))
                                sfx_func("SFX/Click.mp3")
                                skill_used_this_turn = True 
                        else:
                            log("Not enough SP!", (255, 100, 100))
                            
                    elif skill_shield_btn.checkForInput(MOUSE_POS):
                        if skill_points >= skill_costs[skill_shield_btn]:
                            if shield_active:
                                log("Shield Already Activated!", (0, 200, 255))
                            else:
                                sfx_func("SFX/bat_hit.mp3")
                                skill_points -= skill_costs[skill_shield_btn]
                                shield_active = True
                                log("Shield Activated!", (0, 200, 255))
                                sfx_func("SFX/Click.mp3")
                                skill_used_this_turn = True
                        else:
                            log("Not enough SP!", (255, 100, 100))

                    elif skill_stop_btn.checkForInput(MOUSE_POS):
                        if skill_points >= skill_costs[skill_stop_btn]:
                            if time_stopped_for_card:
                                log("Time Stop Already Activated!", (0, 200, 255))
                            else:
                                sfx_func("SFX/time-stop.mp3")
                                skill_points -= skill_costs[skill_stop_btn]
                                time_stopped_for_card = True 
                                log("Time Stop Activated!", (0, 200, 255))
                                sfx_func("SFX/Click.mp3")
                                skill_used_this_turn = True 
                        else:
                            log("Not enough SP!", (255, 100, 100))

                    elif skill_maxhp_btn.checkForInput(MOUSE_POS):
                        if skill_points >= skill_costs[skill_maxhp_btn]:
                            skill_points -= skill_costs[skill_maxhp_btn]
                            if gingerbread_eaten == 0:
                                sfx_func("SFX/nomnomnom.mp3")
                                gingerbread_eaten = 1
                                log("Ate 1/2 Gingerbread...", (200, 200, 200))
                                sfx_func("SFX/Click.mp3")
                                skill_used_this_turn = True 
                            elif gingerbread_eaten == 1:
                                sfx_func("SFX/heal.mp3")
                                gingerbread_eaten = 0 
                                max_hp += 1
                                hp += 1 
                                log("Max HP Increased!", (255, 255, 0))
                                sfx_func("SFX/Click.mp3")
                                skill_used_this_turn = True 
                        else:
                            log("Not enough SP for 2/2!", (255, 100, 100))

        # --- 7. Game State Logic ---
        
        # 7.1 หมดเวลา
        if game_state == "WAITING" and not time_stopped_for_card:
            elapsed = (pygame.time.get_ticks() - card_start_time) / 1000.0
            if elapsed > per_card_time:
                log("Time Out!", (255, 100, 100))
                handle_answer("TIMEOUT")
        
        # 7.2 หมดเวลาเฉลย -> ไปการ์ดใหม่
        if game_state == "REVEALING":
            if pygame.time.get_ticks() > reveal_until:
                if not running:
                    pygame.time.wait(500) 
                    return result
                game_state = "NEW_CARD"
                
        # 7.3 สร้างการ์ดใหม่
        if game_state == "NEW_CARD":
            skill_used_this_turn = False
            
            if not queue: 
                if not wrong_cards: 
                    if all(mhp <= 0 for mhp in monster_hp):
                         result = "VICTORY"
                    else:
                         log("Cards finished, but monsters remain...", (255, 100, 100))
                         result = "DEFEAT"
                    running = False 
                    continue 
                else:
                    log("Reshuffling wrong cards...", (200, 200, 255))
                    queue = wrong_cards[:]
                    wrong_cards.clear()
                    random.shuffle(queue)

            if queue:
                current_card_dict = queue.pop(0)
                card_w, card_h = 335, 458
                card_rect_x = (screen_width // 2) - (card_w // 2)
                card_rect_y = (screen_height // 2) - (card_h // 2) - 50 
                card_rect = (card_rect_x, card_rect_y, card_w, card_h)
                current_card_obj = DraggableCard(card_rect, 
                                                current_card_dict.get("word", "??"), 
                                                current_card_dict.get("meaning", "??"), 
                                                card_style_img)
                game_state = "WAITING"
                card_start_time = pygame.time.get_ticks()
                time_stopped_for_card = False

        # --- 8. Drawing ---
        screen_color()
        
        # --- [แก้ไข] วาดโซนลาก (ยึดกลางจอ) ---
        zone_width = 450
        s_left = pygame.Surface((zone_width, screen_height), pygame.SRCALPHA)
        s_left.fill((255, 100, 100, 50))
        # ตำแหน่ง X = กลางจอ - (ครึ่งจอ) = 0
        s_left_x = (screen_width // 2) - (screen_width // 2) + 190
        SCREEN.blit(s_left, (s_left_x, 0))
        
        s_right = pygame.Surface((zone_width, screen_height), pygame.SRCALPHA)
        s_right.fill((100, 255, 100, 50))
        # ตำแหน่ง X = กลางจอ + ครึ่งจอ - ความกว้างโซน = 1920 - 400 = 1520
        s_right_x = (screen_width // 2) + (screen_width // 2) - zone_width - 190
        SCREEN.blit(s_right, (s_right_x, 0))
        
        # --- [แก้ไข] วาดข้อความโซน (ยึดกลางจอ) ---
        title_font = get_font(40, 1).render("Don't Know", True, "white")
        # ตำแหน่ง X = กลางจอ - 760 (เพื่อให้ไปอยู่กลางโซนซ้ายที่ 200)
        title_rect_left = title_font.get_rect(center=((screen_width // 2) - 560, screen_height // 2))
        SCREEN.blit(title_font, title_rect_left)
        
        title_font = get_font(40, 1).render("Know", True, "white")
        # ตำแหน่ง X = กลางจอ + 760 (เพื่อให้ไปอยู่กลางโซนขวาที่ 1720)
        title_rect_right = title_font.get_rect(center=((screen_width // 2) + 560, screen_height // 2))
        SCREEN.blit(title_font, title_rect_right)
        
        # --- [แก้ไข] วาด HP (ยึดกลางจอ) ---
        # ตำแหน่ง X = กลางจอ - 940 (เพื่อให้ไปอยู่ซ้ายสุดที่ 20)
        hp_x_start = (screen_width // 2) - 600
        for i in range(max_hp):
            if i == (hp - 1) and shield_active:
                SCREEN.blit(heart_shield_overlay, (hp_x_start + i * 74, 75))
            elif i < hp:
                SCREEN.blit(heart_full, (hp_x_start + i * 74, 75))
            else:
                SCREEN.blit(heart_dmg, (hp_x_start + i * 74, 75))
        
        # (แสดง HP และ Streak เป็นข้อความ)
        hp_text = f"HP: {hp} / {max_hp}"
        hp_text_surf = get_font(25, 1).render(hp_text, True, "white")
        hp_text_rect = hp_text_surf.get_rect(left=hp_x_start, top=20 + 120) # (y=75)
        SCREEN.blit(hp_text_surf, hp_text_rect)

        streak_text = f"Streak: {streak}"
        streak_text_surf = get_font(25, 1).render(streak_text, True, "white")
        streak_text_rect = streak_text_surf.get_rect(left=hp_x_start, top=20 + 140) # (y=105)
        SCREEN.blit(streak_text_surf, streak_text_rect)

        
        # --- [แก้ไข] วาดมอนสเตอร์ (Sprite และ HP เหนือหัว) ---
        hp_bar_font = get_font(20, 1) # Font สำหรับ HP มอนสเตอร์
        for i in range(monsters_count):
            if monster_hp[i] > 0:
                # 1. วาด Sprite
                sprite_img = assigned_monster_sprites[i]
                sprite_rect = monster_sprite_rects[i]
                SCREEN.blit(sprite_img, sprite_rect)

                # 2. คำนวณ HP Bar
                bar_width = 100
                bar_height = 15
                hp_pct = monster_hp[i] / max_monster_hp
                current_hp_width = int(bar_width * hp_pct)
                
                # 3. ตำแหน่ง Bar (ยึดตาม rect ของ sprite)
                bar_x = sprite_rect.centerx - (bar_width // 2)
                bar_y = sprite_rect.top - 25 # (เหนือหัว 25px)

                # 4. วาด Bar (พื้นหลังสีแดง/เทา)
                pygame.draw.rect(SCREEN, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
                # 5. วาด Bar (เลือดปัจจุบันสีเขียว)
                pygame.draw.rect(SCREEN, (60, 200, 60), (bar_x, bar_y, current_hp_width, bar_height), border_radius=4)
                
                # 6. วาด HP Text
                hp_text_mon = f"{monster_hp[i]} / {max_monster_hp}"
                hp_surf = hp_bar_font.render(hp_text_mon, True, "white")
                hp_rect = hp_surf.get_rect(center=(sprite_rect.centerx, bar_y - 15)) # (เหนือ Bar 15px)
                SCREEN.blit(hp_surf, hp_rect)

        # วาดการ์ด
        if current_card_obj:
            current_card_obj.draw(SCREEN)

        # วาด Timer (ยึดกลางจอ)
        if game_state == "WAITING" or (game_state == "REVEALING" and time_stopped_for_card):
            t_left = per_card_time
            if not time_stopped_for_card:
                elapsed = (pygame.time.get_ticks() - card_start_time) / 1000.0
                t_left = max(0, per_card_time - elapsed)
            
            bar_w = 400
            pct = 1.0 if time_stopped_for_card else (t_left / per_card_time)
            bar_color = (220,243,255) if time_stopped_for_card else (80, 160, 240)
            
            # (กลางจอ - 200, สูง - 250)
            timer_bar_x = (screen_width // 2) - (bar_w // 2)
            timer_bar_y = screen_height - 300
            
            pygame.draw.rect(SCREEN, (50,50,50), (timer_bar_x, timer_bar_y, bar_w, 20), border_radius=8)
            pygame.draw.rect(SCREEN, bar_color, (timer_bar_x, timer_bar_y, int(bar_w * pct), 20), border_radius=8)
            
            timer_text = "FREEZE" if time_stopped_for_card else f"{t_left:.1f}s"
            timer_surf = get_font(25, 1).render(timer_text, True, "white")
            timer_rect = timer_surf.get_rect(center=(screen_width // 2, timer_bar_y - 30))
            SCREEN.blit(timer_surf, timer_rect)

        # --- [แก้ไข] วาด Witch Sprite (ยึดกลางจอ) ---
        if witch_img:
            # (กลางจอ - 920 = 40, กลางจอ + ครึ่งจอ - 40 = 1040)
            witch_x = (screen_width // 2) - 920
            witch_y_bottom = (screen_height // 2) + (screen_height // 2) - 40
            witch_rect = witch_img.get_rect(bottomleft=(witch_x, witch_y_bottom))
            SCREEN.blit(witch_img, witch_rect)


        # --- [แก้ไข] วาด UI สกิล (ยึดกลางจอ) ---
        font_skill_cost = get_font(20, 1)
        font_skill_points = get_font(35, 1)
        
        # (แสดง Skill Points เหนือปุ่ม)
        sp_surf = font_skill_points.render(f"Skill Points: {skill_points}", True, triadic_3)
        sp_rect = sp_surf.get_rect(center=(screen_width // 2, skill_y - 80)) # (y=840)
        SCREEN.blit(sp_surf, sp_rect)
        
        # (ลบ Streak ออกจากตรงนี้ เพราะไปอยู่มุมซ้ายบนแล้ว)

        # อัปเดตเงื่อนไข is_locked
        is_locked = (game_state != "WAITING") or skill_used_this_turn
        
        for btn in skill_buttons:
            cost = skill_costs[btn]
            btn.update(SCREEN)
            
            cost_text = f"({cost} SP)"
            if btn == skill_maxhp_btn:
                cost_text = f"({cost} SP) [{gingerbread_eaten}/2]"
                
            cost_surf = font_skill_cost.render(cost_text, True, "white")
            cost_rect = cost_surf.get_rect(center=(btn.rect.centerx, btn.rect.bottom + 15))
            SCREEN.blit(cost_surf, cost_rect)
            
            if is_locked:
                lock_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
                lock_surf.fill((0, 0, 0, 180))
                SCREEN.blit(lock_surf, btn.rect.topleft)
            elif skill_points < cost and (btn != skill_maxhp_btn or gingerbread_eaten == 0):
                lock_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
                lock_surf.fill((200, 0, 0, 100))
                SCREEN.blit(lock_surf, btn.rect.topleft)

        # --- [แก้ไข] วาด Game Log (ยึดกลางจอ) ---
        log_y_start = (screen_height // 2) + 200 # (y=740)
        log_x = (screen_width // 2) - 510 # (x=450)
        for i, (msg, color) in enumerate(game_log):
            SCREEN.blit(get_font(22, 2).render(msg, True, color), (log_x, log_y_start + i * 25)) 

        pygame.display.flip()

    # --- 9. Battle End ---
    return result
def show_battle_result(result, deck_name):
    """
    หน้าจอสรุปผลแพ้/ชนะ
    """
    sfx_func("SFX/boom.mp3" if result == "DEFEAT" else "SFX/mus_wawa.mp3")

    sfx_func("SFX/victory.mp3") if result == "VICTORY" else sfx_func("SFX/fail.mp3")
    
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(basecolor if result == "VICTORY" else (50, 0, 0))
        result_text_surf = get_font(100, 1).render(result, True, triadic_3 if result == "VICTORY" else (255, 50, 50))
        SCREEN.blit(result_text_surf, result_text_surf.get_rect(center=(screen_width//2, screen_height//2 - 100)))

        BACK_BUTTON = Button(None, (screen_width//2, screen_height//2 + 100), "BACK", get_font(75, 1), triadic_2, triadic_3)
        BACK_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    # กลับไปหน้า deck_choice_menu
                    transition_to(lambda: deck_choice_menu(deck_name), "Music/017. Snowy.mp3")
                    return
        
        pygame.display.update()

def choose_stage_and_start(deck_name):
    """
    หน้าจอเลือกด่าน (5, 10, 15, 20, Boss)
    นี่คือฟังก์ชันใหม่ที่มาแทน play_deck เดิม
    """
    data = load_deck_file(deck_name)
    n_cards = len(data.get("cards", []))
    
    available_stages = []
    if n_cards >= 5: available_stages.append(5)
    if n_cards >= 10: available_stages.append(10)
    if n_cards >= 15: available_stages.append(15)
    if n_cards >= 20: available_stages.append(20)
    if n_cards > 20: available_stages.append(n_cards) # Boss Stage
    
    if not available_stages:
        # ไม่สามารถเริ่มได้ (การ์ดน้อยกว่า 5)
        while True:
            MOUSE_POS = pygame.mouse.get_pos()
            screen_color()
            err_text = get_font(40, 2).render(f"Deck '{deck_name}' needs at least 5 cards to play.", True, (255, 100, 100))
            SCREEN.blit(err_text, err_text.get_rect(center=(screen_width//2, screen_height//2 - 50)))
            
            BACK_BUTTON = Button(None, (screen_width//2, screen_height//2 + 100), "BACK", get_font(75, 1), triadic_2, triadic_3)
            BACK_BUTTON.changeColor(MOUSE_POS)
            BACK_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if BACK_BUTTON.checkForInput(MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        transition_to(lambda: deck_choice_menu(deck_name), "Music/017. Snowy.mp3")
                        return
            pygame.display.update()
    
    # มีด่านให้เลือก
    stage_buttons = []
    total_btns = len(available_stages)
    btn_width = 200
    btn_spacing = 50
    total_width = (total_btns * btn_width) + ((total_btns - 1) * btn_spacing)
    start_x = (screen_width - total_width) // 2
    
    for i, stage_count in enumerate(available_stages):
        is_boss = (stage_count > 20)
        text = f"BOSS ({stage_count})" if is_boss else f"{stage_count} Cards"
        font_size = 40 if is_boss else 50
        
        btn = Button(None, (start_x + i * (btn_width + btn_spacing) + (btn_width//2), screen_height//2), text, get_font(font_size, 1), triadic_2, triadic_3)
        stage_buttons.append((btn, stage_count, is_boss))

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        screen_color()
        
        title_text = get_font(65, 1).render("Choose Your Stage", True, triadic_3)
        SCREEN.blit(title_text, title_text.get_rect(center=(screen_width//2, 200)))

        for btn, count, is_boss in stage_buttons:
            btn.changeColor(MOUSE_POS)
            btn.update(SCREEN)
            
        BACK_BUTTON = Button(None, (screen_width//2, screen_height - 150), "BACK", get_font(75, 1), triadic_2, triadic_3)
        BACK_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    transition_to(lambda: deck_choice_menu(deck_name), "Music/017. Snowy.mp3")
                    return
                
                for btn, count, is_boss in stage_buttons:
                    if btn.checkForInput(MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        # เริ่มเกม
                        result = battle_screen(deck_name, count, is_boss)
                        # แสดงผลลัพธ์
                        show_battle_result(result, deck_name)
                        return # กลับไปหน้า deck_choice_menu (ผ่าน show_battle_result)

        pygame.display.update()

def play_deck(deck_name):
    """
    ฟังก์ชันนี้ถูกเรียกโดย transition_to เมื่อกด "PLAY"
    เราจะเรียกฟังก์ชันเลือกด่าน (choose_stage_and_start) จากตรงนี้
    """
    # หยุดเพลงที่กำลังเล่นจาก transition
    pygame.mixer.music.fadeout(500) 
    
    # เรียกหน้าจอเลือกด่าน
    choose_stage_and_start(deck_name)
    
    # (ฟังก์ชันนี้จะจบลงเมื่อ choose_stage_and_start/battle_screen/show_battle_result
    # เรียก transition_to กลับไปที่ deck_choice_menu)
    return

# =================================================================
# ===== [ 3. โค้ดเดิมของ WitchMemo.py (ไม่เปลี่ยนแปลง) ] =====
# =================================================================

def select_mode():
    background_music("Music/003. Your Best Friend.mp3", background_music_volume, -1)
    global intro_time
    if intro_time > 3:
        sfx_func("SFX/thatsawonderfulidea.mp3")
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        # screen_color()
        bg = pygame.image.load("Image/Background/selectmode_bg.png")
        bg = pygame.transform.scale(bg, (screen_width, screen_height))
        SCREEN.blit(bg, (0, 0))
        PLAY_TEXT = get_font(45, 1).render(user_name + ", Please Select Mode To Play.", True, triadic_2)
        PLAY_RECT = PLAY_TEXT.get_rect(center = (screen_width//2, 150))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image = None, pos = (screen_width//2, 940), text_input = "BACK", font = get_font(75, 1), base_color = triadic_2, hovering_color = triadic_3)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        base_card = pygame.image.load("Image/cards/card.png").convert_alpha()
        base_card = pygame.transform.scale(base_card, (469, 641))

        STORY_BUTTON = Button(image=base_card, pos=(screen_width//2 - 300, screen_width//2 - 400), 
                            text_input="STORY", font=get_font(49, 1), base_color="#95884A", hovering_color = "#BCB277")
        
        FREEFORALL_BUTTON = Button(image=base_card, pos=(screen_width//2 + 300, screen_width//2 - 400), 
                            text_input="FREE FOR ALL", font=get_font(27, 1), base_color="#95884A", hovering_color = "#BCB277")

        for button in [STORY_BUTTON, FREEFORALL_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if STORY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        transition_to(story_mode, "Music/024. Bonetrousle.mp3")
                    if FREEFORALL_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        transition_to(free_for_all, "Music/017. Snowy.mp3")
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        transition_to(main_menu, "Music/092. Reunited.mp3")
        pygame.display.update()

def create_deck(style_path):
    deck_dir = "decks"
    os.makedirs(deck_dir, exist_ok=True)
    user_input = ""
    clock = pygame.time.Clock()
    error_text = ""
    error_timer = 0  # เวลาแสดง error 2 วินาที

    while True:
        CREATE_MOUSE_POS = pygame.mouse.get_pos()
        editdeck3_bg = pygame.image.load("Image/Background/editing_deck3.png")
        SCREEN.blit(editdeck3_bg, (0, 0))

        PROMPT = get_font(55, 1).render("Enter New Deck Name:", True, triadic_2)
        SCREEN.blit(PROMPT, PROMPT.get_rect(center=(screen_width//2, 250)))

        BOX = pygame.Rect(screen_width//2 - 300, 350, 600, 80)
        pygame.draw.rect(SCREEN, (255,255,255), BOX, border_radius=8)
        pygame.draw.rect(SCREEN, (160,100,220), BOX, 3, border_radius=8)
        SCREEN.blit(get_font(50, 2).render(user_input, True, (90,0,130)), (BOX.x + 20, BOX.y))

        BACK_BUTTON = Button(None, (screen_width//2, 800), "BACK", get_font(75, 1), triadic_3, triadic_2)
        CREATE_BUTTON = Button(None, (screen_width//2, 600), "CREATE", get_font(75, 1), (200,180,255), (255,255,255))

        for button in [BACK_BUTTON, CREATE_BUTTON]:
            button.changeColor(CREATE_MOUSE_POS)
            button.update(SCREEN)

        # แสดงข้อความ error (สีแดง)
        if error_text:
            err_surface = get_font(40, 1).render(error_text, True, (255, 60, 60))
            SCREEN.blit(err_surface, err_surface.get_rect(center=(screen_width//2, 500)))
            error_timer -= clock.get_time()
            if error_timer <= 0:
                error_text = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition_to(free_for_all, "Music/017. Snowy.mp3")
                    return
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    deck_name = user_input.strip()
                    fname = os.path.join(deck_dir, deck_name + ".json")
                    if not deck_name:
                        sfx_func("SFX/wrong.mp3")
                        error_text = "Name cannot be empty!"
                        error_timer = 2000
                    elif os.path.exists(fname):
                        sfx_func("SFX/wrong.mp3")
                        error_text = "Deck name already exists!"
                        error_timer = 2000
                    else:
                        with open(fname, "w", encoding="utf-8") as f:
                            json.dump({"style": style_path, "cards": []}, f, ensure_ascii=False, indent=4)
                        sfx_func("SFX/Click.mp3")
                        transition_to(free_for_all, "Music/017. Snowy.mp3")
                        return
                else:
                    if len(user_input) < 20:
                        user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BACK_BUTTON.checkForInput(CREATE_MOUSE_POS):
                    transition_to(free_for_all, "Music/017. Snowy.mp3")
                    return
                if CREATE_BUTTON.checkForInput(CREATE_MOUSE_POS):
                    deck_name = user_input.strip()
                    fname = os.path.join(deck_dir, deck_name + ".json")
                    if not deck_name:
                        sfx_func("SFX/wrong.mp3")
                        error_text = "Name cannot be empty!"
                        error_timer = 2000
                    elif os.path.exists(fname):
                        sfx_func("SFX/wrong.mp3")
                        error_text = "Deck name already exists!"
                        error_timer = 2000
                    else:
                        with open(fname, "w", encoding="utf-8") as f:
                            json.dump({"style": style_path, "cards": []}, f, ensure_ascii=False, indent=4)
                        sfx_func("SFX/Click.mp3")
                        transition_to(free_for_all, "Music/017. Snowy.mp3")
                        return

        pygame.display.update()
        clock.tick(60)



def free_for_all():
    background_music("Music/017. Snowy.mp3", background_music_volume, -1)
    deck_dir = "decks"
    os.makedirs(deck_dir, exist_ok=True)

    scroll_offset = 0
    scroll_speed = 60
    clock = pygame.time.Clock()

    # โหลดพื้นหลังและการ์ดหลักแค่ครั้งเดียว
    bg = pygame.image.load("Image/Background/selectmode_bg.png").convert()
    base_card = pygame.image.load("Image/cards/card.png").convert_alpha()
    base_card = pygame.transform.scale(base_card, (335, 458))

    # โหลดภาพการ์ดแบบ cache
    loaded_styles = {}

    def get_card_image(style_path):
        """โหลดภาพการ์ดจาก path ถ้ามีใน cache แล้วใช้เลย"""
        if style_path not in loaded_styles:
            if not os.path.exists(style_path):
                style_path = "Image/cards/card.png"
            img = pygame.image.load(style_path).convert_alpha()
            img = pygame.transform.scale(img, (335, 458))
            loaded_styles[style_path] = img
        return loaded_styles[style_path]

    while True:
        FREEFORALL_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(bg, (0, 0))

        title_text = get_font(65, 1).render("Select Your Deck", True, triadic_3)
        SCREEN.blit(title_text, title_text.get_rect(center=(screen_width // 2, 100)))

        deck_files = [f for f in os.listdir(deck_dir) if f.endswith(".json")]

        box_w, box_h = 335, 458
        spacing_x, spacing_y = 375, 500
        max_per_row = 4

        total_rows = (len(deck_files) + 1 + max_per_row - 1) // max_per_row
        start_x = (screen_width - (max_per_row * spacing_x - (spacing_x - box_w))) // 2
        start_y = 200 + scroll_offset

        deck_buttons = []

        for i, deck in enumerate(deck_files):
            deck_path = os.path.join(deck_dir, deck)
            try:
                with open(deck_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    style_path = data.get("style", "Image/cards/card.png")
            except:
                style_path = "Image/cards/card.png"

            card_img = get_card_image(style_path)

            row = i // max_per_row
            col = i % max_per_row
            box_x = start_x + col * spacing_x
            box_y = start_y + row * spacing_y
            box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

            hovering = box_rect.collidepoint(FREEFORALL_MOUSE_POS)
            if hovering:
                hover_overlay = pygame.Surface(card_img.get_size(), pygame.SRCALPHA)
                hover_overlay.fill((255, 255, 255, 80))
                card_img_hover = card_img.copy()
                card_img_hover.blit(hover_overlay, (0, 0))
                SCREEN.blit(card_img_hover, (box_x, box_y))
            else:
                SCREEN.blit(card_img, (box_x, box_y))

            deck_name = deck.replace(".json", "")
            name_text = get_font(30, 2).render(deck_name, True, triadic_2)
            name_rect = name_text.get_rect(center=(box_rect.centerx, box_rect.bottom + 10))
            SCREEN.blit(name_text, name_rect)
            deck_buttons.append((box_rect, deck_name))

        # ปุ่ม CREATE NEW DECK
        create_index = len(deck_files)
        row = create_index // max_per_row
        col = create_index % max_per_row
        create_x = start_x + col * spacing_x
        create_y = start_y + row * spacing_y
        SCREEN.blit(base_card, (create_x, create_y))

        plus_text = get_font(200, 1).render("+", True, "#BCB277")
        SCREEN.blit(plus_text, plus_text.get_rect(center=(create_x + box_w//2, create_y + box_h//2)))
        label_text = get_font(35, 1).render("CREATE NEW DECK", True, triadic_2)
        SCREEN.blit(label_text, label_text.get_rect(center=(create_x + box_w//2, create_y + box_h + 10)))

        BACK_BUTTON = Button(None, (screen_width//2, screen_height-120), "BACK", get_font(75,1), triadic_3, triadic_2)
        BACK_BUTTON.changeColor(FREEFORALL_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * scroll_speed
                scroll_offset = max(min(0, scroll_offset), -((total_rows * spacing_y) - screen_height + 350))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, name in deck_buttons:
                    if rect.collidepoint(FREEFORALL_MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        transition_to(lambda: deck_choice_menu(name), "Music/017. Snowy.mp3")
                        return
                if pygame.Rect(create_x, create_y, box_w, box_h).collidepoint(FREEFORALL_MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    transition_to(choose_card_style, "Music/017. Snowy.mp3")
                    return
                if BACK_BUTTON.checkForInput(FREEFORALL_MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    transition_to(select_mode, "Music/092. Reunited.mp3")
                    return

        pygame.display.update()
        clock.tick(60)  # จำกัด FPS ไว้ที่ 60


def deck_choice_menu(fname):
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        preparedeck_bg = pygame.image.load("Image/Background/prepare_deck.jpg")
        SCREEN.blit(preparedeck_bg, (0, 0))

        OPTIONS_TEXT = get_font(85, 2).render(f"Deck: {fname}", True, triadic_2)
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_TEXT.get_rect(center=(screen_width//2, 130)))

        buttons = [
            ("PLAY", 300),
            ("EDIT", 400),
            ("RENAME", 500),
            ("CHANGE STYLE", 600),
            ("DELETE", 700),
            ("BACK", 940)
        ]
        deck_buttons = []
        for text, y in buttons:
            btn = Button(None, (screen_width//2, y), text, get_font(75, 1), triadic_2, triadic_3)
            if text == "DELETE":
                btn.hovering_color = (255, 0, 0)
            btn.changeColor(OPTIONS_MOUSE_POS)
            btn.update(SCREEN)
            deck_buttons.append((text, btn))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for text, btn in deck_buttons:
                    if btn.checkForInput(OPTIONS_MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        if text == "BACK":
                            transition_to(free_for_all, "Music/017. Snowy.mp3")
                            return
                        elif text == "PLAY":
                            # <<<<<<<<<<<<<<<< [ นี่คือจุดที่แก้ไข ] <<<<<<<<<<<<<<<<
                            # transition_to(lambda: play_deck(fname), "Music/017. Snowy.mp3")
                            # เราจะเรียก play_deck โดยตรง (ซึ่งจะเรียก choose_stage_and_start)
                            # และ transition_to จะถูกเรียกจากข้างในแทน
                            play_deck(fname)
                            return
                        elif text == "EDIT":
                            transition_to(lambda: edit_deck(fname), "Music/017. Snowy.mp3")
                        elif text == "RENAME":
                            transition_to(lambda: rename_deck(fname), "Music/017. Snowy.mp3")
                            return
                        elif text == "CHANGE STYLE":
                            transition_to(lambda: change_style(fname), "Music/017. Snowy.mp3")
                            return
                        elif text == "DELETE":
                            try:
                                os.remove(os.path.join("decks", fname + ".json"))
                            except Exception as e:
                                print("Delete error", e)
                            sfx_func("SFX/boom.mp3")
                            transition_to(free_for_all, "Music/017. Snowy.mp3")
                            return

        pygame.display.update()

def edit_deck(deck_name):
    deck_path = os.path.join("decks", deck_name + ".json")
    os.makedirs("decks", exist_ok=True)

    # โหลด deck ถ้ามีอยู่แล้ว
    if os.path.exists(deck_path):
        with open(deck_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"style": "Image/cards/card.png", "cards": []}
    else:
        data = {"style": "Image/cards/card.png", "cards": []}

    # ดึงข้อมูลจาก dict
    words = data.get("cards", [])
    style_path = data.get("style", "Image/cards/card.png")

    MAX_WORDS = 30
    input_word = ""
    input_meaning = ""
    active_input = "word"

    # Scroll control
    scroll_offset = 0
    scroll_speed = 40
    clock = pygame.time.Clock()

    while True:
        EDIT_MOUSE_POS = pygame.mouse.get_pos()
        dt = clock.tick(60) / 16.67
        cw_bg = pygame.image.load("Image/Background/crafting-witch.png")
        SCREEN.blit(cw_bg, (0, 0))

        if not 23 - len(input_word):
            word_ismax = (255, 0, 0)
        else:
            word_ismax = triadic_3

        if not 23 - len(input_meaning):
            mean_ismax = (255, 0,0 )
        else:
            mean_ismax = triadic_3

        if input_word.strip() and input_meaning.strip() and len(words) < MAX_WORDS:
            all_ismax = triadic_3
        else:
            all_ismax = (255, 0, 0)

        # -------------------------------
        # Title
        # -------------------------------
        TITLE = get_font(70, 2).render(f"Edit Deck: {deck_name}", True, triadic_3)
        SCREEN.blit(TITLE, TITLE.get_rect(center=(screen_width // 2, 140)))

        hint = get_font(35, 1).render(f"Max Characters Is 23 Per Box", True, triadic_3)
        SCREEN.blit(hint, hint.get_rect(center=(screen_width // 2, 200)))

        word_left = get_font(35, 1).render(f"Word Characters Left : {23 - len(input_word)}", True, word_ismax)
        SCREEN.blit(word_left, word_left.get_rect(center=(screen_width//2 - 330, 350)))

        mean_left = get_font(35, 1).render(f"Word Characters Left : {23 - len(input_meaning)}", True, mean_ismax)
        SCREEN.blit(mean_left, mean_left.get_rect(center=(screen_width//2 + 340, 350)))

        # กล่องใส่คำ
        word_box = pygame.Rect(screen_width//2 - 600, 250, 550, 70)
        meaning_box = pygame.Rect(screen_width//2 + 70, 250, 550, 70)
        pygame.draw.rect(SCREEN, (220, 180, 255) if active_input == "word" else (255, 255, 255), word_box, border_radius=8)
        pygame.draw.rect(SCREEN, triadic_3, word_box, 3, border_radius=8)
        pygame.draw.rect(SCREEN, (220, 180, 255) if active_input == "meaning" else (255, 255, 255), meaning_box, border_radius=8)
        pygame.draw.rect(SCREEN, triadic_3, meaning_box, 3, border_radius=8)

        SCREEN.blit(get_font(35, 2).render(input_word or "Word", True, (90, 0, 130)), (word_box.x + 20, word_box.y + 15))
        SCREEN.blit(get_font(35, 2).render(input_meaning or "Meaning", True, (90, 0, 130)), (meaning_box.x + 20, meaning_box.y + 15))

        # ปุ่ม Add / Back
        ADD_BUTTON = Button(image=None, pos=(screen_width//2, 400),
                            text_input="ADD WORD", font=get_font(55, 1),
                            base_color=(200, 180, 255), hovering_color=all_ismax)
        BACK_BUTTON = Button(image=None, pos=(screen_width//2, 950),
                             text_input="BACK", font=get_font(75, 1),
                             base_color=triadic_3, hovering_color=triadic_2)
        for button in [ADD_BUTTON, BACK_BUTTON]:
            button.changeColor(EDIT_MOUSE_POS)
            button.update(SCREEN)

        # แสดงคำใน deck
        list_start_y = 500 + scroll_offset
        item_height = 50
        total_height = len(words) * item_height
        visible_top = 480
        visible_bottom = screen_height - 200

        for i, item in enumerate(words):
            y_pos = list_start_y + i * item_height
            if y_pos < visible_top - item_height or y_pos > visible_bottom + item_height:
                continue

            word_display = f"{i+1}. {item['word']}  -  {item['meaning']}"
            SCREEN.blit(get_font(35, 2).render(word_display, True, triadic_2), (screen_width//2 - 520, y_pos))

            # ปุ่มลบ
            del_rect = pygame.Rect(screen_width//2 + 530, y_pos, 100, 40)
            pygame.draw.rect(SCREEN, (255, 80, 80), del_rect, border_radius=5)
            SCREEN.blit(get_font(30, 1).render("DEL", True, (255,255,255)), del_rect.move(20, 5))

            # ตรวจจับลบ
            if pygame.mouse.get_pressed()[0] and del_rect.collidepoint(EDIT_MOUSE_POS):
                sfx_func("SFX/boom.mp3")
                del words[i]
                data["cards"] = words
                with open(deck_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                break

        # Counter
        counter_text = get_font(30, 1).render(f"{len(words)}/{MAX_WORDS} words", True, triadic_2)
        SCREEN.blit(counter_text, (screen_width//2 + 550, screen_height//2 - 460))

        # Scroll bar
        if total_height > (visible_bottom - visible_top):
            bar_h = max(50, (visible_bottom - visible_top)**2 / total_height)
            bar_y = visible_top + (-scroll_offset / total_height) * (visible_bottom - visible_top - bar_h)
            pygame.draw.rect(SCREEN, triadic_3, (screen_width - 50, bar_y, 15, bar_h), border_radius=6)

        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * scroll_speed
                scroll_offset = max(min(0, scroll_offset), visible_bottom - (total_height + visible_top))

            if event.type == pygame.KEYDOWN:
                sfx_func("SFX/Click.mp3")
                if event.key == pygame.K_ESCAPE:
                    transition_to(deck_choice_menu(deck_name), "Music/017. Snowy.mp3")
                    return
                elif event.key == pygame.K_TAB:
                    active_input = "meaning" if active_input == "word" else "word"
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == "word":
                        input_word = input_word[:-1]
                    else:
                        input_meaning = input_meaning[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_word.strip() and input_meaning.strip() and len(words) < MAX_WORDS:
                        words.append({"word": input_word.strip(), "meaning": input_meaning.strip()})
                        input_word, input_meaning = "", ""
                        data["cards"] = words
                        with open(deck_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                    else:
                        sfx_func("SFX/wrong.mp3")
                else:
                    if active_input == "word" and len(input_word) < 23:
                        input_word += event.unicode
                    elif active_input == "meaning" and len(input_meaning) < 23:
                        input_meaning += event.unicode
                    else:
                        sfx_func("SFX/wrong.mp3")

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if word_box.collidepoint(EDIT_MOUSE_POS):
                    sfx_func("SFX/Click.mp3"); active_input = "word"
                elif meaning_box.collidepoint(EDIT_MOUSE_POS):
                    sfx_func("SFX/Click.mp3"); active_input = "meaning"
                if ADD_BUTTON.checkForInput(EDIT_MOUSE_POS):
                    if input_word.strip() and input_meaning.strip() and len(words) < MAX_WORDS:
                        sfx_func("SFX/Click.mp3")
                        words.append({"word": input_word.strip(), "meaning": input_meaning.strip()})
                        input_word, input_meaning = "", ""
                        data["cards"] = words
                        with open(deck_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                    else:
                        sfx_func("SFX/wrong.mp3")
                if BACK_BUTTON.checkForInput(EDIT_MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    transition_to(deck_choice_menu(deck_name), "Music/017. Snowy.mp3")
                    return

        pygame.display.update()

def change_style(deck_name):
    """เปลี่ยน style ของ deck ที่เลือก"""
    deck_path = os.path.join("decks", deck_name + ".json")
    if not os.path.exists(deck_path):
        print("Deck not found.")
        transition_to(free_for_all, "Music/017. Snowy.mp3")
        return

    try:
        with open(deck_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"cards": [], "style": "Image/cards/card.png"}

    scroll_offset = 0
    scroll_speed = 80

    styles = [
        ("Ank", "Image/cards/ank.png"),
        ("Circle", "Image/cards/circle.png"),
        ("Cross", "Image/cards/cross.png"),
        ("Eye", "Image/cards/eye.png"),
        ("Heart", "Image/cards/heart.png"),
        ("Triple Moon", "Image/cards/triplemoon.png"),
    ]

    loaded_styles = []
    for name, path in styles:
        if not os.path.exists(path):
            continue
        icon = pygame.image.load(path).convert_alpha()
        icon = pygame.transform.scale(icon, (335, 458))
        loaded_styles.append((name, path, icon))

    base_card = pygame.image.load("Image/cards/card.png").convert_alpha()
    base_card = pygame.transform.scale(base_card, (335, 458))

    card_hover = base_card.copy()
    hover_surface = pygame.Surface(card_hover.get_size(), pygame.SRCALPHA)
    hover_surface.fill((255, 255, 255, 60))
    card_hover.blit(hover_surface, (0, 0))

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        preparedeck_bg = pygame.image.load("Image/Background/prepare_deck.jpg")
        SCREEN.blit(preparedeck_bg, (0, 0))

        title_text = get_font(65, 1).render(f"Change Style for {deck_name}", True, triadic_3)
        SCREEN.blit(title_text, title_text.get_rect(center=(screen_width // 2, 100)))

        spacing_x = 375
        spacing_y = 500
        max_per_row = 3
        box_w, box_h = 335, 458

        total_rows = (len(loaded_styles) + max_per_row - 1) // max_per_row
        grid_height = total_rows * spacing_y
        start_x = (screen_width - (max_per_row * spacing_x - (spacing_x - box_w))) // 2
        start_y = 250 + scroll_offset

        card_buttons = []
        for i, (name, path, icon) in enumerate(loaded_styles):
            row = i // max_per_row
            col = i % max_per_row
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            rect = pygame.Rect(x, y, box_w, box_h)

            hovering = rect.collidepoint(MOUSE_POS)
            SCREEN.blit(card_hover if hovering else base_card, (x, y))
            SCREEN.blit(icon, (x, y))
            text = get_font(35, 1).render(name, True, triadic_2)
            SCREEN.blit(text, text.get_rect(center=(rect.centerx, rect.bottom + 20)))
            card_buttons.append((rect, path))

        BACK_BUTTON = Button(
            image=None,
            pos=(screen_width // 2, screen_height - 120),
            text_input="BACK",
            font=get_font(75, 1),
            base_color=triadic_3,
            hovering_color=triadic_2,
        )
        BACK_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * scroll_speed
                max_scroll = 0
                min_scroll = min(0, screen_height - (grid_height + 400))
                scroll_offset = max(min_scroll, min(scroll_offset, max_scroll))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, path in card_buttons:
                    if rect.collidepoint(MOUSE_POS):
                        data["style"] = path
                        with open(deck_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        sfx_func("SFX/Click.mp3")
                        transition_to(lambda: deck_choice_menu(deck_name), "Music/017. Snowy.mp3")
                        return
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    transition_to(lambda: deck_choice_menu(deck_name), "Music/017. Snowy.mp3")
                    return

        pygame.display.update()

def rename_deck(old_name):
    deck_dir = "decks"
    old_path = os.path.join(deck_dir, old_name + ".json")
    user_input = old_name
    clock = pygame.time.Clock()
    error_text = ""
    error_timer = 0

    while True:
        RENAME_MOUSE_POS = pygame.mouse.get_pos()
        bg = pygame.image.load("Image/Background/editing_deck3.png")
        SCREEN.blit(bg, (0, 0))

        PROMPT = get_font(55, 1).render("Enter New Deck Name:", True, triadic_2)
        SCREEN.blit(PROMPT, PROMPT.get_rect(center=(screen_width//2, 250)))

        BOX = pygame.Rect(screen_width//2 - 300, 350, 600, 80)
        pygame.draw.rect(SCREEN, (255,255,255), BOX, border_radius=8)
        pygame.draw.rect(SCREEN, triadic_2, BOX, 3, border_radius=8)
        SCREEN.blit(get_font(50, 2).render(user_input, True, (90,0,130)), (BOX.x + 20, BOX.y))

        BACK_BUTTON = Button(None, (screen_width//2, 800), "BACK", get_font(75, 1), triadic_3, triadic_2)
        SAVE_BUTTON = Button(None, (screen_width//2, 600), "SAVE", get_font(75, 1), (200,180,255), (255,255,255))

        for b in [BACK_BUTTON, SAVE_BUTTON]:
            b.changeColor(RENAME_MOUSE_POS)
            b.update(SCREEN)

        if error_text:
            err_surface = get_font(40, 1).render(error_text, True, (255, 60, 60))
            SCREEN.blit(err_surface, err_surface.get_rect(center=(screen_width//2, 500)))
            error_timer -= clock.get_time()
            if error_timer <= 0:
                error_text = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                sfx_func("SFX/Click.mp3")
                if event.key == pygame.K_ESCAPE:
                    transition_to(lambda: deck_choice_menu(old_name), "Music/017. Snowy.mp3")
                    return
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    new_name = user_input.strip()
                    new_path = os.path.join(deck_dir, new_name + ".json")
                    if not new_name:
                        error_text = "Name cannot be empty!"
                        error_timer = 2000
                    elif os.path.exists(new_path):
                        error_text = "Deck name already exists!"
                        error_timer = 2000
                    else:
                        os.rename(old_path, new_path)
                        transition_to(lambda: deck_choice_menu(new_name), "Music/017. Snowy.mp3")
                        return
                else:
                    if len(user_input) < 20:
                        user_input += event.unicode
                    else:
                        sfx_func("SFX/wrong.mp3")

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BACK_BUTTON.checkForInput(RENAME_MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    transition_to(lambda: deck_choice_menu(old_name), "Music/017. Snowy.mp3")
                    return
                if SAVE_BUTTON.checkForInput(RENAME_MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    new_name = user_input.strip()
                    new_path = os.path.join(deck_dir, new_name + ".json")
                    if not new_name:
                        sfx_func("SFX/wrong.mp3")
                        error_text = "Name cannot be empty!"
                        error_timer = 2000
                    elif os.path.exists(new_path):
                        sfx_func("SFX/wrong.mp3")
                        error_text = "Deck name already exists!"
                        error_timer = 2000
                    else:
                        os.rename(old_path, new_path)
                        transition_to(lambda: deck_choice_menu(new_name), "Music/017. Snowy.mp3")
                        return

        pygame.display.update()
        clock.tick(60)


def choose_card_style():
    scroll_offset = 0
    scroll_speed = 80  

    base_card = pygame.image.load("Image/cards/card.png").convert_alpha()
    base_card = pygame.transform.scale(base_card, (335, 458))

    card_hover = base_card.copy()
    hover_surface = pygame.Surface(card_hover.get_size(), pygame.SRCALPHA)
    hover_surface.fill((255, 255, 255, 60))
    card_hover.blit(hover_surface, (0, 0))

    styles = [
        ("Ank", "Image/cards/ank.png"),
        ("Circle", "Image/cards/circle.png"),
        ("Cross", "Image/cards/cross.png"),
        ("Eye", "Image/cards/eye.png"),
        ("Heart", "Image/cards/heart.png"),
        ("Triple Moon", "Image/cards/triplemoon.png"),
    ]

    loaded_styles = []
    for name, path in styles:
        if not os.path.exists(path):
            continue
        icon = pygame.image.load(path).convert_alpha()
        icon = pygame.transform.scale(icon, (335, 458))
        loaded_styles.append((name, path, icon))

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        # screen_color()
        preparedeck_bg = pygame.image.load("Image/Background/prepare_deck.jpg")
        SCREEN.blit(preparedeck_bg, (0, 0))

        title_text = get_font(65, 1).render("Choose Your Card Style", True, triadic_3)
        title_rect = title_text.get_rect(center=(screen_width // 2, 100))
        SCREEN.blit(title_text, title_rect)

        spacing_x = 375
        spacing_y = 500
        max_per_row = 3 #ตอนนี้ทำมาแค่ 6 รูปแบบจริงๆ อยากได้สัก 10 แล้วให้ max เป็น 4
        box_w, box_h = 335, 458

        total_rows = (len(loaded_styles) + max_per_row - 1) // max_per_row
        grid_height = total_rows * spacing_y
        start_x = (screen_width - (max_per_row * spacing_x - (spacing_x - box_w))) // 2
        start_y = 250 + scroll_offset


        card_buttons = []
        for i, (name, path, icon) in enumerate(loaded_styles):
            row = i // max_per_row
            col = i % max_per_row
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y

            rect = pygame.Rect(x, y, box_w, box_h)
            hovering = rect.collidepoint(MOUSE_POS)
            SCREEN.blit(card_hover if hovering else base_card, (x, y))
            SCREEN.blit(icon, (x, y))

            text = get_font(35, 1).render(name, True, triadic_2)
            text_rect = text.get_rect(center=(rect.centerx, rect.bottom + 20))
            SCREEN.blit(text, text_rect)
            card_buttons.append((rect, path))

        BACK_BUTTON = Button(
            image=None,
            pos=(screen_width // 2, screen_height - 120),
            text_input="BACK",
            font=get_font(75, 1),
            base_color=triadic_3,
            hovering_color=triadic_2,
        )
        BACK_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * scroll_speed
                max_scroll = 0
                min_scroll = min(0, screen_height - (grid_height + 400))
                scroll_offset = max(min_scroll, min(scroll_offset, max_scroll))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, path in card_buttons:
                    if rect.collidepoint(MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        transition_to(lambda: create_deck(path), "Music/017. Snowy.mp3")
                        return
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    transition_to(free_for_all, "Music/017. Snowy.mp3")
                    return

        pygame.display.update()

def story_mode():
    sfx_func("SFX/mus_wawa.mp3")
    background_music("Music/024. Bonetrousle.mp3", background_music_volume, -1)
    while True:
        STORY_MODE_MOUSE_POS = pygame.mouse.get_pos()

        screen_color()

        STORY_MODE_TEXT = get_font(95, 1).render("Sorry, Not Now :(", True, triadic_3)
        STORY_MODE_RECT = STORY_MODE_TEXT.get_rect(center=(screen_width//2, screen_height//2))
        SCREEN.blit(STORY_MODE_TEXT, STORY_MODE_RECT)

        STORY_MODE_BACK = Button(image=None, pos=(screen_width//2, 940),
        text_input="BACK", font=get_font(75, 1), base_color = triadic_3, hovering_color = triadic_2)

        STORY_MODE_BACK.changeColor(STORY_MODE_MOUSE_POS)
        STORY_MODE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if STORY_MODE_BACK.checkForInput(STORY_MODE_MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        transition_to(select_mode, "Music/092. Reunited.mp3")

        pygame.display.update()

def options():
    global background_music_volume, ishint, answer_time
    background_music("Music/005. Ruins.mp3", background_music_volume, -1)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        # screen_color()
        sw_bg = pygame.image.load("Image/Background/setting-witch.png")
        SCREEN.blit(sw_bg, (0, 0))
        
        # ปุ่มเพิ่ม/ลดเสียง
        OPTIONS_TEXT = get_font(45, 1).render("Background Music Volume", True, triadic_2)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width//2, 200))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        PLUS_BUTTON = Button(image=None, pos=(screen_width//2 + 150, 250),
                            text_input="+", font=get_font(75, 1), base_color=(200,180,255), hovering_color=(255,255,255))
        MINUS_BUTTON = Button(image=None, pos=(screen_width//2 - 150, 250),
                            text_input="-", font=get_font(75, 1), base_color=(200,180,255), hovering_color=(255,255,255))
        
        VOL_TEXT = get_font(55, 1).render(str(int(round(background_music_volume * 100, 2))) + " %", True, triadic_2)
        VOL_RECT = VOL_TEXT.get_rect(center=(screen_width//2, 250))
        SCREEN.blit(VOL_TEXT, VOL_RECT)

        #Hint
        OPTIONS_FAST = get_font(45, 1).render(f"Hint : {ishint}", True, triadic_2)
        OPTIONS_FAST_RECT = OPTIONS_FAST.get_rect(center=(screen_width//2, 325))
        SCREEN.blit(OPTIONS_FAST, OPTIONS_FAST_RECT)

        OPTIONS_FAST = Button(image=None, pos=(screen_width//2, 325),
                            text_input = f"Hint : {ishint}", font=get_font(45, 1), base_color=triadic_2, hovering_color=triadic_3)
        
        # ปุ่มเพิ่ม/ลดเวลาตอบ
        OPTIONS_TEXT_ANSWER_TIME = get_font(45, 1).render("Answer Time", True, triadic_2)
        OPTIONS_RECT_ANSWER_TIME = OPTIONS_TEXT_ANSWER_TIME.get_rect(center=(screen_width//2, 400))
        SCREEN.blit(OPTIONS_TEXT_ANSWER_TIME, OPTIONS_RECT_ANSWER_TIME)

        PLUS_BUTTON_ANSWER_TIME = Button(image=None, pos=(screen_width//2 + 150, 450),
                            text_input="+", font=get_font(75, 1), base_color=(200,180,255), hovering_color=(255,255,255))
        MINUS_BUTTON_ANSWER_TIME = Button(image=None, pos=(screen_width//2 - 150, 450),
                            text_input="-", font=get_font(75, 1), base_color=(200,180,255), hovering_color=(255,255,255))
        
        VOL_TEXT_ANSWER_TIME = get_font(55, 1).render(str(int(round(answer_time, 2))) + " Second", True, triadic_2)
        VOL_RECT_ANSWER_TIME = VOL_TEXT_ANSWER_TIME.get_rect(center=(screen_width//2, 450))
        SCREEN.blit(VOL_TEXT_ANSWER_TIME, VOL_RECT_ANSWER_TIME)
        
        #ย้อน
        OPTIONS_BACK = Button(image=None, pos=(screen_width//2, 940),
                            text_input="BACK", font=get_font(75, 1), base_color=triadic_2, hovering_color=triadic_3)

        for button in [PLUS_BUTTON, MINUS_BUTTON, OPTIONS_BACK, OPTIONS_FAST, PLUS_BUTTON_ANSWER_TIME, MINUS_BUTTON_ANSWER_TIME]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    transition_to(main_menu, "Music/092. Reunited.mp3")
                if OPTIONS_FAST.checkForInput(OPTIONS_MOUSE_POS):
                    sfx_func("SFX/Click.mp3")
                    if ishint: ishint = False
                    else: ishint = True
                if PLUS_BUTTON.checkForInput(OPTIONS_MOUSE_POS) and not intro_time > 3:
                    sfx_func("SFX/Click.mp3")
                    if event.button in (1, 4):
                        background_music_volume = min(1, background_music_volume + 0.1)
                    else:
                        background_music_volume = max(0, background_music_volume - 0.1)
                    pygame.mixer.music.set_volume(background_music_volume)
                if MINUS_BUTTON.checkForInput(OPTIONS_MOUSE_POS) and not intro_time > 3:
                    sfx_func("SFX/Click.mp3")
                    if event.button in (1, 5):
                        background_music_volume = max(0, background_music_volume - 0.1)
                    else:
                        background_music_volume = min(1, background_music_volume + 0.1)
                    pygame.mixer.music.set_volume(background_music_volume)

                if PLUS_BUTTON_ANSWER_TIME.checkForInput(OPTIONS_MOUSE_POS) and not intro_time > 3:
                    sfx_func("SFX/Click.mp3")
                    if event.button in (1, 4):
                        answer_time = min(30, answer_time + 1)
                    else:
                        answer_time = max(1, answer_time - 1)
                if MINUS_BUTTON_ANSWER_TIME.checkForInput(OPTIONS_MOUSE_POS) and not intro_time > 3:
                    sfx_func("SFX/Click.mp3")
                    if event.button in (1, 5):
                        answer_time = max(1, answer_time - 1)
                    else:
                        answer_time = min(30, answer_time + 1)
        pygame.display.update()

def main_menu():
    background_music("Music/092. Reunited.mp3", background_music_volume, -1)

    while True:
        if intro_time > 3:
            screen_color()
            MENU_TEXT = pygame.font.Font("Font/PixelMedium.ttf", 75).render(user_name +" " + computer_name +" ?", True, "red")
        else:
            SCREEN.blit(BG, (0, 0))
            MENU_TEXT = get_font(100, 1).render("Witch's Memo", True, triadic_2)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width//2, 150))
        PLAY_BUTTON = Button(image=pygame.image.load("Image/Play Rect.png"), pos=(screen_width//2, 350), 
                            text_input="PLAY", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)
        OPTIONS_BUTTON = Button(image=pygame.image.load("Image/Options Rect.png"), pos=(screen_width//2, 500), 
                            text_input="OPTIONS", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)
        QUIT_BUTTON = Button(image=pygame.image.load("Image/Quit Rect.png"), pos=(screen_width//2, 650), 
                            text_input="QUIT", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)
        
        witch = pygame.image.load("Image/MC Witch.png")
        witch = pygame.transform.scale(witch, (400, 400))
        witch_rect = witch.get_rect(center=(screen_width//2 + 400, screen_height//2 + 200))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(witch, witch_rect)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        transition_to(select_mode, "Music/003. Your Best Friend.mp3")
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        transition_to(options, "Music/005. Ruins.mp3")
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        sfx_func("SFX/Click.mp3")
                        pygame.mixer.music.stop()
                        if intro_time > 3:
                            pygame.time.wait(500)
                            sfx_func("SFX/OMG Laugh.mp3")
                            pygame.time.wait(1000)
                        intro()
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

def intro():
    global intro_time
    clock = pygame.time.Clock()
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((255, 255, 255))
    alpha = 255  # เริ่มจากจอขาว
    fade_speed = 2  #ความเร็วการจาง
    intro_time += 1

    if intro_time > 3:
        logo = pygame.image.load("Image/Cahethel.png")
        logo = pygame.transform.scale(logo, (400, 400))
        logo_rect = logo.get_rect(center=(screen_width//2, screen_height//2))
    else:
        logo = pygame.image.load("Image/star.png")
        logo = pygame.transform.scale(logo, (400, 400))
        logo_rect = logo.get_rect(center=(screen_width//2, screen_height//2))

    while True:
        SCREEN.blit(logo, logo_rect)
        fade_surface.set_alpha(alpha)
        SCREEN.blit(fade_surface, (0, 0))

        pygame.display.update()
        clock.tick(60)

        # ลดความทึบลง
        if alpha > 0:
            alpha -= fade_speed
        else:
            transition_to(main_menu, "Music/092. Reunited.mp3")
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not intro_time > 3:
                if event.button == 1:
                    sfx_func("SFX/Click.mp3")
                    transition_to(main_menu, "Music/092. Reunited.mp3")
                    return

# --- [เพิ่ม] เรียกใช้ Cache Monster ก่อนเริ่มเกม ---
MONSTER_SPRITE_CACHE = load_sprite_cache_from_folder("Image/Monster/Gigi", (100, 0, 100))
BOSS_SPRITE_CACHE = load_sprite_cache_from_folder("Image/Monster/Boss", (255, 0, 0))
intro()
