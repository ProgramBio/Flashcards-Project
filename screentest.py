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

current_music = None

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
        pygame.draw.rect(SCREEN, triadic_3, BOX, 3, border_radius=8)

        INPUT_TEXT = get_font(50, 1).render(user_input, True, (90,0,130))
        SCREEN.blit(INPUT_TEXT, (BOX.x + 20, BOX.y + 15))

        BACK_BUTTON = Button(image=None, pos=(screen_width//2, 800),
                             text_input="BACK", font=get_font(75, 1),
                             base_color=triadic_3, hovering_color=triadic_2)

        CREATE_BUTTON = Button(image=None, pos=(screen_width//2, 600),
                               text_input="CREATE", font=get_font(75, 1),
                               base_color=triadic_3, hovering_color=triadic_2)

        for button in [BACK_BUTTON, CREATE_BUTTON]:
            button.changeColor(CREATE_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_input.strip():
                        fname = os.path.join(deck_dir, user_input.strip() + ".json")
                        with open(fname, "w", encoding="utf-8") as f:
                            json.dump([], f, ensure_ascii=False, indent=4)
                        return
                else:
                    if len(user_input) < 20:
                        user_input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BACK_BUTTON.checkForInput(CREATE_MOUSE_POS):
                    free_for_all()
                    return
                if CREATE_BUTTON.checkForInput(CREATE_MOUSE_POS) and user_input.strip():
                    fname = os.path.join(deck_dir, user_input.strip() + ".json")
                    with open(fname, "w", encoding="utf-8") as f:
                        json.dump([], f, ensure_ascii=False, indent=4)
                    free_for_all()
                    return

        pygame.display.update()
        clock.tick(60)

def free_for_all():
    background_music("Music/Anticipation.mp3", background_music_volume, -1)
    while True:
        FREEFORALL_MOUSE_POS = pygame.mouse.get_pos()
        screen_color()

        FREEFORALL_TEXT = get_font(55, 1).render("Select Your Deck", True, triadic_3)
        FREEFORALL_RECT = FREEFORALL_TEXT.get_rect(center=(screen_width//2, 120))
        SCREEN.blit(FREEFORALL_TEXT, FREEFORALL_RECT)

        CREATE_BUTTON = Button(image=None, pos=(screen_width//2, 400),
                               text_input="CREATE NEW DECK", font=get_font(75, 1),
                               base_color=(200,180,255), hovering_color=(255,255,255))

        FREEFORALL_BACK = Button(image=None, pos=(screen_width//2, 800),
                                text_input="BACK", font=get_font(75, 1),
                                base_color=triadic_3, hovering_color=triadic_2)
        
        BOX = pygame.Rect(screen_width//2 - 700, 200, 320, 480)
        pygame.draw.rect(SCREEN, (255,255,255), BOX, border_radius=8)
        pygame.draw.rect(SCREEN, triadic_3, BOX, 3, border_radius=8)

        INPUT_TEXT = get_font(120, 1).render("+", True, (90,0,130))
        SCREEN.blit(INPUT_TEXT, (BOX.x + 130, BOX.y + 180))
        INPUT_TEXT = get_font(40, 1).render("CREATE NEW DECK", True, (90,0,130))
        SCREEN.blit(INPUT_TEXT, (BOX.x, BOX.y + 480))

        for button in [CREATE_BUTTON, FREEFORALL_BACK]:
            button.changeColor(FREEFORALL_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_sound()
                if CREATE_BUTTON.checkForInput(FREEFORALL_MOUSE_POS):
                    create_deck()
                if FREEFORALL_BACK.checkForInput(FREEFORALL_MOUSE_POS):
                    free_for_all()

        pygame.display.update()

free_for_all()
