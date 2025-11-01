"""Witch Memo Game Script"""
import pygame, sys, random, socket, getpass, json, os
from button import Button

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 1920, 1080
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Witch's Memo")

background_music_volume = 0.5
ishint = False
answer_time = 5

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

def click_sound():
    pygame.mixer.Sound("SFX/Click.mp3").play()

def sfx_func(sfx):
    pygame.mixer.Sound(sfx).play()

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
        "Will you remember me?", "No no no no no no no no no no no no no no no no no no no no no no no no no no no no no no no no no no",
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
                    click_sound()
                    next_function()
                    return

    if intro_time > 10:
        pygame.time.wait(1500)
        pygame.quit()
    if ishint:
        pygame.time.wait(1000)
    next_function()


def select_mode():
    background_music("Music/003. Your Best Friend.mp3", background_music_volume, -1)
    global intro_time
    if intro_time > 3:
        sfx_func("SFX/thatsawonderfulidea.mp3")
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()
        PLAY_TEXT = get_font(45, 1).render(user_name + ", please select mode to play.", True, triadic_2)
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
                    click_sound()
                    if STORY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        transition_to(story_mode, "Music/003. Your Best Friend.mp3")
                    if FREEFORALL_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        transition_to(free_for_all, "Music/Anticipation.mp3")
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        transition_to(main_menu, "Music/034. Memory.mp3")
        pygame.display.update()

def create_deck(style_path):
    deck_dir = "decks"
    os.makedirs(deck_dir, exist_ok=True)
    user_input = ""
    clock = pygame.time.Clock()

    while True:
        CREATE_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()

        PROMPT = get_font(55, 1).render("Enter New Deck Name:", True, triadic_2)
        SCREEN.blit(PROMPT, PROMPT.get_rect(center=(screen_width//2, 250)))

        BOX = pygame.Rect(screen_width//2 - 300, 350, 600, 80)
        pygame.draw.rect(SCREEN, (255,255,255), BOX, border_radius=8)
        pygame.draw.rect(SCREEN, (160,100,220), BOX, 3, border_radius=8)
        SCREEN.blit(get_font(50, 2).render(user_input, True, (90,0,130)), (BOX.x + 20, BOX.y)) #ถ้าใช้ font pixel ต้องเป็น (BOX.x + 20, BOX.y + 15)

        BACK_BUTTON = Button(None, (screen_width//2, 800), "BACK", get_font(75, 1), triadic_3, triadic_2)
        CREATE_BUTTON = Button(None, (screen_width//2, 600), "CREATE", get_font(75, 1), (200,180,255), (255,255,255))

        for button in [BACK_BUTTON, CREATE_BUTTON]:
            button.changeColor(CREATE_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition_to(free_for_all, "Music/Anticipation.mp3")
                    return
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_input.strip():
                        fname = os.path.join(deck_dir, user_input.strip() + ".json")
                        with open(fname, "w", encoding="utf-8") as f:
                            json.dump({"style": style_path, "cards": []}, f, ensure_ascii=False, indent=4)
                        transition_to(free_for_all, "Music/Anticipation.mp3")
                        return
                else:
                    if len(user_input) < 20:
                        user_input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BACK_BUTTON.checkForInput(CREATE_MOUSE_POS):
                    transition_to(free_for_all, "Music/Anticipation.mp3")
                    return
                if CREATE_BUTTON.checkForInput(CREATE_MOUSE_POS) and user_input.strip():
                    fname = os.path.join(deck_dir, user_input.strip() + ".json")
                    with open(fname, "w", encoding="utf-8") as f:
                        json.dump({"style": style_path, "cards": []}, f, ensure_ascii=False, indent=4)
                    transition_to(free_for_all, "Music/Anticipation.mp3")
                    return

        pygame.display.update()
        clock.tick(60)


def free_for_all():
    background_music("Music/Anticipation.mp3", background_music_volume, -1)
    deck_dir = "decks"
    os.makedirs(deck_dir, exist_ok=True)

    scroll_offset = 0
    scroll_speed = 60

    while True:
        FREEFORALL_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()

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

            if not os.path.exists(style_path):
                style_path = "Image/cards/card.png"

            card_img = pygame.image.load(style_path).convert_alpha()
            card_img = pygame.transform.scale(card_img, (box_w, box_h))

            row = i // max_per_row
            col = i % max_per_row
            box_x = start_x + col * spacing_x
            box_y = start_y + row * spacing_y
            box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

            hovering = box_rect.collidepoint(FREEFORALL_MOUSE_POS)
            if hovering:
                hover_overlay = pygame.Surface(card_img.get_size(), pygame.SRCALPHA)
                hover_overlay.fill((255, 255, 255, 80))
                card_img.blit(hover_overlay, (0, 0))

            SCREEN.blit(card_img, (box_x, box_y))

            deck_name = deck.replace(".json", "")
            name_text = get_font(40, 2).render(deck_name, True, triadic_2)
            name_rect = name_text.get_rect(center=(box_rect.centerx, box_rect.bottom + 10))
            SCREEN.blit(name_text, name_rect)

            deck_buttons.append((box_rect, deck_name))

        # ปุ่ม CREATE NEW DECK
        create_index = len(deck_files)
        row = create_index // max_per_row
        col = create_index % max_per_row
        create_x = start_x + col * spacing_x
        create_y = start_y + row * spacing_y
        base_card = pygame.image.load("Image/cards/card.png").convert_alpha()
        base_card = pygame.transform.scale(base_card, (box_w, box_h))
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
                scroll_offset = max(min(0, scroll_offset), -((total_rows * spacing_y) - screen_height + 300))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_sound()
                for rect, name in deck_buttons:
                    if rect.collidepoint(FREEFORALL_MOUSE_POS):
                        transition_to(deck_choice_menu(name), "Music/Anticipation.mp3")
                        return
                if pygame.Rect(create_x, create_y, box_w, box_h).collidepoint(FREEFORALL_MOUSE_POS):
                    transition_to(choose_card_style, "Music/Anticipation.mp3")
                    return
                if BACK_BUTTON.checkForInput(FREEFORALL_MOUSE_POS):
                    transition_to(select_mode, "Music/034. Memory.mp3")
                    return

        pygame.display.update()

def deck_choice_menu(fname):
    background_music("Music/Anticipation.mp3", background_music_volume, -1)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()
        
        #ชื่อ Deck
        OPTIONS_TEXT = get_font(45, 2).render(f"Deck: {fname}", True, triadic_2)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width//2, 120))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        #
        OPTIONS_EDIT = Button(image=None, pos=(screen_width//2, 700),
                              text_input="EDIT", font=get_font(75, 1), base_color=triadic_2, hovering_color=triadic_3)

        #ลบ
        OPTIONS_DELETE = Button(image=None, pos=(screen_width//2, 800),
                              text_input="DELETE", font=get_font(75, 1), base_color=triadic_2, hovering_color=(255,0,0))

        #ย้อน
        OPTIONS_BACK = Button(image=None, pos=(screen_width//2, 940),
                              text_input="BACK", font=get_font(75, 1), base_color=triadic_2, hovering_color=triadic_3)

        for button in [OPTIONS_BACK, OPTIONS_DELETE, OPTIONS_EDIT]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_sound()
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    transition_to(free_for_all, "Music/034. Memory.mp3")
                if OPTIONS_EDIT.checkForInput(OPTIONS_MOUSE_POS):
                    transition_to(lambda: edit_deck(fname), "Music/034. Memory.mp3")
                if OPTIONS_DELETE.checkForInput(OPTIONS_MOUSE_POS):
                    try:
                        os.remove(os.path.join(f"decks/{fname}.json"))
                    except Exception as e:
                        print("Delete error", e)
                    sfx_func("SFX/boom.mp3")
                    transition_to(free_for_all, "Music/034. Memory.mp3")
        pygame.display.update()

def choose_card_style():
    background_music("Music/Anticipation.mp3", background_music_volume, -1)
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
        screen_color()

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
                click_sound()
                for rect, path in card_buttons:
                    if rect.collidepoint(MOUSE_POS):
                        transition_to(lambda: create_deck(path), "Music/Anticipation.mp3")
                        return
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    transition_to(free_for_all, "Music/Anticipation.mp3")
                    return

        pygame.display.update()


def play_deck(deck_name):
    background_music("Music/Anticipation.mp3", background_music_volume, -1)
    deck_path = os.path.join("decks", deck_name + ".json")

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()

        TITLE = get_font(70, 1).render(deck_name, True, triadic_3)
        TITLE_RECT = TITLE.get_rect(center=(screen_width//2, 200))
        SCREEN.blit(TITLE, TITLE_RECT)

        TEXT = get_font(45, 1).render("This deck is ready for flashcard creation!", True, triadic_2)
        TEXT_RECT = TEXT.get_rect(center=(screen_width//2, 400))
        SCREEN.blit(TEXT, TEXT_RECT)

        EDIT_BUTTON = Button(image=None, pos=(screen_width//2, 600),
                             text_input="EDIT DECK", font=get_font(75, 1),
                             base_color=(200,180,255), hovering_color=(255,255,255))
        BACK_BUTTON = Button(image=None, pos=(screen_width//2, 800),
                             text_input="BACK", font=get_font(75, 1),
                             base_color=triadic_3, hovering_color=triadic_2)
        for button in [EDIT_BUTTON, BACK_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_sound()
                if EDIT_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    transition_to(lambda: edit_deck(deck_name), "Music/Anticipation.mp3")
                    return
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    transition_to(free_for_all, "Music/Anticipation.mp3")
                    return

        pygame.display.update()

def edit_deck(deck_name):
    deck_path = os.path.join("decks", deck_name + ".json")
    os.makedirs("decks", exist_ok=True)

    # โหลด deck ถ้ามีอยู่แล้ว
    if os.path.exists(deck_path):
        with open(deck_path, "r", encoding="utf-8") as f:
            try:
                words = json.load(f)
            except json.JSONDecodeError:
                words = []
    else:
        words = []

    # 🔧 เผื่อ deck เก่ามี key "cards"
    if isinstance(words, dict):
        words = words.get("cards", [])

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
        dt = clock.tick(60) / 16.67  # ล็อก FPS
        screen_color()

        # -------------------------------
        # Title
        # -------------------------------
        TITLE = get_font(70, 1).render(f"Edit Deck: {deck_name}", True, triadic_3)
        SCREEN.blit(TITLE, TITLE.get_rect(center=(screen_width // 2, 100)))

        # -------------------------------
        # กล่องใส่คำศัพท์
        # -------------------------------
        word_box = pygame.Rect(screen_width//2 - 400, 250, 350, 70)
        meaning_box = pygame.Rect(screen_width//2 + 70, 250, 350, 70)

        word_color = (220, 180, 255) if active_input == "word" else (255, 255, 255)
        meaning_color = (220, 180, 255) if active_input == "meaning" else (255, 255, 255)

        pygame.draw.rect(SCREEN, word_color, word_box, border_radius=8)
        pygame.draw.rect(SCREEN, triadic_3, word_box, 3, border_radius=8)
        pygame.draw.rect(SCREEN, meaning_color, meaning_box, border_radius=8)
        pygame.draw.rect(SCREEN, triadic_3, meaning_box, 3, border_radius=8)

        word_text = get_font(40, 1).render(input_word or "Word", True, (90, 0, 130))
        meaning_text = get_font(40, 1).render(input_meaning or "Meaning", True, (90, 0, 130))
        SCREEN.blit(word_text, (word_box.x + 20, word_box.y + 15))
        SCREEN.blit(meaning_text, (meaning_box.x + 20, meaning_box.y + 15))

        # -------------------------------
        # ปุ่ม Add / Back
        # -------------------------------
        ADD_BUTTON = Button(image=None, pos=(screen_width//2, 400),
                            text_input="ADD WORD", font=get_font(55, 1),
                            base_color=(200, 180, 255), hovering_color=(255, 255, 255))
        BACK_BUTTON = Button(image=None, pos=(screen_width//2, 950),
                             text_input="BACK", font=get_font(75, 1),
                             base_color=triadic_3, hovering_color=triadic_2)
        for button in [ADD_BUTTON, BACK_BUTTON]:
            button.changeColor(EDIT_MOUSE_POS)
            button.update(SCREEN)

        # -------------------------------
        # พื้นที่เลื่อนของคำทั้งหมด
        # -------------------------------
        list_start_y = 500 + scroll_offset
        item_height = 50
        total_height = len(words) * item_height
        visible_top = 480
        visible_bottom = screen_height - 200

        for i, item in enumerate(words):
            y_pos = list_start_y + i * item_height
            if y_pos < visible_top - item_height or y_pos > visible_bottom + item_height:
                continue  # ข้ามถ้าอยู่นอกจอ

            word_display = f"{i+1}. {item['word']}  -  {item['meaning']}"
            word_text = get_font(35, 2).render(word_display, True, triadic_2)
            SCREEN.blit(word_text, (screen_width//2 - 400, y_pos))

        # -------------------------------
        # Counter
        # -------------------------------
        counter_text = get_font(30, 1).render(f"{len(words)}/{MAX_WORDS} words", True, triadic_2)
        SCREEN.blit(counter_text, (screen_width//2 + 550, screen_height//2 - 460))

        # -------------------------------
        # Scrollbar (แสดงให้เห็นว่ามีเลื่อน)
        # -------------------------------
        if total_height > (visible_bottom - visible_top):
            bar_h = max(50, (visible_bottom - visible_top) * (visible_bottom - visible_top) / total_height)
            bar_y = visible_top + (-scroll_offset / total_height) * (visible_bottom - visible_top - bar_h)
            pygame.draw.rect(SCREEN, triadic_3, (screen_width - 50, bar_y, 15, bar_h), border_radius=6)

        # -------------------------------
        # Event Handler
        # -------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # scroll mouse wheel
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * scroll_speed
                max_scroll = 0
                min_scroll = min(0, visible_bottom - (total_height + visible_top))
                scroll_offset = max(min_scroll, min(scroll_offset, max_scroll))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition_to(deck_choice_menu(deck_name), "Music/Anticipation.mp3")
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
                        with open(deck_path, "w", encoding="utf-8") as f:
                            json.dump(words, f, ensure_ascii=False, indent=4)
                        click_sound()
                else:
                    if active_input == "word" and len(input_word) < 20:
                        input_word += event.unicode
                    elif active_input == "meaning" and len(input_meaning) < 30:
                        input_meaning += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if word_box.collidepoint(EDIT_MOUSE_POS):
                    active_input = "word"
                elif meaning_box.collidepoint(EDIT_MOUSE_POS):
                    active_input = "meaning"
                if ADD_BUTTON.checkForInput(EDIT_MOUSE_POS):
                    if input_word.strip() and input_meaning.strip() and len(words) < MAX_WORDS:
                        words.append({"word": input_word.strip(), "meaning": input_meaning.strip()})
                        input_word, input_meaning = "", ""
                        with open(deck_path, "w", encoding="utf-8") as f:
                            json.dump(words, f, ensure_ascii=False, indent=4)
                        click_sound()
                if BACK_BUTTON.checkForInput(EDIT_MOUSE_POS):
                    transition_to(deck_choice_menu(deck_name), "Music/Anticipation.mp3")
                    return

        pygame.display.update()

def story_mode():
    background_music("Music/Anticipation.mp3", background_music_volume, -1)
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
                    click_sound()
                    if STORY_MODE_BACK.checkForInput(STORY_MODE_MOUSE_POS):
                        transition_to(select_mode, "Music/034. Memory.mp3")

        pygame.display.update()

def options():
    global background_music_volume, ishint, answer_time
    background_music("Music/Anticipation.mp3", background_music_volume, -1)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()
        
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
                if event.button == 1:
                    click_sound()
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound()
                    transition_to(main_menu, "Music/034. Memory.mp3")
                if OPTIONS_FAST.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound()
                    if ishint: ishint = False
                    else: ishint = True
                if PLUS_BUTTON.checkForInput(OPTIONS_MOUSE_POS) and not intro_time > 3:
                    click_sound()
                    if event.button in (1, 4):
                        background_music_volume = min(1, background_music_volume + 0.1)
                    else:
                        background_music_volume = max(0, background_music_volume - 0.1)
                    pygame.mixer.music.set_volume(background_music_volume)
                if MINUS_BUTTON.checkForInput(OPTIONS_MOUSE_POS) and not intro_time > 3:
                    click_sound()
                    if event.button in (1, 5):
                        background_music_volume = max(0, background_music_volume - 0.1)
                    else:
                        background_music_volume = min(1, background_music_volume + 0.1)
                    pygame.mixer.music.set_volume(background_music_volume)

                if PLUS_BUTTON_ANSWER_TIME.checkForInput(OPTIONS_MOUSE_POS) and not intro_time > 3:
                    click_sound()
                    if event.button in (1, 4):
                        answer_time = min(30, answer_time + 1)
                    else:
                        answer_time = max(1, answer_time - 1)
                if MINUS_BUTTON_ANSWER_TIME.checkForInput(OPTIONS_MOUSE_POS) and not intro_time > 3:
                    click_sound()
                    if event.button in (1, 5):
                        answer_time = max(1, answer_time - 1)
                    else:
                        answer_time = min(30, answer_time + 1)
        pygame.display.update()

def main_menu():
    background_music("Music/034. Memory.mp3", background_music_volume, -1)

    while True:
        if intro_time > 3:
            SCREEN.fill("black")
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
                    click_sound()
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        transition_to(select_mode, "Music/003. Your Best Friend.mp3")
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        transition_to(options, "Music/Anticipation.mp3")
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
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
            transition_to(main_menu, "Music/034. Memory.mp3")
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not intro_time > 3:
                if event.button == 1:
                    click_sound()
                    transition_to(main_menu, "Music/034. Memory.mp3")
                    return

intro()
