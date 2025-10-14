"""Witch Memo Game Script"""
import pygame, sys, random, socket, getpass, json, os
from button import Button
pygame.init()
pygame.mixer.init()

screen_width, screen_height = 1920, 1080
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Witch's Memo")

background_music_volume = 0.5

computer_name = socket.gethostname()
user_name = getpass.getuser()

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
    global current_music
    global background_music_volume
    try:
        if intro_time > 3:
            path = "Music/So cold.mp3"
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
        elif current_music != path and not intro_time > 3:
            current_music = path
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

def transition_to(next_function, next_music_path):
    hint_number = random.randint(0,count_hints)

    clock = pygame.time.Clock()
    fade_surface = pygame.Surface((screen_width, screen_height))

    if intro_time > 3:
        fade_surface.fill((138, 3, 3))  # เลือด
        fade_speed = 5
    else:
        fade_surface.fill((255, 255, 255))  # ขาว
        fade_speed = 15

    alpha = 0
    start_volume = pygame.mixer.music.get_volume()

    current_scene = SCREEN.copy()

    while alpha < 255:
        SCREEN.blit(current_scene, (0, 0))
        fade_surface.set_alpha(alpha)
        SCREEN.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)

        current_vol = max(0, start_volume * (1 - alpha / 255))
        pygame.mixer.music.set_volume(current_vol)
        alpha += fade_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    background_music(next_music_path, background_music_volume, -1)

    alpha = 255
    fade_surface.set_alpha(alpha)

    while alpha > 0:
        if not intro_time > 3:
            hint(hint_number)
        else:
            hint(random.randint(0, count_hints))
        fade_surface.set_alpha(alpha)
        SCREEN.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)
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
    pygame.time.wait(1500)
    next_function()


def play():
    background_music("Music/003. Your Best Friend.mp3", background_music_volume, -1)
    global intro_time
    intro_time -= 1
    if intro_time > 3:
        sfx_func("SFX/thatsawonderfulidea.mp3")
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()
        PLAY_TEXT = get_font(45, 1).render("Hey " + user_name + ", buddy it's not time to play.", True, triadic_2)
        PLAY_RECT = PLAY_TEXT.get_rect(center = (screen_width//2, 310))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image = None, pos = (screen_width//2, 510), text_input = "BACK", font = get_font(75, 1), base_color = triadic_2, hovering_color = triadic_3)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        STORY_BUTTON = Button(image=pygame.image.load("Image/Play Rect.png"), pos=(screen_width//2, 700), 
                            text_input="STORY", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)
        FREEFORALL_BUTTON = Button(image=pygame.image.load("Image/Options Rect.png"), pos=(screen_width//2, 850), 
                            text_input="FREE FOR ALL", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)

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

def create_deck():
    deck_dir = "decks"
    os.makedirs(deck_dir, exist_ok=True)
    user_input = ""
    clock = pygame.time.Clock()

    while True:
        CREATE_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()

        PROMPT = get_font(55, 1).render("Enter New Deck Name:", True, triadic_2)
        PROMPT_RECT = PROMPT.get_rect(center=(screen_width//2, 250))
        SCREEN.blit(PROMPT, PROMPT_RECT)

        BOX = pygame.Rect(screen_width//2 - 300, 350, 600, 80)
        pygame.draw.rect(SCREEN, (255,255,255), BOX, border_radius=8)
        pygame.draw.rect(SCREEN, (160,100,220), BOX, 3, border_radius=8)

        INPUT_TEXT = get_font(50, 1).render(user_input, True, (90,0,130))
        SCREEN.blit(INPUT_TEXT, (BOX.x + 20, BOX.y + 15))

        BACK_BUTTON = Button(image=None, pos=(screen_width//2, 800),
                             text_input="BACK", font=get_font(75, 1),
                             base_color=triadic_3, hovering_color=triadic_2)

        CREATE_BUTTON = Button(image=None, pos=(screen_width//2, 600),
                               text_input="CREATE", font=get_font(75, 1),
                               base_color=(200,180,255), hovering_color=(255,255,255))

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
                            json.dump([], f, ensure_ascii=False, indent=4)
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
                        json.dump([], f, ensure_ascii=False, indent=4)
                    transition_to(free_for_all, "Music/Anticipation.mp3")
                    return

        pygame.display.update()
        clock.tick(60)

def free_for_all():
    background_music("Music/Anticipation.mp3", background_music_volume, -1)
    while True:
        FREEFORALL_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()

        # ชื่อหน้า
        FREEFORALL_TEXT = get_font(65, 1).render("Select Your Deck", True, triadic_3)
        FREEFORALL_RECT = FREEFORALL_TEXT.get_rect(center=(screen_width//2, 120))
        SCREEN.blit(FREEFORALL_TEXT, FREEFORALL_RECT)

        # -------------------------------
        # กล่องปุ่ม CREATE NEW DECK
        # -------------------------------
        box_w, box_h = 320, 480
        box_x, box_y = screen_width//2 - 700, screen_height//2 - box_h//2
        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

        # ตรวจว่าเมาส์ชี้ไหม
        hovering = box_rect.collidepoint(FREEFORALL_MOUSE_POS)

        # สีเปลี่ยนตาม hover
        fill_color = (245, 240, 255) if hovering else (255, 255, 255)
        border_color = triadic_2 if hovering else triadic_3

        pygame.draw.rect(SCREEN, fill_color, box_rect, border_radius=16)
        pygame.draw.rect(SCREEN, border_color, box_rect, 5, border_radius=16)

        # สัญลักษณ์ "+"
        plus_text = get_font(200, 1).render("+", True, (120, 80, 200))
        plus_rect = plus_text.get_rect(center=(box_rect.centerx, box_rect.centery - 40))
        SCREEN.blit(plus_text, plus_rect)

        # ข้อความด้านล่าง
        label_text = get_font(35, 1).render("CREATE NEW DECK", True, (90, 0, 130))
        label_rect = label_text.get_rect(center=(box_rect.centerx, box_rect.bottom - 60))
        SCREEN.blit(label_text, label_rect)

        # ปุ่ม BACK
        FREEFORALL_BACK = Button(
            image=None,
            pos=(screen_width//2, 900),
            text_input="BACK",
            font=get_font(75, 1),
            base_color=triadic_3,
            hovering_color=triadic_2
        )
        FREEFORALL_BACK.changeColor(FREEFORALL_MOUSE_POS)
        FREEFORALL_BACK.update(SCREEN)

        # -------------------------------
        # Event Handler
        # -------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_sound()
                if box_rect.collidepoint(FREEFORALL_MOUSE_POS):
                    transition_to(create_deck, "Music/Anticipation.mp3")
                if FREEFORALL_BACK.checkForInput(FREEFORALL_MOUSE_POS):
                    transition_to(play, "Music/034. Memory.mp3")

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
                        transition_to(play, "Music/034. Memory.mp3")

        pygame.display.update()

def options():
    global background_music_volume
    background_music("Music/Anticipation.mp3", background_music_volume, -1)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()

        OPTIONS_TEXT = get_font(45, 1).render("Background Music Volume", True, triadic_2)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width//2, 200))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # ปุ่มเพิ่ม/ลดเสียง
        PLUS_BUTTON = Button(image=None, pos=(screen_width//2 + 150, 275),
                             text_input="+", font=get_font(75, 1), base_color=(200,180,255), hovering_color=(255,255,255))
        MINUS_BUTTON = Button(image=None, pos=(screen_width//2 - 150, 275),
                             text_input="-", font=get_font(75, 1), base_color=(200,180,255), hovering_color=(255,255,255))
        
        VOL_TEXT = get_font(55, 1).render(str(int(round(background_music_volume * 100, 2))) + " %", True, triadic_2)
        VOL_RECT = VOL_TEXT.get_rect(center=(screen_width//2, 275))
        SCREEN.blit(VOL_TEXT, VOL_RECT)

        OPTIONS_BACK = Button(image=None, pos=(screen_width//2, 800),
                              text_input="BACK", font=get_font(75, 1), base_color=triadic_2, hovering_color=triadic_3)

        for button in [PLUS_BUTTON, MINUS_BUTTON, OPTIONS_BACK]:
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
        PLAY_BUTTON = Button(image=pygame.image.load("Image/Play Rect.png"), pos=(screen_width//2, 300), 
                            text_input="PLAY", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)
        OPTIONS_BUTTON = Button(image=pygame.image.load("Image/Options Rect.png"), pos=(screen_width//2, 450), 
                            text_input="OPTIONS", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)
        QUIT_BUTTON = Button(image=pygame.image.load("Image/Quit Rect.png"), pos=(screen_width//2, 600), 
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
                        transition_to(play, "Music/003. Your Best Friend.mp3")
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
