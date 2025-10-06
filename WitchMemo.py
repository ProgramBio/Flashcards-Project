"""Witch Memo Game Script"""
import pygame, sys, random, socket, getpass
from button import Button
pygame.init()
pygame.mixer.init()

screen_width, screen_height = 1280, 720
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Witch's Memo")

computer_name = socket.gethostname()
user_name = getpass.getuser()

BG = pygame.image.load("Image/Background/menubackgroundtest.jpg")
BG = pygame.transform.scale(BG, (screen_width, screen_height))
basecolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) #สุ่มสีเริ่มต้น
triadic_2 = [basecolor[0] + 85, basecolor[1] + 85, basecolor[2] + 85] #การทำสีที่สองของ Triadic Theory
triadic_3 = [triadic_2[0] + 85, triadic_2[1] + 85, triadic_2[2] + 85] #การทำสีที่สามของ Triadic Theory
for i in range(3): #แปลงรหัสสีตาม Triadic Theory
    if triadic_2[i] > 255:
        triadic_2[i] -= 255
    if triadic_3[i] > 255:
        triadic_3[i] -= 255

intro_time = 0

current_music = None
def background_music(path, volume, loop):
    global current_music
    try:
        if intro_time > 3:
            path = "Music/So cold.mp3"
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
        if current_music != path and intro_time == 1:
            current_music = path
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
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

def hint(hint_number):
    pygame.time.Clock().tick(5)
    if not intro_time > 3:
        if hint_number == 1:
            hint_text = "การจดจำเพียงอย่างเดียวอาจไม่ได้ช่วยอะไร จงมั่นฝึกฝนด้วย!"
        elif hint_number == 2:
            hint_text = "ทุกการจดจำคือการเรียนรู้!"
        elif hint_number == 3:
            hint_text = "การทบทวนทีละนิดนั้นดีกว่าการไม่ทำอะไรเลย!"
        elif hint_number == 4:
            hint_text = "การเรียนรู้คือเวทย์มนต์ที่แท้จริง!"
        else:
            hint_text = "ยิ่งจดจำได้มากเท่าไหร่ก็แปลว่าความสามารถของคุณก็เพิ่มขึ้นเช่นกัน!"
        PLAY_TEXT = get_font(35, 2).render(hint_text, True, triadic_2)
    else:
        if hint_number == 1:
            hint_text = user_name + " why?"
        elif hint_number == 2:
            hint_text = "You wanna leave me alone?"
        elif hint_number == 3:
            hint_text = "Do you really want this " + user_name + "?"
        elif hint_number == 4:
            hint_text = "why? why? why? why? why?"
        elif hint_number == 5:
            hint_text = user_name + " " + user_name + " " + user_name+ " " + user_name + " " + user_name
        else:
            hint_text = "AHAHHAHAHAHAHHAAHHAAHHAHAHA!"
        PLAY_TEXT = get_font(35, 2).render(hint_text, True, (255, 255, 255))
    PLAY_RECT = PLAY_TEXT.get_rect(center=(screen_width//2, screen_height//2))
    SCREEN.blit(PLAY_TEXT, PLAY_RECT)

def transition_to(next_function, next_music_path):
    if intro_time:
        click_sound()
    hint_number = random.randint(1,5)

    clock = pygame.time.Clock()
    fade_surface = pygame.Surface((screen_width, screen_height))

    if intro_time > 3:
        fade_surface.fill((138, 3, 3))  # เลือด
        fade_speed = 4
    else:
        fade_surface.fill((255, 255, 255))  # ขาว
        fade_speed = 12

    alpha = 0
    start_volume = pygame.mixer.music.get_volume()

    current_scene = SCREEN.copy()

    while alpha < 255:
        SCREEN.blit(current_scene, (0, 0))
        fade_surface.set_alpha(alpha)
        SCREEN.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(120)

        current_vol = max(0, start_volume * (1 - alpha / 255))
        pygame.mixer.music.set_volume(current_vol)
        alpha += fade_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    background_music(next_music_path, 0.5, -1)

    alpha = 255
    fade_surface.set_alpha(alpha)

    while alpha > 0:
        if not intro_time > 3:
            hint(hint_number)
        else:
            hint(random.randint(1, 5))
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
                next_function()
                return

    if intro_time > 10:
        pygame.time.wait(1500)
        pygame.quit()
    pygame.time.wait(1500)
    next_function()


def play():
    background_music("Music/003. Your Best Friend.mp3", 0.5, -1)
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()
        PLAY_TEXT = get_font(45, 1).render("Hey " + user_name + ", buddy it's not time to play.", True, triadic_2)
        PLAY_RECT = PLAY_TEXT.get_rect(center = (640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image = None, pos = (640, 460), text_input = "BACK", font = get_font(75, 1), base_color = triadic_2, hovering_color = triadic_3)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    transition_to(main_menu, "Music/034. Memory.mp3")
        pygame.display.update()

def options():
    background_music("Music/Anticipation.mp3", 0.5, -1)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen_color()

        OPTIONS_TEXT = get_font(45, 1).render("You thing I had made this? You fool.", True, triadic_2)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
        text_input="BACK", font=get_font(75, 1), base_color = triadic_2, hovering_color = triadic_3)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    transition_to(main_menu, "Music/034. Memory.mp3")

        pygame.display.update()

def main_menu():
    background_music("Music/034. Memory.mp3", 0.5, -1)

    while True:
        if intro_time > 3:
            SCREEN.fill("black")
            MENU_TEXT = pygame.font.Font("Font/PixelMedium.ttf", 75).render(user_name +" " + computer_name +" ?", True, "red")
        else:
            SCREEN.blit(BG, (0, 0))
            MENU_TEXT = get_font(100, 1).render("Witch's Memo", True, triadic_2)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Image/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)
        OPTIONS_BUTTON = Button(image=pygame.image.load("Image/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)
        QUIT_BUTTON = Button(image=pygame.image.load("Image/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75, 1), base_color="#d7fcd4", hovering_color = triadic_3)
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    transition_to(play, "Music/003. Your Best Friend.mp3")
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    transition_to(options, "Music/Anticipation.mp3")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound()
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
        logo = pygame.transform.scale(logo, (300, 300))
        logo_rect = logo.get_rect(center=(screen_width//2, screen_height//2))
    else:
        logo = pygame.image.load("Image/star.png")
        logo = pygame.transform.scale(logo, (300, 300))
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
                transition_to(main_menu, "Music/034. Memory.mp3")
                return

intro()
